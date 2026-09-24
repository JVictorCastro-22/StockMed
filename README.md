

<div align="center">

# 💊 StockMed — Sistema de Controle Farmacêutico

<img src="static/logo.png" alt="StockMed Logo" width="140"/>

*Um sistema web robusto e intuitivo de gestão de inventário e medicamentos, inspirado em padrões corporativos (ERP).*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 📋 Sobre o Projeto

O **StockMed** foi desenvolvido como parte do curso de **Análise e Desenvolvimento de Sistemas**. Trata-se de uma aplicação web completa para o controle de estoque em estabelecimentos farmacêuticos, focando em segurança de dados, controle de lotes, validades e níveis hierárquicos de acesso corporativo.

---

## ✨ Funcionalidades Principais

- 🔐 **Autenticação Segura:** Sistema de login e registro com criptografia de senhas (*Werkzeug Security*).
- 👥 **Controle de Permissões (RBAC):** Níveis de acesso distintos para **Administrador** (gestão total, exclusão e auditoria) e **Operador/Auxiliar**.
- 📦 **Gestão de Inventário:** Cadastro detalhado contendo código de barras, nome, descrição, lote, quantidade atual, data de validade e laboratório fabricante.
- 🔍 **Busca e Filtros Avançados:** Consulta dinâmica de estoque com filtragem em tempo real por nome ou código de barras.
- 🎨 **Identidade Visual Personalizada:** Interface responsiva desenhada com paleta de cores corporativa e logótipo próprio.

---

## 🚀 Tecnologias e Ferramentas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask (com gerenciamento de sessões seguras)
- **Banco de Dados:** MySQL / MySQL Workbench
- **Estilização:** HTML5, CSS3 (Design System próprio)
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
│   ├── index.html                # Menu Principal / Dashboard
│   └── login.html                # Tela de autenticação
│
├── .gitignore                    # Arquivos ignorados pelo Git
├── app.py                        # Lógica principal, rotas e controle de sessões
├── criar_admin.py                # Utilitário para geração de usuário administrador
└── README.md                     # Documentação oficial do projeto
```

---

⚙️ **Instalação e Configuração Passo a Passo**

### 1. Clonar o Repositório

Abra o seu terminal ou prompt de comando e execute:

```bash
git clone [https://github.com/JVictorCastro-22/sistema_farmacia.git](https://github.com/JVictorCastro-22/sistema_farmacia.git)
cd sistema_farmacia/sistema_farmacia

```

### 2. Instalar as Dependências

Instale o Flask, o conector do MySQL e as ferramentas de segurança:

```bash
pip install flask mysql-connector-python werkzeug

```

### 3. Configurar o Banco de Dados

Abra o seu **MySQL Workbench** e execute os comandos SQL abaixo para criar o banco e as tabelas estruturadas:

```sql
CREATE DATABASE IF NOT EXISTS farmacia;
USE farmacia;

-- Tabela de Usuários (com controle de perfil)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(250) NOT NULL,
    perfil VARCHAR(50) DEFAULT 'Auxiliar',
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Medicamentos
CREATE TABLE medicamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    lote VARCHAR(50) NOT NULL,
    quantidade_atual INT DEFAULT 0,
    validade DATE NOT NULL,
    laboratorio VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Movimentações de Estoque (Auditoria)
CREATE TABLE movimentacoes_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_medicamento INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    quantidade INT NOT NULL,
    data DATE NOT NULL DEFAULT (CURRENT_DATE),
    hora TIME NOT NULL DEFAULT (CURRENT_TIME),
    motivo VARCHAR(150),
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```

### 4. Ajustar as Credenciais de Conexão

Abra o arquivo `app.py` no seu editor de código (como o VS Code) e verifique se as configurações de conexão com o MySQL correspondem ao seu ambiente local:

```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        database="farmacia",
        user="root",
        password=""  # Insira sua senha do MySQL, se houver
    )
    return conn

```

---

## 🚀 Como Executar a Aplicação

1. Com o terminal aberto na pasta do sistema, execute o servidor Flask:
```bash
py app.py

```


2. O terminal exibirá um endereço local (geralmente `http://127.0.0.1:5000`).
3. Abra o seu navegador web de preferência, acesse **`http://127.0.0.1:5000/login`** e faça o login no sistema.

---

## 👨‍💻 Autor

Desenvolvido por **João Victor de Souza e Silva Castro** (JVictorCastro-22).

