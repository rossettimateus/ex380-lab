#!/usr/bin/env python3
"""Validação posterior ao Sync manual. Não cria MCs nem Application."""
from common import *
import hashlib
import yaml

D=env(); guard(D); failures=[]
ns=D.get('ARGOCD_NAMESPACE','openshift-gitops')
instance=D.get('ARGOCD_NAME','openshift-gitops')
appname=D.get('APP_NAME','node-config')
poolname=D.get('LAB_POOL','worker')

def check(name, function):
    try:
        assert function(), 'condição não satisfeita'
        print('PASS',name)
    except Exception as error:
        failures.append(name)
        print('FAIL',name,str(error))

argo=obj('argocd',instance,ns)
check('Grupo contém usuário',lambda:D['LAB_USER'] in obj('group','gitops-admins').get('users',[]))
check('RBAC só gitops-admins explícito',lambda:[line.strip() for line in argo['spec']['rbac']['policy'].splitlines() if line.strip() and not line.strip().startswith('#')]==['g, gitops-admins, role:admin'])
check('Instância disponível',lambda:argo['status']['phase']=='Available')
check('Route reencrypt admitida',lambda:any(r['spec'].get('tls',{}).get('termination')=='reencrypt' and any(c.get('status')=='True' and c['type']=='Admitted' for i in r.get('status',{}).get('ingress',[]) for c in i.get('conditions',[])) for r in obj('route',ns=ns)['items']))
app=None
try: app=obj('application',appname,ns)
except Exception: pass
check('Application existe',lambda:app is not None)
check('Fonte e destino',lambda:app['spec']['source']['repoURL']==D['REPO_URL'] and app['spec']['source']['targetRevision']=='main' and app['spec']['source']['path']=='machineconfigs' and app['spec']['project']==D.get('APP_PROJECT','default') and app['spec']['destination']['server']=='https://kubernetes.default.svc' and app['spec']['destination']['namespace']==ns)
check('Application Synced',lambda:app['status']['sync']['status']=='Synced')
check('Operação Succeeded',lambda:app['status']['operationState']['phase']=='Succeeded')
for name,file,mode in [('99-lab-site','site.conf',420),('99-lab-banner','banner.txt',493)]:
    expected=yaml.safe_load((ROOT/'machineconfigs'/(name+'.yaml')).read_text())
    check('MC '+name,lambda name=name,e=expected:obj('mc',name)['spec']==e['spec'] and obj('mc',name)['metadata']['labels'].get('machineconfiguration.openshift.io/role')=='worker')
for pool in obj('mcp')['items']:
    s=pool['status']
    check('Pool '+pool['metadata']['name'],lambda p=pool,s=s:cond(p,'Updated')=='True' and cond(p,'Updating')=='False' and cond(p,'Degraded')=='False' and s['machineCount']==s['readyMachineCount']==s['updatedMachineCount'])
nodes=[n for n in obj('nodes')['items'] if 'node-role.kubernetes.io/worker' in n['metadata']['labels'] and not any('node-role.kubernetes.io/'+r in n['metadata']['labels'] for r in ['master','control-plane'])]
check('Workers dedicados presentes',lambda:len(nodes)>0)
for node in nodes:
    name=node['metadata']['name'];a=node['metadata'].get('annotations',{})
    check(name+' Ready/Done',lambda n=node,a=a:cond(n,'Ready')=='True' and a.get('machineconfiguration.openshift.io/state')=='Done' and a.get('machineconfiguration.openshift.io/currentConfig')==a.get('machineconfiguration.openshift.io/desiredConfig'))
    for file,mode in [('site.conf','644'),('banner.txt','755')]:
        sha=hashlib.sha256((ROOT/'http'/file).read_bytes()).hexdigest()
        check(name+' hash '+file,lambda n=name,f=file,e=sha:oc('debug','node/'+n,'--quiet','--','chroot','/host','sha256sum','/etc/ex380-lab/'+f).split()[0]==e)
        check(name+' modo/dono '+file,lambda n=name,f=file,m=mode:oc('debug','node/'+n,'--quiet','--','chroot','/host','stat','-c','%a %u %g','/etc/ex380-lab/'+f)==m+' 0 0')
print('Resultado:',len(failures),'falhas. Login e criação de apps na UI exigem teste manual.')
sys.exit(bool(failures))
