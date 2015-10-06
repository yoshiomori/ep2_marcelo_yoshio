# coding=utf-8


class Registro(object):
    def __init__(self, nome="", endereco=0, tamanho=0):
        self.nome = nome
        self.endereco = endereco
        self.tamanho = tamanho

    def insere(self, nome, tamanho):
        if self.nome != "":
            raise RuntimeError("Registro %s não está livre" % self.nome)
        if self.tamanho < tamanho:
            raise RuntimeError("Não há %d unidades de espaço nesse registro livre" % tamanho)
        self.nome = nome
        tamanho_restante, self.tamanho = self.tamanho - tamanho, tamanho
        return None if tamanho_restante == 0 else Registro(endereco=self.endereco + tamanho, tamanho=tamanho_restante)

    def igual(self, valor):
        if type(valor) is not Registro:
            raise TypeError
        if self.nome == valor.nome and self.endereco == valor.endereco and self.tamanho == valor.tamanho:
            return True
        else:
            return False
