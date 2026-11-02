# Laboratório de OpenShift, GitOps e MachineConfig

Pratique instalação de GitOps, autenticação, autorização, sincronização e configuração
de um worker RHCOS. Você recebe o enunciado, os payloads e as ferramentas de preparação
e validação; escreve seus manifests por conta própria. **Não há gabarito.**
Exercício autoral de estudo, sem vínculo com a Red Hat e sem reprodução de prova oficial.

## Requisitos

- Cluster OpenShift **4.22.x isolado e descartável**, com ao menos dois workers
  RHCOS separados do control plane. O roteiro de referência usa três control planes.
  SNO, compacto sem workers separados e Sandbox de namespace não atendem.
- Privilégios administrativos efetivos: chamar-se `admin` não comprova permissões.
  MachineConfig pode causar drain, reinicializações e degradação do MCO.
- Estação Linux, incluindo Pop!_OS, com `oc` 4.22, Git, Python 3 e curl.
  PyYAML é necessário para o experimento opcional de falha.
- Conta GitHub e um fork público seu, ou Git/HTTP em uma VM externa ao cluster.
- Um usuário OAuth real para a prova e outro fora do grupo do exercício para o teste
  negativo. `oc create user` sozinho não cria credenciais autenticáveis.

O perfil é GitOps `gitops-1.21` e Ignition 3.5.0. Confirme a versão efetiva pela API e
a disponibilidade do canal. Este projeto não provisiona cluster ou recursos pagos.

## Começar

1. Faça **Fork** deste repositório na sua conta, preferencialmente só de `main`.
   Cada estudante usa seu próprio fork e cluster; não publique respostas no upstream.
2. Clone seu fork e crie o arquivo local de configuração:

   ```bash
   git clone https://github.com/SEU-USUARIO/ex380-lab.git
   cd ex380-lab
   cp lab.env.example lab.env
   ```

3. Siga [a preparação completa](docs/01-preparacao.md). Preencha `lab.env` com a API,
   worker, usuários e URLs **do seu ambiente**; os exemplos não concedem acesso a um cluster.
4. Só após os checks passarem, abra [o enunciado](docs/02-prova.md). Tempo sugerido:
   90 minutos de configuração, excluindo instalação e reboots; não é tempo oficial.
5. Edite **`machineconfigs/`**, faça commit e publique no `main` do seu fork.
6. Execute [a validação](docs/03-validacao.md). Depois, opcionalmente, faça
   [a falha controlada](docs/04-falha-controlada.md). Consulte também
   [diagnóstico](docs/05-troubleshooting.md) e [recuperação e limpeza](docs/06-recuperacao-limpeza.md).

No GitHub, o clone atual é seu checkout de trabalho. Não rode `prep/serve.sh` nem
crie outro checkout em `work/candidate/`: esses caminhos são do modo VM auxiliar.

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
Seu fork / main / machineconfigs/ -> Argo CD -> MachineConfig -> MCO -> worker lab
Seu fork / main / config/         -> HTTPS raw --------------------> download no node
```

Não precisa de aplicação nem GitHub Pages. Use seu fork público:

```text
REPO_URL=https://github.com/SEU-USUARIO/ex380-lab.git
HTTP_BASE=https://raw.githubusercontent.com/SEU-USUARIO/ex380-lab/main
```

Os payloads ficam em `HTTP_BASE/config/site.conf` e `HTTP_BASE/config/banner.txt`.
Os arquivos em `http/` são as referências locais usadas pelos verificadores e devem
ser idênticos aos de `config/`. Preserve os payloads durante o exercício.
HTTPS substitui o HTTP da alternativa com VM. Não precisa manter o computador ligado;
mantenha o fork público durante todo o exercício e a recuperação.

## Estrutura e limites

| Local | Uso |
|---|---|
| `docs/` | Preparação, enunciado, validação e recuperação |
| `AGENTS.md` e `agent.md` | Preparação por agentes de IA |
| `machineconfigs/` | Você escreve os dois manifests aqui |
| `config/` | Payloads publicados por HTTPS raw |
| `http/` | Payloads de referência para comparação local |
| `prep/` | Pool dedicado e alternativa de servidor externo |
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
