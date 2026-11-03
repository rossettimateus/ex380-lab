# Escopo

O usuário escreve uma MachineConfig para /etc/motd nos workers e a publica via
Kustomize/Argo CD. Não gere a resposta nem aplique a configuração por ele.
Mantenha machineconfigs/kustomization.yaml como base vazia até ele escrever o YAML.
config/motd.txt contém a URL HTTP do texto de referência; os bytes da resposta
serão incorporados em data URI, não o endereço da URL.
Não acrescente enunciados, scripts de solução, pools, AppProjects, RBAC ou cenários.
Durante a prática, preserve a Application e o RBAC configurados pelo usuário.

Se o usuário disser "reinicie", ele autoriza o reset deste exercício: guarde o SHA
concluído, remova a Application/MC e as configurações de acesso/conexão exclusivas
do exercício, aguarde rollback e saúde dos workers e deixe o Git com base vazia.
Preserve infraestrutura, Operator, usuário de acesso e conteúdo de referência.
Não crie a nova instância, namespace, RBAC, repo cadastrado ou Application pelo aluno.
Confirme o rollback do MOTD e a convergência real, sem forçar estados ou annotations
para simular sucesso. Não reescreva o histórico Git para apagar as tentativas.
Nunca imprima tokens, senhas, Secrets ou kubeconfig completo.
