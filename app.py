from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")#raiz Method GET POSt PUT DELETE
def paginaInicial():
    listaFrutas = ["Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana","Abacaxi", "uva", "Pera", "Banana"]
    return render_template("paginaInicial.html", tdsb = listaFrutas, nome = "Zezinho")
            #/sorvete/Zezinho
@app.route("/sorvete/<int:nome>",methods=["GET", "POST"])
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
    return "PAgina GET"