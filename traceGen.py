import random

init = 0
f = open("trace", "w")
f.write("{0} {1}\n".format(random.randint(500, 1000), random.randint(500, 1000)))
for i in range(0, random.randint(1, 10)):
    init = random.randint(init, init + 5)
    end = random.randint(init, init + 10)
    size = random.randint(10, 1000)
    f.write("{0} {1} {2} {3} ".format(init, "teste{0}".format(i), end, size))
    for ii in range(0, random.randint(1, 5)):
        f.write("{0} {1} ".format(random.randint(init, end), random.randint(0, size)))
    f.write("\n")
f.close()
