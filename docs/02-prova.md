# Parte 2 — Prova simulada

Use somente os dados de `lab.env` e `work/dados-da-prova.md`, documentação oficial e o cluster preparado. Este documento não contém comandos de resolução nem YAMLs finais. Este repositório não distribui gabarito; resolva os requisitos sem pedir à IA os manifests finais.

## Cenário

A equipe de plataforma quer distribuir dois arquivos de configuração a um worker RHCOS por GitOps. Nenhum serviço do SO deve ser modificado. As alterações devem ser reproduzíveis pelo Git e confirmadas no host, com o cluster saudável ao término.

## Requisitos

1. Instale Red Hat OpenShift GitOps, canal `gitops-1.21`, no namespace `openshift-gitops-operator`. Use aprovação manual e registre o CSV efetivamente instalado. Confirme a compatibilidade com 4.22. Não instale 1.11.
2. Crie o namespace `lab-gitops` e uma instância Argo CD denominada `lab`. Ela deve gerenciar recursos de escopo de cluster. Preserve o escopo da instância padrão, se houver.
3. Disponibilize a UI por Route com TLS `reencrypt` e SSO pelo OAuth do OpenShift via Dex. Não desabilite TLS. Use o usuário definido na preparação.
4. Crie o grupo `gitops-admins`, adicione `LAB_USER` e conceda a esse grupo administração no Argo CD. Usuários autenticados fora do grupo devem ter somente leitura no Argo CD. Não é requisito dar cluster-admin ao grupo no OpenShift.
5. Conceda à identidade efetivamente usada pelo application-controller permissão de ler, criar, atualizar, alterar e remover MachineConfigs. Não crie binding de cluster-admin para resolver esta etapa. A leitura de cluster fornecida pelo Operator pode permanecer.
6. Crie AppProject `node-os` em `lab-gitops`, autorizando apenas o repositório indicado, o destino local e o kind cluster-scoped MachineConfig. Não permita deploy de recursos namespaced nesse projeto.
7. No branch `main`, diretório `machineconfigs` do Git fornecido, crie estes dois manifests de MachineConfig:

| Recurso | Destino no node | Conteúdo de origem |
|---|---|---|
| `99-lab-site` | `/etc/ex380-lab/site.conf` | `HTTP_BASE` + `/config/site.conf` |
| `99-lab-banner` | `/etc/ex380-lab/banner.txt` | `HTTP_BASE` + `/config/banner.txt` |

Cada MC deve usar Ignition **3.5.0**, aplicar-se exclusivamente pelo papel `lab`, ter um arquivo com modo `0644` e proprietário root:root. Referencie os arquivos HTTP diretamente; não incorpore o texto em data URI. Preserve os bytes fornecidos. Não altere os payloads HTTP nem use caminhos de serviços críticos.

8. Crie Application `node-config` em `lab-gitops`, no projeto `node-os`, com REPO_URL fornecida, branch `main`, path `machineconfigs`, destino `https://kubernetes.default.svc`, namespace de destino `lab-gitops`. Os MachineConfigs continuam sem namespace. Configure sincronização **manual**, sem auto-sync, self-heal, prune automático ou finalizer de exclusão em cascata.
9. Envie seu commit ao repositório, sincronize pela Application e registre o SHA. Não aplique os MachineConfigs diretamente com o cliente Kubernetes para concluir a prova.
10. Demonstre os dois MCs rastreados pela Application, a revisão Git correta e a aplicação efetiva no único worker de `lab`. Todos os pools devem terminar sem Degraded/Updating. O node deve terminar Ready, MCD Done e currentConfig=desiredConfig=rendered do pool. Os dois arquivos devem existir e coincidir byte a byte com os payloads, incluindo a quebra de linha final.

## Critérios de conclusão

| Área | Evidência necessária |
|---|---|
| Instalação e instância | CSV Succeeded, instância Available e Route admitida |
| Autenticação | Login SSO com usuário nomeado; UI funcional |
| Autorização | Grupo administra Argo CD; usuário externo ao grupo não pode sincronizar; SA do controller tem permissão MC |
| GitOps | Fonte/destino/projeto corretos, commit atual Synced e operação Succeeded |
| MachineConfig | Ambos objetos e referências HTTP corretos; render inclui os dois |
| Convergência | Pool com exatamente um node, sem pausa, atualizado, pronto e sem degradação |
| Host | Hashes, modo e proprietário corretos; node Ready e Done |

Este laboratório é concluído somente com todas as evidências, inclusive verificações manuais de SSO. Não há correspondência entre esta lista e pesos/notas oficiais da EX380.

Após resolver o exercício, escreva: em qual camada ocorreria uma falha de Git, de RBAC, de renderização Ignition, de download HTTP e de drift do host? Qual evidência distinguiria essas falhas?
