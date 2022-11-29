import base64
# todo: should consider the data format when upload, otherwise, it's too redundant


def encrypt(i: bytes) -> bytes:
    if type(i) is bytes:
        b = i
    else:
        raise TypeError(f"require bytes type to do encryption in encrypt() security.py, but accept {type(i)} of {i}")
    return base64.b64encode(b)


def decrypt(i: bytes) -> bytes:
    return base64.b64decode(i)


if __name__ == "__main__":
    pass
