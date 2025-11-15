from models.pessoa_model import Pessoa

class Cliente(Pessoa): 
    def __init__(self, id, nome, cpf, telefone):
        self._id = id
        self._nome = nome
        self._cpf = cpf 
        self._telefone = telefone 
    
    def get_salario(self): 
        return self._salario; 

    def set_salario(self, salario): 
        self._salario = salario 

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "cpf": self._cpf,
            "telefone": self._telefone,
        }