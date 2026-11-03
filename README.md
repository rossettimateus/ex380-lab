# GitOps: configurar /etc/motd nos workers

## Seu exercício

Escreva **uma MachineConfig** para colocar o texto de [config/motd.txt](config/motd.txt)
em `/etc/motd` nos **workers**, com proprietário root:root e permissão **0444**
(decimal 292). Use Ignition compatível com OpenShift 4.22 e conteúdo incorporado
em uma data URI base64. O exemplo deste exercício não usa download HTTP pelo MCD.

O repo não fornece a MachineConfig pronta. Você escreve e aplica pelo Argo CD.

## Repositório e Kustomize

- Git: https://github.com/rossettimateus/ex380-lab.git
- Branch: **main**
- Path da Application: **machineconfigs**

```text
config/motd.txt                     # texto que você vai colocar no host
machineconfigs/kustomization.yaml  # base vazia para você adicionar seu YAML
```

Primeiro crie sua instância Argo CD em um namespace separado, configure seu acesso
e conecte este Git. O Operator já instalado pode ser reutilizado. Depois:

1. Crie seu arquivo YAML em machineconfigs/.
2. Adicione o nome dele à lista resources do kustomization.yaml.
3. Faça commit e push.
4. Faça Refresh e Sync na sua Application do Argo CD.
5. Aguarde o pool worker atualizado e sem degradação; confira /etc/motd em um worker.

No reset, a base volta a ficar vazia e os recursos do exercício são retirados para
você refazer o processo. O histórico Git preserva suas tentativas anteriores.
Masters não são alvo deste exercício.
Mudanças de MachineConfig podem causar drain e reinicialização dos workers.
