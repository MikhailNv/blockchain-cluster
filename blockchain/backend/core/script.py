class Script:
    def __init__(self, cmds=None):
        self.cmds = cmds if cmds else []

    @classmethod
    def p2pkh_script(cls, h160):
        """Takes a hash160 and returns the p2pkh script publickey"""
        return Script([0x76, 0xa9, h160, 0x88, 0xac])