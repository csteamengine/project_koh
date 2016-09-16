def write_new(first, last, id_num):
    """
    Create a new entry in the storage text file.

    :param first: the first name
    :param last: the last name
    :param id_num: id number
    :return: None
    """
    with open("database.txt", "a") as f:
        f.write("{}, {}, {}\n".format(first, last, id_num))


def get_id(first_name, last_name):
    """
    :param first_name: The first_name to search for.
    :param last_name: The last_name to search for.
    :return: The id number for the given first/last name, otherwise None.
    """
    with open("database.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if not line:
                continue
            first, last, _id = line.split(", ")
            if first_name == first and last_name == last:
                return _id
    return None


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
            first, last, _id = line.split(", ")
            if id_num_string == _id:
                return first, last
    return None, None
