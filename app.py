from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import criar_tabelas, criar_usuario, validar_usuario, adicionar_cliente, listar_clientes, buscar_cliente, atualizar_cliente, remover_cliente

app = Flask(__name__)
app.secret_key = "troque_esta_chave_por_uma_aleatoria_em_producao"

# Inicizaliza as tabelas
criar_tabelas()

# Decorator simples
def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar essa página", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return redirect(url_for("lista_clientes"))

# Registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        if not username or not password:
            flash("Preencha usuário e senha", "danger")
            return render_template("register.html")
        ok = criar_usuario(username, password)
        if ok:
            flash("Usuário criado com sucesso. Faça login.", "success")
            return redirect(url_for("login"))
        else:
            flash("Erro ao criar usuário", "danger")
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        uid = validar_usuario(username, password)
        if uid:
            session["user_id"] = uid
            session["username"] = username
            flash(f"Bem-vindo, {username}!", "success")
            return redirect(url_for("lista_clientes"))
        else:
            flash("Usuário ou senha inválidos", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu... Volte em breve", "info")
    return redirect(url_for("login"))

# Lista de clientes(protegida)
@app.route("/clientes")
@login_required
def lista_clientes():
    dados = listar_clientes()
    return render_template("index.html", clientes = dados)

# Adicionar cliente
@app.route("/clientes/adicionar", methods=["GET", "POST"])
@login_required
def route_adicionar():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone =request.form.get("telefone")
        observacoes = request.form.get("observacoes")
        adicionar_cliente(nome, email, telefone, observacoes)
        flash("Cliente adicionado", "success")
        return redirect(url_for("lista_clientes"))
    return render_template("adicionar.html")

# Editar
@app.route("/clientes/editar/<int:cid>", methods=["GET", "POST"])
@login_required
def route_editar(cid):
    cliente = buscar_cliente(cid)
    if not cliente:
        flash("Cliente não encontrado","danger")
        return redirect(url_for("lista_clientes"))
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone =request.form.get("telefone")
        observacoes = request.form.get("observacoes")
        atualizar_cliente(cid, nome, email, telefone, observacoes)
        flash("Cliente atualizado", "success")
        return redirect(url_for("lista_clientes"))
    return render_template("editar.html", cliente=cliente)

# Remover
@app.route("/clientes/remover/<int:cid>", methods=["POST"])
@login_required
def route_remover(cid):
    remover_cliente(cid)
    flash("Cliente removido", "info")
    return redirect(url_for("lista_clientes"))

if __name__ == "__main__":
    app.run(debug=True)

