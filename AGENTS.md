# Escopo

O usuário escreve uma MachineConfig para /etc/motd nos workers e a publica via
Kustomize/Argo CD. Não gere a resposta nem aplique a configuração por ele.
Mantenha machineconfigs/kustomization.yaml como base vazia até ele escrever o YAML.
O texto de referência fica em config/motd.txt; os bytes serão incorporados em data URI.
Não acrescente enunciados, scripts de solução, pools, AppProjects, RBAC ou cenários.
Preserve a Application e o RBAC configurados pelo usuário.
Nunca imprima tokens, senhas, Secrets ou kubeconfig completo.
