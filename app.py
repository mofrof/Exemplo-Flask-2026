from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Sei lá"

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


listaUsuario = [
                {"login":"zezinho", "senha":"1234", "nivel":"normal"},
                {"login":"maria", "senha":"4321", "nivel":"adm"},
                ]


@app.errorhandler(404)
def paginaErro(error):
    return render_template("/erros/erro404.html"), 404

@app.route("/paginaInicial")#raiz Method GET POSt PUT DELETE
def paginaInicial():
    if("logado" in session and session["logado"] == True):
        listaFrutas = ["Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana"]
        return render_template("paginaInicial.html", tdsb = listaFrutas, nome = "Zezinho")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def paginaLogin():
    if(request.method == "GET"):
        return render_template("login.html")
    else:
        login = request.form["login"]
        passWord = request.form["Manga"]

        #usuario = pegarUsuarioBD(Login)
        #if(usuairo["login"] == loing and usuairo["senha"] == passWord)
        if(login == "zezinho"):
            if(passWord == "1234"):
                session["logado"] = True
                session["nivel"] = "adm"
                session["usuario"] = "Zezinho"
                # flash(f"{listaUsuario[0]["nivel"]}")
                return redirect(url_for("paginaInicial"))
            else:
                flash("Erro Senha")
                return render_template("login.html")
        elif(login == "maria" and passWord == "4321" ):
            session["logado"] = True
            session["nivel"] = "adm"
            session["usuario"] = "mary"
            flash(f"{listaUsuario[0]["nivel"]}")
            return redirect(url_for("paginaInicial"))

        else:
            flash("Erro Login")
            return render_template("login.html")

# String
@app.route("/sorvete/<path:nome>")
def paginaSorvete(nome):
    html = "" 
    
    if(nome == "get"):
        html = "<h1>Carregado com variable rules GET</h1>"
    elif(nome == "post"):
        html = "<h1>Carregado com variable rules Post</h1>"
    else:
         html = f"<h1>Nome {nome}</h1> <h1>info get {request.args.get('tempero')} {request.args.get('carne')}</h1>"
    return html


@app.get("/logout")
def logout():
    if("logado" in session and session["logado"] == True):
        session.clear()
        return redirect("/login")
    else:
        return redirect("/login")


@app.post("/rotaPost")
def paginaPost():
    login = request.form["login"]
    senha = request.form["senha"]
    nivel = request.form["nivel"]

    listaUsuario.append({"login":login, "senha":senha, "nivel":nivel},)
    return "Pagina POST"

@app.put("/rotaGET")
def paginaGet():
    return "Pagina GET"

@app.route("/loginEspecial", methods=["POST", "GET"])
def loginEspecial():
    return render_template("loginEspecial.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['arquivo']
        f.save(f"./uploads/{secure_filename(f.filename)}")
        flash("Upload Bem sucedido!")
        return redirect(url_for("upload_file"))
    else:
        return render_template("paginaUpload.html")