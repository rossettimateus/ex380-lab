# Laboratório de OpenShift, GitOps e MachineConfig

Pratique instalação de GitOps, autenticação, autorização, sincronização e configuração
de um worker RHCOS. Você recebe o enunciado, os payloads e as ferramentas de preparação
e validação; escreve seus manifests por conta própria. **Não há gabarito.**
Exercício autoral de estudo, sem vínculo com a Red Hat e sem reprodução de prova oficial.

## Requisitos do ambiente de laboratório

- Cluster OpenShift **4.22.x isolado e descartável**, com ao menos dois workers
  RHCOS separados do control plane. O roteiro de referência usa três control planes.
  SNO, compacto sem workers separados e Sandbox de namespace não atendem.
- Privilégios administrativos efetivos: chamar-se `admin` não comprova permissões.
  MachineConfig pode causar drain, reinicializações e degradação do MCO.
- Uma CLI com o binário `oc` compatível com 4.22 e acesso à API do cluster.
- Um repositório Git público com acesso de escrita, somente para seus manifests.
- Um usuário OAuth real para a prova e outro fora do grupo do exercício para o teste
  negativo. `oc create user` sozinho não cria credenciais autenticáveis.

O perfil é GitOps `gitops-1.21` e Ignition 3.5.0. Confirme a versão efetiva pela API e
a disponibilidade do canal. Este projeto não provisiona cluster ou recursos pagos.

## Ferramentas auxiliares

Para acessar o cluster pela CLI, use `oc`. Para editar e publicar seus manifests,
use um editor e seu fluxo de trabalho Git habitual.

Os scripts deste kit usam Python 3 e `oc`; os arquivos `.sh` usam Bash. PyYAML é
necessário somente para o script opcional de falha. Execute esses auxiliares em
um ambiente que forneça suas dependências. Veja [a preparação](docs/01-preparacao.md).

## Começar

1. Clone este repositório para consultar o material e executar os auxiliares:

   ```bash
   git clone https://github.com/rossettimateus/ex380-lab.git
   cd ex380-lab
   cp lab.env.example lab.env
   ```

2. Siga [a preparação completa](docs/01-preparacao.md), incluindo
   [a configuração do seu repositório de manifests](docs/00-repositorio-do-aluno.md).
   Nesse fluxo, ele recebe os manifests que você escrever; não é necessário copiar o kit.
3. Preencha `lab.env`: `REPO_URL` aponta para seu repo de manifests; `HTTP_BASE`
   já aponta para os arquivos deste repositório e deve ser mantido.
4. Após os checks passarem, abra [o enunciado](docs/02-prova.md). Tempo sugerido:
   90 minutos de configuração, excluindo instalação e reboots; não é tempo oficial.
5. Edite `work/candidate/machineconfigs/`, faça commit e publique no `main` do
   seu repo de manifests. O caminho observado pelo Argo CD continua `machineconfigs`.
6. Execute [a validação](docs/03-validacao.md). Depois, opcionalmente, faça
   [a falha controlada](docs/04-falha-controlada.md). Consulte também
   [diagnóstico](docs/05-troubleshooting.md) e [recuperação e limpeza](docs/06-recuperacao-limpeza.md).

O clone deste kit e o repo de manifests são diretórios Git separados. Não troque
seus remotes nem publique as respostas no repositório do material.

Já está dentro do Argo CD? Vá às etapas C e E do [enunciado](docs/02-prova.md):
primeiro confira repositório e AppProject; depois use a
[tabela de criação da Application](docs/02-prova.md#e1-criar-a-application).

## Preparar com ajuda de uma IA

Abra seu clone em um agente com terminal e envie:

> Leia AGENTS.md e docs/01-preparacao.md. Inspecione minhas ferramentas e o cluster
> da sessão local do oc. Execute somente a preparação, deixando a prova para mim.
> Antes de modificar o cluster, apresente API, topologia e worker proposto e peça
> uma única confirmação de que o cluster é isolado e descartável, incluindo alterações
> de MachineConfig e possíveis reinicializações. Verifique permissões, rede e saúde.
> Não imprima credenciais, não publique dados locais e não resolva o enunciado.

[AGENTS.md](AGENTS.md) contém as instruções canônicas. [agent.md](agent.md) é uma
entrada alternativa para quem pedir esse nome explicitamente. A IA deverá pedir
login ou informações faltantes; não envie tokens ou senhas no chat.

## Git e arquivos HTTPS, sem servidor próprio

```text
Seu repo / main / machineconfigs/ -> Argo CD -> MachineConfig -> MCO -> worker lab
rossettimateus/ex380-lab / config/ -> HTTPS raw --------------------> download no node
```

Enunciado, instruções, scripts e payloads permanecem neste repositório. Seu repo
é o destino dos manifests que você criar. O fluxo recomendado mantém os materiais e
os payloads referenciados aqui, sem precisar duplicá-los.

```text
REPO_URL=https://github.com/SEU-USUARIO/ex380-meus-manifests.git
HTTP_BASE=https://raw.githubusercontent.com/rossettimateus/ex380-lab/main
```

Os nodes baixam os arquivos diretamente pelos endereços:

- https://raw.githubusercontent.com/rossettimateus/ex380-lab/main/config/site.conf
- https://raw.githubusercontent.com/rossettimateus/ex380-lab/main/config/banner.txt

As cópias em `http/` servem apenas à comparação local pelos verificadores.
Não é necessário servidor próprio, aplicação ou GitHub Pages. Mantenha seu repo
de manifests acessível durante o exercício e a recuperação.

Forks, cópias e adaptações são bem-vindos. Para seguir o roteiro de referência,
recomendamos manter `HTTP_BASE` apontando para este repositório e consultar aqui
as instruções atualizadas. Fazer um fork não exige mudar os URLs dos payloads.

## Estrutura e limites

| Local | Uso |
|---|---|
| `docs/` | Preparação, enunciado, validação e recuperação |
| `AGENTS.md` e `agent.md` | Preparação por agentes de IA |
| `work/candidate/machineconfigs/` | Checkout local do seu repo de manifests (ignorado pelo kit) |
| `git-seed/` | Esqueleto inicial sem respostas |
| `config/` | Payloads publicados por HTTPS raw |
| `http/` | Payloads de referência para comparação local |
| `prep/` | Preparação do pool dedicado |
| `scripts/` | Preflight, validação, evidências e falha local opcional |
| `tests/` | Testes locais, sem acesso ao cluster |
| `lab.env.example` | Modelo sem dados de um cluster real |

`lab.env`, `work/`, `evidence/`, `.venv/` e kubeconfigs são locais e ignorados pelo Git.
Nunca publique credenciais ou Secrets. Não abra portas do roteador, publique serviços
ou crie recursos pagos sem autorização específica. Git/HTTP dentro do cluster não
substituem a hospedagem externa necessária durante reboots e recuperação.

A preparação deixa para você: GitOps Operator, instância Argo CD, RBAC/grupo,
AppProject, Application e os dois manifests de MachineConfig. A validação final
verifica também revisão Git e conteúdo no host, além do estado da Application.

Contribua por issue ou PR, sem credenciais nem respostas em `machineconfigs/`.
Antes de enviar, execute `python3 tests/test_preparation.py`.
Veja [o que foi testado e seus limites](docs/TESTES.md).
