from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

class Contato:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f'Nome: {self.nome}, Telefone: {self.telefone}, Email: {self.email}'

class Agenda:
    def __init__(self):
        self.contatos = []

    def adicionar_contato(self, contato):
        self.contatos.append(contato)

    def listar_contatos(self):
        return self.contatos

    def buscar_contato(self, nome):
        for contato in self.contatos:
            if contato.nome == nome:
                return contato
        return None

    def remover_contato(self, nome):
        for contato in self.contatos:
            if contato.nome == nome:
                self.contatos.remove(contato)
                return True
        return False

    def salvar_em_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'w') as file:
            json.dump([contato.__dict__ for contato in self.contatos], file)

    def carregar_de_arquivo(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as file:
                contatos = json.load(file)
                self.contatos = [Contato(**contato) for contato in contatos]
        except FileNotFoundError:
            pass

agenda = Agenda()
agenda.carregar_de_arquivo('agenda.json')

@app.route('/')
def index():
    contatos = agenda.listar_contatos()
    return render_template('index.html', contatos=contatos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    contato = Contato(nome, telefone, email)
    agenda.adicionar_contato(contato)
    agenda.salvar_em_arquivo('agenda.json')
    return redirect(url_for('index'))

@app.route('/remover/<nome>', methods=['POST'])
def remover(nome):
    agenda.remover_contato(nome)
    agenda.salvar_em_arquivo('agenda.json')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
