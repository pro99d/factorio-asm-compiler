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
    "out":"r2"
}
REP = {
    r"mov *(\d+) r(\d+)":r"sub d\1 m\2"
}
"""
sav *2 r1 # задать регистру 1 значение 2
sav r1 r2 # задать регистру 2 значение регистра 1
* - число
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
    print(lines)
to_machine_code("test.asm")