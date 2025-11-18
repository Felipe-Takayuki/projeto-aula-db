from datetime import datetime

class Compra:
    def __init__(self, id, id_cliente, id_funcionario, id_produto, quantidade, valor_total, data_compra=None):
        self._id = id
        self._id_cliente = id_cliente
        self._id_funcionario = id_funcionario
        self._id_produto = id_produto
        self._quantidade = quantidade
        self._valor_total = valor_total
        self._data_venda = data_venda if data_venda else datetime.now()

    def get_id(self):
        return self._id
    
    def get_id_cliente(self):
        return self._id_cliente

    def get_id_funcionario(self):
        return self._id_funcionario

    def get_id_produto(self):
        return self._id_produto

    def get_quantidade(self):
        return self._quantidade

    def get_valor_total(self):
        return self._valor_total

    def get_data_venda(self):
        return self._data_venda

    def set_id(self, id):
        self._id = id

    def set_id_cliente(self, id_cliente):
        self._id_cliente = id_cliente

    def set_id_funcionario(self, id_funcionario):
        self._id_funcionario = id_funcionario

    def set_id_produto(self, id_produto):
        self._id_produto = id_produto

    def set_quantidade(self, quantidade):
        self._quantidade = quantidade

    def set_valor_total(self, valor_total):
        self._valor_total = valor_total