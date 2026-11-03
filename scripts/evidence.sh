#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence
oc get clusterversion version -o yaml > evidence/version.yaml
oc get mcp -o yaml > evidence/pools.yaml
oc get mc 99-lab-site 99-lab-banner -o yaml > evidence/machineconfigs.yaml
oc get nodes -o yaml > evidence/nodes.yaml
oc get application node-config -n openshift-gitops -o yaml > evidence/application.yaml
printf 'Evidências locais; não publique sem revisar. Nenhum Secret exportado.\n'
