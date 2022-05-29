from random import randint

class Ship:
    def __init__(self, ship, n):
        self.ship = ship
        self.n = n

class Board:
    def __init__(self):
        self.playing_field = [
            [' ', '1', '2', '3', '4', '5', '6', ''],
            ['1', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['2', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['3', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['4', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['5', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['6', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
            ['', '', '', '', '', '', '', '']
        ]
        self.type_of_ships = [3, 2, 2, 1, 1, 1, 1]
        self.limit_of_ships = (4, 2, 1)
        self.number_of_ships = [0, 0, 0]
        self.ships = []

    @staticmethod
    def draw_the_playing_field(playing_field, player):
        for m in range(len(playing_field) - 1):
            string = (' | '.join(playing_field[m]))
            if player == 'AI':
                string = string.replace('■', '⭘')
            print(string)
        print('\n')

    @staticmethod
    def cell_selection(player):
        if player == 'man':
            while True:
                try:
                    i = int(input('Укажите номер строки для поля, которое хотите выбрать.\n'))
                    j = int(input('А теперь номер столбца.\n'))
                except ValueError:
                    print('Неверный символ! Нужно ввести число в диапазоне 1-6!')
                    continue
                if (i or j) not in range(1, 7):
                    print('Значения должны быть в диапазоне 1-6!')
                else:
                    return i, j
        else:
            i = randint(1, 6)
            j = randint(1, 6)
            return i, j

    def ship_on_board_man(self):
        while True:
            try:
                n = int(input('Укажите тип корабля 1 - однопалубный, 2 - двухпалубный, 3 - трехпалубный.\n '))
            except ValueError:
                print('Неверный символ! Нужно ввести число в диапазоне 1-3!\n ')
                continue
            if n not in range(1, 4):
                print('Значения должны быть в диапазоне 1-3!\n ')
                continue
            elif self.number_of_ships[n-1] + 1 > self.limit_of_ships[n-1]:
                print('Все корабли данного типа уже построены, выберите другой тип корабля.\n ')
                continue
            else:
                break
        cell = Board.cell_selection(player='man')
        if n > 1:
            direct = input('Если хотите постоить корабль по горизонтали - введите любой символ,\
если по вертикали - просто нажмите ввод. \n')
        else:
            direct = '1'
        ship = self.ship_on_board_check(cell[0], cell[1], direct, n, player='man')
        if ship is not None:
            ship_class = Ship(ship, n)
            self.ships.append(ship_class)
            # self.ships.append(ship)
            self.number_of_ships[n-1] += 1
        if sum(self.number_of_ships) >= 7:
            print('Ваш флот простроен!')
            Board.draw_the_playing_field(self.playing_field, player='man')
        else:
            Board.draw_the_playing_field(self.playing_field, player='man')
            return self.ship_on_board_man()

    def ship_on_board_AI(self):
        ship = None
        attempt = 0
        for n in self.type_of_ships:
            ship = None
            while ship is None:
                attempt += 1
                if attempt > 2000:
                    break
                cell = Board.cell_selection(player='AI')
                direct = randint(0, 1)
                ship = self.ship_on_board_check(cell[0], cell[1], direct, n, player='AI')
            if ship is None:
                self.playing_field = [
                    [' ', '1', '2', '3', '4', '5', '6', ''],
                    ['1', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['2', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['3', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['4', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['5', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['6', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', '\u2B58', ''],
                    ['', '', '', '', '', '', '', '']
                ]
                self.ships = []
                return self.ship_on_board_AI()
            else:
                ship_class = Ship(ship, n)
                self.ships.append(ship_class)

    def ship_on_board_check(self, i, j, direct, n, player):
        ship = []
        try:
            if direct:
                if j + n > 7:
                    if player == 'man':
                        print('Корабль выходит за пределы игрового поля!\n')
                    return None
                for i_ in range(i - 1, i + 2):
                    if '\u25A0' in self.playing_field[i_][j - 1:j + n + 1]:
                        if player == 'man':
                            print('С этого поля нельзя начинать строить корабль! Выберите другое!\n')
                        return None
                for j_ in range(j, j + n):
                    self.playing_field[i][j_] = '\u25A0'
                    a = (i, j_)
                    ship.append(a)
                return ship
            else:
                if i + n > 7:
                    if player == 'man':
                        print('Корабль выходит за пределы игрового поля!\n')
                    return None
                for i_ in range(i - 1, i + n + 1):
                    if '\u25A0' in self.playing_field[i_][j - 1:j + 2]:
                        if player == 'man':
                            print('С этого поля нельзя начинать строить корабль! Выберите другое!\n')
                        return None
                for i_ in range(i, i + n):
                    self.playing_field[i_][j] = '\u25A0'
                    a = (i_, j)
                    ship.append(a)
                return ship
        except IndexError:
            if player == 'man':
                print('С этого поля нельзя начинать строить корабль! Выберите другое!\n')
            return None


class Player:
    def __init__(self, enemy_playing_field, enemy_ships, player, enemy):
        self.number_of_ships = [4, 2, 1]
        self.playing_field = enemy_playing_field
        self.ships = enemy_ships
        self.player = player
        self.enemy = enemy

    def shot(self):
        Board.draw_the_playing_field(self.playing_field, self.enemy)
        cell = Board.cell_selection(self.player)
        i = cell[0]
        j = cell[1]
        for ship_ in self.ships:
            if (i, j) in ship_.ship:
                self.playing_field[i][j] = 'X'
                ship_.n -= 1
                if ship_.n == 0:
                    if self.player == 'man':
                        print("Корабль противника уничтожен!\n")
                    else:
                        print("Ваш корабль уничтожен!\n")
                    self.number_of_ships[len(ship_.ship)-1] -= 1
                    bow = ship_.ship[0]
                    stern = ship_.ship[-1]
                    for i_ in range(bow[0]-1, stern[0]+2):
                        for j_ in range(bow[1]-1, stern[1]+2):
                            if self.playing_field[i_][j_] == '⭘':
                                self.playing_field[i_][j_] = '+'
                    if sum(self.number_of_ships) == 0:
                        return False
                    else:
                        return self.shot()
                else:
                    if self.player == 'man':
                        print("Корабль противника ранен!\n")
                    else:
                        print("Ваш корабль ранен!\n")

                    return self.shot()
            else:
                if self.playing_field[i][j] == '+' or self.playing_field[i][j] == 'X':
                    if self.player == 'man':
                        print(
                            "Вы уже делали выстрел в это поле или в этом поле не может быть корабля! Выберите другое!\n")
                    return self.shot()
                elif self.playing_field[i][j] == '⭘':
                    if self.player == 'man':
                        print("Вы промахнулись! Переход хода.\n")
                    else:
                        print("Противник промахнулся!\n")
                    self.playing_field[i][j] = '+'
                    Board.draw_the_playing_field(self.playing_field, self.enemy)
                    return False


print('-------------------------------------------')
print('--------- Морской бой начинается! ---------')
print('-------------------------------------------\n')

print('--- Для начала расставьте свои корабли! ---\n')

ai_board = Board()

ai_board.ship_on_board_AI()

man_board = Board()

Board.draw_the_playing_field(man_board.playing_field, player='man')

man_board.ship_on_board_man()

man = Player(ai_board.playing_field, ai_board.ships, player='man', enemy='AI')

ai = Player(man_board.playing_field, man_board.ships, player='AI', enemy='man')

while True:

    while True:

        print('---------------- Ваш ход! -----------------', '\n')

        print('----------- Это поле противника -----------', '\n')

        x = man.shot()

        if x is False:
            break

    if sum(man.number_of_ships) == 0:
        print('Вы победили! \n')
        break

    while True:

        print('---------------- Ходит противник! -----------------', '\n')

        print('----------------- Это ваше поле --------------------', '\n')

        y = ai.shot()

        if y is False:
            break

    if sum(ai.number_of_ships) == 0:
        print('Вы проиграли! \n')
        break


