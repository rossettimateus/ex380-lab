# Parte 3 — Validação

Na raiz do kit, obtenha o SHA final do repo de manifests com `git -C work/candidate rev-parse HEAD` e registre o valor completo em `EXPECTED_REVISION` no `lab.env`. Confirme que foi enviado: `git -C work/candidate ls-remote origin refs/heads/main`. Isso evita aceitar um Synced de commit antigo.

Execute, com o administrador e na raiz do projeto:

```bash
python3 scripts/validate.py
bash scripts/evidence.sh
```

O validador retorna código 0 quando suas verificações passam e 1 se há falhas. É uma avaliação instantânea, não aguarda automaticamente o rollout. Falhas durante a convergência são esperadas; investigue e rode novamente após estabilizar. Erros de conexão/permissão podem interromper coleta: resolva o acesso, não interprete ausência de dados como aprovação.

O script verifica configuração de Argo CD, Dex, grupo, Route, permissões por impersonation, AppProject, origem/destino, política manual, estado de sincronização, revisão, dois MCs, fontes HTTP, render do pool, contagens/gerações, estado do node, hash SHA256, modo e proprietário. O teste de permissão observa a autorização efetiva; não é uma auditoria completa de todos os privilégios preexistentes do SA.

`oc debug` cria pods temporários; os comandos dentro do host são somente leitura. A versão exata do patch GitOps é registrada pelas evidências/CSV e pode ser posterior a 1.21.5. Há uma limitação deliberada: a configuração RBAC é comparada ao mapeamento esperado; políticas equivalentes escritas de outra forma podem exigir avaliação manual.

## Testes manuais obrigatórios

- Abra a Route em navegador confiando na CA do cluster e faça login **via OpenShift**, com LAB_USER, sem usar o admin local do Argo CD.
- Verifique a associação a `gitops-admins` na sessão e realize refresh/sync da Application. Um login bem-sucedido não prova permissão.
- Em sessão privada, entre com o usuário de leitura fora do grupo. Ele deve ver a aplicação e receber negação ao tentar sincronizar. Não use um token administrativo para testar esse usuário.
- Inspecione os pods da instância e eventos para detectar Pending, CrashLoop ou problemas de recursos; `Available` sozinho não substitui o teste da UI.
- Confira que não adicionou um binding cluster-admin para o controller. `oc auth can-i` confirma o permitido, mas não a origem da permissão.
- Compare baseline e final para garantir que master e outros workers não receberam o papel `lab`.

Uma Application pode mostrar `Healthy` sem comprovar o conteúdo do host: MachineConfig não fornece automaticamente um health check end-to-end do rollout do MCP. Este roteiro não exige personalização de health check; o avaliador externo faz essa comprovação.
