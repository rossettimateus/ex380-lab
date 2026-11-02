#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
prepare_only=false
if [ "${1:-}" = '--prepare-only' ] && [ "$#" -eq 1 ]; then
  prepare_only=true
elif [ "$#" -ne 0 ]; then
  printf 'Uso: bash prep/serve.sh [--prepare-only]\n' >&2
  exit 2
fi
# Execute na VM auxiliar externa ao cluster. Não expõe credenciais.
mkdir -p work/www/config work/www/repos
cp http/site.conf http/banner.txt work/www/config/
if [ ! -d work/www/repos/ex380.git ]; then
  git init --bare --initial-branch=main work/www/repos/ex380.git
  printf '#!/bin/sh
exec git update-server-info
' > work/www/repos/ex380.git/hooks/post-update
  chmod +x work/www/repos/ex380.git/hooks/post-update
  git -C work/www/repos/ex380.git update-server-info
fi
if [ ! -d work/candidate/.git ]; then
  mkdir -p work/candidate
  cp -R git-seed/. work/candidate/
  git -C work/candidate init --initial-branch=main
  git -C work/candidate add .
  git -C work/candidate -c user.name='Lab preparation' -c user.email='lab@example.invalid' commit -m 'Initial exercise skeleton'
  git -C work/candidate remote add origin "$(pwd)/work/www/repos/ex380.git"
  git -C work/candidate push -u origin main
fi
if [ "$prepare_only" = true ]; then
  printf 'Git e payloads preparados em work/. Nenhum servidor iniciado.\n'
  exit 0
fi
printf 'Servidor em foreground. Mantenha este terminal aberto; Ctrl-C encerra.
'
exec python3 -m http.server 8080 --bind 0.0.0.0 --directory work/www
