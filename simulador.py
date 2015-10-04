# coding=utf-8
from re import match, findall
from cmd import Cmd
from threading import Thread, Semaphore
from gerenciador_de_espaco import Gerenciador
from time import sleep, time


class Simulador(Cmd):
    prompt = '[Ep2]: '
    total = 0
    virtual = 0
    processos = []
    inicio = 0
    gerenciador = None
    semaforo = Semaphore(1)

    def espere(self, t):
        s = t - int(time() - self.inicio)
        if s > 0:
            sleep(s)

    def processe(self, processo):
        # O processo faz a solicitação de memória
        # Só um processo pode chamar a função fit por vez, controle de concorrência da memória implementado
        self.semaforo.acquire()
        self.gerenciador.fit(processo["nome"], processo["b"])
        self.semaforo.release()
        print processo["nome"]

        # Faz o acesso a memória
        for p, t in processo["posicao_tempo"]:
            self.espere(t)
            print "Faz acesso a posição %d" % p

        # Esperar até a hora que o processo finaliza
        self.espere(processo["tf"])
        self.semaforo.acquire()
        self.gerenciador.remova(processo["nome"])
        self.semaforo.release()

    def do_carrega(self, arg):
        """Carrega um arquivo trace"""
        trace = open(arg)
        self.total, self.virtual = map(int, trace.readline().split())
        for line in trace.readlines():
            info = match(r"(\d+) (\w+) (\d+) (\d+) (.+)", line)
            processo = dict(t0=int(info.group(1)), nome=info.group(2), tf=int(info.group(3)), b=int(info.group(4)),
                            posicao_tempo=[])
            for info in [match(r"(\d+) (\d+)", palavra) for palavra in findall(r"\d+ \d+", info.group(5))]:
                processo["posicao_tempo"].append([int(info.group(1)), int(info.group(2))])
            self.processos.append(processo)
        trace.close()
        self.gerenciador = Gerenciador(self.virtual)

    def do_espaco(self, arg):
        print "espaço num %s" % arg
        self.gerenciador.faz_fit(arg)

    def do_substitui(self, arg):
        print "substituindo num %s" % arg

    def do_executa(self, arg):
        print "executando intervalo %s" % arg
        self.inicio = time()
        for processo in self.processos:
            self.espere(processo["t0"])
            Thread(target=self.processe, args=(processo,)).start()

    def do_sai(self, arg):
        return True
