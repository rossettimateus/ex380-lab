#!/usr/bin/env python3
"""Lê o cluster; oc debug cria pods transitórios e só lê arquivos do host."""
from common import *
import hashlib, re
D=env(); guard(D); failures=[]
def check(name,fn):
    try:
        assert fn(), 'condição não satisfeita'
        print('PASS',name)
    except Exception as e:
        failures.append(name); print('FAIL',name, str(e))
ns='lab-gitops'; app='node-config'; names=['99-lab-site','99-lab-banner']
check('CSV GitOps 1.21 Succeeded',lambda:any(x['status'].get('phase')=='Succeeded' and x['spec']['version'].startswith('1.21.') for x in obj('csv',ns='openshift-gitops-operator')['items']))
check('ArgoCD lab',lambda:obj('argocd','lab',ns)['status'].get('phase')=='Available')
check('Dex OAuth',lambda:obj('argocd','lab',ns)['spec']['sso']['dex']['openShiftOAuth'] is True)
check('RBAC grupo admin',lambda:'g, gitops-admins, role:admin' in obj('argocd','lab',ns)['spec']['rbac']['policy'])
check('Escopo groups',lambda:'groups' in obj('argocd','lab',ns)['spec']['rbac']['scopes'])
check('Grupo contém usuário',lambda:D['LAB_USER'] in obj('group','gitops-admins').get('users',[]))
check('Route reencrypt admitida',lambda:any(x['spec'].get('tls',{}).get('termination')=='reencrypt' and any(any(c['type']=='Admitted' and c['status']=='True' for c in i.get('conditions',[])) for i in x.get('status',{}).get('ingress',[])) for x in obj('route',ns=ns)['items']))
sa='system:serviceaccount:lab-gitops:lab-argocd-application-controller'
for verb in ['get','list','watch','create','update','patch','delete']:
    check('controller pode '+verb+' MC',lambda v=verb:oc('auth','can-i',v,'machineconfigs.machineconfiguration.openshift.io','--as',sa)=='yes')
check('App origem/destino/projeto',lambda:(lambda s:s['source']['repoURL']==D['REPO_URL'] and s['source']['path']=='machineconfigs' and s['source']['targetRevision']=='main' and s['destination']['server']=='https://kubernetes.default.svc' and s['project']=='node-os')(obj('application',app,ns)['spec']))
check('AppProject permite MC',lambda:{'group':'machineconfiguration.openshift.io','kind':'MachineConfig'} in obj('appproject','node-os',ns)['spec']['clusterResourceWhitelist'])
check('Sync manual',lambda:not obj('application',app,ns)['spec'].get('syncPolicy',{}).get('automated'))
check('Application Synced',lambda:obj('application',app,ns)['status']['sync']['status']=='Synced')
check('Última operação Succeeded',lambda:obj('application',app,ns)['status']['operationState']['phase']=='Succeeded')
check('Revision esperada',lambda:bool(re.fullmatch('[0-9a-f]{40}',D['EXPECTED_REVISION'])) and obj('application',app,ns)['status']['sync']['revision']==D['EXPECTED_REVISION'])
for name,file,path in [('99-lab-site','site.conf','/etc/ex380-lab/site.conf'),('99-lab-banner','banner.txt','/etc/ex380-lab/banner.txt')]:
    def mc_ok(name=name,file=file,path=path):
        m=obj('mc',name); c=m['spec']['config']; f=c['storage']['files']
        return m['metadata']['labels']['machineconfiguration.openshift.io/role']=='lab' and c['ignition']['version']=='3.5.0' and len(f)==1 and f[0]['path']==path and f[0]['mode']==420 and f[0]['contents']['source']==D['HTTP_BASE'].rstrip('/')+'/config/'+file
    check('MachineConfig '+name,mc_ok)
    check('MC rastreado pela Application '+name,lambda name=name:any(x.get('kind')=='MachineConfig' and x['name']==name and x.get('status')=='Synced' for x in obj('application',app,ns)['status']['resources']))
pool=obj('mcp','lab'); status=pool.get('status',{})
check('Pool seleciona worker + lab',lambda:set(next(x['values'] for x in pool['spec']['machineConfigSelector']['matchExpressions'] if x['key']=='machineconfiguration.openshift.io/role'))=={'worker','lab'})
check('Pool converge sem pausa',lambda:not pool['spec'].get('paused',False) and pool['metadata']['generation']==status.get('observedGeneration') and cond(pool,'Updated')=='True' and cond(pool,'Updating')=='False' and cond(pool,'Degraded')=='False' and status.get('machineCount')==status.get('updatedMachineCount')==status.get('readyMachineCount')==1 and status.get('unavailableMachineCount',0)==status.get('degradedMachineCount',0)==0 and pool['spec']['configuration']['name']==status['configuration']['name'])
check('Rendered inclui ambos MC',lambda:set(names)<=set(x['name'] for x in status['configuration']['source']))
node=obj('node',D['LAB_NODE']); a=node['metadata'].get('annotations',{})
check('Apenas worker escolhido no pool',lambda:[x['metadata']['name'] for x in obj('node')['items'] if 'node-role.kubernetes.io/lab' in x['metadata']['labels']]==[D['LAB_NODE']])
check('Node Ready, Done, current=desired=pool',lambda:cond(node,'Ready')=='True' and a.get('machineconfiguration.openshift.io/state')=='Done' and a.get('machineconfiguration.openshift.io/currentConfig')==a.get('machineconfiguration.openshift.io/desiredConfig')==status['configuration']['name'])
for f in ['site.conf','banner.txt']:
    expected=hashlib.sha256((ROOT/'http'/f).read_bytes()).hexdigest()
    check('SHA256 no node '+f,lambda f=f,e=expected:oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','sha256sum','/etc/ex380-lab/'+f).split()[0]==e)
    check('Modo/proprietário '+f,lambda f=f:oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','stat','-c','%a %u %g','/etc/ex380-lab/'+f)=='644 0 0')
for p in obj('mcp')['items']:
    check('Pool saudável '+p['metadata']['name'],lambda p=p:cond(p,'Degraded')=='False' and cond(p,'Updating')=='False')
print('\nResultado:',len(failures),'falhas. Login SSO e autorização efetiva na UI exigem teste manual; veja docs/03-validacao.md.')
sys.exit(bool(failures))
