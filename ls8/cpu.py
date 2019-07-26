"""CPU functionality."""

import sys
from datetime import datetime
import time


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0xff  # Ram 0x00 - 0xff
        self.reg = [0] * 0x08  # Registers R0 - R7
        self.IM = 0x05  # R5 will be the Interrupt Mask
        self.IS = 0x06  # R6 will be the Interrupt Status
        self.SP = 0x07  # R7 will be the Stack Pointer
        self.reg[self.SP] = 0xf4  # Set Stack Pointer equal to 0xf4
        self.PC = 0x00  # Program Counter
        self.IR = 0x00  # Instruction Register
        self.MAR = 0b0000000  # Memory Address Register
        self.MDR = 0b0000000  # Memory Data Register
        self.FL = 0b0000000  # Flags
        self.halted = False  # Used to handle HLT
        self.disint = False  # Disable Interrupts
        self.timestamp = datetime.now().timestamp()  # Use to run interrupt timer
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0B10100000
        ST = 0b10000100
        JMP = 0b01010100
        PRA = 0b01001000
        IRET = 0b00010011
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        SUB = 0b10100001
        self.dispatch = {
            HLT: self.handle_HLT,
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            MUL: self.handle_MUL,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            CALL: self.handle_CALL,
            RET: self.handle_RET,
            ADD: self.handle_ADD,
            ST: self.handle_ST,
            JMP: self.handle_JMP,
            PRA: self.handle_PRA,
            IRET: self.handle_IRET,
            CMP: self.handle_CMP,
            JEQ: self.handle_JEQ,
            JNE: self.handle_JNE,
            SUB: self.handle_SUB
        }

    def handle_HLT(self):
        self.halted = True
        print('Program halted. Exiting LS-8 Emulator.')

    def handle_LDI(self, a, b):
        self.reg[a] = b

    def handle_PRN(self, a):
        print(self.reg[a])

    def handle_MUL(self, a, b):
        self.alu('MUL', a, b)

    def handle_PUSH(self, a):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]

    def handle_POP(self, a):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def handle_CALL(self, a):
        self.reg[0x04] = self.PC + 2
        self.handle_PUSH(0x04)
        self.PC = self.reg[a]

    def handle_RET(self):
        self.handle_POP(0x04)
        self.PC = self.reg[0x04]

    def handle_ADD(self, a, b):
        self.alu('ADD', a, b)

    def handle_ST(self, a, b):
        self.ram[self.reg[a]] = self.reg[b]

    def handle_JMP(self, a):
        self.PC = self.reg[a]

    def handle_PRA(self, a):
        print(chr(self.reg[a]))

    def handle_IRET(self):
        for reg in range(6, -1, -1):
            self.handle_POP(reg)
        self.handle_POP(0x04)
        self.FL = self.reg[0x04]
        self.handle_POP(0x04)
        self.PC = self.reg[0x04]
        self.disint = False

    def handle_CMP(self, a, b):
        if a < b:
            self.FL = self.FL + 0b00000100
        elif a > b:
            self.FL = self.FL + 0b00000010
        else:
            self.FL = self.FL + 0b00000001

    def handle_JEQ(self, a, b):
        pass

    def handle_JNE(self, a, b):
        pass

    def handle_SUB(self, a, b):
        self.alu('SUB', a, b)

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

    def alu(self, op, a, b):
        """ALU operations."""

        if op == 'ADD':
            self.reg[a] += self.reg[b]
        elif op == 'MUL':
            self.reg[a] *= self.reg[b]
        elif op == 'SUB':
            self.reg[a] -= self.reg[b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            self.FL,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        ST = 0b10000100
        JMP = 0b01010100
        PRA = 0b01001000
        IRET = 0b00010011
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        SUB = 0b10100001
        opcodes = {HLT, LDI, PRN, MUL, PUSH, POP,
                   CALL, RET, ADD, ST, JMP, PRA, IRET, CMP, JEQ, JNE, SUB}

        while self.halted == False:
            # Interrupt Timer
            timecheck = datetime.now().timestamp()
            if timecheck - self.timestamp >= 1:
                self.timestamp = timecheck
                self.reg[self.IS] += 0b00000001

            # Interrupt Check (if interrupts not disabled)
            if not self.disint:
                self.MDR = self.reg[self.IM] & self.reg[self.IS]
                for bit in range(8):
                    if self.MDR >> bit & 0b00000001 == 1:
                        self.disint = True
                        self.reg[self.IS] = self.reg[self.IS] - \
                            (0b00000001 << bit)
                        self.reg[0x04] = self.PC
                        self.handle_PUSH(0x04)
                        self.reg[0x04] = self.FL
                        self.handle_PUSH(0x04)
                        for reg in range(7):
                            self.handle_PUSH(reg)
                        self.MAR = self.ram[0xF8 + bit]
                        self.PC = self.MAR
                        break
                if self.disint:
                    continue

            self.IR = self.PC
            opsNum = (self.ram[self.IR] >> 6) & 0b11
            setPC = (self.ram[self.IR] >> 4) & 0b0001

            if self.ram[self.IR] in opcodes:
                if opsNum == 0:
                    # operation()
                    self.dispatch[self.ram[self.IR]]()
                if opsNum == 1:
                    # operation(operand a)
                    self.dispatch[self.ram[self.IR]](
                        self.ram_read(self.PC + 1))
                if opsNum == 2:
                    # operation(operand a, operand b)
                    self.dispatch[self.ram[self.IR]](self.ram_read(
                        self.PC + 1), self.ram_read(self.PC + 2))
            else:
                print('Error: Unknown opcode in program. Exiting LS-8 Emulator.')
                sys.exit()

            if setPC == 0:
                self.PC += opsNum + 1
