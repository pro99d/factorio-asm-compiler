from blueprint_encoder import encode, base
import re
INSTRUCTIONS = {
    "and":"i1",
    "mov":"i2",
    "add":"i3",
    "sub":"i4",
    "sav":"i5",
    "bpl":"i7",
    "beq":"i9",
    "br":"i10",
    "cla":"i13",
    "rol":"i17",
    "ror":"i18",
    "nop":"i0",
    "in":"r1",
    "out":"r2",
    "result":"r3"
}

REP = {}
"""

r - регистр
result - результат предыдущей операции
r1 - ввод, только чтение
r2 - вывод, - только запись
r3 - буфер для значений (например result)
"""
def to_machine_code(file):
    lines = []
    with open(file, "r") as asm:
        for line in asm.readlines():
            lines.append(line.split(" "))
    for line in range(len(lines)):
        if lines[line-1][0].startswith("$"):
            name = lines[line][0][1:]
            INSTRUCTIONS[name] = lines[line][1]
            lines.pop(line-1)
        for ins in range(len(lines[line-1])):
            print()
            g = lines[line-1][ins-1]
            print(g)
            if "\n" in g:
                g = g[0:-1]
                if g in INSTRUCTIONS:
                    lines[line][ins] = INSTRUCTIONS[g]+"\n"

            if g in INSTRUCTIONS:
                lines[line][ins] = INSTRUCTIONS[g]
    #for ine in lines:

    with open(file+"mc", "w") as mc:
        for line in lines:
            mc.write("".join(line))


    print(lines)
to_machine_code("test.asm")
