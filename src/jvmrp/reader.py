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


def read_u4(f):
    u2_1 = read_u2(f)
    u2_2 = read_u2(f)
    return (u2_1 << 16) + u2_2


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
    interfaces_count = read_u2(f)
    # TODO
    if interfaces_count > 0:
        raise Exception()
    fields_count = read_u2(f)
    # TODO
    if fields_count > 0:
        raise Exception()
    methods_count = read_u2(f)
    methods = [read_method_info(f, constant_pool) for _ in range(methods_count)]
    attributes_count = read_u2(f)
    attributes = [read_attribute(f, constant_pool) for _ in range(attributes_count)]

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
        "methods": methods,
        "attributes": attributes,
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


def read_method_info(f, constant_pool):
    access_flags = read_u2(f)
    name_index = read_u2(f)
    name = constant_pool[name_index - 1]["bytes"]
    descriptor_index = read_u2(f)
    descriptor = constant_pool[descriptor_index - 1]["bytes"]
    attributes_count = read_u2(f)
    attributes = [read_attribute(f, constant_pool) for _ in range(attributes_count)]

    return {
        "access_flags": access_flags,
        "name_index": name_index,
        "name": name,
        "descriptor_index": descriptor_index,
        "descriptor": descriptor,
        "attributes_count": attributes_count,
        "attributes": attributes,
    }


def read_attribute(f, constant_pool):
    attribute_name_index = read_u2(f)
    attribute_length = read_u4(f)
    attribute_name = constant_pool[attribute_name_index - 1]["bytes"]

    match attribute_name:
        case b"Code":
            max_stack = read_u2(f)
            max_locals = read_u2(f)
            code_length = read_u4(f)
            code = [b for b in f.read(code_length)]
            exception_table_length = read_u2(f)
            # TODO
            if exception_table_length > 0:
                raise Exception()
            exception_table = []
            attributes_count = read_u2(f)
            attributes = [
                read_attribute(f, constant_pool) for _ in range(attributes_count)
            ]
            attribute = {
                "attribute_name_index": attribute_name_index,
                "attribute_name": attribute_name,
                "attribute_length": attribute_length,
                "max_stack": max_stack,
                "max_locals": max_locals,
                "code_length": code_length,
                "code": code,
                "exception_table_length": exception_table_length,
                "exception_table": exception_table,
                "attributes_count": attributes_count,
                "attributes": attributes,
            }
        case b"LineNumberTable":
            line_number_table_length = read_u2(f)
            line_number_table = [
                {"start_pc": read_u2(f), "line_number": read_u2(f)}
                for _ in range(line_number_table_length)
            ]
            attribute = {
                "attribute_name_index": attribute_name_index,
                "attribute_name": attribute_name,
                "attribute_length": attribute_length,
                "line_number_table_length": line_number_table_length,
                "line_number_table": line_number_table,
            }
        case b"SourceFile":
            attribute = {
                "attribute_name_index": attribute_name_index,
                "attribute_name": attribute_name,
                "sourcefile_index": read_u2(f),
            }
        case _:
            raise Exception(f"Not implemented: {attribute_name}")

    return attribute
