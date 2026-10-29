from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Sei lá"

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


listaUsuario = [
                {"login":"zezinho", "senha":"1234", "nivel":"adm"},
                {"login":"maria", "senha":"4321", "nivel":"normal"},
                ]


@app.route("/b1")
def bloco1():
    return render_template("exemploBloco1.html")

@app.route("/b2")
def bloco2():
    return render_template("exemploBloco2.html")





@app.errorhandler(404)
def paginaErro(error):
    return render_template("/erros/erro404.html"), 404

@app.route("/paginaIniciallll")#raiz Method GET POSt PUT DELETE
def paginaInicial():
    if("logado" in session and session["logado"] == True):
        listaFrutas = ["Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana"]
        return render_template("paginaInicial.html", tdsb = listaFrutas, nome = "Zezinho")
    else:
        return redirect(url_for("paginaLogin"))

@app.route("/loginggggg", methods=["GET", "POST"])
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
                flash(f"{listaUsuario[0]["nivel"]}")
                return redirect(url_for("paginaInicial"))
            else:
                flash("Erro Senha")
                return render_template("login.html",erro="Login ou senha invalidos")
        elif(login == "maria" and passWord == "4321" ):
            session["logado"] = True
            session["nivel"] = "aluno"
            session["usuario"] = "mary"
            flash(f"{listaUsuario[1]["nivel"]}")
            flash(f"outra mensagem")
            flash(f"outra mensagem")
            return redirect(url_for("paginaInicial"))

        else:
            flash("Erro Login")
            flash("TESTE exemplo")
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
        return redirect(url_for("paginaLogin"))
    else:
        return redirect(url_for("paginaLogin"))


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