from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")#raiz Method GET POSt PUT DELETE
def paginaInicial():
    listaFrutas = ["Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana"]
    return render_template("paginaInicial.html", tdsb = listaFrutas, nome = "Zezinho")
            #/sorvete/Zezinho

@app.route("/login", methods=["GET", "POST"])
def paginaLogin():
    if(request.method == "GET"):
        tipoLogin = request.args.get("pera")
        if(tipoLogin == "Especial"):
            return render_template("loginEspecial.html")
        else:
            return render_template("login.html")
    else:
        login = request.form["Manga"]
        passWord = request.form["password"]

        if(login == "zezinho" and passWord == "1234"):
            return render_template("paginaInicial.html")
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

@app.post("/rotaPost")
def paginaPost():
    return "Pagina POST"

@app.get("/rotaGET")
def paginaGet():
    return "Pagina GET"