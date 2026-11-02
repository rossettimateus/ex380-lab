# Falha separada — source sem esquema HTTP(S)

Faça somente após concluir o caminho feliz, salvar o commit bom e executar o validador com sucesso. Este teste não é pré-requisito da prova. Não há promessa de erro idêntico entre versões: a API pode aceitar o objeto, mas a validação Ignition do MCO pode recusar a renderização. O `Degraded` pode ser de renderização, sem que o arquivo ruim chegue ao node.

## A. Registrar e limitar

1. Confirme API, único worker de `lab`, ausência de workload real e saúde dos demais pools.
2. Salve o SHA bom: `git -C work/candidate rev-parse HEAD`. Registre também currentConfig/desiredConfig do node e o rendered atual do MCP.
3. Confirme auto-sync desativado. Pause **somente** `lab`: `oc patch mcp lab --type=merge -p '{"spec":{"paused":true}}'`. Pausa limita rollout; não impede renderização nem protege contra uma atualização já iniciada. Por isso comece de um estado convergido.

## B. Alteração só no Git local

```bash
python3 scripts/break-source.py work/candidate/machineconfigs/99-lab-site.yaml
git -C work/candidate diff
```

O script remove exclusivamente o esquema `http://` ou `https://` do primeiro arquivo de `99-lab-site`, verifica nome/papel/caminho e não acessa o cluster. Adapte o nome local se seu arquivo tiver outro nome. `99-lab-banner` deve continuar intacto.

Antes do push, tente `oc apply --dry-run=server -f work/candidate/machineconfigs/99-lab-site.yaml`. Guarde a resposta. **Dry-run aceito não prova que Ignition/MCO renderiza ou aplica.** Se for rejeitado, o objetivo de observar a primeira camada de rejeição já foi atingido; não tente contorná-la.

Se a API aceitar, faça commit dessa única alteração, push e uma sincronização manual. Não use prune. Aguarde a reconciliação e colete eventos, status da Application, condições de `lab`, logs do machine-config-controller e estado do node. `scripts/evidence.sh` pode ser usado, copiando a pasta para um nome novo antes de cada coleta.

## C. O que comparar

| Evidência | Pergunta |
|---|---|
| Application operação/Synced | O objeto foi persistido? Houve falha já no sync? |
| MCP conditions | Apareceu RenderDegraded, NodeDegraded ou outra condição? Qual mensagem exata? |
| Rendered desejado | Foi gerado um novo rendered ou o anterior permaneceu? |
| Node annotations | desired/current mudaram? O node permaneceu Done? |
| Arquivo no host | O conteúdo bom foi preservado? |

Não é necessário despausar para observar um erro de renderização. Se, excepcionalmente, a renderização aceitar essa fonte e você quiser observar a etapa seguinte, só despause após revisar o diagnóstico e confirmar que o worker é descartável. Espere impacto no MCO e possível reboot. Este roteiro não despausa automaticamente para produzir degradação.

## D. Recuperar

Reverta **o commit de falha** no Git (não necessariamente HEAD se fez outros commits), publique a reversão e sincronize manualmente. Confira a URL válida no objeto live e a ausência do erro de renderização. Depois retire a pausa com `oc patch mcp lab --type=merge -p '{"spec":{"paused":false}}'`. Atualize EXPECTED_REVISION para o commit de recuperação e repita a validação completa.

Se a recuperação não convergir, siga `06-recuperacao-limpeza.md`; não edite annotations para fingir Done, não apague rendered configs e não use force file como primeira tentativa.

## Por que data: não é a correção?

`http://host:8080/config/site.conf` aponta para um download remoto. `data:,texto` incorpora texto; `data:;base64,...` incorpora bytes codificados. `data:host/caminho` não transforma host em HTTP e normalmente nem forma uma data URI válida (falta separador vírgula). Use o protocolo exigido pelo conteúdo remoto. Um curl no laptop não comprova que o node ou o controlador alcançam o mesmo endereço.
