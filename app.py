from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa (db.Model):
    __tablename__= 'cliente'
    _id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    
    def __init__ (self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
        

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods = ['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        
        if nome and telefone and cpf and email:
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)

@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get(id)
    if request.method == 'POST':
        # Atualizar os dados da pessoa com base no formulário
        pessoa.nome = request.form.get("nome")
        pessoa.telefone = request.form.get("telefone")
        pessoa.cpf = request.form.get("cpf")
        pessoa.email = request.form.get("email")
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template("editar.html", pessoa=pessoa)

@app.route("/excluir/<int:id>", methods=['GET', 'POST'])
def excluir(id):
    pessoa = Pessoa.query.get(id)
    if request.method == 'POST':
        db.session.delete(pessoa)
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template("excluir.html", pessoa=pessoa)
            
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

