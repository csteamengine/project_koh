def write_new(first, last, id_num):
    """
    Create a new entry in the storage text file.

    :param first: the first name
    :param last: the last name
    :param id_num: id number
    :return: None
    """
    with open("database.txt", "w") as f:
        f.write("{}, {}, {}\n".format(first, last, id_num))


def get_name(id_num):
    """
    Return the first and last name associated with an ID.

    :param id_num: the id number to search for
    :return: a tuple of the (first_name, last_name), or (None, None) if not found
    """
    with open("database.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            id_num_string = str(id_num)
            if not line:
                continue
            elif id_num_string in line:
                first, last, _ = line.split(', ')
                return first, last
    return None, None
