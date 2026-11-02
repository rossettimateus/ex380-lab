# Recuperação e limpeza ordenada

## Recuperação da URL inválida

1. Confirme o cluster e preserve evidências. Suspenda novas sincronizações. Auto-sync já deve estar desligado.
2. Repare/reverta a fonte no Git, publique e sincronize manualmente. Não corrija apenas o objeto live deixando Git errado.
3. Confirme que a MC live tem a URL correta e que o erro de renderização foi resolvido. Se lab estiver pausado, despause para que a versão boa possa convergir.
4. Observe `oc get mcp lab -w`, conditions do pool e logs do MCD do node. A API pode aceitar o reparo enquanto o MCD ainda está recuperando; aguarde.
5. Atualize EXPECTED_REVISION e valide arquivos, node e pools novamente.

Se o node já estava Degraded por drift, corrigir a URL pode não bastar. Compare os arquivos com a **currentConfig** efetivamente aplicada e os logs do MCD. Não copie arquivos aleatórios, altere currentConfig/desiredConfig ou crie `/run/machine-config-daemon-force` sem entender a divergência e a documentação aplicável. Para este lab descartável, se o node não recuperar com o retorno à configuração boa, guarde os logs e recrie o worker por seu mecanismo de provisionamento (ou recrie o cluster). Não incluí automação de destruição de máquinas, pois isso depende do provedor.

Os commits, pushes e reversões destas instruções são feitos em work/candidate/,
no repo de manifests do aluno, nunca no repo do material.

## Limpeza após recuperar a saúde

A opção mais simples, ao terminar, é destruir **o cluster descartável** pelo mesmo mecanismo que o criou. Confirme recursos e custos remanescentes no provedor. Se quiser preservar o cluster de treinamento, siga esta ordem:

1. Mantenha Git/HTTP ligados. Garanta pool lab saudável e despausado. Remova os dois YAMLs do repo, commit e push. Na Application, sincronize selecionando **Prune explicitamente só nesta limpeza**, revisando que apenas `99-lab-site` e `99-lab-banner` serão removidos. Não delete a Application primeiro. A remoção das MCs desencadeia outro rollout para retirar seus arquivos.
2. Aguarde o rendered novo sem as duas MCs, pool atualizado e node Done. Use `oc debug node/<NODE> -- chroot /host test ! -e /etc/ex380-lab/site.conf` e equivalente para banner. Este procedimento exige que os caminhos não existissem antes do lab; se existiam, interrompa e restaure segundo seu baseline.
3. Apague Application `node-config` e AppProject `node-os` de lab-gitops. Confirme ausência de finalizer de cascade ou de recursos pendentes antes de prosseguir.
4. Remova apenas `node-role.kubernetes.io/lab` do worker: `oc label node <NODE> node-role.kubernetes.io/lab-`. **Mantenha** `node-role.kubernetes.io/worker`. Aguarde o retorno ao rendered do pool worker, Ready/Done, worker saudável e `lab.status.machineCount=0`.
5. Só então remova MCP `lab`: `oc delete mcp lab`.
6. Remova ArgoCD `lab`, aguarde seus componentes sumirem; exclua `lab-machineconfig-manager` (ClusterRoleBinding e ClusterRole) e o namespace `lab-gitops`. Remova o grupo `gitops-admins` somente se foi criado exclusivamente para este exercício.
7. Remova `lab-gitops` da lista ARGOCD_CLUSTER_CONFIG_NAMESPACES da Subscription, preservando os demais valores. Se o Operator inteiro foi instalado apenas para este lab e nenhuma outra instância depende dele, desinstale pelo console (Subscription/CSV). Não exclua CRDs globais indiscriminadamente. A instância padrão pode ainda existir.
8. Verifique todos os pools e o Machine Config Operator saudáveis. Mantenha o repo de manifests do aluno acessível até terminar a recuperação; os payloads continuam no repositório central. Remova apenas o diretório `work/` desta cópia do projeto se quiser descartar Git/payloads temporários; preserve evidências úteis.

O validador principal espera MCs e pool presentes, portanto deixa de ser o teste correto após limpeza. Na limpeza use o baseline, ausência dos arquivos e saúde dos pools remanescentes.
