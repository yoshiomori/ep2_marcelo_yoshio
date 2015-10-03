# coding=utf-8
from lista_ligada import ListaLigada
from registro import Registro


class Gerenciador(object):
    registro_zero = None
    inicio = None

    def __init__(self, tamanho):
        self.registro_zero = ListaLigada(Registro(tamanho=tamanho))
        self.inicio = self.registro_zero
        self.mais_requisitados = {}
        
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

    def quick_fit(self, nome, tamanho):
        chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave >= tamanho]
        chave = min(chaves_candidatas) if len(chaves_candidatas) else None
        if chave is not None:
            self.inicio = self.mais_requisitados[chave].pop()
            if len(self.mais_requisitados[chave]) == 0:
                self.mais_requisitados.pop(chave)
        self.next_fit(nome, tamanho)
        # Se sobrou espaço livre vou tentar guardar esse espaço no maior tamanho dos mais requisitados
        if self.inicio.valor.nome == "":
            tamanho_restante = self.inicio.valor.tamanho
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave <= tamanho_restante]
            chave = max(chaves_candidatas) if len(chaves_candidatas) else tamanho if tamanho >= tamanho_restante\
                else None
            if chave is not None:
                if chave not in self.mais_requisitados.keys():
                    self.mais_requisitados[chave] = []
                self.mais_requisitados[chave].append(self.inicio)

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

print "quick fit"
gerenciador = Gerenciador(10)
gerenciador.quick_fit("proc1", 3)
gerenciador.quick_fit("proc2", 3)
gerenciador.quick_fit("proc3", 3)
gerenciador.quick_fit("proc4", 1)
print gerenciador.registro_zero.valor.nome
print gerenciador.inicio.valor.nome
