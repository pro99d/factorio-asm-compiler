from blueprint_encoder import encode, base
import json
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
debug = True
with open("sample_memory.json", "r") as fl:
    memory = json.load(fl)
"""
r - регистр
result - результат предыдущей операции
r1 - ввод, только чтение
r2 - вывод, - только запись
r3 - буфер 
"""
def add_new_instruction(old_json, instruction, line):
    """
    :param old_json: словарь
    :param instruction: инструкции,
    :param line:  строка кода
    :return: новый словарь:
    #   Сигналы
    #   0 - I
    #   1 - M
    #   2 - D
    #   3 - A
    """
    needed_instrs = ["i", "m", "a", "d"]
    for i in needed_instrs:
        if i not in instruction:
            instruction[i] = 0
    adding_entities = memory["blueprint"]["entities"]
    adding_wires = memory["blueprint"]["wires"]
    for i in range(len(adding_entities)):
        adding_entities[i]["position"]["x"] += 2
        adding_entities[i]["entity_number"] += 4*line
    for i in range(len(adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"])):
        if adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["name"] == "SIGNAL-I":
            adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["count"] = instruction["i"]
        elif adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["name"] == "SIGNAL-A":
            adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["count"] = instruction["a"]
        elif adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["name"] == "SIGNAL-M":
            adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["count"] = instruction["m"]
        elif adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["name"] == "SIGNAL-D":
            adding_entities[3]["control_behavior"]["sections"]["sections"][0]["filters"][i]["count"] = instruction["d"]
    adding_entities[3]["control_behavior"]["sections"]["sections"][0]["group"] = str(line)
    for i in range(len(adding_entities)):
        old_json["blueprint"]["entities"].append(adding_entities[i])
    for i in range(len(adding_wires)):
        old_json["blueprint"]["wires"].append(adding_wires[i])
    for i in range(len(adding_wires)):
        adding_wires[i][0] += 4*line
        adding_wires[i][2] += 4*line
    adding_wires.append(
        [
            line-4,
            1,
            line,
            1
        ]
    )
    adding_wires.append(
        [
            line - 4,
            2,
            line,
            2
        ]
    )
    return old_json

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
            g = lines[line-1][ins-1]
            if "\n" in g:
                g = g[0:-1]
                if g in INSTRUCTIONS:
                    lines[line-1][ins-1] = INSTRUCTIONS[g]+"\n"

            if g in INSTRUCTIONS:
                lines[line-1][ins-1] = INSTRUCTIONS[g]

    with open(file+".dat", "w") as mc:
        for line in lines:
            mc.write("".join(line))

    if debug:
        print(lines)
#to_machine_code("test.asm")
if __name__ == "__main__":
    res = add_new_instruction(memory, {"i":3, "a":4, "m":1}, 2)
    print(res)