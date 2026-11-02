# Troubleshooting por camada

Antes de alterar algo, formule uma hipótese e encontre evidência. Preserve o commit, a mensagem exata e o horário. Não atribua automaticamente toda degradação ao prefixo HTTP.

| Sintoma | Camada provável | Evidência / próximo passo |
|---|---|---|
| Operator não instala | OLM/catálogo | Subscription, InstallPlan, CSV, aprovação manual, pull e versão do canal |
| Argo CD Pending | Agendamento/capacidade | Describe dos pods, taints, requests, eventos; não remova taints indiscriminadamente |
| Login funciona, sync negado | RBAC Argo CD | Identidade/grupos do token, policy e scopes; saia/entre após mudar grupo |
| Sync retorna Forbidden de MC | RBAC Kubernetes | SA real do controller, ClusterRoleBinding, `oc auth can-i` por impersonation |
| Recurso não permitido no projeto | AppProject | clusterResourceWhitelist, sourceRepos e destinations |
| Repo inacessível / revision inexistente | Git/rede | URL de leitura, main, hook update-server-info, logs repo-server, acesso dos pods |
| Synced mas MC não aparece no render de lab | Seletores | label role=lab, MCP herda worker+lab, nome correto e recurso rastreado |
| RenderDegraded | Payload Ignition | `spec.config`, versão 3.5.0, URI válida, conflitos de caminhos e controller logs |
| NodeDegraded | Aplicação/drift | Logs MCD do node exato, arquivos divergentes, downloads, permissões |
| Pool parado em Updating | Rollout | drain, PDB, workloads, Ready, MCD; compare desired/current e generation |
| HTTP falha | Transporte | DNS, rota, firewall, proxy/noProxy, porta, status 404, arquivo, redirecionamento |
| x509 no Git/Route | TLS/CA | CA de confiança apropriada; não desabilite verificação indiscriminadamente |

## Comandos de diagnóstico (não são solução da prova)

```bash
oc get subscription,installplan,csv -n openshift-gitops-operator
oc get argocd lab -n lab-gitops -o yaml
oc get pods,route -n lab-gitops
oc get application node-config -n lab-gitops -o yaml
oc get appproject node-os -n lab-gitops -o yaml
oc get mc 99-lab-site 99-lab-banner -o yaml
oc get mcp lab -o yaml
oc describe mcp lab
oc get node <NODE> -o yaml
oc get co machine-config
oc logs -n openshift-machine-config-operator deployment/machine-config-controller --tail=200
oc get pods -n openshift-machine-config-operator -o wide
oc logs -n openshift-machine-config-operator <POD-MCD-DO-NODE> -c machine-config-daemon --tail=200
oc get events -A --sort-by=.metadata.creationTimestamp
oc auth can-i patch machineconfigs.machineconfiguration.openshift.io --as system:serviceaccount:lab-gitops:lab-argocd-application-controller
oc debug node/<NODE> -- chroot /host curl -v --max-time 15 http://<IP>:8080/config/site.conf
```

Para repo-server/controller, primeiro liste os pods e containers da instância e então leia logs do componente correto. Não presuma que `server` realiza a escrita Kubernetes: normalmente é o application-controller. O RBAC da UI e o Kubernetes RBAC são duas autorizações distintas.

`MachineConfig` e `MachineConfigPool` são cluster-scoped. `Application`, `AppProject` e `ArgoCD` vivem em um namespace. `destination.namespace` não transforma MachineConfig em recurso namespaced.

No OCP 4.22, use a versão documentada 3.5.0; encontrar 3.2.0 em um exemplo antigo ou numa MC existente não identifica a versão mais recente suportada. `oc explain machineconfig.spec.config` não necessariamente descreve o esquema interno completo do Ignition. Confira documentação da release e valide o render; não escolha simplesmente o maior número visto na internet.

Alterar o arquivo no HTTP sem mudar o objeto Git não é estratégia de rollout. Downloads e conversões acontecem no processamento da configuração; a reconciliação não oferece um mecanismo geral de polling do conteúdo remoto. Para um teste posterior, use arquivo/URL versionados e um novo commit. Checksums Ignition são uma extensão útil, mas não foram exigidos no exercício principal para isolar o erro de URI.
