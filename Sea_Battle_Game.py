from random import randint, shuffle


class Ship:
    """Класс для представления кораблей"""

    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, length: int, tp: int = HORIZONTAL, x: int = None, y: int = None):
        self._length = length  # длина корабля
        self._tp = tp  # ориентация корабля(1 - горизонтальная, 2 - вертикальная)
        self._x = x  # координаты начала корабля(первая палуба)
        self._y = y
        self._is_move = True  # возможность перемещения корабля(если не было попадания - True, иначе False)
        self._cells = [1] * length  # список с палубами корабля(1 - попадания не было, 2 - попадание было)

    def __repr__(self):
        return f'({self._length}-палубный, {"Горизонтальный" if self._tp == 1 else "Вертикальный"}, ' \
               f'{"Целый" if self._is_move else "Подбитый"}, ' \
               f'x={self._x} y={self._y})'

    @property
    def tp(self):
        return self._tp

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def length(self):
        return self._length

    @property
    def is_move(self):
        return self._is_move

    def set_start_coords(self, x: int, y: int):
        """Метод для установки начальных координат корабля"""
        self._x = x
        self._y = y

    def get_start_coords(self) -> tuple:
        """Получение начальных координат корабля"""
        return self._x, self._y

    def move(self, go: int):
        """Метод реализует перемещения корабля в направлении его ориентации на 'go' клеток"""
        if self._is_move:
            x, y = self.get_start_coords()
            if self._tp == self.HORIZONTAL:
                self.set_start_coords(x + go, y)
            elif self._tp == self.VERTICAL:
                self.set_start_coords(x, y + go)

    @staticmethod
    def _get_place_and_around_coordinates(ship_orientation: int, ship: 'Ship') -> tuple:
        """Метод для получения координат нахождения всего корабля и
        координат вокруг корабля"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)  # индексы вокруг клетки
        all_coord = set()  # координаты корабля и координаты вокруг корабля
        ship_coord = set()  # координаты только корабля
        x, y, length = ship._x, ship._y, ship._length

        if ship_orientation == ship.HORIZONTAL:
            ship_coord = {(x + j, y) for j in range(length)}  # сбор координат каждой палубы корабля

        elif ship_orientation == ship.VERTICAL:
            ship_coord = {(x, y + i) for i in range(length)}

        # сбор координат вокруг корабля и самого корабля
        for a, b in indexes:
            for c, d in ship_coord:
                all_coord.add((a + c, b + d))

        return all_coord, ship_coord

    def is_collide(self, ship: 'Ship') -> bool:
        """Метод для проверки на столкновение или соприкосновение с другим кораблем 'ship'"""
        if isinstance(ship, Ship):
            # получение координат текущего корабля и другого корабля
            all_coord_ship, ship_coord = self._get_place_and_around_coordinates(self._tp, self)
            all_coord_self, self_coord = ship._get_place_and_around_coordinates(ship._tp, ship)
            common_coord = all_coord_ship & all_coord_self  # общие координаты двух кораблей
            # координаты мест пересечения кораблей(если таких нет - значит корабли не пересекаются и не касаются)
            result = (ship_coord & common_coord) | (self_coord & common_coord)
            return len(result) != 0

    def is_out_pole(self, size: int) -> bool:
        """Метод для проверки на выход корабля за пределы игрового поля"""
        x, y = self._x, self._y
        last_part_coord = (x + self._length - 1, y) if self._tp == self.HORIZONTAL else (x, y + self._length - 1)
        return x < 0 or last_part_coord[0] > size - 1 or y < 0 or last_part_coord[1] > size - 1

    def _check_index(self, index) -> bool:
        """Метод для проверки индекса для работы со списком _cells"""
        return 0 <= index <= len(self._cells)

    def __getitem__(self, item: int) -> int:
        """Метод для считывания значения из списка _cells по индексу item"""
        if self._check_index(item):
            return self._cells[item]

    def __setitem__(self, key, value):
        """Метод для записи нового значения в _cells по индексу key"""
        if self._check_index(key) and isinstance(value, int) and value in (1, 2):
            self._cells[key] = value


class GamePole:
    """Класс для описания игрового поля"""

    def __init__(self, size: int = 10):
        self._size = size  # размер игрового поля
        self._ships = []  # список из кораблей на поле
        self._field = [[0] * self._size for _ in range(self._size)]  # игровое поле

    @property
    def ships(self):
        return self._ships

    def _check_ships_around(self, length: int, head_coord: tuple, orientation: int) -> int:
        """Метод для проверки наличия кораблей вокруг и на месте установки корабля"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)
        head_x, head_y = head_coord
        result = 0

        if orientation == 1:  # горизонтально
            j = head_x
            k = 0
            while length > k:  # пока не проверили на наличие кораблей вокруг и на месте установки
                result += sum(self._field[head_y + x][j + y] for x, y in indexes
                              if 0 <= head_y + x < self._size and 0 <= j + y < self._size)
                j += 1
                k += 1

        elif orientation == 2:  # вертикально
            i = head_y
            k = 0
            while length > k:  # пока не проверили на наличие кораблей вокруг и на месте установки
                result += sum(self._field[i + x][head_x + y] for x, y in indexes
                              if 0 <= i + x < self._size and 0 <= head_x + y < self._size)
                i += 1
                k += 1

        return result

    def init(self):
        """Метод для начальной инициализации игрового поля"""
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]

        for ship in self._ships:
            tp, length = ship.tp, ship.length
            while True:  # пока корабли не расставлены
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)  # ship_x -> j; ship_y -> i
                if tp == ship.HORIZONTAL:  # если расположение корабля горизонтальное
                    if x + (length - 1) > self._size - 1:  # если длина корабля выходит за поле
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:  # если кораблей нет рядом и нет на месте
                        k = 0
                        for j in range(x, x + length):
                            self._field[y][j] = ship.__getitem__(k)  # установка корабля на поле с k-палубами
                            k += 1
                    else:
                        continue

                elif tp == ship.VERTICAL:  # если расположение корабля вертикальное
                    if y + (length - 1) > self._size - 1:  # если длина корабля выходит за поле
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:  # если кораблей нет рядом и нет на месте
                        k = 0
                        for i in range(y, y + length):
                            self._field[i][x] = ship.__getitem__(k)
                            k += 1
                    else:
                        continue

                ship.set_start_coords(x, y)  # установить в текущем корабле его начальные координаты
                break

    def get_ships(self) -> list:
        """Метод для возврата списка кораблей на поле"""
        return self._ships

    def update_game_field(self):
        """Метод для обновления игрового поля
        после движения кораблей и после каждого хода"""
        for i in range(self._size):  # обнуление поля
            for j in range(self._size):
                self._field[i][j] = 0

        for ship in self._ships:
            x, y, length = ship.x, ship.y, ship.length
            ship_part = 0

            if ship.tp == ship.HORIZONTAL:
                for j in range(x, x + length):
                    self._field[y][j] = ship.__getitem__(ship_part)  # установка корабля на поле с k-палубами
                    ship_part += 1
            elif ship.tp == ship.VERTICAL:
                for i in range(y, y + length):
                    self._field[i][x] = ship.__getitem__(ship_part)
                    ship_part += 1

    def move_ships(self):
        """Метод для перемещения каждого корабля на одну клетку"""
        for ship in self._ships:
            old_x, old_y = ship.get_start_coords()
            directions = ['forward', 'back']  # допустимые направления движения
            is_conflict = False
            while directions or not is_conflict:
                shuffle(directions)  # перемешивание списка с направлениями
                direction = directions.pop()  # и взятие первого

                x = y = 0  # переменные для новых (возможных) координат
                if direction == 'forward' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x + 1
                    y = ship.y
                elif direction == 'back' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x - 1
                    y = ship.y
                elif direction == 'forward' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y + 1
                elif direction == 'back' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y - 1
                else:
                    break

                ship.set_start_coords(x, y)  # применяем новые координаты начала для корабля
                if ship.is_out_pole(self._size):  # если корабль выходит за поле - попробовать другое направление
                    ship.set_start_coords(old_x, old_y)
                    continue

                for curr_ship in self._ships:
                    if curr_ship != ship:
                        if not ship.is_collide(curr_ship):  # проверка столкновения текущего корабля с другими
                            continue
                        else:  # если было столкновение или пересечение
                            ship.set_start_coords(old_x, old_y)  # сброс новых координат до начальных
                            is_conflict = True  # и установка флага конфликта
                            break
                if is_conflict:  # если был обнаружен конфликт - попробовать переместить корабль в другую сторону
                    continue
                break

        self.update_game_field()  # обновить поле с новым размещением кораблей

    def show(self):
        """Метод для отображения игрового поля в консоли"""
        print('_' * (self._size * 2 - 1))
        for row in self._field:
            print(*row, end='\n')
        print('_' * (self._size * 2 - 1))

    def get_pole(self) -> tuple:
        """Метод для получения текущего игрового поля"""
        return tuple(tuple(row) for row in self._field)

    def __repr__(self) -> str:
        return f'Размер поля - {self._size} x {self._size}'


class SeaBattle:
    """Класс для настройки и работы игрового процесса"""
    _x_coord_translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}

    def __init__(self, size_field):
        self.computer = GamePole(size_field)
        self.human = GamePole(size_field)

    def init_fields(self):
        """Метод инициализации полей компьютера и человека.
        Метод производит расстановку кораблей на полях соперников"""
        self.computer.init()
        self.human.init()

    def recognize_shell_place(self, shell_coord: tuple):
        """Метод для распознавания места куда попал снаряд"""
        pass

    def human_go(self):
        """Метод для реализации хода человека"""
        x = y = None
        while True:
            try:
                coord = input('Введите координаты поля для выстрела в формате "a 1", "j 10", "g 3"').split()
                x, y = coord
            except (TypeError, IndexError, ValueError):
                print('Введен не верный тип и/или диапазон координат')
                continue
            else:
                if coord[0] in 'abcdefghij' and '1' <= coord[1] in '123456789':
                    x, y = self._x_coord_translate.get(coord[0]) - 1, int(coord[1]) - 1
                    print('Неверный формат ввода')
                    break
                continue

        field_comp = self.computer.get_pole()
        aim = field_comp[x][y]

    def computer_go(self):
        """Метод для реализации хода компьютера
         случайным образом в свободные клетки"""


battle = SeaBattle(10)
battle.init_fields()
battle.human.show()
battle.computer.show()
battle.human_go()
pass
