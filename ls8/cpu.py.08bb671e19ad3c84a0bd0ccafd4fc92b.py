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

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            # 0b01000111,  # PRN R0
            # 0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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

        running = True
        while running:
            self.IR = self.PC
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if self.ram[self.IR] == 0b00000001:  # HLT
                running = False
            elif self.ram[self.IR] == 0b10000010:  # LDI
                self.reg[operand_a] = operand_b
                self.PC += 3


cpu = CPU()
print(cpu.ram)
print(cpu.reg)
cpu.ram_write(0b00010001, 0xa5)
print(cpu.ram_read(0xa5))
cpu.load()
cpu.run()
