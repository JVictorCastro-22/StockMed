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


# 1. ROTA: LOGIN (Exibe tela e valida senha)

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



# 2. ROTA: LOGOUT (Encerra a sessão)

@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso!")
    return redirect(url_for("login"))


# 3. ROTA: CADASTRO DE USUÁRIOS

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        perfil = request.form.get("perfil", "Auxiliar")
        
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



# 4. ROTA PRINCIPAL / DASHBOARD (Menu Inicial)

@app.route("/")
def pagina_inicial():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    
    return render_template(
        "index.html",
        usuario_nome=session.get("usuario_nome"),
        usuario_perfil=session.get("usuario_perfil")
    )



# 5. ROTA: TELA DE CADASTRO DE MEDICAMENTO

@app.route("/medicamento/novo", methods=["GET", "POST"])
def cadastrar_medicamento():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        codigo = request.form["codigo_barras"]
        nome = request.form["nome"]
        descricao = request.form.get("descricao", "")
        lote = request.form["lote"]
        quantidade = request.form["quantidade_atual"]
        validade = request.form["validade"]
        laboratorio = request.form["laboratorio"]
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO medicamentos (codigo_barras, nome, descricao, lote, quantidade_atual, validade, laboratorio) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (codigo, nome, descricao, lote, quantidade, validade, laboratorio))
            conn.commit()
            flash("Medicamento cadastrado com sucesso!", "sucesso")
        except mysql.connector.Error as err:
            flash(f"Erro ao cadastrar medicamento: {err}", "erro")
        finally:
            cur.close()
            conn.close()
            
        return redirect(url_for("listar_estoque"))
        
    return render_template("cadastrar_medicamento.html")



# 6. ROTA: LISTAR E FILTRAR ESTOQUE

@app.route("/estoque")
def listar_estoque():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    termo_busca = request.args.get("busca", "")
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    if termo_busca:
        # Filtra por nome ou código de barras
        sql = "SELECT * FROM medicamentos WHERE nome LIKE %s OR codigo_barras LIKE %s;"
        like_termo = f"%{termo_busca}%"
        cur.execute(sql, (like_termo, like_termo))
    else:
        cur.execute("SELECT * FROM medicamentos;")
        
    medicamentos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template(
        "estoque.html",
        lista_medicamentos=medicamentos,
        busca=termo_busca,
        usuario_perfil=session.get("usuario_perfil")
    )


# 7. ROTA: EXCLUIR MEDICAMENTO (Apenas Administrador)

@app.route("/medicamento/deletar/<int:id>", methods=["POST"])
def deletar_medicamento(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    # Trava de segurança no backend: verifica se é administrador
    if session.get("usuario_perfil") != "Administrador":
        flash("Acesso negado! Apenas administradores podem excluir registros.")
        return redirect(url_for("listar_estoque"))
        
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM medicamentos WHERE id = %s;", (id,))
        conn.commit()
        flash("Medicamento excluído com sucesso!")
    except mysql.connector.Error as err:
        flash(f"Erro ao excluir: {err}")
    finally:
        cur.close()
        conn.close()
        
    return redirect(url_for("listar_estoque"))

if __name__ == "__main__":
    app.run(debug=True)