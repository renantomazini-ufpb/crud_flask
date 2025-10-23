from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS # Importe o CORS


app = Flask(__name__)
CORS(app)

#depois passo para um banco 21/10
#pessoas = []
#pessoas_id_control = 1

#depois chegou! 23/10
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # criado DB

from models.pessoa import Pessoa #importando modelo

#garante criação das tabelas
with app.app_context():
    db.create_all()



#vamos resolver aqui
@app.route("/pessoas", methods=["POST"])
def criar_pessoa():
    '''global pessoas_id_control
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
'''
    data = request.get_json()

    try:
        new_pessoa = Pessoa(
            nome=data.get("nome"),
            cargo=data.get("cargo"),
            setor=data.get("setor"),
            salario=data.get("salario"),
            tipo=data.get("tipo"),
            ativo=data.get("ativo", False)
        )
        db.session.add(new_pessoa)
        db.session.commit()
        return jsonify({"message":"Cadastro realizado", "pessoa": new_pessoa.to_dict()}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar pessoa: {str(e)}"}), 500
    #mds

#precisa de rota para ativar
@app.route("/pessoas/<int:pessoa_id>/ativar", methods=["PATCH"])
def ativar_pessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify({"message": "Pessoa não encontrada"}), 404
    
    if pessoa.ativo:
        return jsonify({"message": "Pessoa já ativa"}), 200
    
    pessoa.ativar()
    #salvar no banco de dados
    try:
        db.session.commit()
        return jsonify({"message": "Pessoa ativada com sucesso!", "pessoa": pessoa.to_dict()}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao ativar pessoa: {str(e)}"}), 500
    
#precisa de rota para desativar
@app.route("/pessoas/<int:pessoa_id>/desativar", methods=["PATCH"])
def desativar_pessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify({"message": "Pessoa não encontrada"}), 404
    
    if not pessoa.ativo:
        return jsonify({"message": "Pessoa já desativada"}), 200
    
    pessoa.desativar()
    #salvar no banco de dados
    try:
        db.session.commit()
        return jsonify({"message": "Pessoa desativada com sucesso!", "pessoa": pessoa.to_dict()}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao desativar pessoa: {str(e)}"}), 500



@app.route("/pessoas", methods=["GET"])
def get_pessoas():
    pessoas = Pessoa.query.all()
    pessoas_dict = [p.to_dict() for p in pessoas]
    return jsonify({"pessoas": pessoas_dict, "total": len(pessoas_dict)})

@app.route("/pessoas/<int:pessoa_id>", methods=["GET"])
def get_pessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id) 
    if not pessoa:
        return jsonify({"message": "Não encontrado"}), 404
    return jsonify(pessoa.to_dict())

@app.route("/pessoas/<int:pessoa_id>", methods=["PUT"]) 
def update_pessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    
    if not pessoa:
        return jsonify({"message": "Colaborador não encontrado"}), 404
    
    data = request.get_json()

    pessoa.nome = data.get("nome", pessoa.nome)
    pessoa.cargo = data.get("cargo", pessoa.cargo)
    pessoa.setor = data.get("setor", pessoa.setor)
    pessoa.salario = data.get("salario", pessoa.salario)
    pessoa.tipo = data.get("tipo", pessoa.tipo)
    pessoa.ativo = data.get("ativo", pessoa.ativo)

    try:
        db.session.commit() 
        return jsonify({"message": "Colaborador atualizado com sucesso!", "pessoa": pessoa.to_dict()})
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar pessoa: {str(e)}"}), 500


@app.route("/pessoas/<int:pessoa_id>", methods=["DELETE"])
def delete_pessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)

    if not pessoa:
        return jsonify({"message": "Pessoa não encontrada"}), 404

    try:

        db.session.delete(pessoa)
        db.session.commit()
        
        return jsonify({"message": "Pessoa deletada com sucesso!"}), 200
        
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao deletar pessoa: {str(e)}"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)