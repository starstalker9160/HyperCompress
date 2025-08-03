class HyperCompress:
    def __init__(self):
        self.acceptableTypes = []
        # yes yes, i know, this list isn't very binary format of me but ill change it pinky promise
        self._values = []

    def add(self, val):
        if type(val) not in self.acceptableTypes:
            raise TypeError(f"{type(val).__name__} not accepted")
        self._values.append(val)

    @property
    def value(self):
        return self._encode()

    def _encode(self):
        # using 'type headers + compressed' format
        # temporarily ofcourse
        # surely ill change to something better right?
        out = b''
        for i in self._values:
            if isinstance(i, int):
                out += b'i' + i.to_bytes(4, 'big', signed=True)
            elif isinstance(i, str):
                encoded = i.encode('utf-8')
                out += b's' + len(encoded).to_bytes(2, 'big') + encoded
            elif isinstance(i, bool):
                out += b'b' + (b'\x01' if i else b'\x00')
        return out

    def decode(self, blob):
        result = []
        i = 0
        while i < len(blob):
            type_code = blob[i:i+1]
            i += 1
            # i have a strong feeling this is gonna go horribly
            # the sam fuck of all if-else statements
            # maybe the real upgrade is a switch-case? (please god no)
            if type_code == b'i':
                result.append(int.from_bytes(blob[i:i+4], 'big', signed=True))
                i += 4
            elif type_code == b's':
                length = int.from_bytes(blob[i:i+2], 'big')
                i += 2
                result.append(blob[i:i+length].decode('utf-8'))
                i += length
            elif type_code == b'b':
                result.append(blob[i:i+1] == b'\x01')
                i += 1
            else:
                raise ValueError("Unknown type prefix")
        return result
