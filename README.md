<div align="center">

# 💊 StockMed — Sistema de Controle Farmacêutico

<img src="static/logo.png" alt="StockMed Logo" width="140"/>

*Um sistema web robusto e intuitivo de gestão de inventário e medicamentos, inspirado em padrões corporativos (ERP).*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-success?style=for-the-badge&logo=render&logoColor=white)](https://stockmed-oy39.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 Teste a Aplicação Online

Você já pode testar o **StockMed** diretamente na nuvem através do link abaixo:
👉 **[Acessar StockMed em Produção](https://stockmed-oy39.onrender.com)**

---

## 📋 Sobre o Projeto

O **StockMed** foi desenvolvido como parte do curso de **Análise e Desenvolvimento de Sistemas** na Universidade Estácio. Trata-se de uma aplicação web completa para o controle de estoque em estabelecimentos farmacêuticos, focando em segurança de dados, controle de lotes, validades, auditoria de movimentações e níveis hierárquicos de acesso corporativo.

---

## ✨ Funcionalidades Principais

- 🔐 **Autenticação Segura:** Sistema de login e registro com criptografia avançada de senhas (*Werkzeug Security*).
- 👥 **Controle de Permissões (RBAC):** Níveis de acesso distintos para **Administrador** (gestão total, exclusão de itens e painel de auditoria) e **Operador**.
- 📦 **Gestão de Inventário:** Cadastro detalhado contendo código de barras único, nome, descrição, lote, quantidade atual, data de validade e laboratório fabricante.
- 🔄 **Lançamento de Movimentações:** Registro de entradas, saídas/vendas, avarias, vencimentos e empréstimos com baixa automática no estoque.
- 🛡️ **Auditoria de Estoque:** Relatório completo e restrito a administradores com o histórico de todas as operações realizadas no sistema.
- 📱 **Design Responsivo e Mobile-First:** Layouts adaptados para computadores e dispositivos móveis, com tabelas otimizadas e rolagem horizontal fluida.
- 🎨 **Identidade Visual Personalizada:** Interface desenhada com paleta de cores corporativa e logótipo próprio.

---

## 🚀 Tecnologias e Ferramentas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask (com gerenciamento de sessões seguras)
- **Servidor WSGI:** Gunicorn
- **Banco de Dados:** MySQL (Hospedado na nuvem via Aiven)
- **Hospedagem & Deploy:** Render (Pipeline contínua integrada ao GitHub)
- **Estilização:** HTML5, CSS3 (Design System próprio com Media Queries)
- **Controle de Versão:** Git & GitHub

---

## 📂 Estrutura do Projeto

```text
sistema_farmacia/
│
├── static/
│   └── logo.png                  # Logótipo oficial do StockMed
├── templates/
│   ├── cadastrar.html            # Registro de novos usuários
│   ├── cadastrar_medicamento.html# Cadastro de novos produtos e lotes
│   ├── estoque.html              # Consulta, filtros e ações de exclusão
│   ├── historico_movimentacoes.html # Auditoria e relatório de movimentações
│   ├── index.html                # Menu Principal / Dashboard responsivo
│   ├── login.html                # Tela de autenticação
│   └── movimentacao.html         # Registro de entradas, saídas e avarias
│
├── .gitignore                    # Arquivos ignorados pelo Git
├── app.py                        # Lógica principal, rotas, conexão DB e sessões
├── criar_admin.py                # Utilitário para geração de usuário administrador
├── requirements.txt              # Dependências do projeto (Flask, Gunicorn, MySQL)
└── README.md                     # Documentação oficial do projeto
⚙️ Instalação e Configuração Local (Opcional)

Se desejar executar o projeto localmente na sua máquina:

1. Clonar o Repositório
Bash
git clone [https://github.com/JVictorCastro-22/StockMed.git](https://github.com/JVictorCastro-22/StockMed.git)
cd StockMed/sistema_farmacia
2. Instalar as Dependências
Bash
pip install -r requirements.txt
3. Configurar o Banco de Dados
Execute os scripts SQL no seu MySQL Workbench para criar as tabelas necessárias (usuarios, medicamentos, movimentacoes_estoque) com suporte a codificação utf8mb4.

4. Executar a Aplicação Localmente
Bash
python app.py
Acesse no navegador: http://127.0.0.1:5000

👨‍💻 Autor
Desenvolvido por João Victor de Souza e Silva Castro (JVictorCastro-22).