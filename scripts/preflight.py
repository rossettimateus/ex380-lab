#!/usr/bin/env python3
from common import *
import urllib.request
D=env(); n=guard(D)
assert cond(n,'Ready')=='True', 'Node não Ready'
for p in obj('mcp')['items']:
    assert cond(p,'Degraded')=='False' and cond(p,'Updating')=='False', 'Pool não estabilizado: '+p['metadata']['name']
assert obj('clusteroperator','machine-config')['status']['conditions'], 'MCO ausente'
for c in obj('clusteroperator')['items']:
    assert cond(c,'Available')=='True' and cond(c,'Degraded')=='False' and cond(c,'Progressing')=='False', 'ClusterOperator não estabilizado: '+c['metadata']['name']
workers=obj('node')['items']
assert sum('node-role.kubernetes.io/worker' in w['metadata']['labels']
           and not any('node-role.kubernetes.io/'+r in w['metadata']['labels'] for r in ['master','control-plane'])
           and 'CoreOS' in w['status']['nodeInfo']['osImage'] for w in workers)>=2, 'Use no mínimo dois workers RHCOS dedicados'
for f in ['site.conf','banner.txt']:
    u=D['HTTP_BASE'].rstrip('/')+'/config/'+f
    with urllib.request.urlopen(u,timeout=15) as r: actual=r.read()
    assert actual==(ROOT/'http'/f).read_bytes(), 'HTTP incorreto: '+f
    # Teste no network namespace do host, sem escrever no host.
    out=oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','curl','-fsS','--max-time','15',u)
    assert out==(ROOT/'http'/f).read_text().strip(), 'Node não obteve o payload esperado'
for f in ['site.conf','banner.txt']:
    oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','test','!','-e','/etc/ex380-lab/'+f)
print(oc('get','packagemanifest','openshift-gitops-operator','-n','openshift-marketplace','-o','jsonpath={.status.channels[*].name}'))
print('PASS: conectividade HTTP e baseline. Confirme canal gitops-1.21, capacidade, OAuth e Git antes da prova.')
