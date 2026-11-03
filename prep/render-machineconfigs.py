#!/usr/bin/env python3
"""Gera os dois YAMLs locais; não acessa ou modifica o cluster."""
import argparse
from pathlib import Path
from urllib.parse import urlsplit
import yaml


def render(base, output):
    parsed = urlsplit(base)
    if (parsed.scheme != 'http' or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or any(c.isspace() for c in base)):
        raise ValueError('Informe uma base http:// real, sem credenciais, query ou fragmento')
    output.mkdir(parents=True, exist_ok=True)
    for name, file, mode in [('99-lab-site', 'site.conf', 420), ('99-lab-banner', 'banner.txt', 493)]:
        manifest = {'apiVersion': 'machineconfiguration.openshift.io/v1', 'kind': 'MachineConfig',
                    'metadata': {'name': name, 'labels': {'machineconfiguration.openshift.io/role': 'worker'}},
                    'spec': {'config': {'ignition': {'version': '3.5.0'}, 'storage': {'files': [
                        {'path': '/etc/ex380-lab/'+file, 'mode': mode, 'user': {'id': 0}, 'group': {'id': 0},
                         'contents': {'source': base.rstrip('/')+'/config/'+file}}]}}}}
        (output/(name+'.yaml')).write_text(yaml.safe_dump(manifest, sort_keys=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--http-base', required=True)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]/'machineconfigs')
    args = parser.parse_args()
    render(args.http_base, args.output)
    print('Dois YAMLs gerados. Não foram aplicados ao cluster.')
