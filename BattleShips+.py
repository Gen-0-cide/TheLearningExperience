from random import randint

class BoardOutException(Exception):
    def __str__(self):
        return "Клетка выходит за границы поля"

class AlphaException(Exception):
    def __str__(self):
        return "Первая координата клетки должна быть буквой 'А', 'Б', 'В', 'Г', 'Д' или 'Е'"

class DigitException(Exception):
    def __str__(self):
        return "Вторая координата клетки должна быть цифрой"

class ShipOutException(Exception):
    def __str__(self):
        return "Выберите другое место размещения корабля"


class LenKoordException(Exception):
    def __str__(self):
        return "Координата клетки должна состоять из двух значений\nВведите значение координаты клетки в формате 'А4'"

class PointBusy(Exception):
    def __str__(self):
        return "Данная клетка занята"


class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Ship():
    def __init__(self, lenght, point, position):
        self.lenght = lenght
        self.point = point
        self.lives = self.lenght
        self.position = position

    def __str__(self):
        return f"{self.lenght}-палубный корабль с координатой x равной {self.point.x} и координатой y равной {self.point.y}"

    def __repr__(self):
        return f"{self.lenght}-палубный корабль с координатой x равной {self.point.x} и координатой y равной {self.point.y}"

    @property
    def dots(self):
        x = self.point.x
        y = self.point.y
        ship_dots = []
        for _ in range(self.lenght):
            ship_dots.append(Dot(x, y))
            if self.position == "horizontal":
                y += 1
            elif self.position == "vertical":
                x += 1
        return ship_dots


class Board():
    def __init__(self, hid=False):
        self.field = [["O" for x in range(6)] for y in range(6)]
        self.list_ships = []
        self.hid = hid
        self.count = 7
        self.ship_list_dots = []


    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.ship_list_dots:
                raise ShipOutException
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.ship_list_dots.append(dot)
        self.list_ships.append(ship)
        self.contour(ship)

    def contour(self, ship, death=False):
        dots = ship.dots
        for x in range(dots[0].x - 1, dots[-1].x + 2):
            for y in range(dots[0].y - 1, dots[-1].y + 2):
                if (not self.out(Dot(x=x, y=y))) and (not Dot(x=x, y=y) in self.ship_list_dots):
                    self.ship_list_dots.append(Dot(x=x, y=y))
                if (not self.out(Dot(x=x, y=y))) and death and Dot(x=x, y=y) not in dots:
                    self.field[x][y] = "."

    def out(self, point):

        if 0 <= point.x <= 5 and 0 <= point.y <= 5:
            return False
        else:
            return True

    def shot(self, metka):
        if self.out(metka):
            raise BoardOutException
        if self.field[metka.x][metka.y] == "X" or self.field[metka.x][metka.y] == "." or self.field[metka.x][metka.y] == "T":
            raise PointBusy
        for ship in self.list_ships:
            if metka in ship.dots:
                self.field[metka.x][metka.y] = "X"
                ship.lives -= 1
                if ship.lives == 0:
                    print("Корабль пошёл ко дну!")
                    self.contour(ship, death=True)
                    self.count -= 1
                    return True
                else:
                    print("Ранен!")
                    return True
        print("Мимо!")
        self.field[metka.x][metka.y] = "T"
        return False

    def show(self):
        field_show = ""
        field_show += "   | А | Б | В | Г | Д | Е |\n"
        for i in range(6):
            field_show += f" {i + 1} | {' | '.join(self.field[i])} |\n"
        if self.hid:
            print(field_show.replace("■", "O"))
        else:
            print(field_show)


class Player():
    def __init__(self, my_board, opponent_board, name):
        self.my_board = my_board
        self.opponent_board = opponent_board
        self.name = name
        self.coordinats = {"А":1, "Б":2, "В":3, "Г":4, "Д":5, "Е":6}

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                check = self.opponent_board.shot(target)
                return check
            except PointBusy as e:
                if self.name == "Игрок":
                    print(e)
            except BoardOutException as e:
                if self.name == "Игрок":
                    print(e)


class AI(Player):
    def ask(self):
        x = randint(0, 5)
        y = randint(0, 5)
        return Dot(x=x, y=y)

class User(Player):
    def ask(self):
        while True:
            try:
                koord = input("Введите координаты клетки\n-->").replace(" ", "").upper()
                if len(koord)!=2:
                    raise LenKoordException
                y = koord[0]
                if not y.isalpha() or "АБВГДЕ".find(y) == -1:
                    raise AlphaException
                y = int(self.coordinats[koord[0]]) - 1
                x = koord[1]
                if not x.isdigit():
                    raise DigitException
                x = int(x) -1
                return Dot(x=x, y=y)
            except DigitException as e:
                print(e)
            except AlphaException as e:
                print(e)
            except LenKoordException as e:
                print(e)

class Game():
    def __init__(self):
        self.user_board = self.random_board()
        self.opponent_board = self.random_board()
        self.opponent_board.hid = True
        self.user = User(my_board=self.user_board, opponent_board=self.opponent_board, name="Игрок")
        self.opponent = AI(my_board=self.opponent_board, opponent_board=self.user_board, name="Компьютер")

    def random_board(self):
        result_board = None
        while True:
            result_board = self.filling_board()
            if result_board:
                return result_board


    def filling_board(self):
        positions = ["vertical", "horizontal"]
        any_board = Board()
        count = 0
        for item in [3, 2, 2, 1, 1, 1, 1]:
            while True:
                count+=1
                if count > 3000:
                    return None
                try:
                    any_board.add_ship(Ship(lenght=item, point=Dot(x=randint(0, 5), y=randint(0, 5)), position = positions[randint(0, 1)]))
                    break
                except ShipOutException:
                    pass
        return any_board

    def greet(self):
        print("______________________________________________")
        print("  Приветствуем  Вас  в игре  Морской  бой!    ")
        print("______________________________________________")
        print("     расположение   кораблей  по х  и  у      ")
        print("где 'х' - буква строки, а 'у' - номер столбца ")


    def loop(self):
        step = 0
        while True:
            print("Ваша доска")
            self.user.my_board.show()
            print("Доска противника")
            self.user.opponent_board.show()
            if not step % 2:
                print("Ваш ход")
                shoot = self.user.move()
            else:
                print("Ход компьютера")
                shoot = self.opponent.move()
            if shoot:
                step +=1
            step += 1

            if not self.user.my_board.count:
                print("Победа Компьютерра!")
                return

            if not self.user.opponent_board.count:
                print("Ваша победа!")
                return

    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()

