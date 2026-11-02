# Fontes e decisões de versão

Consulta: 02/11/2026. Fontes primárias; verificação documental não substitui teste no cluster.

| Decisão | Referência |
|---|---|
| GitOps 1.21.5 inclui OCP 4.22; usar canal 1.21 e registrar patch disponível | [Release notes 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/release_notes/gitops-release-notes) |
| Instalação por catálogo, namespace e Subscription | [Installing GitOps 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/installing_gitops/installing-openshift-gitops) |
| OCP 4.22 orienta novos MCs com Ignition 3.5 | [Machine configuration 4.22](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/machine_configuration/machine-configs-configure) |
| Namespace da instância cluster-scoped via Subscription | [Declarative cluster configuration 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/declarative_cluster_configuration/configuring-an-openshift-cluster-by-deploying-an-application-with-cluster-configurations) |
| Elevação de escopo e permissões padrão não equivalentes a cluster-admin | [Multitenancy 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/multitenancy/multitenancy-support-in-gitops) |
| Dex com openShiftOAuth | [SSO Dex 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/access_control_and_user_management/configuring-sso-for-argo-cd-using-dex) |
| Instância e reencrypt | [Argo CD instance 1.21](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.21/html/argo_cd_instance/setting-up-argocd-instance) |
| Ciclo de vida e compatibilidade histórica de 1.11 | [OpenShift Operator Life Cycles](https://access.redhat.com/support/policy/updates/openshift_operators) |
| Semântica de URL e data URI, bytes/mode | [Ignition specification 3.5.0 — upstream primário](https://coreos.github.io/ignition/configuration-v3_5/) |
| Instalação conforme plataforma | [Documentação OCP 4.22](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22) |

As decisões de topologia (Git/HTTP externos, dois workers, pool de um node, payloads inofensivos, sync manual) são escolhas deste exercício para limitar impacto e tornar o diagnóstico observável, não requisitos universais do produto. Nenhuma delas transforma o procedimento em seguro para produção.

As APIs usadas são `machineconfiguration.openshift.io/v1` para MC/MCP, `argoproj.io/v1beta1` para ArgoCD e `argoproj.io/v1alpha1` para Application/AppProject, além de OLM Subscription v1alpha1/OperatorGroup v1 e RBAC v1. O pacote recomenda dry-run e inspeção dos CRDs realmente servidos antes da aplicação; não houve validação server-side nesta sessão.
