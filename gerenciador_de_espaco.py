# coding=utf-8
from lista_ligada import ListaLigada

unidades_alocacao = 10


class Gerenciador(object):
    registro_zero = None  # Lista que contem a informação da região da memória virtual que contem a posição inicial
    inicio = None  # Usado para configurar a primeira lista a ser analizada para os algoritmos de gerência de memória
    mais_requisitados = {}  # Contém a informação das regiões livres de tamanho mais requisitados
    tabela_pagina = [0]  # Tabela que informa em que quadro a página está carregada, usada na tradução do endereço
    pagina_presente = [False]  # Tabela que informa se uma página está num quadro, usada na tradução do endereço
    acha_posicao = None  # Guarda a função do algoritmo para gerência de espaço livre
    comprimento_offset = 0  # É o número de bits do offset usado para traduzir endereços virtuais em físico
    mascara = 0  # A máscara é usada para selecionar o offset do endereço virtual
    quadro = None  # Ponteiro para o início da fila dos quadro. Será usado para aplicar os algoritmos de substituição
    substituicao = None  # Guarda a função do algoritmo de substituição de página
    r_m = [0]  # Usado para armazenar o bits r e m de cada página
    contador = [0]  # Usado para armazenar o contador de cada página

    def __init__(self, total, virtual):
        self.total = total
        self.virtual = virtual
        numero_paginas = virtual.tamanho / 16  # O tamanho de uma página é 16 bits

        # Lista dublamente encadeada informando regiões livres na memória virtual
        self.registro_zero = ListaLigada({'processo': None, 'posicao inicial': 0, 'tamanho': numero_paginas * 16})

        # Início e registro_zero serão usados nos algoritmos de gerência de espaço livre
        self.inicio = self.registro_zero

        # Atualizando a tabela de página para corresponder com o número de páginas
        self.tabela_pagina *= numero_paginas

        # Criando a função que traduz o endereço
        self.comprimento_offset = (numero_paginas * 16 - 1).bit_length() - (numero_paginas - 1).bit_length()
        self.mascara = (1 << self.comprimento_offset) - 1

        self.r_m *= numero_paginas  # Inicializando os bits r m para cada página
        self.contador *= numero_paginas  # Inicializando o contador de cada página
        self.pagina_presente *= numero_paginas  # Inicializando o bit presente para cada pagina

        # As páginas são inicializados conforme o tamanho da memória física
        self.quadro = ListaLigada({'quadro': 0, 'pagina': None})
        for i in range(1, total.tamanho / 16 - 1):
            self.quadro.faz_proximo(ListaLigada({'quadro': i, 'pagina': None}))

    def traduz_endereco(self, endereco):
        print endereco
        # Calculando endereço físico
        pagina = endereco >> self.comprimento_offset  # Achando a página para esse endereço
        if not self.pagina_presente[pagina]:  # page fault
            quadro = self.substituicao()  # Usando uma algoritmo de substituição seleciona um quadro
            if quadro.valor['pagina'] is not None:
                if self.r_m[quadro.valor['pagina']] & 1:  # Tratando o caso que a pagina do quadro foi modificado
                    # Escreve na memória virtual o conteudo do quadro da memória fisica
                    self.virtual.escreve(quadro.valor['pagina'] >> self.comprimento_offset,
                                         self.total.le(quadro.valor['quadro'] << self.comprimento_offset, 16))
                self.pagina_presente[quadro.valor['pagina']] = False
            quadro.valor['pagina'] = pagina
            self.pagina_presente[pagina] = True
            self.tabela_pagina[pagina] = quadro.valor['quadro']
        quadro = self.tabela_pagina[pagina]
        # return quadro << self.comprimento_offset | self.mascara & endereco
        return quadro

    def fit(self, nome, tamanho):
        # Atualizando tamanho para corresponder a um multiplo de páginhas
        tamanho = tamanho if tamanho % 16 == 0 else tamanho + 16 - tamanho % 16
        return self.acha_posicao(nome, tamanho)

    def faz_fit(self, num):
        if num == "1":
            self.acha_posicao = self.first_fit
        elif num == "2":
            self.acha_posicao = self.next_fit
        elif num == "3":
            self.acha_posicao = self.quick_fit
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
            return lista_encontrada.valor['posicao inicial'], lista_encontrada.valor['tamanho']

    # Essa função recebe como o argumento o nome e o tamanho do processo
    def first_fit(self, nome, tamanho):
        self.inicio = self.registro_zero.anterior
        return self.next_fit(nome, tamanho)

    def quick_fit(self, nome, tamanho):
        chaves_candidatas = [chave for chave in self.mais_requisitados.keys() if chave >= tamanho]
        chave = min(chaves_candidatas) if len(chaves_candidatas) else None
        if chave is not None:
            self.inicio = self.mais_requisitados[chave].pop()
            if len(self.mais_requisitados[chave]) == 0:
                self.mais_requisitados.pop(chave)
        base, tamanho_alocado = self.next_fit(nome, tamanho)
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
        return base, tamanho_alocado

    # Removendo o registro de um certo nome
    def remova(self, nome):
        # Percorre todos os registros a partir do registro que contem o endereço zero. Se não achou lança erro.
        lista_encontrada = self.registro_zero.busca(lambda lista: lista.valor['processo'] == nome)
        if lista_encontrada is None:
            raise RuntimeError("Processo %s inexistente" % nome)
        # Se chegou nesse ponto, a lista contendo o valor nome foi encontrado.

        # É necessário remover a todas as páginas carregadas
        pagina_inicial = lista_encontrada.valor['posicao inicial'] >> self.comprimento_offset
        numemro_paginas = lista_encontrada.valor['tamanho'] >> self.comprimento_offset
        for i in range(pagina_inicial, numemro_paginas):
            if self.pagina_presente[i]:
                quadro = self.quadro.busca(lambda lista: lista.valor['quadro'] == self.tabela_pagina[i])
                quadro.valor['pagina'] = None
                self.pagina_presente[i] = False
                self.contador[i] = 0
                self.r_m[i] = 0

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

    def faz_substituicao(self, num):
        if num == '1':
            self.substituicao = self.nrup
        elif num == '2':
            self.substituicao = self.fifo
        elif num == '3':
            self.substituicao = self.scp
        elif num == '4':
            self.substituicao = self.lrup
        else:
            raise RuntimeError("Não lidamos com a opção %s" % num)

    def nrup(self):
        quadro = self.quadro
        quadro_menos_usado = quadro
        while True:
            if quadro.valor['pagina'] is None:
                return quadro
            elif self.r_m[quadro.valor['pagina']] == 0:
                return quadro
            elif self.r_m[quadro.valor['pagina']] < self.r_m[quadro_menos_usado.valor['pagina']]:
                quadro_menos_usado = quadro
            elif quadro != self.quadro.anterior:
                quadro = quadro.proximo
            else:
                return quadro_menos_usado

    def fifo(self):
        quadro = self.quadro
        self.quadro = self.quadro.proximo
        return quadro

    def scp(self):
        while True:
            quadro = self.quadro
            self.quadro = quadro.proximo
            if quadro.valor['pagina'] is None:
                return quadro
            elif self.r_m[quadro.valor['pagina']] & 2 == 0:
                return quadro
            else:
                self.r_m[quadro.valor['pagina']] &= 1

    def lrup(self):
        menor_contador = self.quadro
        quadro = menor_contador.proximo
        while quadro != self.quadro:
            if quadro.valor['pagina'] is None:
                return quadro
            elif self.contador[menor_contador.valor['pagina']] > self.contador[quadro.valor['pagina']]:
                menor_contador = quadro
            quadro = quadro.proximo
        return menor_contador

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
