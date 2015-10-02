# coding=utf-8

# Um registro é lista com 5 elementos cujo primeiro elemento é o nome do processo, segundo elemento
# é a posição inicial da região na memória, terceiro elemento é o tamanho da região, quarto elemento é uma
# referencia para o registro da região anterior e ultimo elemento é uma referencia para o registro da região posterior
# O registro inicialmente:
# Registros = [None, 0, 10, None, None]


# A inserção de um registro é feita especificando o nome do processo, tamanho ocupado e um registro livre
# Se a região da memória registrada por lista_ligada ocupar mais espaço do que o tamanho do proc1 então o registro de
# proc1 estará entre as regiões registradas por lista_ligada[3] e lista_ligada atualizada da forma especificada abaixo
# senão se a lista_ligada[3] for igual à 3 então lista_ligada é registrada para o proc1
# senão não é possível fazer a inserção
def insercao(nome, tamanho, lista_ligada):
    if lista_ligada[0] is not None:  # Lança excessão quando tenta-se fazer a inserção num registro ocupado
        raise Exception
    if tamanho < lista_ligada[2]:
        lista_auxiliar = [nome, 0, tamanho, None, None]  # Criando novo processo de tamanho 3 unidades
        lista_auxiliar[1] = lista_ligada[1]  # Atualiza posição inicial da lista do quadro de página do processo
        lista_auxiliar[3] = lista_ligada[3]  # Atualiza lista anterior da lista do quadro de página do novo processo
        lista_auxiliar[4] = lista_ligada  # Atualiza a próxima lista da lista do quadro de página do novo processo
        lista_ligada[1] += lista_auxiliar[2]  # Atualiza a posição inicial da lista do quadro de página livre
        lista_ligada[2] -= lista_auxiliar[2]  # Atualiza a quantidade de unidades da lista do quadro de página livre
        lista_ligada[3] = lista_auxiliar  # Atualiza a lista anterior da lista do quadro de página livre
        lista_ligada = lista_auxiliar
    elif tamanho == lista_ligada[2]:
        lista_ligada[0] = nome
    else:  # Lança excessão quando não há espaço suficiente
        raise Exception


# Remoção de um registro
def remocao(lista_ligada):
    if lista_ligada[0] is None:  # Lança excessão quando tenta-se remover registro que já está livre
        raise Exception
    if lista_ligada[4] is not None:
        lista_auxiliar = lista_ligada[4]
        if lista_auxiliar[0] is None:  # Removendo o próximo registro se está livre
            lista_auxiliar[1] = lista_ligada[1]
            lista_auxiliar[2] += lista_ligada[2]
            lista_auxiliar[3] = lista_ligada[3]
            del lista_ligada[:]
            lista_ligada = lista_auxiliar
    if lista_ligada[3] is not None:
        lista_auxiliar = lista_ligada[3]
        if lista_auxiliar[0] is None:  # Removendo o registro anterior se está livre
            lista_auxiliar[2] += lista_ligada[2]
            lista_auxiliar[4] = lista_ligada[4]
            del lista_ligada[:]
            lista_ligada = lista_auxiliar
    lista_ligada[0] = None

