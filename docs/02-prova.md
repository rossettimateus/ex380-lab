# Exercício — GitOps e duas MachineConfigs

O suporte já está preparado: GitOps, Route HTTPS reencrypt, usuário/grupo, servidor
HTTP e dois manifests no Git. Use os dados do handoff ou lab.env.

## 1. Configurar o grupo no Argo CD

Edite o recurso **ArgoCD openshift-gitops**, namespace **openshift-gitops**.
Na política RBAC, mantenha como grupo administrativo:

```yaml
policy: |
  g, gitops-admins, role:admin
```

Remova desse campo os outros grupos definidos explicitamente. Confirme que seu
usuário pertence a gitops-admins. Entre na Route fornecida pela opção OAuth OpenShift
e confira acesso para criar Applications. A Route usa HTTPS reencrypt.
O preparador deve ter verificado a permissão Kubernetes do controller para MCs.

## 2. Conectar o Git

Na UI, em **Settings → Repositories**, conecte **REPO_URL** do handoff.
O Git contém os dois YAMLs em machineconfigs/. As fontes HTTP ficam dentro deles.

## 3. Criar a Application

Em **Applications → New App**, configure:

| Campo | Valor |
|---|---|
| Application Name | `node-config` |
| Project Name | **`default`** |
| Sync Policy | **Manual** |
| Repository URL | `REPO_URL` do handoff |
| Revision | `main` |
| Path | **`machineconfigs`** |
| Destination Cluster URL | `https://kubernetes.default.svc` |
| Destination Namespace | `openshift-gitops` |

Use o projeto default existente. Path é relativo à raiz do Git, sem barra inicial:

```text
repo/
└── machineconfigs/
    ├── 99-lab-site.yaml
    └── 99-lab-banner.yaml
```

O campo Repository URL recebe o Git, não o servidor HTTP. O destino é o cluster
local da instância. MachineConfigs são cluster-scoped e não recebem namespace;
o campo Namespace da Application não altera isso.

## 4. Conferir e sincronizar

| MachineConfig | Papel | Arquivo no host | Modo |
|---|---|---|---|
| `99-lab-site` | `worker` | `/etc/ex380-lab/site.conf` | `0644` (decimal `420`) |
| `99-lab-banner` | `worker` | `/etc/ex380-lab/banner.txt` | `0755` (decimal `493`) |

Ambas usam Ignition 3.5.0, root:root e contents.source com URLs http:// diferentes.
O modo é declarativo; não execute chmod no host. Não é preciso executar o arquivo
de modo 0755, alterar serviços ou criar outro pool.

Confira as duas MCs na Application e faça **Sync manual**. Não aplique os YAMLs
com oc para concluir o exercício.

## 5. Validar

- Application Synced e operação bem-sucedida; Healthy quando aplicável.
- Duas MachineConfigs criadas no OpenShift.
- Pool **worker** UPDATED=True, UPDATING=False e DEGRADED=False.
- Workers Ready e currentConfig=desiredConfig.
- Dois arquivos com conteúdo das fontes HTTP, root:root e modos 0644/0755.

Masters ficam fora do exercício. Aguarde o MCO: pode haver reboots sequenciais.
Confira os arquivos no host, além de Synced na UI. Veja [a validação](03-validacao.md).
