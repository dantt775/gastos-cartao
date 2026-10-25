# 💳 Controle de Gastos com GitHub Issues & Actions

Sistema serverless e 100% gratuito para controle de gastos do cartão de crédito utilizando **GitHub Issues** como interface e **GitHub Actions** como processador.

---

## 📁 Estrutura do Projeto

```text
gastos-cartao/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── novo-gasto.yml        # Formulário estruturado para abrir a Issue
│   └── workflows/
│       └── processar-gasto.yml   # Action que roda ao abrir a issue
├── data/
│   └── gastos.json               # Banco de dados com gastos e totais mensais
├── scripts/
│   └── registrar.py              # Script Python que processa a despesa
├── .gitignore
└── README.md
```

---

## 🚀 Como Inicializar este Repositório no GitHub

1. Crie um novo repositório **Privado** no [GitHub](https://github.com/new) com o nome que desejar (ex: `gastos-cartao`).
2. No seu terminal, navegue até esta pasta e suba os arquivos:

```bash
cd c:\Users\admin\Documents\repos\gastos-cartao
git init
git add .
git commit -m "feat: inicializa sistema de controle de gastos"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/gastos-cartao.git
git push -u origin main
```

---

## 🔒 Configuração de Permissões no GitHub

Para que o GitHub Actions consiga salvar as alterações e fechar as issues:

1. No seu repositório no GitHub, vá em **Settings** > **Actions** > **General**.
2. Na seção **Workflow permissions**, selecione:
   - ✅ **Read and write permissions**
3. Clique em **Save**.

---

## 📱 Como Usar no Dia a Dia

1. No computador ou pelo app do **GitHub no celular**, vá na aba **Issues**.
2. Clique em **New Issue** e escolha o template **"Registrar Gasto"**.
3. Preencha:
   - **Valor:** Ex: `45.90` ou `120,00`
   - **Descrição:** Ex: `Supermercado Carrefour`
   - **Categoria:** Escolha no dropdown
4. Clique em **Submit new issue**.
5. Em cerca de 15 segundos:
   - A Action processa o gasto.
   - Atualiza o arquivo `data/gastos.json` com o novo total do mês.
   - Responde na Issue com uma tabela com o valor registrado e o total acumulado do mês.
   - Fecha a Issue automaticamente.
