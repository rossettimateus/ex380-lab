import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def env():
    p=ROOT/'lab.env'
    if not p.exists(): raise SystemExit('Copie lab.env.example para lab.env e preencha os valores.')
    d={}
    for line in p.read_text().splitlines():
        line=line.strip()
        if line and not line.startswith('#'):
            k,v=line.split('=',1); d[k]=v.strip().strip('"').strip("'")
    return d
def run(*args):
    return subprocess.check_output(args,text=True,stderr=subprocess.PIPE).strip()
def oc(*args): return run('oc',*args)
def obj(kind,name=None,ns=None):
    a=['get',kind]
    if name: a.append(name)
    if ns: a+=['-n',ns]
    return json.loads(oc(*a,'-o','json'))
def cond(o,key): return next((c.get('status') for c in o.get('status',{}).get('conditions',[]) if c['type']==key),None)
def guard(d):
    if oc('whoami','--show-server').rstrip('/') != d['LAB_API'].rstrip('/'):
        raise SystemExit('API atual difere de LAB_API. Pare e confira o kubeconfig.')
    v=obj('clusterversion','version')['status']['desired']['version']
    if not v.startswith('4.22.'): raise SystemExit('Este perfil exige OpenShift 4.22.x: '+v)
    n=obj('node',d['LAB_NODE']); labels=n['metadata']['labels']
    if any('node-role.kubernetes.io/'+r in labels for r in ['master','control-plane']):
        raise SystemExit('Node de control plane proibido neste exercício.')
    if 'node-role.kubernetes.io/worker' not in labels: raise SystemExit('Escolha um worker RHCOS.')
    if 'CoreOS' not in n['status']['nodeInfo']['osImage']: raise SystemExit('Worker precisa ser RHCOS.')
    if oc('auth','can-i','*','*','--all-namespaces')!='yes': raise SystemExit('Use o administrador do laboratório.')
    return n
def confirm(d):
    print('Cluster:',d['LAB_API'],'| Worker:',d['LAB_NODE'])
    if input('Digite LAB-DESCARTAVEL para autorizar esta alteração: ')!='LAB-DESCARTAVEL':
        raise SystemExit('Cancelado.')
