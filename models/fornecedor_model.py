class Fornecedor:

    def __init__(self, id, nome, cnpj, telefone):
        self._id = id
        self._nome = nome
        self._cnpj = cnpj
        self._telefone = telefone

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_cnpj(self):
        return self._cnpj

    def get_telefone(self):
        return self._telefone

    def set_id(self, id):
        self._id = id

    def set_nome(self, nome):
        self._nome = nome

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj

    def set_telefone(self, telefone):
        self._telefone = telefone