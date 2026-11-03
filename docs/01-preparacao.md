# Preparação do laboratório

Leia também [AGENTS.md](../AGENTS.md). Esta etapa não instala GitOps nem resolve o
enunciado. Execute os comandos na raiz do clone, salvo indicação contrária.

## 1. Ferramentas e sessão

Para acessar o cluster, tenha o binário `oc` compatível com 4.22 disponível em uma
CLI com acesso à API. Obtenha a CLI pela página de ferramentas do console ou pela
distribuição oficial da Red Hat.

Para editar e publicar manifests, use seu editor e fluxo Git habitual. Se optar
pelos scripts de preparação e validação fornecidos, confira as dependências no
ambiente onde eles serão executados:

| Ferramenta | Uso nos auxiliares |
|---|---|
| Python 3 e `oc` | Preflight, criação do pool e validação |
| Git | Clone, publicação e conferência de revisão |
| curl | Verificações de conectividade |
| Bash | Scripts `.sh` e suíte de testes do kit |
| PyYAML | Script opcional de falha, após concluir a prova |

Os exemplos usam sintaxe de shell POSIX; adapte os comandos ao seu terminal.
Use `python` ou `python3` conforme a instalação. Bash é necessário para executar
os `.sh`, e não para usar o `oc`. As dependências dos auxiliares podem ficar em
um terminal remoto. O modo GitHub dispensa o servidor de `prep/serve.sh`.

Use a sessão do oc no ambiente de terminal escolhido. Se faltar autenticação, faça login no próprio terminal;
não envie tokens ou senhas à IA. Inspecione sem alterar recursos:

```bash
oc whoami
oc whoami --show-server
oc get clusterversion version
oc auth can-i '*' '*' --all-namespaces
oc get nodes -o wide
oc get mcp
oc get co
oc get infrastructure cluster -o jsonpath='{.status.platformStatus.type}{"\n"}{.status.controlPlaneTopology}{"\n"}'
oc adm top nodes
oc get pdb -A
oc get pods -A --field-selector=status.phase=Pending
```

Confirme pela API a versão efetiva **4.22.x**, permissões e saúde. Inspecione também
requests/limits e capacidade para reagendar as cargas do worker; métricas de baixo uso
não garantem que os requests caibam nos outros nodes. Se métricas faltarem, use
capacidade alocável e requests. Confira labels/annotations, sem exportar credenciais.

## 2. Topologia e autorização

Exija ao menos dois workers RHCOS separados do control plane. O roteiro de referência
usa três control planes. Nunca use um node com master ou control-plane como substituto,
mesmo se também tiver worker. SNO, compacto sem workers separados e Sandbox de
namespace não atendem. Escolha apenas um worker para lab; os demais sustentam as cargas.

Antes de alterar, mostre API exata, topologia e worker proposto. Obtenha uma única
confirmação de cluster isolado e descartável, autorizando MachineConfig, drains e
possíveis reboots. A confirmação vale para a preparação da mesma API/worker; não é
necessário repeti-la a cada comando. Nome admin não comprova cluster-admin.

## 3. Git e payloads externos

### Material e payloads: repositório central

Use o clone de https://github.com/rossettimateus/ex380-lab.git para consultar o
roteiro e executar os auxiliares. Forks e adaptações também são possíveis; o fluxo
de referência mantém os materiais e os payloads vinculados ao repositório central.
Os dois arquivos são servidos pelo próprio repositório, via HTTPS raw.

### Manifests: repo de escrita do aluno

Siga [a configuração do repositório de manifests](00-repositorio-do-aluno.md).
O checkout fica em work/candidate/ e recebe apenas machineconfigs/; o material
continua neste kit. Configure identidade Git e autenticação de escrita no terminal.
Se usar GitHub CLI, gh auth login permite autorizar pelo navegador sem enviar tokens
à IA. Um endereço SSH sozinho não configura uma chave nem autentica a conta.

Preencha lab.env, na raiz do kit, com valores reais:

```text
LAB_API=https://api.SEÚ-CLUSTER:6443
LAB_NODE=SEU-WORKER-RHCOS
HTTP_BASE=https://raw.githubusercontent.com/rossettimateus/ex380-lab/main
REPO_URL=https://github.com/SEU-USUARIO/ex380-meus-manifests.git
LAB_USER=SEU-USUARIO-OAUTH
LAB_NEGATIVE_USER=SEU-USUARIO-NEGATIVO
EXPECTED_REVISION=
```

Mantenha HTTP_BASE acima, sem /config no final. REPO_URL é o destino dos seus
manifests, e não o repositório do material. EXPECTED_REVISION fica vazio até seu
commit final da prova. Os scripts leem valores literais; não use variáveis shell
ou espaços no fim. LAB_API deve corresponder ao servidor atual do oc.

Mantenha o repo de manifests público durante o exercício e a recuperação. Os nodes
e pods precisam de DNS e saída HTTPS para GitHub e raw.githubusercontent.com.
Se o acesso ao conteúdo central falhar, investigue a rede e registre o bloqueio.
Outra hospedagem externa é uma adaptação possível: ajuste HTTP_BASE e repita os
testes de conteúdo e conectividade. Serviços dentro do cluster não atendem ao
requisito de disponibilidade externa durante recuperação. No fluxo recomendado,
não é necessário executar prep/serve.sh ou manter servidor próprio.
Não publique lab.env, work/ ou credenciais.

## 4. OAuth e canal

Reutilize um usuário OAuth existente quando adequado; o administrador pode ser o
usuário da prova. Prepare também outro usuário OAuth real fora de gitops-admins para
o teste negativo. Não crie o grupo ou RBAC da prova nesta etapa. oc create user sozinho
não cria credenciais. Teste autenticação real, preservando a sessão administrativa.

Se necessário, acrescente HTPasswd pela [documentação oficial 4.22](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/authentication_and_authorization/configuring-identity-providers),
preservando todos os IdPs existentes. Gere o arquivo com htpasswd -B. O OAuth deste
perfil reconhece bcrypt $2a$/$2y$, mas não $2b$. Guarde novas senhas em arquivo local
0600, pasta 0700; não imprima senha, hash ou Secret. Use kubeconfig temporário para
testar login, revogue a sessão de teste e aguarde authentication estabilizar.

Confira o canal, sem instalar:

```bash
oc get packagemanifest openshift-gitops-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}{"\n"}'
```

Se gitops-1.21 faltar, resolva o catálogo ou revise conscientemente o perfil e o
validador com a documentação oficial. Não use 1.11 como substituto automático.

## 5. Conectividade antes do pool

Teste os URLs completos dos dois arquivos na estação e compare com http/. Confira
main no Git. Após a autorização, rode:

```bash
python3 scripts/preflight.py
```

O preflight verifica baseline e os payloads da estação e do worker alvo, além de
exigir ausência dos caminhos finais no host. **Não substitui** testes nos demais
nodes, em um Pod e de Git. Em cada node, para cada URL real, use oc debug node/NODE
--quiet -- chroot /host curl -fsS --max-time 30 URL-REAL e compare o conteúdo completo.
Os comandos no host são de leitura, mas oc debug cria pods privilegiados transitórios.

Crie também um pod temporário com imagem aprovada que tenha curl. Para UBI minimal,
use UID numérico sem privilégios, runAsNonRoot, seccomp RuntimeDefault,
allowPrivilegeEscalation=false e capabilities drop ALL. Confira fase, exit code e
logs; compare os payloads. Falha de pull ou CreateContainerConfigError não é erro HTTP.
Remova o pod após o teste. Confira Git pela rede de pods: no GitHub, o endpoint
REPO_URL/info/refs?service=git-upload-pack deve anunciar o serviço Git. Se houver
imagem aprovada com Git, git ls-remote REPO_URL refs/heads/main é outra opção.
O acesso pelo repo-server fica para a prova, após instalar GitOps.

Se faltar infraestrutura ou rede, registre o bloqueio exato; não declare prontidão
nem substitua os endpoints externos por serviços dentro do cluster.

## 6. Baseline, pool e estabilização

Salve antes de alterar labels ou criar MachineConfigs, substituindo SEU-WORKER:

```bash
mkdir -p evidence
oc get mcp -o yaml > evidence/baseline-pools.yaml
oc get node SEU-WORKER -o yaml > evidence/baseline-node.yaml
oc get clusterversion version -o yaml > evidence/baseline-version.yaml
python3 prep/create-pool.py
```

O preparador pede LAB-DESCARTAVEL, cria apenas lab e adiciona o label ao worker
escolhido, preservando worker. Ele recusa pools customizados preexistentes e baseline
não saudável. A entrada só pode ser respondida após revisar e autorizar a API/worker.
Se lab já existir, revise o estado; não force uma nova criação ou altere seletores.

Observe oc get mcp e oc get nodes. Exija:

- lab selecionando exatamente o worker proposto, herdando worker e lab;
- observedGeneration correspondente à geração atual;
- machineCount=readyMachineCount=updatedMachineCount=1 e contagem degradada zero;
- Updated=True, Updating=False, Degraded=False;
- currentConfig=desiredConfig igual ao rendered atual de lab e node Done;
- demais pools atualizados, todos os nodes Ready, Operators disponíveis sem
  degradação/progressão e ClusterVersion estabilizada.

Um oc wait Updated=True imediato pode aceitar estado antigo. Investigue PDBs,
drain, capacidade e logs se não convergir; não remova proteções nem falsifique annotations.

## 7. Handoff e início

Registre em work/dados-da-prova.md API, versão exata, worker/pool, URLs completas,
usuários, localização privada de credenciais novas, canal, verificações executadas,
limitações e forma de editar/publicar. Mantenha lab.env local com os dados vinculantes.

Pronto significa ferramentas, identidades reais, Git/payloads externos acessíveis e
pool/cluster estabilizados. Consulte o material neste clone, edite os manifests em
work/candidate/ e mantenha o repo de manifests acessível. Não instale GitOps, Argo CD, RBAC/grupo,
AppProject, Application ou os dois manifests, nem execute a falha controlada.
Sem pendências, abra [02-prova.md](02-prova.md).
