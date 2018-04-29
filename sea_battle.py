import random
# this module contains a game of Sea Battle
# Two players take turns at guessing the location of the enemy`s ships using
# rows and columns of a 10x10 square (for example, A1 or D6). The first one
# to kill all of the enemy`s ships wins.


class Game:
    """
    This class represents the game of Sea Battle.
    """
    def __init__(self):
        """
        Creates an instance of class Game with two players and fields.
        """
        self.__fields = [Field(), Field()]
        self.__players = [Player('', 1), Player('', 2)]
        self.__current = self.__players[0]

    def read_position(self, row, column):
        """
        Takes input in a form of A1 or g8 and converts it into a location on
        the field (a list of two digits between 0 and 9).
        :param row: None
        :param column: None
        :return: list
        """
        letter = 'ABCDEFGHIJ'
        while row is None or column is None:
            attack = input("Enter the target square, e.g. A1, {}: ".format
                             (self._Game__current._Player__name)).strip()
            column = letter.index(attack[0].upper()) \
                if len(attack) > 1 and attack[0].upper() in letter else None
            row = int(attack[1:])-1 if \
                attack[1:].isdigit() and int(attack[1:]) < 11 else None
        return [column, row]

    def field_without_ships(self, index):
        print('field of player {}'.
              format(self._Game__players[index]._Player__name))
        self._Game__fields[index].field_without_ships()

    def field_with_ships(self, index):
        print('field of player {}'.
              format(self._Game__players[index]._Player__name))
        self._Game__fields[index].field_with_ships()
        # print(field_.ships)


class Player:
    """
    This class represents a player in the game, with their name and field.
    """
    def __init__(self, name, index):
        self.__name = name
        while len(self.__name) < 1:
            me = Player(input("Enter your name, player no. {}: "
                              .format(index)).strip(), index)
            self.__name = me.__name


class Field:
    """
    This class represents the field of each player, which is 10x10 and
    has 10 ships on it.
    """
    def __init__(self):
        """
        Creates an instance of class Field. Creates ten instances of class
        Ship and puts them on the field.
        """
        ships = []
        field = [[' '] * 12 for i in range(12)]
        for length, quantity in zip([1, 2, 3, 4], [4, 3, 2, 1]):
            count = 0
            while count < quantity:
                new_ship = Ship(length, field)
                field = new_ship.field
                count += 1
                ships.append(new_ship)
        self.field = [i[1:11] for i in field[1:11]]
        self.__ships = ships

    def shoot_at(self, coords):
        """
        Takes the location in a form of two digits representing row and
        column and checks if there is a ship in that location on the field
        and calls a method of a ship instance if there is, and returns True.
        If there is no ship, it changes the location to 'used' and returns
        False.
        :param coords: list
        :return: bool
        """
        column = coords[0]
        row = coords[1]
        # to check if the location has already been used by the player
        if self.field[row][column] in ['╳', '︵']:
            print("Already used it.")
            return True  # so that the player gets another chance to try
        for i in self._Field__ships:
            if i.bow == [column, row]:
                i._Ship__hit += 1
            elif i._Ship__horizontal and row == i.bow[1] and column in \
                    range(i.bow[0], i.bow[0]+i._Ship__length):
                    i._Ship__hit += 1
            elif not i._Ship__horizontal and column == i.bow[0] and row \
                    in range(i.bow[1], i.bow[1]+i._Ship__length):
                    i._Ship__hit += 1
            else:
                continue
            if i._Ship__hit:
                self.field = i.shoot_at([row, column], self.field)
                if len([1 for i in self._Field__ships if
                        i._Ship__hit == i._Ship__length]) == 10:
                    self._Field__ships = []
                return True
        self.field[row][column] = "︵"
        print('Miss. (◕︵◕)')
        return False

    def field_with_ships(self):
        """
        Prints out the field with ships and killed ships on it.
        :return: str
        """
        print('  𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧')
        for i in self.field:
            print(self.field.index(i)+1, end=' ') if self.field.index(i) < 9 \
                else print(self.field.index(i)+1, end='')
            print(''.join(i).replace('-', '～').replace(' ', '～'))
        return ""

    def field_without_ships(self):
        """
        Prints out the field with killed ships only (how it should be seen by
        the other player.
        :return: str
        """
        print('  𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧')
        for i in self.field:
            print(self.field.index(i) + 1, end=' ') if self.field.index(i) < 9 \
                else print(self.field.index(i) + 1, end='')
            print(''.join(i).replace('-', '～').replace(' ', '～')
                  .replace('▇', '～'))
        return ""


class Ship:
    """
    The class represents a ship on the field.
    """
    def __init__(self, length, field):
        """
        Creates an instance of a Ship class with the given length and on the
        given field. Tries a random two-digit location and if the ship fits
        vertically, it puts it on the field, if it doesn't fit vertically
        it tries to put it horizontally.
        :param length: int
        :param field: list
        """
        count = 0
        self.__horizontal = True
        self.reverse = False
        while count < 1:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            field_alternative = [[i[j] for i in field] for j in range(12)]
            if field_alternative[x][y:length + y] == [" "] * length and \
                    length + y < 12:
                field = field_alternative
                self.reverse = True
                self.__horizontal = False
            if field[x][y:length + y] == [" "] * length and length + y < 12:
                field[x][y:length + y] = ['▇'] * length
                field[x][y + length] = "-"
                field[x][y - 1] = "-"
                for i in [-1, 1]:
                    field[x + i][y - 1:y + length + 1] = ["-"] * (length + 2)
                count += 1
            if self.reverse:
                field = [[i[j] for i in field] for j in range(12)]
        self.field = field
        self.bow = [x-1, y-1] if self.reverse else [y-1, x-1]
        self.__length = length
        self.__hit = 0

    def shoot_at(self, location, field):
        """
        Changes the location to 'killed' and if the ship is dead changes the
        surrounding squares to 'used' so that it is easier to see if the ship
        is dead later in the game.
        :param location: list
        :param field: list
        :return: list
        """
        field[location[0]][location[1]] = '╳'
        print("Hit. (◕‿◕) ")
        x = self.bow[1]+1
        y = self.bow[0]+1
        length = self.__length
        if self._Ship__hit == self._Ship__length:
            print('Ship is dead.')
            field = [[' '] + field[i - 1] + [' '] if 0 < i < 11 else
                     [' '] * 12 for i in range(len(field) + 2)]
            if not self.__horizontal:
                field = [[i[j] for i in field] for j in range(12)]
                x, y = self.bow[0]+1, self.bow[1]+1
            field[x][y + length] = "︵"
            field[x][y - 1] = "︵"
            for i in [-1, 1]:
                field[x + i][y - 1:y + length + 1] = ["︵"] * (length + 2)
            return [field[i][1:11] for i in range(1, len(field)-1)] if \
                self.__horizontal else [[field[i][j] for i in range
                                     (1, len(field)-1)] for j in range(1, 11)]
        return field


def main():
    """
    The main function of the module which starts the game.
    :return: None
    """
    game = Game()
    while True:
        index = game._Game__players.index(game._Game__current)
        game.field_without_ships(abs(index-1))
        position = game.read_position(None, None)
        if not game._Game__fields[abs(index-1)].shoot_at(position):
            game._Game__current = game._Game__players[abs(index-1)]
        if not game._Game__fields[index-1]._Field__ships:
            print("{} is the winner! Congrats! ┑(￣▽￣)┍ ".
                  format(game._Game__current._Player__name))
            yes = input('If you wish to play again, type "yes"').strip()
            if yes == 'yes':
                game = Game()
            else:
                break
