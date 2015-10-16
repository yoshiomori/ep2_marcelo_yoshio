# coding=utf-8
from re import match, findall
from cmd import Cmd
from threading import Thread, Semaphore, active_count, current_thread
from gerenciador_de_espaco import Gerenciador
from time import sleep, time
from memoria import Memoria


def inicia_arquivo(nome_arquivo, tamanho):
    arquivo = open(nome_arquivo, 'wb')
    for i in range(tamanho):
        arquivo.write(bytearray([255]))  # 255 é o valor decimal de -1 em binário com um byte
    arquivo.close()


class Simulador(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '[Ep2]: '
        self.total = None
        self.virtual = None
        self.memoria_fisica = None
        self.memoria_virtual = None
        self.processos = []
        self.inicio = 0
        self.gerenciador = None
        self.semaforo = Semaphore(1)

    def espere(self, t):
        s = t - int(time() - self.inicio)
        if s > 0:
            sleep(s)

    def processe(self, i, processo):
        # O processo fica dormindo até a hora de começar
        self.espere(processo["t0"])
        # O processo faz a solicitação de memória
        # Só um processo pode chamar a função fit por vez, controle de concorrência da memória implementado
        self.semaforo.acquire()
        base = self.gerenciador.fit(processo["nome"], processo["b"])
        self.semaforo.release()
        print processo["nome"]

        # Faz o acesso a memória
        for p, t in processo["posicao_tempo"]:
            self.espere(t)
            self.semaforo.acquire()
            print "Faz acesso a posição %d(%d) escrevendo %d" % (p, self.gerenciador.traduz_endereco(p + base), i)
            self.memoria_fisica.escreve(self.gerenciador.traduz_endereco(p + base), bytearray([i]))
            self.semaforo.release()

        # Esperar até a hora que o processo finaliza
        self.espere(processo["tf"])
        self.semaforo.acquire()
        self.gerenciador.remova(processo["nome"])
        self.semaforo.release()
        print "Tchau processo %s" % processo["nome"]

    def do_carrega(self, arg):
        """Carrega um arquivo trace"""
        trace = open(arg)
        self.total, self.virtual = map(int, trace.readline().split())
        self.memoria_fisica = Memoria(self.total, 'mem')
        self.memoria_virtual = Memoria(self.virtual, 'vir')
        for line in trace.readlines():
            info = match(r"(\d+) (\w+) (\d+) (\d+) (.+)", line)
            processo = dict(t0=int(info.group(1)), nome=info.group(2), tf=int(info.group(3)), b=int(info.group(4)),
                            posicao_tempo=[])
            for info in [match(r"(\d+) (\d+)", palavra) for palavra in findall(r"\d+ \d+", info.group(5))]:
                processo["posicao_tempo"].append([int(info.group(1)), int(info.group(2))])
            self.processos.append(processo)
        trace.close()
        self.gerenciador = Gerenciador(self.memoria_fisica, self.memoria_virtual)

    def do_espaco(self, arg):
        self.gerenciador.faz_fit(arg)

    def do_substitui(self, arg):
        self.gerenciador.faz_substituicao(arg)

    def do_executa(self, arg):
        print "executando intervalo %s" % arg
        self.inicio = time()
        for i, processo in enumerate(self.processos):
            Thread(target=self.processe, args=(i, processo)).start()
        while active_count() > 1:
            relogio = int(time() - self.inicio + 1)
            for i in range(len(self.gerenciador.contador)):
                if self.gerenciador.r_m[i] & 2 == 2:  # só vai incrementar o contador da página i se r for 1
                    self.gerenciador.contador[i] += 1
            if relogio % 15:  # De tempos em tempos eu zero o bit de referencia
                for i in range(len(self.gerenciador.r_m)):
                    self.gerenciador.r_m[i] &= 1

                    print ":".join("{:02x}".format(ord(c)) for c in self.memoria_fisica.le(0, self.total))
                    print ":".join("{:02x}".format(ord(c)) for c in self.memoria_virtual.le(0, self.virtual))

                    lista = self.gerenciador.registro_zero
                    print 'nome do processo: %s\nposição inicial: %d\ntamanho: %d\n\n' % (
                        lista.valor['processo'], lista.valor['posicao inicial'], lista.valor['tamanho'])
                    lista = lista.proximo
                    while lista != self.gerenciador.registro_zero:
                        print 'nome do processo: %s\nposição inicial: %d\ntamanho: %d\n\n' % (
                            lista.valor['processo'], lista.valor['posicao inicial'], lista.valor['tamanho'])
                        lista = lista.proximo
            print "Relógio: %d" % relogio
            sleep(1)

    def do_sai(self, arg):
        return True
