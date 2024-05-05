def read_u2(f):
    return int.from_bytes(f.read(2), "big")


def read_class(f):
    magic = f.read(4)
    minor_version = read_u2(f)
    major_version = read_u2(f)

    return {
        "magic": magic,
        "minor_version": minor_version,
        "major_version": major_version,
    }
