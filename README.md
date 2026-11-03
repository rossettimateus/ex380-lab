# Laboratório GitOps + MachineConfig — OpenShift 4.22

Configure acesso administrativo ao Argo CD, conecte o Git e sincronize duas
MachineConfigs com fontes HTTP e modos diferentes. Exercício autoral de estudo,
sem vínculo oficial com a Red Hat ou reprodução de questão de certificação.

## Preparado para você

- GitOps e instância padrão openshift-gitops, com OAuth e Route HTTPS reencrypt.
- Grupo gitops-admins com o usuário informado no handoff.
- Dois arquivos em servidor HTTP direto, sem redirecionamento.
- Dois YAMLs em machineconfigs/, com modos 0644 e 0755, para o pool padrão worker.

## Sua execução manual

1. Configure o RBAC do recurso ArgoCD para gitops-admins.
2. Entre pelo OAuth OpenShift na UI informada.
3. Conecte o repo Git fornecido.
4. Crie uma Application com projeto **default**, branch **main** e Path **machineconfigs**.
5. Execute Sync e confira o pool worker e os arquivos no host.

Abra [o enunciado](docs/02-prova.md). Os dados reais ficam em lab.env e no handoff
local. Não há AppProject customizado, pool lab ou experimento de falha obrigatório.
Masters ficam fora deste exercício.

```text
Git / machineconfigs/ -> Argo CD -> MachineConfig -> pool worker
Servidor HTTP        -> contents.source         -> arquivos nos workers
```

Os payloads de referência estão em config/ e http/. A preparação os publica num
servidor HTTP com duas réplicas, para manter disponibilidade durante o rollout.
Em outro cluster, gere URLs reais antes de usar os manifests desta execução.

Para acesso ao cluster, use oc em uma CLI. Os auxiliares de preparação usam
Python 3/PyYAML e Git no terminal escolhido. Veja [a preparação](docs/01-preparacao.md)
ou peça a uma IA para ler [AGENTS.md](AGENTS.md). A conexão Git, a Application,
o RBAC da UI e o Sync são trabalho manual do aluno.

Forks e adaptações são bem-vindos. Não publique credenciais, Secrets, kubeconfig,
lab.env, work/ ou evidence/.

[Validação](docs/03-validacao.md) · [Diagnóstico](docs/05-troubleshooting.md) ·
[Limpeza](docs/06-recuperacao-limpeza.md) · [Testes](docs/TESTES.md)
