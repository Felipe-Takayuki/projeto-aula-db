class Pessoa: 
    def __init__(self, id, nome, cpf, telefone):
        self._id = id
        self._nome = nome
        self._cpf = cpf 
        self._telefone = telefone 

    def get_id(self):
        return self._id
    def set_id(self, id):
        self._id = id

    def get_nome(self): 
        return self._nome
    def set_nome(self, nome):
        self._nome = nome 
    
    def get_cpf(self): 
        return self._cpf
    def set_cpf(self, cpf):
        self._cpf = cpf 
    
    def get_telefone(self): 
        return self._telefone 
    def set_telefone(self, telefone):
        self._telefone = telefone 
    
    def to_dict(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "cpf": self._cpf,
            "telefone": self._telefone
        }