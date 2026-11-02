#!/usr/bin/env python3
"""Falha opcional: altera somente um arquivo local; não acessa Git remoto ou cluster."""
import sys
from pathlib import Path


def without_http_scheme(url):
    for prefix in ('https://', 'http://'):
        if url.startswith(prefix):
            return url[len(prefix):]
    raise ValueError('Esperava URL válida http:// ou https://')


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python3 scripts/break-source.py CAMINHO-DO-MANIFEST')
    try:
        import yaml
    except ImportError:
        raise SystemExit('Instale PyYAML no seu venv: python3 -m pip install PyYAML')
    p = Path(sys.argv[1])
    d = yaml.safe_load(p.read_text())
    assert d['kind'] == 'MachineConfig' and d['metadata']['name'] == '99-lab-site'
    assert d['metadata']['labels']['machineconfiguration.openshift.io/role'] == 'lab'
    f = d['spec']['config']['storage']['files'][0]
    assert f['path'] == '/etc/ex380-lab/site.conf'
    f['contents']['source'] = without_http_scheme(f['contents']['source'])
    p.write_text(yaml.safe_dump(d, sort_keys=False))
    print('Somente arquivo local alterado. Revise git diff; siga docs/04-falha-controlada.md.')


if __name__ == '__main__':
    main()
