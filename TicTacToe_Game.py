from random import randint


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.__human_win = False
        self.__computer_win = False
        self.__is_draw = False

    # объекты свойства
    @property
    def is_human_win(self):
        return self.__human_win

    @property
    def is_computer_win(self):
        return self.__computer_win

    @property
    def is_draw(self):
        return self.__is_draw

    def init(self):
        """Метод для инициализации игры - очистка поля и закрытие клеток"""
        self.clear()
        self.__human_win = False
        self.__computer_win = False
        self.__is_draw = False

    def show(self):
        """Метод для отображения текущего состояния игрового поля"""
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == self.FREE_CELL:
                    print('-', end=' ')  # ячейка пустая
                elif self.pole[i][j].value == self.HUMAN_X:
                    print('x', end=' ')  # установлен крестик
                elif self.pole[i][j].value == self.COMPUTER_O:
                    print('o', end=' ')  # установлен нолик
            print()
        print()

    def __check_status(self):
        # проверка строк
        # проверка главной диагонали
        # проверка побочной диагонали
        if any(map(lambda x: all(i.value == self.HUMAN_X for i in x), (row for row in self.pole))) or \
                all(self.pole[i][j].value == self.HUMAN_X for i in range(3) for j in range(3) if i == j) or \
                all(self.pole[i][j].value == self.HUMAN_X for i in range(3) for j in range(3) if i == (3 - j - 1)):
            self.__human_win = True  # победа человека
            return

        if any(map(lambda x: all(i.value == self.COMPUTER_O for i in x), (row for row in self.pole))) or \
                all(self.pole[i][j].value == self.COMPUTER_O for i in range(3) for j in range(3) if i == j) or \
                all(self.pole[i][j].value == self.COMPUTER_O for i in range(3) for j in range(3) if i == (3 - j - 1)):
            self.__computer_win = True  # победа компьютера
            return

        # проверка столбцов
        result_h = []  # список True/False для ходов человека
        result_c = []  # список True/False для ходов компьютера
        for i in range(3):
            for j in range(3):
                result_h.append(self.pole[j][i].value == self.HUMAN_X)
                result_c.append(self.pole[j][i].value == self.COMPUTER_O)
            if all(result_h):
                self.__human_win = True  # победа человека
                return
            elif all(result_c):
                self.__computer_win = True  # победа человека
                return
            else:
                result_h.clear()
                result_c.clear()

    def human_go(self):
        """Метод для реализации хода игрока
        (запрашивает координаты свободной клетки и ставит туда крестик)"""
        i, j = map(int, input().split())  # получение координат из командной строки
        if isinstance(i, int) and isinstance(j, int):
            if self.pole[i][j].is_free:
                self[i, j] = self.HUMAN_X
                self.pole[i][j].is_free = False
            self.__check_status()  # проверка результата хода

    def computer_go(self):
        """Метод для реализации хода компьютера
        (ставит случайным образом нолик в свободную клетку)"""
        while True:
            i, j = randint(0, 2), randint(0, 2)  # случайные координаты
            if self.pole[i][j].is_free:
                self[i, j] = self.COMPUTER_O
                self.pole[i][j].is_free = False
                self.__check_status()  # проверка результата хода
                break

    def clear(self):
        """Метод для очистки игрового поля
         (все клетки заполняются нулями и переводятся в закрытое состояние)"""
        for i in range(3):
            for j in range(3):
                self.pole[i][j].value = self.FREE_CELL
                self.pole[i][j].is_free = True

    @staticmethod
    def _check_index(index):
        """Метод для проверки индекса"""
        if not isinstance(index[0], int) or not isinstance(index[1], int) \
                or not 0 <= index[0] < 3 or not 0 <= index[1] < 3:
            raise IndexError('некорректно указанные индексы')

    def __setitem__(self, key, value):
        """Метод для записи нового значения в клетку с индексами i, j"""
        if isinstance(key, tuple):
            self._check_index(key)
            i, j = key
            if not self.pole[i][j].is_free:
                raise ValueError('клетка уже занята')

            self.pole[i][j].value = value
            self.pole[i][j].is_free = False
            self.__check_status()  # проверка результата хода

    def __getitem__(self, item):
        """Метод для получения значения из клетки с индексами i, j"""
        if isinstance(item[0], int) and isinstance(item[1], int):
            self._check_index(item)
            i, j = item
            return self.pole[i][j].value

    def __bool__(self):
        """Метод для проверки статуса игры (нужно ли делать следующий ход)"""
        return any(cell.is_free for row in self.pole for cell in row) and not \
            self.is_human_win and not self.is_computer_win


class Cell:
    def __init__(self):
        self.is_free = True  # True, если клетка свободна; False в противном случае
        self.value = 0  # значение поля: 1 - крестик; 2 - нолик (по умолчанию 0)

    def __bool__(self):
        return self.value == 0

