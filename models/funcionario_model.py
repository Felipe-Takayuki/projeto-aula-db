from models.pessoa_model import Pessoa

class Funcionario(Pessoa): 
    def __init__(self, id, nome, cpf, telefone, salario):
        self._id = id
        self._nome = nome
        self._cpf = cpf 
        self._telefone = telefone 
        self._salario = float(salario)
    
    def get_salario(self): 
        return float(self._salario); 

    def set_salario(self, salario): 
        if salario <= 0:
            raise ValueError("Salário deve ser positivo")
        self._salario = float(salario) 

    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "cpf": self._cpf,
            "telefone": self._telefone,
            "salario": float(self._salario)
        }