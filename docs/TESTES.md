# Testes e limites

Execute `python3 tests/test_preparation.py` com Python 3 e PyYAML. A suíte verifica
os manifests, Ignition, URLs HTTP, modos/propriedade, payloads do suporte e links.
Não chama oc, não aplica MCs nem sincroniza.

A preparação valida dry-run server-side e HTTP 200 sem redirect pela estação,
nodes e pod. Isso não comprova aplicação no host: RBAC manual, conexão Git,
Application, Sync e resultado do rollout ficam para o aluno.
