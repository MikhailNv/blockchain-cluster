from utils import int_to_little_endian, encode_variant


class Script:
    def __init__(self, cmds=None):
        self.cmds = cmds if cmds else []

    def serialize(self):
        result = b''

        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length > 0x100 and length <= 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError("Команда cmd слишком длинная")
                result += cmd

        total = len(result)
        return encode_variant(total) + result

    @classmethod
    def p2pkh_script(cls, h160):
        """Takes a hash160 and returns the p2pkh script publickey"""
        return Script([0x76, 0xa9, h160, 0x88, 0xac])