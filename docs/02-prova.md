# Parte 2 — Prova simulada

## Objetivo e resultado esperado

Distribua **dois arquivos de texto a um único worker RHCOS**, usando GitOps.
Você configura a instância Argo CD, suas permissões, o projeto e a Application;
escreve duas MachineConfigs, publica no Git e sincroniza manualmente.
Nenhum serviço do sistema operacional precisa ser modificado.

Este enunciado apresenta os valores e os resultados exigidos, sem entregar os YAMLs
ou comandos de resolução. Use documentação oficial quando precisar consultar a sintaxe.
Se já concluiu uma etapa, confira seus requisitos e continue da próxima.

## Antes de começar: seus dados e o alvo

Abra `lab.env` e `work/dados-da-prova.md` no clone do material. Confira estes valores:

| Dado | Como será usado |
|---|---|
| `LAB_API` | API do cluster em que você executa o exercício |
| `LAB_NODE` | **Único worker** que deve receber os dois arquivos |
| `LAB_USER` | Usuário OAuth que administrará o Argo CD via SSO |
| `LAB_NEGATIVE_USER` | Usuário OAuth fora de `gitops-admins`, para testar somente leitura |
| `REPO_URL` | Git onde você pode publicar **seus manifests** |
| `HTTP_BASE` | Servidor HTTPS dos **arquivos de texto fornecidos** |
| `EXPECTED_REVISION` | SHA completo do commit final; preencher após publicar |

O pool `lab` já foi criado na preparação e seleciona `LAB_NODE`. Você vai criar
**duas MachineConfigs para esse mesmo pool**. Não crie outro MachineConfigPool,
não altere seus seletores e não aplique estas configurações aos papéis worker/master.
Masters e outros workers não devem receber os dois arquivos do exercício.

No fluxo recomendado, os materiais e os payloads permanecem em
`rossettimateus/ex380-lab`; o repo de escrita do aluno contém os manifests.
Para configurar esse destino de escrita, consulte [o guia do repo do aluno](00-repositorio-do-aluno.md).
Os valores efetivos da sua execução são os registrados em `lab.env`.

## Mapa dos recursos que você precisa criar

| Recurso | Nome exigido | Onde existe | Função |
|---|---|---|---|
| GitOps Operator | Red Hat OpenShift GitOps | `openshift-gitops-operator` | Instalar o Operator pelo canal exigido |
| Namespace | `lab-gitops` | Cluster | Conter a instância e os recursos Argo CD |
| Instância ArgoCD | `lab` | Namespace `lab-gitops` | Executar o Argo CD do exercício |
| Grupo OpenShift | `gitops-admins` | Cluster | Identificar os administradores da UI |
| Permissões Kubernetes | Para o application-controller real | Cluster | Autorizar a escrita de MachineConfigs |
| AppProject | `node-os` | Namespace `lab-gitops` | Delimitar Git, destino e tipos permitidos |
| Application | `node-config` | Namespace `lab-gitops` | Ler os dois manifests e sincronizá-los |
| MachineConfig | `99-lab-site` | Cluster, sem namespace | Criar o arquivo site.conf no worker lab |
| MachineConfig | `99-lab-banner` | Cluster, sem namespace | Criar o arquivo banner.txt no worker lab |

O AppProject é um projeto **do Argo CD**. O namespace `lab-gitops` é um recurso
**do OpenShift**. Ambos são necessários e têm funções diferentes.

## Etapa A — Instalar e acessar sua instância Argo CD

Realize esta etapa no OpenShift, pelo console ou por manifests/comandos de sua autoria.

- Instale Red Hat OpenShift GitOps no namespace `openshift-gitops-operator`, canal
  `gitops-1.21`, com aprovação manual. Registre o CSV e a versão efetivamente instalados,
  compatíveis com OpenShift 4.22. Não use GitOps 1.11.
- Crie `lab-gitops` e, nele, a instância ArgoCD `lab`. Configure-a para gerenciar
  recursos de escopo de cluster. Preserve o escopo da instância padrão, se houver.
- Disponibilize a UI dessa instância por Route com TLS `reencrypt`.
- Configure SSO pelo OAuth do OpenShift via Dex. Entre usando `LAB_USER` pela opção
  de login OpenShift, com a confiança de CA adequada, sem desabilitar TLS.

**Para avançar:** Operator instalado, instância disponível, Route admitida e login
SSO funcionando na **instância lab**. Use a Route de `lab-gitops`, não a de outra
instância que também esteja instalada no cluster.

## Etapa B — Configurar as duas camadas de autorização

| Camada | Quem recebe a permissão | Resultado exigido |
|---|---|---|
| Argo CD | Grupo OpenShift `gitops-admins`, contendo `LAB_USER` | Administrar a UI e sincronizar a Application |
| Argo CD | Demais usuários autenticados | Somente leitura; sem autorização para Sync |
| Kubernetes | Identidade real do application-controller da instância lab | Ler, listar, observar, criar, atualizar, alterar e remover MachineConfigs |

Crie o grupo e os vínculos necessários. Não conceda cluster-admin ao controller
para cumprir o exercício. A leitura de cluster fornecida pelo Operator pode permanecer.
Também não é necessário dar cluster-admin do OpenShift ao grupo `gitops-admins`.

**Para avançar:** as permissões devem atender às duas camadas. Conseguir entrar na
UI comprova autenticação; confira também a autorização para sincronizar.

## Etapa C — Preparar o Git e o projeto dentro do Argo CD

### C1. Conectar o repositório de manifests

Na UI da instância lab, localize o gerenciamento de repositórios, normalmente em
**Settings → Repositories**. Use a URL de **`REPO_URL`** e confirme o acesso.
Esse é o Git que receberá suas MachineConfigs. O endereço raw dos payloads será
usado dentro delas como fonte dos arquivos, e não como repositório Git da Application.

Se você já cadastrou o repo e ele está conectado, esta parte está feita.
Ainda será necessário criar o AppProject e a Application nas próximas partes.

### C2. Criar o AppProject node-os

Crie o projeto na área de projetos da instância, normalmente em **Settings → Projects**,
ou por um recurso AppProject de sua autoria. O resultado deve ser:

| Propriedade | Requisito |
|---|---|
| Nome | `node-os` |
| Namespace do recurso AppProject | `lab-gitops` |
| Git autorizado | Somente `REPO_URL` |
| Cluster de destino autorizado | `https://kubernetes.default.svc` |
| Namespace de destino autorizado | `lab-gitops` |
| Tipo de recurso cluster-scoped autorizado | Grupo `machineconfiguration.openshift.io`, kind `MachineConfig` |
| Recursos namespaced | Não permitir deploy nesse projeto |

Não use o projeto default para substituir `node-os`.

**Para avançar:** projeto criado, Git e destino autorizados e permissão de tipo de
recurso limitada a MachineConfig. Veja [a documentação de projetos do Argo CD](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/).

## Etapa D — Escrever e publicar suas duas MachineConfigs

No repo definido em `REPO_URL`, use branch **main** e diretório **machineconfigs**.
No fluxo recomendado, o checkout local está em `work/candidate/`, dentro do clone
do material. Portanto, escreva os YAMLs em `work/candidate/machineconfigs/`.

| Nome do recurso | Arquivo a criar no host | Fonte do conteúdo |
|---|---|---|
| `99-lab-site` | `/etc/ex380-lab/site.conf` | `HTTP_BASE` + `/config/site.conf` |
| `99-lab-banner` | `/etc/ex380-lab/banner.txt` | `HTTP_BASE` + `/config/banner.txt` |

Cada MachineConfig deve cumprir **todos** estes requisitos:

| Propriedade | Valor exigido |
|---|---|
| Tipo de recurso | `MachineConfig`, sem namespace |
| Papel selecionado | Exclusivamente `lab`, selecionado pelo pool preparado |
| Versão Ignition | `3.5.0` |
| Quantidade de arquivos | Um por MachineConfig |
| Permissão do arquivo | `0644` em octal, equivalente a `420` em decimal |
| Proprietário e grupo do arquivo | `root:root` |
| Origem dos bytes | Download direto da URL HTTP(S) indicada |
| Conteúdo | Idêntico ao payload fornecido, incluindo a quebra de linha final |

O modo é uma propriedade do arquivo descrita na configuração; não há tarefa de
executar chmod no node. Referencie a URL na fonte do conteúdo: não cole o texto
no manifest, não use data URI e não altere os payloads fornecidos. Não é necessário
criar unidades systemd, configurar serviços ou executar comandos no host.

No fluxo de referência, os endereços completos são:

- https://raw.githubusercontent.com/rossettimateus/ex380-lab/main/config/site.conf
- https://raw.githubusercontent.com/rossettimateus/ex380-lab/main/config/banner.txt

Faça commit e push no repo definido em REPO_URL. Use nomes de arquivos YAML de sua
escolha; os **nomes dos recursos** precisam corresponder à tabela. No fluxo recomendado
para alunos, esse repo recebe os manifests e os payloads continuam no repositório central.

**Para avançar:** main publicado com os dois manifests em machineconfigs/. Não os
aplique diretamente pelo cliente Kubernetes para concluir o exercício.

## Etapa E — Criar a Application node-config e sincronizar

### E1. Criar a Application

Na área **Applications** da UI da instância lab, crie uma nova Application,
normalmente pelo botão **New App**. Você também pode criar o recurso por um manifest
de sua autoria. Configure o resultado abaixo; os nomes dos campos podem variar na UI.

| Área / campo da UI | Valor exigido |
|---|---|
| General → Application Name | `node-config` |
| General → Project Name | `node-os` |
| General → Sync Policy | `Manual` |
| Source → Repository URL | Valor de `REPO_URL` no seu lab.env |
| Source → Revision | `main` |
| Source → Path | `machineconfigs` |
| Destination → Cluster URL | `https://kubernetes.default.svc`, o cluster local da instância |
| Destination → Namespace | `lab-gitops` |
| Namespace do recurso Application | `lab-gitops` |

#### Atenção ao Source → Path

Preencha **Path = `machineconfigs`**, relativo à raiz do Git informado em Repository URL.
A estrutura publicada nesse repositório deve ser:

```text
raiz-do-seu-repo/
└── machineconfigs/
    ├── seu-primeiro-manifest.yaml
    └── seu-segundo-manifest.yaml
```

Use `machineconfigs` sem barra inicial. Não coloque nesse campo a URL completa,
um caminho do seu computador como `work/candidate/machineconfigs`, nem o caminho
`config/` dos arquivos de texto. O Argo CD vai ler os YAMLs dentro desse diretório.

| Informação | Onde preencher |
|---|---|
| URL do Git dos seus manifests | Application → Source → Repository URL |
| Branch `main` | Application → Source → Revision |
| Diretório `machineconfigs` desse Git | Application → Source → Path |
| URL HTTPS de site.conf ou banner.txt | Fonte do conteúdo do arquivo dentro da respectiva MachineConfig |

Mantenha auto-sync, self-heal e prune automático desativados. Não adicione finalizer
de exclusão em cascata. O namespace de destino da Application não torna as
MachineConfigs namespaced: elas continuam sem namespace e afetam nodes pelo pool.

**Para avançar:** node-config aparece na instância lab, associada a node-os e
apontando para o Git, branch e diretório corretos. Consulte também
[a criação de Applications pela UI](https://argo-cd.readthedocs.io/en/stable/getting_started/#creating-apps-via-ui).

### E2. Revisar e sincronizar

Faça Refresh se a revisão publicada ainda não aparecer. Antes do Sync, confira
que a Application apresenta exatamente as duas MachineConfigs esperadas para
sincronização. A árvore não deve incluir o kit, o pool lab ou recursos de instalação.
Revise o diff e faça **Sync manual**, sem Prune nesta etapa.

Registre o SHA completo do commit sincronizado em EXPECTED_REVISION no lab.env.
Confirme que a revisão do Argo CD é a mesma enviada ao Git.

## Etapa F — Comprovar o resultado no cluster e no host

A sincronização do objeto e a aplicação no node são etapas diferentes. Aguarde o
MCO convergir e demonstre:

- As duas MachineConfigs rastreadas por node-config, com a revisão Git correta e
  a última operação de sincronização bem-sucedida.
- Pool lab com exatamente um node, sem pausa, atualizado, pronto e sem degradação;
  seu rendered inclui as duas MachineConfigs.
- LAB_NODE Ready, MCD Done e currentConfig=desiredConfig=rendered do pool lab.
- Os dois arquivos no LAB_NODE com bytes, modo e proprietário corretos.
- Todos os demais pools estabilizados, sem Degraded/Updating.
- LAB_USER administrando a UI via SSO; o usuário fora de gitops-admins consegue
  consultar a Application, mas recebe negação ao tentar sincronizar.

Siga [03-validacao.md](03-validacao.md) para executar o validador e os testes manuais.
Healthy/Synced na UI, isoladamente, não comprova os arquivos no host.
O experimento de falha fica para depois da conclusão e validação desta etapa.

## Checklist final

| Entrega | Evidência |
|---|---|
| Operator e instância | CSV Succeeded, instância Available e Route admitida |
| Login | SSO OpenShift com LAB_USER na instância lab |
| Permissões | Grupo administra, usuário externo tem somente leitura, controller autorizado para MC |
| AppProject | node-os com origem, destino e tipos restritos |
| Application | node-config, node-os, REPO_URL/main/machineconfigs, Sync manual |
| Git | Dois manifests publicados, SHA correto sincronizado |
| MachineConfigs | Fontes HTTP(S), papel lab e requisitos dos arquivos atendidos |
| Convergência | Pool de um worker atualizado, node Ready/Done, arquivos conferidos |

Tempo sugerido: 90 minutos de configuração, excluindo instalação/reboots.
Este exercício autoral não corresponde a pesos ou notas oficiais da EX380.
Após resolver, explique como distinguir uma falha de Git, de RBAC, de renderização
Ignition, de download HTTP e de drift do host usando evidências de cada camada.
