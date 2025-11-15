class Produto:
    
    def __init__(self, id, nome, descricao, quantidade, preco, id_categoria):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._quantidade = quantidade
        self._preco = float(preco)
        self._id_categoria = id_categoria
    
    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_descricao(self):
        return self._descricao

    def get_quantidade(self):
        return self._quantidade

    def get_preco(self):
        return float(self._preco)
        
    def get_id_categoria(self):
        return self._id_categoria
    
    def set_id(self, id):
        self._id = id

    def set_nome(self, nome):
        self._nome = nome

    def set_descricao(self, descricao):
        self._descricao = descricao

    def set_quantidade(self, quantidade):
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self._quantidade = quantidade

    def set_preco(self, preco):
        if preco <= 0:
            raise ValueError("Valor unitário deve ser positivo")
        self._preco = float(preco)
        
    def set_id_categoria(self, id_categoria):
        self._id_categoria = id_categoria

    def calcular_valor_total(self):
        return self._preco * self._quantidade