# Diagnóstico rápido

| Sintoma | Confira |
|---|---|
| Login sem administração | Grupo gitops-admins, usuário correto e RBAC do ArgoCD |
| Git/destino não permitido | Use o projeto default e os dados do handoff |
| Diretório não encontrado | Branch main e Path machineconfigs, relativo à raiz |
| Sync Forbidden de MC | Permissões Kubernetes do application-controller |
| Download falha | URL http://, DNS, status 200 e acesso do node |
| Pool Updating | Drain, PDBs, capacidade, condições do pool e logs MCD |
| Synced sem arquivo | Convergência MCO, papel worker, currentConfig/desiredConfig |

Não falsifique annotations nem use force files. Preserve a mensagem antes de corrigir.
