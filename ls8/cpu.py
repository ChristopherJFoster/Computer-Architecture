"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0xff
        self.reg = [0] * 0x08
        self.PC = 0x00  # Program Counter, address of the currently executing instruction
        self.IR = 0x00  # Instruction Register, contains a copy of the currently executing instruction
        self.MAR = 0  # Memory Address Register, holds the memory address we're reading or writing
        self.MDR = 0  # Memory Data Register, holds the value to write or the value just read
        self.FL = 0  # Flags

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print(
                'Expected program name in command line (after ls8.py). Exiting LS-8 Emulator.')
            sys.exit()

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                if line[0] != '#' and line != '\n':
                    self.ram[address] = int(line[0:8], 2)
                    address += 1
            f.closed

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.FL,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # opcodes
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        running = True
        while running:
            self.IR = self.PC
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if self.ram[self.IR] == HLT:
                running = False
            elif self.ram[self.IR] == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif self.ram[self.IR] == PRN:
                print(self.reg[operand_a])
                self.PC += 2
