# coding=utf-8
from lista_ligada import ListaLigada
from registro import Registro


class Gerenciador(object):
    registro_zero = None
    inicio = None
    fit = None

    def __init__(self, tamanho):
        self.registro_zero = ListaLigada(Registro(tamanho=tamanho))
        self.inicio = self.registro_zero
        self.mais_requisitados = {}

    def faz_fit(self, num):
        if num == "1":
            self.fit = self.first_fit
        elif num == "2":
            self.fit = self.next_fit
        elif num == "3":
            self.fit = self.quick_fit
        else:
            raise RuntimeError("Argumento %s não é válido" % num)
        
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

    # Removendo o registro de um certo nome
    def remova(self, nome):
        # Percorre todos os registros a partir do registro que contem o endereço zero. Se não achou lança erro.
        lista = self.registro_zero
        achou = False
        while not achou:
            if lista.valor.nome == nome:
                achou = True
            else:
                lista = lista.proximo
                if lista == self.registro_zero:
                    raise RuntimeError("Processo %s inexistente" % nome)
        # Se chegou nesse ponto, a lista contendo o valor nome foi encontrado.
        # A remoção é feita olhando para os registros vizinhos e fazendo a junção do espaço que vai ficar livre com os
        # espaços livres vizinhos.
        # O registro de menor posição será espandido e os outros registros serão removidos.
        lista.valor.nome = ""
        anterior = lista.anterior
        proximo = lista.proximo
        if lista != self.registro_zero and anterior.valor.nome == "":
            anterior.valor.tamanho += lista.valor.tamanho
            anterior.proximo = lista.proximo
            proximo.anterior = anterior
            if lista == self.inicio:
                self.inicio = self.inicio.proximo
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave <= lista.valor.tamanho]
            chave = max(chaves_candidatas) if len(chaves_candidatas) else None
            if chave is not None:
                self.mais_requisitados[chave].pop(lista)
            del lista
            lista = anterior
        if lista != self.registro_zero.anterior and proximo.valor.nome == "":
            lista.valor.tamanho += proximo.valor.tamanho
            lista.proximo = proximo.proximo
            proximo.proximo.anterior = lista
            if proximo == self.inicio:
                self.inicio = self.inicio.proximo
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave <= proximo.valor.tamanho]
            chave = max(chaves_candidatas) if len(chaves_candidatas) else None
            if chave is not None:
                self.mais_requisitados[chave].pop(lista)
            del proximo

# Teste
# print "next fit"
# gerenciador = Gerenciador(10)
# gerenciador.next_fit("proc1", 3)
# gerenciador.next_fit("proc2", 3)
# gerenciador.next_fit("proc3", 3)
# gerenciador.next_fit("proc4", 1)
# print gerenciador.registro_zero.valor.nome
# print gerenciador.inicio.valor.nome
#
# print "first fit"
# gerenciador = Gerenciador(10)
# gerenciador.first_fit("proc1", 3)
# gerenciador.first_fit("proc2", 3)
# gerenciador.first_fit("proc3", 3)
# gerenciador.first_fit("proc4", 1)
# print gerenciador.registro_zero.valor.nome
# print gerenciador.inicio.valor.nome
#
# print "quick fit"
# gerenciador = Gerenciador(10)
# gerenciador.quick_fit("proc1", 3)
# gerenciador.quick_fit("proc2", 3)
# gerenciador.remova("proc1")
# gerenciador.quick_fit("proc3", 3)
# gerenciador.quick_fit("proc4", 3)
# gerenciador.remova("proc3")
# gerenciador.remova("proc2")
# print gerenciador.registro_zero.valor.nome
# print gerenciador.inicio.valor.nome
