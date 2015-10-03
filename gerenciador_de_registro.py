# coding=utf-8

# Um registro é lista com 5 elementos cujo primeiro elemento é o nome do processo, segundo elemento
# é a posição inicial da região na memória, terceiro elemento é o tamanho da região, quarto elemento é uma
# referencia para o registro da região anterior e ultimo elemento é uma referencia para o registro da região posterior


# Faz o registro de ocupação de um certo tamanho numa regiao_livre da memória
def insere(nome, tamanho, regiao_livre):
    if regiao_livre[0] is not None or tamanho > regiao_livre[2]:
        raise ValueError
    regiao_livre[0] = nome
    if tamanho < regiao_livre[2]:
        regiao_livre[2], regiao_livre[4] = tamanho, [None, regiao_livre[1] + tamanho, regiao_livre[2] - tamanho,
                                                     regiao_livre, regiao_livre[4]]


# Remoção de um registro
def remova(lista_ligada):
    if lista_ligada[0] is None:  # Lança excessão quando tenta-se remover registro que já está livre
        raise ValueError
    lista_ligada[0] = None
    anterior = lista_ligada[3]
    posterior = lista_ligada[4]
    if posterior is not None:
        if posterior[0] is None:  # Removendo o próximo registro se está livre
            lista_ligada[2] += posterior[2]
            lista_ligada[4] = posterior[4]
            del posterior[:]
    if anterior is not None:
        if anterior[0] is None:  # Removendo o registro anterior se está livre
            anterior[2] += lista_ligada[2]
            anterior[4] = posterior
            del lista_ligada[:]


# Essa função recebe como o argumento o nome e o tamanho do processo
def first_fit(nome, tamanho):
    global registros
    registro = registros
    nao_registrado = True
    try:
        while nao_registrado:
            try:
                insere(nome, tamanho, registro)  # tenta fazer a inserção
                nao_registrado = False
            except ValueError:
                registro = registro[4]  # Passa para o próximo registro quando não consegue
    except TypeError:
        print("Não tem espaço para o processo %s" % nome)


registros = [None, 0, 10, None, None]  # Nos registros, é informado que temos 10 unidades de memória livres
first_fit("proc1", 3)
first_fit("proc2", 3)
first_fit("proc3", 3)
nao_encontrado = True
registro = registros
while nao_encontrado:
    if registro[0] == "proc2":
        remova(registro)
        nao_encontrado = False
    registro = registro[4]
first_fit("proc4", 3)
first_fit("proc5", 1)
print registros
