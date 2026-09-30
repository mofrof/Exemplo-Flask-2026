from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "Sei lá"

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


listaUsuario = [
                {"login":"zezinho", "senha":"1234", "nivel":"normal"},
                {"login":"maria", "senha":"4321", "nivel":"adm"},
                ]

@app.route("/")#raiz Method GET POSt PUT DELETE
def paginaInicial():
    if("logado" in session and session["logado"] == True):
        listaFrutas = ["Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana"]
        return render_template("paginaInicial.html", tdsb = listaFrutas, nome = "Zezinho")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def paginaLogin():
    if(request.method == "GET"):
            if("logado" in session and session["logado"] == True):
                return redirect("/")
            else:
                return render_template("login.html")
    else:
        login = request.form["login"]
        passWord = request.form["password"]

        if(login == "zezinho" and passWord == "1234"):
            session["logado"] = True
            session["nivel"] = listaUsuario[0]["nivel"]
            session["usuario"] = listaUsuario[0]["login"]
            return redirect("/")
        elif(login == "maria" and passWord == "4321" ):
            session["logado"] = True
            session["nivel"] = "adm"
            session["usuario"] = "mary"
            return redirect("/")

        else:
            return render_template("login.html")

# String
@app.route("/sorvete/<float:nome>",methods=["GET", "POST"])
def paginaSorvete(nome):
    html = "" 
    
    if(nome == "get"):
        html = "<h1>Carregado com parametro GET</h1>"
    elif(nome == "post"):
        html = "<h1>Carregado com parametro Post</h1>"
    else:
         html = f"<h1>Numero {nome}</h1> <h1>info get {request.args.get('tempero')} {request.args.get('carne')}</h1>"
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

@app.get("/rotaGET")
def paginaGet():
    return "Pagina GET"

@app.route("/loginEspecial", methods=["POST", "GET"])
def loginEspecial():
    return render_template("loginEspecial.html")