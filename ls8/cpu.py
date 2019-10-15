"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8  # make 8 registers
        self.pc = 0  # program counter
        self.ir = 0  # Instruction Register, contains a copy of the currently executing instruction
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

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

        while running:
            print("running...")

            command = self.ram[self.pc]

            if command == 0b10000010:  # LDI
                num = self.ram[self.pc + 1]
                reg = self.ram[self.pc + 2]

                self.register[reg] = num
                self.pc += 3

            elif command == 0b01000111:  # PRN
                reg = self.ram[self.pc + 1]
                print(self.register[reg])
                self.pc += 2

            elif command == 0b00000001:  # HLT
                running = False
                pc += 1

            else:
                print(f"Unknown command: {command}")
                sys.exit(1)

    def ram_read(self, location):
        # Read from RAM
        # Accepts the address to read and return the value stored there
        return self.ram[location]

    # accept a value to write, and the addres to write it to
    def ram_write(self, location, value):
        self.ram[location] = value
