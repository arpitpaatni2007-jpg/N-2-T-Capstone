
import sys
import os
import re

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    PREDEFINED["R" + str(i)] = i

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


def clean_lines(filename):
    instructions = []

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
            line = line.split("//")[0].strip()
            line = line.replace(" ", "").replace("\t", "")

            if line:
                instructions.append((line, line_number))

    return instructions


def first_pass(instructions):
    symbols = PREDEFINED.copy()
    address = 0
    labels = set()

    for line, line_number in instructions:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if not re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", label):
                raise ValueError(f"Line {line_number}: Invalid label")

            if label in labels:
                print(f"Warning: Duplicate label '{label}' at line {line_number}")
            else:
                if label in symbols:
                    print(f"Warning: Label '{label}' conflicts with a predefined symbol")
                else:
                    symbols[label] = address

                labels.add(label)

        else:
            address += 1

    return symbols


def second_pass(instructions, symbols):
    machine_code = []
    next_variable = 16

    for line, line_number in instructions:
        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            symbol = line[1:]

            if not symbol:
                raise ValueError(f"Line {line_number}: Missing address")

            if re.fullmatch(r"[0-9]+", symbol):
                address = int(symbol)

            elif symbol in symbols:
                address = symbols[symbol]

            else:
                if not re.fullmatch(r"[A-Za-z_.$:][A-Za-z0-9_.$:]*", symbol):
                    raise ValueError(f"Line {line_number}: Invalid symbol")

                address = next_variable
                symbols[symbol] = address
                next_variable += 1

            if address < 0 or address > 32767:
                raise ValueError(f"Line {line_number}: Address out of range")

            machine_code.append(format(address, "016b"))

        else:
            if line.count("=") > 1 or line.count(";") > 1:
                raise ValueError(f"Line {line_number}: Invalid C-instruction")

            if "=" in line:
                dest, remaining = line.split("=")
            else:
                dest, remaining = "", line

            if any(char not in "ADM" for char in dest):
                raise ValueError(f"Line {line_number}: Invalid destination")

            if len(set(dest)) != len(dest):
                raise ValueError(f"Line {line_number}: Duplicate destination")

            dest = "".join(char for char in "AMD" if char in dest)

            if ";" in remaining:
                comp, jump = remaining.split(";")
            else:
                comp, jump = remaining, ""

            if dest not in DEST:
                raise ValueError(f"Line {line_number}: Invalid destination")

            if comp not in COMP:
                raise ValueError(f"Line {line_number}: Invalid computation")

            if jump not in JUMP:
                raise ValueError(f"Line {line_number}: Invalid jump")

            instruction = "111" + COMP[comp] + DEST[dest] + JUMP[jump]
            machine_code.append(instruction)

    return machine_code


def assemble(input_file):
    instructions = clean_lines(input_file)
    symbols = first_pass(instructions)
    machine_code = second_pass(instructions, symbols)

    output_file = os.path.splitext(input_file)[0] + ".hack"

    with open(output_file, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")

    print("Assembly completed successfully.")
    print("Input:", input_file)
    print("Output:", output_file)
    print("Total instructions:", len(machine_code))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py filename.asm")
        sys.exit(1)

    try:
        assemble(sys.argv[1])
    except (ValueError, OSError) as error:
        print("Error:", error)
        sys.exit(1)
