import random


def read_field(filename):
    """ str -> list
    Returns a list of rows.
    """
    with open(filename, 'r', errors='ignore') as file_1:
        file = file_1.readlines()
    return [i.strip('\n') for i in file]


def has_ship(datas, let_num):
    """ list, tuple -> bool
    Returns True if the given coordinates represent a cell with a ship.
    """
    letters = 'ABCDEFGHIJ'
    row = datas[let_num[1]-1]
    column = letters.index(let_num[0])
    if column >= len(row):
        return False
    cell = row[column]
    if cell == '*':
        return True
    return False


def check(line, cell):
    """
    Finds the length (or width) of a ship.
    :param line: list
    :param cell: int
    :return: int
    """
    up, down, cell = 0, 0, cell + 3
    line = [' ', ' ', ' '] + line + [' ', ' ', ' ']
    for s in range(1, 4):
        if line[cell + s] == "*" and up == s - 1:
            up += 1
        if line[cell - s] == "*" and down == s - 1:
            down += 1
        elif line[cell - s] != "*" and line[cell + s] != "*":
            break
    return up + down + 1


def ship_size(data, let_num):
    """ list, tuple -> tuple
    Returns the measurements of the ship that is partially located on the
    given coordinates and returns None if the coordinates represent an empty
    field.
    """
    if not has_ship(data, let_num):
        return None
    letters = 'ABCDEFGHIJ'
    row = let_num[1] - 1
    col = letters.index(let_num[0])
    column = [row[col] if len(row) > col else ' ' for row in data]
    width = check([i for i in data[row]], col)
    length = check(column, row)
    return width, length


def is_valid(data):
    """ list -> bool
    Returns True if the given data contains a valid gamefield and False
    if not.
    """
    coords = []
    datas = [[' ']*12]
    datas.extend([[' '] + [i if i != '\n' else ' ' for i in raw] +
                  [' '] * (11-len(raw)) for raw in data])
    datas.extend([[' ']*12])
    for row in range(1,len(datas)-1):
        for column in range(1,len(datas[row])-1):
            if datas[row][column] == "*":
                for x in [-1,1]:
                    if not (datas[row+x][column+x] ==
                            datas[row-x][column+x] == " "):
                        return False
                width = check([i for i in datas[row]], column)
                length = check([raw[column] if len(raw) > column
                                else ' ' for raw in datas], row)
                coord = (width, length)
                coords.append(coord)
    check1 = len(coords) == len([i for i in coords if 1 in i]) == 20
    check2 = coords.count((1, 1)) == 4 and \
             ((coords.count((1, 4)) == 4) != (coords.count((4, 1)) == 4))
    check3 = coords.count((1, 3)) + coords.count((3,
             1)) == coords.count((1, 2)) + coords.count((2, 1))
    return True if ((check1 and check2) and check3) else False


def field_to_str(data):
    """
    Turns the list with field rows to string.
    :param data: list
    :return: str
    """
    field = ''
    for i in data:
        field += str(i)+'\n'
    return field


def generate_field():
    """
    Creates a valid gamefield with ten ships.
    :return: list
    """
    def ship(leng, x, y, field_xy):
        field_xy[x][y:leng + y] = ['*'] * leng
        for i in [-1, 1]:
            field_xy[x][y + leng] = "-"
            field_xy[x][y - 1] = "-"
            field_xy[x + i][y - 1:y + leng] = ["-"] * (leng + 1)
            field_xy[x + 1][y + leng] = "-"
            field_xy[x - 1][y + leng] = "-"
        return field_xy

    def create():
        field = [[' '] * 12 for i in range(12)]
        for leng, quant in zip([1, 2, 3, 4], [4, 3, 2, 1]):
            count = 0
            while count < quant:
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                field_2 = [[i[j] for i in field] for j in range(12)]
                if field_2[x][y:leng + y] == [" "] * leng and leng + y < 12:
                    field = field_2
                if field[x][y:leng + y] == [" "] * leng and leng + y < 12:
                    field = ship(leng, x, y, field)
                    count += 1
        return field
    return [(''.join(i[1:11])).replace('-', ' ') for i in create()[1:11]]


