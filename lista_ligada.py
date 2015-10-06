class ListaLigada(object):
    valor = None
    proximo = None
    anterior = None

    def __init__(self, valor):
        self.valor = valor
        self.proximo = self
        self.anterior = self

    def faz_proximo(self, lista):
        if type(lista) is not ListaLigada:
            raise TypeError
        self_proximo = self.proximo
        lista_anterior = lista.anterior
        self.proximo = lista
        lista.anterior = self
        lista_anterior.proximo = self_proximo
        self_proximo.anterior = lista_anterior

    def remova(self):
        self.proximo.anterior = self.anterior
        self.anterior.proximo = self.proximo
