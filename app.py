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


# ============================================================
# 4. ROTA PRINCIPAL / DASHBOARD (Menu Inicial)
# ============================================================
@app.route("/")
def pagina_inicial():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    
    return render_template(
        "index.html",
        usuario_nome=session.get("usuario_nome"),
        usuario_perfil=session.get("usuario_perfil")
    )


# ============================================================
# 5. ROTA: TELA DE CADASTRO DE MEDICAMENTO
# ============================================================
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


# ============================================================
# 6. ROTA: LISTAR E FILTRAR ESTOQUE
# ============================================================
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


# ============================================================
# 7. ROTA: EXCLUIR MEDICAMENTO (Apenas Administrador)
# ============================================================
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


# ============================================================
# 8. ROTA: REGISTAR NOVA MOVIMENTAÇÃO (Entradas/Saídas)
# ============================================================
@app.route("/movimentacao/nova", methods=["GET", "POST"])
def nova_movimentacao():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        id_medicamento = request.form["id_medicamento"]
        tipo = request.form["tipo"]
        quantidade = int(request.form["quantidade"])
        motivo = request.form.get("motivo", "").strip()
        id_usuario = session["usuario_id"]

        if not motivo:
            flash("Erro: O preenchimento do motivo/justificação é obrigatório!")
            return redirect(url_for("nova_movimentacao"))
        
        # Consulta o estoque atual e nome do medicamento
        cur.execute("SELECT quantidade_atual, nome FROM medicamentos WHERE id = %s", (id_medicamento,))
        med = cur.fetchone()
        
        if not med:
            flash("Medicamento não encontrado!")
            return redirect(url_for("nova_movimentacao"))
            
        qtd_atual = med["quantidade_atual"]
        
        # Calcula o novo estoque com base no tipo de operação
        if tipo == "ENTRADA":
            nova_qtd = qtd_atual + quantidade
        else:  
            # SAIDA, AVARIA, VENCIMENTO, EMPRESTIMO, TRANSFERENCIA reduzem o estoque
            if quantidade > qtd_atual:
                flash(f"Erro: Quantidade insuficiente no estoque para '{med['nome']}'. Disponível: {qtd_atual}")
                return redirect(url_for("nova_movimentacao"))
            nova_qtd = qtd_atual - quantidade
            
        try:
            # 1. Registra a movimentação na auditoria
            sql_mov = """
                INSERT INTO movimentacoes_estoque (id_medicamento, id_usuario, tipo, quantidade, motivo)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(sql_mov, (id_medicamento, id_usuario, tipo, quantidade, motivo))
            
            # 2. Atualiza o saldo na tabela de medicamentos
            sql_update = "UPDATE medicamentos SET quantidade_atual = %s WHERE id = %s"
            cur.execute(sql_update, (nova_qtd, id_medicamento))
            
            conn.commit()
            flash(f"Movimentação '{tipo}' registrada com sucesso e estoque atualizado!")
            return redirect(url_for("listar_estoque"))
            
        except mysql.connector.Error as err:
            conn.rollback() # Cancela a operação se der erro para não corromper dados
            flash(f"Erro ao processar movimentação: {err}")
        finally:
            cur.close()
            conn.close()
            
        return redirect(url_for("listar_estoque"))
        
    # Se for GET: Busca a lista de medicamentos para preencher o formulário
    cur.execute("SELECT id, nome, lote, quantidade_atual FROM medicamentos;")
    medicamentos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("movimentacao.html", medicamentos=medicamentos)


# ============================================================
# 9. ROTA: HISTÓRICO DE MOVIMENTAÇÕES (Auditoria)
# ============================================================
@app.route("/movimentacoes/historico")
def historico_movimentacoes():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
        
    # Opcional: Proteger para apenas Administrador ver o histórico (remova o if se todos puderem ver)
    if session.get("usuario_perfil") != "Administrador":
        flash("Acesso negado! Apenas administradores podem visualizar a auditoria de movimentações.")
        return redirect(url_for("pagina_inicial"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Query com JOIN para trazer os nomes em vez de apenas os IDs numéricos
    sql = """
        SELECT m.id, med.nome AS medicamento_nome, med.lote, u.nome AS usuario_nome, 
               m.tipo, m.quantidade, m.data, m.hora, m.motivo
        FROM movimentacoes_estoque m
        JOIN medicamentos med ON m.id_medicamento = med.id
        JOIN usuarios u ON m.id_usuario = u.id
        ORDER BY m.data DESC, m.hora DESC;
    """
    cur.execute(sql)
    movimentacoes = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template(
        "historico_movimentacoes.html",
        movimentacoes=movimentacoes,
        usuario_perfil=session.get("usuario_perfil")
    )


if __name__ == "__main__":
    app.run(debug=True)