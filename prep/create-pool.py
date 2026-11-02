#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import *
d=env(); n=guard(d)
nodes=obj('node')['items']
workers=[x for x in nodes if 'node-role.kubernetes.io/worker' in x['metadata']['labels']
         and not any('node-role.kubernetes.io/'+r in x['metadata']['labels'] for r in ['master','control-plane'])
         and 'CoreOS' in x['status']['nodeInfo']['osImage']]
assert len(workers)>=2, 'Use no mínimo dois workers RHCOS separados do control plane'
assert all(cond(x,'Ready')=='True' for x in nodes), 'Há node não Ready'
assert all(cond(c,'Available')=='True' and cond(c,'Degraded')=='False' and cond(c,'Progressing')=='False'
           for c in obj('clusteroperator')['items']), 'ClusterOperator não estabilizado'
# Este preparador é somente para um cluster limpo, sem pools customizados.
pools=obj('mcp')['items']
assert {p['metadata']['name'] for p in pools} <= {'master','worker'}, 'Já existe pool customizado: revise manualmente; não sobrepor seletores.'
assert all(cond(p,'Degraded')=='False' and cond(p,'Updating')=='False' for p in pools), 'Baseline não saudável'
assert all('node-role.kubernetes.io/lab' not in x['metadata']['labels'] for x in nodes), 'Label lab já existe'
confirm(d)
print(oc('apply','-f',str(ROOT/'prep/pool.yaml')))
print(oc('label','node',d['LAB_NODE'],'node-role.kubernetes.io/lab='))
print('Aguarde a migração para lab. Confira machineCount=1, currentConfig=desiredConfig, Updated=True antes da prova.')
