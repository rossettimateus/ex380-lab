#!/usr/bin/env python3
"""Baseline antes do aluno executar RBAC, conexão Git, Application e Sync."""
from common import *
import urllib.request

D=env(); guard(D)
for p in obj('mcp')['items']:
    assert cond(p,'Updated')=='True' and cond(p,'Updating')=='False' and cond(p,'Degraded')=='False',p['metadata']['name']
for c in obj('co')['items']:
    assert cond(c,'Available')=='True' and cond(c,'Progressing')=='False' and cond(c,'Degraded')=='False',c['metadata']['name']
assert obj('argocd',D.get('ARGOCD_NAME','openshift-gitops'),D.get('ARGOCD_NAMESPACE','openshift-gitops'))['status']['phase']=='Available'
assert D['LAB_USER'] in obj('group','gitops-admins').get('users',[])
assert D['HTTP_BASE'].startswith('http://')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args): return None
opener=urllib.request.build_opener(NoRedirect)
for file in ['site.conf','banner.txt']:
    url=D['HTTP_BASE'].rstrip('/')+'/config/'+file
    with opener.open(url,timeout=20) as response:
        assert response.status==200 and response.read()==(ROOT/'http'/file).read_bytes()
    out=oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','curl','-fsS','--max-time','30',url)
    assert out==(ROOT/'http'/file).read_text().strip()
    oc('debug','node/'+D['LAB_NODE'],'--quiet','--','chroot','/host','test','!','-e','/etc/ex380-lab/'+file)
print('PASS: suporte disponível e baseline saudável. Testar também outros workers e um pod.')
