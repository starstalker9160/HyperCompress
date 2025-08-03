import struct

class HyperCompress:
    def __init__(self):
        # positional schema
        self.acceptableTypes = []
        self._values = []

    def add(self, val):
        if len(self._values) >= len(self.acceptableTypes):
            print(self._values, "\n", self.acceptableTypes, "\n")
            raise IndexError("Too many values for schema")
        expected_type = self.acceptableTypes[len(self._values)]
        if not isinstance(val, expected_type):
            raise TypeError(f"Expected {expected_type.__name__}, got {type(val).__name__}")
        self._values.append(val)

    @property
    def value(self):
        return self._encode()

    def _encode(self):
        out = bytearray()
        for val, typ in zip(self._values, self.acceptableTypes):
            if typ is int:
                out += val.to_bytes(4, 'big', signed=True)
            elif typ is float:
                out += struct.pack('>d', val)
            elif typ is bool:
                out += b'\x01' if val else b'\x00'
            elif typ is str:
                encoded = val.encode('utf-8')
                out += len(encoded).to_bytes(2, 'big') + encoded
            elif typ is bytes:
                out += len(val).to_bytes(4, 'big') + val
        return bytes(out)

    def decode(self, blob):
        result = []
        i = 0
        for t in self.acceptableTypes:
            if t is int:
                result.append(int.from_bytes(blob[i:i+4], 'big', signed=True))
                i += 4
            elif t is float:
                result.append(struct.unpack('>d', blob[i:i+8])[0])
                i += 8
            elif t is bool:
                result.append(blob[i] == 1)
                i += 1
            elif t is str:
                length = int.from_bytes(blob[i:i+2], 'big')
                i += 2
                result.append(blob[i:i+length].decode('utf-8'))
                i += length
            elif t is bytes:
                length = int.from_bytes(blob[i:i+4], 'big')
                i += 4
                result.append(blob[i:i+length])
                i += length
        return result




# HC File Handling
class HCFile:
    def __init__(self, path, mode):
        if 'b' not in mode:
            mode += 'b'
        self.file = open(path, mode)
        self.closed = False

    def hc_write(self, blob: bytes):
        self.file.write(len(blob).to_bytes(4, 'big'))
        self.file.write(blob)

    def hc_read(self):
        size_bytes = self.file.read(4)
        if not size_bytes:
            return None
        size = int.from_bytes(size_bytes, 'big')
        return self.file.read(size)

    def hc_append(self, blob: bytes):
        self.file.seek(0, 2)
        self.hc_write(blob)

    def close(self):
        if not self.closed:
            self.file.close()
            self.closed = True



# Exposed API functions
def hc_open(path, mode='rb'):
    return HCFile(path, mode)

def hc_close(hcfile):
    hcfile.close()

def hc_read(hcfile):
    return hcfile.hc_read()

def hc_write(hcfile, blob: bytes):
    hcfile.hc_write(blob)

def hc_append(hcfile, blob: bytes):
    hcfile.hc_append(blob)
