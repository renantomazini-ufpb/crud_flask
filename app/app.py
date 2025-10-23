from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)

#depois passo para um banco
#pessoas = []
#pessoas_id_control = 1

#depois chegou!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # criado DB


@app.route("/pessoas", methods=["POST"])
def criar_pessoa():
    global pessoas_id_control
    data = request.get_json() # na parte do front, será enviado os campos
    new_pessoa = {
        "id": pessoas_id_control,
        "nome": data.get("nome"),
        "cargo": data.get("cargo"),
        "setor": data.get("setor"),
        "salario": data.get("salario"),
        "tipo": data.get("tipo"),
        "ativo": False
    }
    pessoas.append(new_pessoa)
    pessoas_id_control += 1
    return jsonify({"message": "cadastro realizado!", "pessoa": new_pessoa}), 201

@app.route("/pessoas", methods=["GET"])
def get_pessoas():
    return jsonify({"pessoas": pessoas, "total": len(pessoas)})

@app.route("/pessoas/<int:pessoa_id>", methods=["GET"])
def get_pessoa(pessoa_id):
    pessoa = next((p for p in pessoas if p["id"] == pessoa_id), None)
    if not pessoa:
        return jsonify({"message": "Não encontrado"}), 404
    return jsonify(pessoa)

@app.route("/pessoas/<int:pessoa_id>")   
def update_pessoa(pessoa_id):
    pessoa = next((p for p in pessoas if p["id"] == pessoas), None)
    if not pessoa:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    data = request.get_json() #atualizando os campos com os dados
    pessoa["nome"] = data.get("nome", pessoa["nome"])
    pessoa["cargo"] = data.get("cargo", pessoa["cargo"])
    pessoa["setor"] = data.get("setor", pessoa["setor"])
    pessoa["salario"] = data.get("salario", pessoa["salario"])
    pessoa["tipo"] = data.get("tipo", pessoa["tipo"])
    return jsonify({"message": "Colaborador atualizada com sucesso!", "nome": pessoa})

@app.route("/pessoas/<int:pessoa_id>", methods=["DELETE"])
def delete_pessoa(pessoa_id):
    global pessoas
    pessoa = next((p for p in pessoas if p["id"] == pessoa_id), None)
    if not pessoa:
        return jsonify({"message": "Pessoa não encontrada"}), 404
    pessoas = [p for p in pessoas if p["id"] != pessoa_id]
    return jsonify({"message": "Pessoa deletada!"})

