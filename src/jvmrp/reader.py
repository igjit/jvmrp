class CPTag:
    Utf8 = 1
    Class = 7
    String = 8
    Fieldref = 9
    Methodref = 10
    NameAndType = 12


def read_u1(f):
    return int.from_bytes(f.read(1), "big")


def read_u2(f):
    return int.from_bytes(f.read(2), "big")


def read_class(f):
    magic = f.read(4)
    minor_version = read_u2(f)
    major_version = read_u2(f)
    constant_pool_count = read_u2(f)
    constant_pool = [read_cp_info(f) for _ in range(constant_pool_count - 1)]
    access_flags = read_u2(f)
    this_class = read_u2(f)
    this_class_name_index = constant_pool[this_class - 1]["name_index"]
    this_class_name = constant_pool[this_class_name_index - 1]["bytes"]
    super_class = read_u2(f)
    super_class_name_index = constant_pool[super_class - 1]["name_index"]
    super_class_name = constant_pool[super_class_name_index - 1]["bytes"]

    return {
        "magic": magic,
        "minor_version": minor_version,
        "major_version": major_version,
        "constant_pool": constant_pool,
        "access_flags": access_flags,
        "this_class": this_class,
        "this_class_name": this_class_name,
        "super_class": super_class,
        "super_class_name": super_class_name,
    }


def read_cp_info(f):
    tag = read_u1(f)
    match tag:
        case CPTag.Utf8:
            length = read_u2(f)
            bytes = f.read(length)
            info = {"length": length, "bytes": bytes}
        case CPTag.Class:
            info = {"name_index": read_u2(f)}
        case CPTag.String:
            info = {"string_index": read_u2(f)}
        case CPTag.Fieldref | CPTag.Methodref:
            info = {"class_index": read_u2(f), "name_and_type_index": read_u2(f)}
        case CPTag.NameAndType:
            info = {"name_index": read_u2(f), "descriptor_index": read_u2(f)}
        case _:
            raise ValueError(f"Unknown tag: {tag}")

    return {"tag": tag, **info}
