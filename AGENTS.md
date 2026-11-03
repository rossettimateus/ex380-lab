# Preparação por IA — escopo atual

Leia README.md e docs/01-preparacao.md. Prepare o suporte e os dois manifests.
Não recupere exigências antigas do histórico Git. O aluno fará RBAC da UI,
conexão Git, Application e Sync manualmente.

Use a sessão local do oc. Confira API, versão 4.22.x efetiva, permissões, nodes
RHCOS, capacidade de drain, pools e Operators. Não presuma cluster-admin pelo nome
admin. Não imprima tokens, senhas, Secrets ou kubeconfig completo. Se faltar sessão,
peça login pelo terminal da pessoa, sem credenciais no chat.

Antes de alterar, mostre API/topologia/alvo e confirme uma vez que o cluster é
isolado e descartável, com possíveis reboots. Preserve a autorização na sessão.
Para reset solicitado, inventarie Applications, MCs e finalizers antes de remover;
não destrua infraestrutura ou recursos de outros Operators.

Prepare GitOps compatível com 4.22 e use a instância padrão openshift-gitops em
openshift-gitops. Prepare OAuth, Route HTTPS reencrypt e gitops-admins com o usuário
informado. Preserve o RBAC da UI para o aluno editar. Confira se as permissões
padrão do controller já permitem escrever MCs; não crie bindings redundantes.

Use o pool worker padrão com workers RHCOS dedicados e capacidade de rollout.
Não crie pool lab, AppProject restritivo, segunda instância, usuário negativo ou
cenário de falha. O projeto da Application será default.

Prepare HTTP puro com 200 sem redirect e bytes corretos. GitHub raw redireciona
HTTP para HTTPS. prep/simple-http.yaml fornece duas réplicas em workers, ConfigMap,
Service e Route HTTP. Obtenha autorização específica para expor os arquivos se
ela ainda não tiver sido dada. Não abra roteador ou crie recursos pagos.
Teste acesso pela estação, workers e um pod; remova pods temporários.

Gere os dois manifests com prep/render-machineconfigs.py: Ignition 3.5.0, papel
worker, root:root e modos 420/493 (0644/0755). Criar/publicar os YAMLs é preparação
expressamente autorizada. Não aplique as MCs, não faça Sync, não crie Application,
não cadastre repo e não configure a política gitops-admins no ArgoCD.

Registre dados reais em lab.env e work/dados-da-prova.md. Credenciais novas, se
necessárias, ficam em arquivo local 0600, pasta 0700. Entregue usuário/acesso,
Route, Git/branch/Path, URLs HTTP, alvo e caminhos/modos. Não declare aplicação no
host validada antes do Sync manual. Para editar o kit, use testes locais e não
altere o cluster só para testar código. Não imponha sistema operacional à estação.
