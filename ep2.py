# coding=utf-8
from sys import argv
from re import match, findall

trace = open(argv[1])
total, virtual = map(int, findall(r"\d+", trace.readline()))
processos = []
for line in trace.readlines():
    info = match(r"(\d+) (\w+) (\d+) (\d+) (.+)", line)
    processo = dict(t0=int(info.group(1)), nome=info.group(2), f=int(info.group(3)), b=int(info.group(4)),
                    tempo_acesso=[])
    for info in [match(r"(\d+) (\d+)", palavra) for palavra in findall(r"\d+ \d+", info.group(5))]:
        processo["tempo_acesso"].append(dict(p=int(info.group(1)), t=int(info.group(2))))
    processos.append(processo)
trace.close()

