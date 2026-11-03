#!/usr/bin/env python3
"""Testes locais dos artefatos preparados, sem oc ou Sync."""
import ast
from pathlib import Path
import re
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]

class PreparationTests(unittest.TestCase):
    def test_machineconfigs(self):
        for name,file,mode in [('99-lab-site','site.conf',420),('99-lab-banner','banner.txt',493)]:
            m=yaml.safe_load((ROOT/'machineconfigs'/(name+'.yaml')).read_text())
            self.assertEqual(m['kind'],'MachineConfig')
            self.assertNotIn('namespace',m['metadata'])
            self.assertEqual(m['metadata']['name'],name)
            self.assertEqual(m['metadata']['labels']['machineconfiguration.openshift.io/role'],'worker')
            c=m['spec']['config'];self.assertEqual(c['ignition']['version'],'3.5.0')
            self.assertEqual(len(c['storage']['files']),1)
            f=c['storage']['files'][0]
            self.assertEqual(f['path'],'/etc/ex380-lab/'+file)
            self.assertEqual(f['mode'],mode)
            self.assertEqual(f['user'],{'id':0});self.assertEqual(f['group'],{'id':0})
            self.assertTrue(f['contents']['source'].startswith('http://'))
            self.assertTrue(f['contents']['source'].endswith('/config/'+file))
    def test_http_support(self):
        resources=list(yaml.safe_load_all((ROOT/'prep/simple-http.yaml').read_text()))
        cm=next(r for r in resources if r['kind']=='ConfigMap')
        for file in ['site.conf','banner.txt']:
            self.assertEqual(cm['data'][file],(ROOT/'http'/file).read_text())
            self.assertEqual((ROOT/'config'/file).read_bytes(),(ROOT/'http'/file).read_bytes())
        dep=next(r for r in resources if r['kind']=='Deployment')
        self.assertEqual(dep['spec']['replicas'],2)
        route=next(r for r in resources if r['kind']=='Route')
        self.assertNotIn('tls',route['spec'])
    def test_code_syntax_and_document_links(self):
        for folder in ['prep','scripts','tests']:
            for p in (ROOT/folder).glob('*.py'):ast.parse(p.read_text(),filename=str(p))
        for p in [ROOT/'README.md',ROOT/'AGENTS.md',ROOT/'agent.md',*(ROOT/'docs').glob('*.md')]:
            for target in re.findall(r'\]\(([^\s)]+)\)',p.read_text()):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((p.parent/target.split('#')[0]).exists(),f'{p}: {target}')

if __name__=='__main__':unittest.main(verbosity=2)
