#!/usr/bin/env python3
"""Testes offline: não chamam oc, GitHub ou o experimento de falha em manifests."""
import ast
import functools
import http.server
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class PreparationTests(unittest.TestCase):
    def test_payloads_and_empty_exam_path(self):
        for name in ('site.conf', 'banner.txt'):
            self.assertEqual((ROOT/'config'/name).read_bytes(), (ROOT/'http'/name).read_bytes())
        self.assertEqual([p.name for p in (ROOT/'machineconfigs').iterdir()], ['.gitkeep'])
        self.assertFalse((ROOT/'gabarito').exists())

    def test_code_syntax_and_document_links(self):
        for folder in ('prep', 'scripts', 'tests'):
            for path in (ROOT/folder).glob('*.py'):
                ast.parse(path.read_text(), filename=str(path))
        for path in [ROOT/'prep/serve.sh', ROOT/'scripts/evidence.sh']:
            run('bash', '-n', str(path))
        for path in [ROOT/'README.md', ROOT/'AGENTS.md', ROOT/'agent.md', * (ROOT/'docs').glob('*.md')]:
            for target in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((path.parent/target.split('#')[0]).exists(), f'{path}: {target}')

    def test_ignored_private_paths(self):
        paths = ['lab.env', 'work/auth/credentials.txt', 'evidence/nodes.json', 'private.kubeconfig', '.venv/test']
        out = run('git', '-C', str(ROOT), 'check-ignore', *paths)
        self.assertEqual(set(out.splitlines()), set(paths))

    def test_http_and_https_scheme_without_touching_manifest(self):
        spec = importlib.util.spec_from_file_location('break_source', ROOT/'scripts/break-source.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for scheme in ('http://', 'https://'):
            self.assertEqual(module.without_http_scheme(scheme+'example.invalid/config/test.txt'),
                             'example.invalid/config/test.txt')
        for url in ('data:,text', 'ftp://example.invalid/test', 'example.invalid/test'):
            with self.assertRaises(ValueError):
                module.without_http_scheme(url)

    def test_external_server_seed_idempotency_and_anonymous_http_clone(self):
        with tempfile.TemporaryDirectory(prefix='ex380-preparation-') as directory:
            temp = Path(directory)
            for name in ('prep', 'http', 'git-seed'):
                shutil.copytree(ROOT/name, temp/name)
            run('bash', str(temp/'prep/serve.sh'), '--prepare-only')
            bare = temp/'work/www/repos/ex380.git'
            candidate = temp/'work/candidate'
            first = run('git', '-C', str(candidate), 'rev-parse', 'HEAD')
            self.assertEqual(run('git', '-C', str(candidate), 'ls-tree', '-r', '--name-only', 'HEAD').splitlines(),
                             ['README.md', 'machineconfigs/.gitkeep'])
            run('bash', str(temp/'prep/serve.sh'), '--prepare-only')
            self.assertEqual(run('git', '-C', str(candidate), 'rev-parse', 'HEAD'), first)
            # Confere que o hook atualiza o dumb HTTP também após um push novo.
            (candidate/'student-note.txt').write_text('temporary test only\n')
            run('git', '-C', str(candidate), 'add', 'student-note.txt')
            run('git', '-C', str(candidate), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                'commit', '-m', 'Test hook')
            run('git', '-C', str(candidate), 'push')
            revision = run('git', '-C', str(candidate), 'rev-parse', 'HEAD')
            handler = functools.partial(QuietHandler, directory=str(temp/'work/www'))
            with http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler) as server:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    base = f'http://127.0.0.1:{server.server_port}'
                    for name in ('site.conf', 'banner.txt'):
                        with urllib.request.urlopen(base+'/config/'+name, timeout=5) as response:
                            self.assertEqual(response.read(), (ROOT/'http'/name).read_bytes())
                    url = base+'/repos/ex380.git'
                    self.assertEqual(run('git', 'ls-remote', url, 'refs/heads/main').split()[0], revision)
                    clone = temp/'http-clone'
                    run('git', 'clone', url, str(clone))
                    self.assertEqual(run('git', '-C', str(clone), 'rev-parse', 'HEAD'), revision)
                    self.assertEqual((clone/'student-note.txt').read_text(), 'temporary test only\n')
                finally:
                    server.shutdown()
                    thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
