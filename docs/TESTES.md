# Verificação e limites

Esta suíte de manutenção foi executada em ambiente com Python 3, Git e Bash.
Ela não determina o sistema operacional necessário ao aluno. Execute na raiz do
clone em um terminal que forneça essas ferramentas:

```bash
python3 tests/test_preparation.py
```

A suíte local verifica:

- igualdade dos payloads públicos e de referência e ausência de respostas no kit;
- sintaxe Python/Bash e links relativos da documentação;
- exclusão de arquivos privados pelo .gitignore;
- tratamento de URLs HTTP e HTTPS sem modificar manifests;
- preparação do Git bare, esqueleto sem respostas e repetição sem perder o commit;
- atualização de metadados pelo hook após novo push;
- download dos payloads, ls-remote e clone Git por HTTP anônimo em localhost.

O teste HTTP escuta somente em 127.0.0.1, usa porta livre e diretório temporário e
encerra o servidor ao terminar. Não chama oc, GitHub, instala Operators ou altera
cluster, credenciais reais ou manifests da prova. O teste da ausência de respostas
é para contribuidores do kit inicial; após escrever sua solução, essa asserção
naturalmente falhará e não deve ser usada para avaliar seu exercício.

Uma execução anterior da preparação validou, em um cluster descartável 4.22.20,
a sessão/permissões administrativas, seis nodes RHCOS (três workers separados),
pool lab com um worker, pools/Operators estabilizados, Git público, os dois
payloads reais na estação/todos os nodes/pod e login OAuth real. Dados do ambiente,
evidências e credenciais não fazem parte deste repositório. Isso não comprova que
outro cluster está pronto: repita todas as verificações de docs/01-preparacao.md.

A instalação do Operator, Argo CD, RBAC do exercício, sync, aplicação dos dois
MachineConfigs, reboot após esses manifests, validação final da prova e recuperação
da falha não foram executados como parte da preparação. scripts/validate.py serve
para essa etapa posterior, depois que o aluno resolver a prova.

A suíte não certifica execução nativa de todos os scripts em Windows ou macOS.
Os `.sh` exigem Bash no ambiente em que forem executados.
