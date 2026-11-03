# Preparação — administrador ou IA

Prepare somente o suporte. O aluno fará RBAC da UI, conexão Git, Application e Sync.
Use a sessão local do oc; não peça nem imprima senhas, tokens ou kubeconfig.

1. Confirme API, OpenShift 4.22.x, permissões, workers RHCOS dedicados, capacidade
   de drain e saúde. Obtenha confirmação de cluster isolado/descartável antes de alterar.
2. Instale/reutilize o GitOps compatível e a instância padrão openshift-gitops,
   em openshift-gitops. Prepare OAuth e Route HTTPS reencrypt. Preserve a política
   RBAC da UI para o aluno configurar.
3. Reutilize o usuário OAuth e prepare gitops-admins com ele. Confira a permissão
   Kubernetes do controller para MCs. Não adicione permissões redundantes.
4. Com autorização para publicar os arquivos, aplique apenas o suporte:
   `oc apply -f prep/simple-http.yaml`. Aguarde Deployment files em ex380-support 2/2.
5. Obtenha o host da Route files. Teste /config/site.conf e /config/banner.txt
   pela estação, workers e um pod: HTTP 200 sem redirects e bytes idênticos aos
   de http/. Remova o pod temporário.
6. Gere os manifests **sem aplicar**:

```text
python3 prep/render-machineconfigs.py --http-base http://HOST-DA-ROUTE
```

7. Publique machineconfigs/ no Git informado. A geração e o push são preparação;
   a conexão na UI e o Sync são do aluno. Em outro cluster, gere URLs reais.
8. Registre os dados em lab.env e work/dados-da-prova.md. Confira suporte saudável,
   grupo/Route e ausência de repo/Application do exercício cadastrados na instância.

Use o pool worker padrão e o projeto default. Não crie pool, projeto restritivo,
segunda instância ou teste negativo. No reset, se MCs já foram aplicadas, retire-as
e aguarde rollback antes de remover o HTTP. Preserve recursos de infraestrutura.
