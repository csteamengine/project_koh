
@staticmethod
def write_new(first, last, id_num):
    """
    Create a new entry in the storage text file.

    :param first: the first name
    :param last: the last name
    :param id_num: id number
    :return: None
    """
    with open("test.txt", "w") as f:
        f.write("{}, {}, {}\n".format(first, last, id_num))

@staticmethod
def get_name(id_num):
    """
    Return the first and last name associated with an ID.

    :param id_num: the id number to search for
    :return: a JSON representation of the data returned, or None if not found
    """
    with open("test.txt", "r") as f:
        for x in f:
            x = x.rstrip()
            if not x: continue
            elif id_num in x:
                first, last, _ = x.split(', ')
                return json.dumps({'first': first, 'last': last})
    return None
