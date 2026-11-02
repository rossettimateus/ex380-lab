# Seu repositório de manifests

O material do exercício, as instruções e os payloads HTTPS ficam em
https://github.com/rossettimateus/ex380-lab. Você precisa de outro repo apenas
para publicar os manifests que escrever e permitir que o Argo CD os leia.
Não faça fork nem copie o kit ou os arquivos de config/ para esse repo.

## 1. Criar o destino de escrita

No GitHub, entre na sua conta e use **New repository**:

- Nome sugerido: `ex380-meus-manifests`.
- Visibilidade: **Public**, para o Argo CD ler sem credenciais.
- Deixe vazio: não inicialize com README, .gitignore ou licença nesta etapa.

Copie a URL HTTPS do repo. Você também pode usar um repo vazio já existente,
desde que tenha permissão para publicar nele. Não use a URL do material como
seu destino de escrita e não envie credenciais ao mantenedor ou a uma IA.

## 2. Preparar o checkout sem respostas

Na raiz do clone do material, execute os exemplos abaixo em um shell compatível,
substituindo nome, e-mail e URL pelos seus valores:

```bash
mkdir -p work/candidate/machineconfigs
cp git-seed/machineconfigs/.gitkeep work/candidate/machineconfigs/.gitkeep
git -C work/candidate init --initial-branch=main
git -C work/candidate config user.name 'SEU NOME'
git -C work/candidate config user.email 'SEU EMAIL GIT'
git -C work/candidate add machineconfigs/.gitkeep
git -C work/candidate commit -m 'Preparar diretório dos manifests'
git -C work/candidate remote add origin https://github.com/SEU-USUARIO/ex380-meus-manifests.git
git -C work/candidate push -u origin main
```

Se work/candidate/ já for um checkout, inspecione git status e git remote -v antes
de alterar qualquer coisa; não reinicialize nem substitua seu remote cegamente.
O único arquivo publicado na preparação é machineconfigs/.gitkeep. O aluno escreve
os YAMLs depois, durante a prova.

O push exige autenticação na sua conta. Configure-a no próprio terminal: se usar
GitHub CLI, `gh auth login` oferece autorização pelo navegador. Para SSH, é preciso
uma chave cadastrada na conta; trocar a URL pelo endereço SSH não autentica sozinho.
Nunca cole tokens, senhas ou chaves no chat ou nos manifests.

## 3. Vincular ao laboratório

No arquivo lab.env da raiz do material, configure:

```text
REPO_URL=https://github.com/SEU-USUARIO/ex380-meus-manifests.git
HTTP_BASE=https://raw.githubusercontent.com/rossettimateus/ex380-lab/main
```

Somente REPO_URL muda por aluno. HTTP_BASE continua apontando para o conteúdo
central. Os demais campos de lab.env descrevem seu cluster e suas identidades.
Na prova, a Application observará main e o caminho machineconfigs do seu repo.
Nenhum YAML de resposta é fornecido por esta configuração.

Confira o commit inicial publicado:

```bash
git -C work/candidate remote -v
git -C work/candidate ls-remote origin refs/heads/main
```

Depois de escrever seus manifests, publique a partir da raiz do material:

```bash
git -C work/candidate add machineconfigs/
git -C work/candidate commit -m 'Adicionar meus manifests'
git -C work/candidate push origin main
```

O Argo CD usa REPO_URL; os nodes usam os URLs HTTP_BASE/config/site.conf e
HTTP_BASE/config/banner.txt. O checkout do material mantém seu próprio origin
apontando para rossettimateus/ex380-lab. Não troque os dois remotes.

Mantenha o repo de manifests público e disponível até concluir a recuperação/limpeza.
Não publique lab.env, credenciais ou evidências. Para continuar a preparação,
volte a [01-preparacao.md](01-preparacao.md).
