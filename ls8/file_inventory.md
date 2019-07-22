# LS-8 File Inventory

## cpu.py

### Description

The CPU class in this file emulates the LS-8 CPU.

### Component: Status

    def **init**(self): **not implemented**

    def load(self): **hardcoded implementation (will need further work)**

    def alu(self, op, reg_a, reg_b): **operation ADD implemented, will probably need other operations**

    def trace(self): **implemented**

    def run(self): **not implemented**

## ls8.py

### Description

I guess file will emulate the rest of the LS-8?

### Component: Status

    There don't seem to be any components in this file. The CPU class is instantiated, and then the load() and run() methods are called.
