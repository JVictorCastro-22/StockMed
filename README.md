Aqui está o **README.md** totalmente atualizado, refletindo todas as evoluções que fizemos no projeto **StockMed** (a identidade visual com o logo, a autenticação de usuários, níveis de permissão entre Administrador e Operador/Auxiliar, filtros de busca, novas rotas e a estrutura completa de pastas):

```markdown
# 💊 StockMed - Sistema de Controle Farmacêutico

Sistema web robusto e moderno desenvolvido em **Python (Flask)** e **MySQL** para o gerenciamento inteligente de estoque e controle de medicamentos em estabelecimentos farmacêuticos. Projeto desenvolvido como parte do curso de Análise e Desenvolvimento de Sistemas.

---

## 🚀 Tecnologias e Ferramentas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask (com gerenciamento de sessões e rotas protegidas)
- **Segurança:** Werkzeug Security (hash seguro de senhas)
- **Banco de Dados:** MySQL / MySQL Workbench
- **Interface e Estilização:** HTML5, CSS3 (Design corporativo personalizado)
- **Controle de Versão:** Git e GitHub

---

## ✨ Funcionalidades do Sistema

- **Autenticação Segura:** Sistema de login e cadastro de usuários com criptografia de senha.
- **Controle de Permissões (RBAC):** Níveis de acesso diferenciados entre **Administrador** (com privilégios para excluir e gerenciar) e **Operador/Auxiliar**.
- **Gestão de Medicamentos:** Cadastro detalhado com código de barras, lote, quantidade, validade e laboratório.
- **Consulta e Filtros Avançados:** Tela de estoque com barra de pesquisa interativa por nome ou código de barras.
- **Identidade Visual Personalizada:** Interface com paleta de cores corporativa e logótipo integrado.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
- [Python](https://www.python.org/) (versão 3.8 ou superior)
- [Git](https://git-scm.com/)
- [MySQL Server / MySQL Workbench](https://dev.mysql.com/downloads/)

---

## 📂 Estrutura do Projeto

```text
sistema_farmacia
│
├── static/
│   └── logo.png                 # Logótipo oficial do StockMed
├── templates/
│   ├── cadastrar.html           # Tela de registro de novos usuários
│   ├── cadastrar_medicamento.html # Tela de cadastro de remédios/lotes
│   ├── estoque.html             # Tabela de consulta, filtros e exclusão
│   ├── index.html               # Menu principal / Dashboard
│   └── login.html               # Tela de autenticação
│
├── .gitignore                   # Arquivos ignorados pelo Git
├── app.py                       # Lógica principal do Flask, rotas e segurança
├── criar_admin.py               # Script utilitário para criar admin inicial
└── README.md                    # Documentação do projeto

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

