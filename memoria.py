# coding=utf-8


class Memoria(object):
    def __init__(self, tamanho, tipo):
        self.tamanho = tamanho
        self.tipo = tipo
        if tipo != 'mem' and tipo != 'vir':
            raise RuntimeError("Tipo %s não suportado" % tipo)
        arquivo = open("/tmp/ep2." + tipo, 'wb')
        arquivo.write(bytearray([255] * tamanho))
        arquivo.close()

    def escreve(self, posicao, informacao):
        if self.tamanho < posicao:
            raise RuntimeError("Posição %d fora do limete" % posicao)
        arquivo = open("/tmp/ep2." + self.tipo, 'r+b')
        arquivo.seek(posicao)
        arquivo.write(informacao)
        arquivo.close()

    def le(self, posicao, n):
        if self.tamanho < posicao:
            raise RuntimeError("Posição %d fora do limete" % posicao)
        arquivo = open('/tmp/ep2.' + self.tipo, 'rb')
        b = arquivo.read(n)
        arquivo.close()
        return b