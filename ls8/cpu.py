"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8  # make 8 registers
        self.pc = 0  # program counter
        self.IR = 0  # Instruction Register, contains a copy of the currently executing instruction
        self.ram = [0] * 256

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        program = []

        if file_name is None:
            print("This file is bad.")  # for stretch
            sys.exit(1)
        try:
            with open(file_name, 'r') as f:
                print("Inside the file")
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#")
                    # Convert any numbers from binary strings to integers
                    num = comment_split[0]
                    try:
                        x = int(num, 2)
                    except ValueError:
                        continue
                    # print in binary and decimal
                    print(f"{x:08b}: {x:d}")
                    program.append(x)
        except ValueError:
            print(f"File not found")

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while running:

            IR = self.ram[self.pc]

            if IR == LDI:  # LDI
                num = self.ram[self.pc + 1]
                reg = self.ram[self.pc + 2]

                self.register[num] = reg
                self.pc += 3

            elif IR == PRN:  # PRN
                reg = self.ram[self.pc + 1]
                print(self.register[reg])
                self.pc += 2

            elif IR == HLT:  # HLT
                running = False
                self.pc += 1

            elif IR == MUL:  # MUL
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.register[reg_a] *= self.register[reg_b]
                self.pc += 3

            else:
                print(f"Unknown IR: {IR}")
                sys.exit(1)

    def ram_read(self, MAR):
        # Read from RAM
        # Accepts the address to read and return the value stored there
        return self.ram[MAR]

    # accept a value to write, and the addres to write it to
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
