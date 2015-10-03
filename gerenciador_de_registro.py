# coding=utf-8
from lista_ligada import ListaLigada
from registro import Registro


class Gerenciador(object):
    registro_zero = None
    inicio = None

    def __init__(self, tamanho):
        self.registro_zero = ListaLigada(Registro(tamanho=tamanho))
        self.inicio = self.registro_zero
        
    def next_fit(self, nome, tamanho):
        registrado = False
        lista = self.inicio
        while not registrado:
            try:
                resto = lista.valor.insere(nome, tamanho)
                if resto is not None:
                    lista.faz_proximo(ListaLigada(resto))
                registrado = True
            except RuntimeError:
                lista = lista.proximo
                if lista == self.inicio:
                    raise RuntimeError("Não há espaço para o processo %s" % nome)
        self.inicio = lista.proximo

    # Essa função recebe como o argumento o nome e o tamanho do processo
    def first_fit(self, nome, tamanho):
        self.inicio = self.registro_zero.anterior
        self.next_fit(nome, tamanho)

    def remova(self, nome):
        raise NotImplementedError

print "next fit"
gerenciador = Gerenciador(10)
gerenciador.next_fit("proc1", 3)
gerenciador.next_fit("proc2", 3)
gerenciador.next_fit("proc3", 3)
gerenciador.next_fit("proc4", 1)
print gerenciador.registro_zero.valor.nome
print gerenciador.inicio.valor.nome

print "first fit"
gerenciador = Gerenciador(10)
gerenciador.first_fit("proc1", 3)
gerenciador.first_fit("proc2", 3)
gerenciador.first_fit("proc3", 3)
gerenciador.first_fit("proc4", 1)
print gerenciador.registro_zero.valor.nome
print gerenciador.inicio.valor.nome
