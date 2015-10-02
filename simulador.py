# coding=utf-8
from re import match, findall
from cmd import Cmd


class Simulador(Cmd):
    prompt = '[Ep2]: '
    total = 0
    virtual = 0
    processos = []

    def do_carrega(self, arg):
        """Carrega um arquivo trace"""
        trace = open(arg)
        self.total, self.virtual = map(int, trace.readline().split())
        for line in trace.readlines():
            info = match(r"(\d+) (\w+) (\d+) (\d+) (.+)", line)
            processo = dict(t0=int(info.group(1)), nome=info.group(2), f=int(info.group(3)), b=int(info.group(4)),
                            tempo_acesso=[])
            for info in [match(r"(\d+) (\d+)", palavra) for palavra in findall(r"\d+ \d+", info.group(5))]:
                processo["tempo_acesso"].append(dict(p=int(info.group(1)), t=int(info.group(2))))
            self.processos.append(processo)
        trace.close()

    def do_espaco(self, arg):
        print "espaço num {}".format(arg)

    def do_substitui(self, arg):
        print "substituindo num {}".format(arg)

    def do_executa(self, arg):
        print "executando intervalo {0}".format(arg)

    def do_sai(self, arg):
        return True
