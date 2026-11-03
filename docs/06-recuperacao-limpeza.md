# Limpeza após concluir

Mantenha HTTP disponível até terminar o rollback.

1. Retire os dois manifests do Git e sincronize a remoção, revisando prune apenas
   para essas MCs. Se remover diretamente do cluster, impeça recriação pela Application.
2. Aguarde workers Ready/Done e pool convergente sem as MCs; confira a retirada dos arquivos.
3. Remova a Application e o cadastro do repo do exercício, preservando outros usos.
4. Se exclusivos do lab, remova ex380-support e gitops-admins. Desinstale GitOps
   somente se não houver outro uso. Confira todos os pools e Operators saudáveis.

Não há pool customizado a remover. Preserve infraestrutura do cluster e provedor.
