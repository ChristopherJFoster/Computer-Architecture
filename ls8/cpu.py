"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0xff
        self.reg = [0] * 0x08
        self.PC = 0x00  # Program Counter
        self.IR = 0x00  # Instruction Register
        self.MAR = 0  # Memory Address Register
        self.MDR = 0  # Memory Data Register
        self.FL = 0  # Flags
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        self.dispatch = {
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            MUL: self.handle_MUL
        }

    def handle_LDI(self, a, b):
        self.reg[a] = b

    def handle_PRN(self, a):
        print(self.reg[a])

    def handle_MUL(self, a, b):
        self.alu('MUL', a, b)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print(
                'Error: Expected program name in command line (after ls8.py). Exiting LS-8 Emulator.')
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
        elif op == 'MUL':
            total = 0b00000010  # store total in R02
            for _ in range(self.reg[reg_b]):
                self.reg[total] += self.reg[reg_a]
            self.reg[reg_a] = self.reg[total]
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

        HLT = 0B00000001

        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        opcodes = {LDI, PRN, MUL}

        running = True

        while running:
            self.IR = self.PC

            opsNum = (self.ram[self.IR] >> 6) & 0b11

            if self.ram[self.IR] == HLT:
                running = False

            elif self.ram[self.IR] in opcodes and opsNum == 0:
                self.dispatch[self.ram[self.IR]]

            elif self.ram[self.IR] in opcodes and opsNum == 1:
                self.dispatch[self.ram[self.IR]](self.ram_read(self.PC + 1))

            elif self.ram[self.IR] in opcodes and opsNum == 2:
                self.dispatch[self.ram[self.IR]](self.ram_read(
                    self.PC + 1), self.ram_read(self.PC + 2))

            else:
                print('Error: Unknown opcode in program. Exiting LS-8 Emulator.')
                sys.exit()

            self.PC += opsNum + 1
