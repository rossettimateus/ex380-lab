# Validação após seu Sync

1. Faça login OAuth com o usuário de gitops-admins e confira acesso para criar apps.
2. Confira a política com gitops-admins como único grupo administrativo explícito.
3. Confira Route HTTPS reencrypt, repo conectado e Application no projeto default.
4. Confira node-config Synced e a última operação bem-sucedida.
5. Consulte `oc get mc 99-lab-site 99-lab-banner` e `oc get mcp worker`.
6. Aguarde UPDATED=True, UPDATING=False e DEGRADED=False no pool worker.
7. Confira os dois arquivos nos workers: bytes das fontes HTTP, root:root e 0644/0755.

`python3 scripts/validate.py`, com lab.env real na raiz, automatiza configuração,
objetos, pools e arquivos. Só lê os hosts via oc debug, que cria pods transitórios.
Execute depois do Sync; ausências antes dele são esperadas. Login e uso da UI
continuam sendo testes manuais. Não há teste negativo ou experimento de falha.
