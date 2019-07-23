
class Dispatch:

    def __init__(self):
        # Set up the branch table
        self.dispatch = {}
        self.dispatch[HLT] = self.handle_HLT
        self.dispatch[LDI] = self.handle_LDI
        self.dispatch[PRN] = self.handle_PRN
        self.dispatch[MUL] = self.handle_MUL

    def handle_HLT(self):
        # TODO
        pass

    def handle_LDI(self):
        # TODO
        pass

    def handle_PRN(self):
        # TODO
        pass

    def handle_MUL(self):
        # TODO
        pass
