from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# --- Chave secreta obrigatória para gerenciar sessões (session) e alertas (flash) ---
app.secret_key = "chave_secreta_farmacia_2026"

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        database="farmacia",
        user="root",
        password=""  # Mude para a sua senha do MySQL se tiver configurado uma
    )
    return conn


# ============================================================
# 1. ROTA: LOGIN (Exibe tela e valida senha)
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha_digitada = request.form["senha"]
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE;", (email,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        # Verifica se o usuário existe e se a senha digitada bate com o hash salvo
        if usuario and check_password_hash(usuario["senha_hash"], senha_digitada):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            session["usuario_perfil"] = usuario["perfil"]
            return redirect(url_for("pagina_inicial"))
        else:
            flash("E-mail ou senha incorretos (ou usuário inativo)!")
            return redirect(url_for("login"))
            
    return render_template("login.html")


# ============================================================
# 2. ROTA: LOGOUT (Encerra a sessão)
# ============================================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso!")
    return redirect(url_for("login"))


# ============================================================
# 3. ROTA: CADASTRO DE USUÁRIOS
# ============================================================
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        perfil = request.form.get("perfil", "Operador")
        
        # Criptografa a senha antes de salvar no MySQL
        senha_hash = generate_password_hash(senha)
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO usuarios (nome, email, senha_hash, perfil) 
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(sql, (nome, email, senha_hash, perfil))
            conn.commit()
            flash("Usuário cadastrado com sucesso! Faça login.")
            return redirect(url_for("login"))
        except mysql.connector.Error as err:
            flash(f"Erro ao cadastrar: {err}")
            return redirect(url_for("cadastrar_usuario"))
        finally:
            cur.close()
            conn.close()
            
    return render_template("cadastrar.html")


# ============================================================
# 4. ROTA PRINCIPAL (Protegida por Login)
# ============================================================
@app.route("/")
def pagina_inicial():
    # Trava de segurança: Redireciona para o login se não estiver logado
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    conn = get_db_connection()
    cur = conn.cursor(buffered=True, dictionary=True)
    cur.execute("SELECT * FROM medicamentos;")
    medicamentos = cur.fetchall()
    cur.close()
    conn.close()
    
    # Envia os dados do usuário para serem exibidos no topo do index.html
    return render_template(
        "index.html",
        lista_medicamentos=medicamentos,
        usuario_nome=session.get("usuario_nome"),
        usuario_perfil=session.get("usuario_perfil")
    )


# ============================================================
# 5. ROTA DE ADIÇÃO DE MEDICAMENTO (Protegida por Login)
# ============================================================
@app.route("/adicionar", methods=["POST"])
def adicionar_medicamento():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    codigo = request.form["codigo_barras"]
    nome = request.form["nome"]
    descricao = request.form.get("descricao", "")  # Captura descrição se enviada
    lote = request.form["lote"]
    quantidade = request.form["quantidade_atual"]
    validade = request.form["validade"]
    laboratorio = request.form["laboratorio"]
    
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO medicamentos (codigo_barras, nome, descricao, lote, quantidade_atual, validade, laboratorio) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (codigo, nome, descricao, lote, quantidade, validade, laboratorio)
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("pagina_inicial"))


if __name__ == "__main__":
    app.run(debug=True)