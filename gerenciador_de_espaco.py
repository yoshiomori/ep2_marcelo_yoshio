# coding=utf-8
from lista_ligada import ListaLigada

unidades_alocacao = 10


class Gerenciador(object):
    registro_zero = None
    inicio = None
    fit = None
    quadro_ocupado = None

    def __init__(self, total, virtual):
        self.registro_zero = ListaLigada({'processo': None, 'posicao inicial': 0, 'tamanho': virtual})
        self.inicio = self.registro_zero
        self.mais_requisitados = {}
        self.paginas = ListaLigada({'quadro': None, 'pagina': 0, 'presente': False, 'R': False, 'M': False})
        # O tamanho da pagina é de 16 bits
        for i in range(1, virtual / 16 - 1):
            self.paginas.faz_proximo(ListaLigada({'quadro': None, 'pagina': i, 'R': False, 'M': False}))

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
        # Busca uma lista vazia de no mínimo um certo tamanho a partir de uma lista inicial
        lista_encontrada = self.inicio.busca(
            lambda lista: lista.valor['processo'] is None and lista.valor['tamanho'] >= tamanho)
        if lista_encontrada is None:
            raise RuntimeError("Não há espaço para o processo %s" % nome)
        else:
            tamanho_restante = lista_encontrada.valor['tamanho'] - tamanho
            lista_encontrada.valor['processo'] = nome
            lista_encontrada.valor['tamanho'] = tamanho
            if tamanho_restante:
                lista_encontrada.faz_proximo(ListaLigada(
                    {'processo': None, 'posicao inicial': lista_encontrada.valor['posicao inicial'] + tamanho,
                     'tamanho': tamanho_restante}))
            self.inicio = lista_encontrada.proximo

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
        if self.inicio.valor['processo'] == "":
            tamanho_restante = self.inicio.valor['tamanho']
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave <= tamanho_restante]
            chave = max(chaves_candidatas) if len(chaves_candidatas) else tamanho if tamanho >= tamanho_restante \
                else None
            if chave is not None:
                if chave not in self.mais_requisitados.keys():
                    self.mais_requisitados[chave] = []
                self.mais_requisitados[chave].append(self.inicio)

    # Removendo o registro de um certo nome
    def remova(self, nome):
        # Percorre todos os registros a partir do registro que contem o endereço zero. Se não achou lança erro.
        lista_encontrada = self.registro_zero.busca(lambda lista: lista.valor['processo'] == nome)
        if lista_encontrada is None:
            raise RuntimeError("Processo %s inexistente" % nome)
        # Se chegou nesse ponto, a lista contendo o valor nome foi encontrado.
        # A remoção é feita olhando para os registros vizinhos e fazendo a junção do espaço que vai ficar livre com os
        # espaços livres vizinhos.
        # O registro de menor posição será espandido e os outros registros serão removidos.
        lista_encontrada.valor['processo'] = ""
        anterior = lista_encontrada.anterior
        proximo = lista_encontrada.proximo
        if lista_encontrada != self.registro_zero and anterior.valor['processo'] == "":
            anterior.valor['tamanho'] += lista_encontrada.valor['tamanho']
            # Removendo todas as referências para a lista
            if lista_encontrada == self.inicio:
                self.inicio = self.inicio.proximo
            lista_encontrada.remova()
            lista_encontrada = anterior
            # Como o tamanho do registro vazio vai mudar, teremos que reinserir nos mais requisitados, para isso
            # vamos remover primeiro
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if
                                 chave <= lista_encontrada.valor['tamanho']]
            if len(chaves_candidatas):
                chave = max(chaves_candidatas)
                if lista_encontrada in self.mais_requisitados[chave]:
                    self.mais_requisitados[chave].pop(lista_encontrada)
        if lista_encontrada != self.registro_zero.anterior and proximo.valor['processo'] == "":
            lista_encontrada.valor['tamanho'] += proximo.valor['tamanho']
            # Removendo todas as referencias para a lista proximo
            if proximo == self.inicio:
                self.inicio = self.inicio.proximo
            # Pode ser que a lista removida esteja num dos conjuntos dos mais requisitados, então vamos verificar.
            chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave <= proximo.valor['tamanho']]
            if len(chaves_candidatas):
                chave = max(chaves_candidatas)
                if lista_encontrada in self.mais_requisitados[chave]:
                    self.mais_requisitados[chave].pop(
                        lista_encontrada)  # Se a lista está referenciada nesse conjuto então remova
            proximo.remova()
        # E agora que temos uma lista livre de tamanho atualizado, vamos re inserir num conjuto de tamanho maior
        chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if
                             chave <= lista_encontrada.valor['tamanho']]
        if len(chaves_candidatas):
            chave = max(chaves_candidatas)
            self.mais_requisitados[chave].append(self.inicio)

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
# gerenciador = Gerenciador(4, 10)
# gerenciador.quick_fit("proc1", 3)
# gerenciador.quick_fit("proc2", 3)
# gerenciador.remova("proc1")
# gerenciador.quick_fit("proc3", 3)
# gerenciador.quick_fit("proc4", 3)
# gerenciador.remova("proc3")
# gerenciador.remova("proc2")
# print gerenciador.registro_zero.valor.nome
# print gerenciador.inicio.valor.nome
