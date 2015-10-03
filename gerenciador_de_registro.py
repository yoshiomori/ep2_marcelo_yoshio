# coding=utf-8

# Um registro é lista com 5 elementos cujo primeiro elemento é o nome do processo, segundo elemento
# é a posição inicial da região na memória, terceiro elemento é o tamanho da região, quarto elemento é uma
# referencia para o registro da região anterior e ultimo elemento é uma referencia para o registro da região posterior


class Registro(object):
    registros = []
    registro = None

    def __init__(self, tamanho):
        self.registros.append(None)  # Não tem nome
        self.registros.append(0)  # Posição inicial
        self.registros.append(tamanho)  # Tamanho inicial
        self.registros.append(None)  # lista anterior (lista circular)
        self.registros.append(None)  # lista posterior (lista circular)
        self.ultimo = self.registros
        
    def next_fit(self, nome, tamanho):
        registro = self.ultimo
        nao_registrado = True
        while nao_registrado:
            if registro[0] is None and tamanho <= registro[2]:
                registro[0] = nome
                if tamanho < registro[2]:
                    registro[2], registro[4] = tamanho, [None, registro[1] + tamanho, registro[2] - tamanho, registro,
                                                         registro[4]]
                self.ultimo = registro
                nao_registrado = False
            else:
                if registro[4] is None:
                    registro = self.registros  # Vai para a primeira lista ligada
                else:
                    registro = registro[4]  # Passa para o próximo registro quando não consegue
                if registro == self.ultimo:  # Para quando iteração passou por todos os elementos
                    print "Não tem espaço para o processo %s" % nome
                    break

    # Essa função recebe como o argumento o nome e o tamanho do processo
    def first_fit(self, nome, tamanho):
        self.ultimo = self.registros
        self.next_fit(nome, tamanho)


    
    def remova(self, nome):
        nao_encontrado = True
        auxiliar = self.registros
        while nao_encontrado:
            if auxiliar[0] == nome:
                if auxiliar[0] is None:  # Lança excessão quando tenta-se remover registro que já está livre
                    raise ValueError
                auxiliar[0] = None
                anterior = auxiliar[3]
                posterior = auxiliar[4]
                if posterior != self.registros:
                    if posterior[0] is None:  # Removendo o próximo registro se está livre
                        auxiliar[2] += posterior[2]
                        auxiliar[4] = posterior[4]
                        del posterior[:]
                if anterior != self.registros:
                    if anterior[0] is None:  # Removendo o registro anterior se está livre
                        anterior[2] += auxiliar[2]
                        anterior[4] = posterior
                        del auxiliar[:]
                nao_encontrado = False
            auxiliar = auxiliar[4]
            if auxiliar == self.registros:
                print "Processo %s não foi encontrado" % nome
                break


# registro = Registro(10)
# registro.first_fit("proc1", 3)
# registro.first_fit("proc2", 3)
# registro.first_fit("proc3", 3)
# registro.remova("proc2")
# registro.first_fit("proc4", 3)
# registro.first_fit("proc5", 1)
# print registro.registros
# 
# registro = Registro(10)
# registro.first_fit("proc1", 3)
# registro.first_fit("proc2", 3)
# registro.first_fit("proc3", 3)
# registro.remova("proc2")
# registro.first_fit("proc4", 3)
# registro.first_fit("proc5", 1)
# print registro.registros
