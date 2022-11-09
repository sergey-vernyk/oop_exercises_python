from unittest import TestCase, main, skip
from git_repo.oop_exercises_python import Sea_Battle_Game


class TestShip(TestCase):
    def setUp(self) -> None:
        self.ship_hor = Sea_Battle_Game.Ship(4, x=1, y=2)
        self.ship_vert = Sea_Battle_Game.Ship(3, tp=2, x=2, y=5)

    def test_set_start_coords(self):
        self.ship_hor.set_start_coords(3, 6)
        self.assertEqual(self.ship_hor.get_start_coords(), (3, 6))

    def test_get_start_coords(self):
        self.assertEqual(self.ship_hor.get_start_coords(), (1, 2))

    def test_move(self):
        self.ship_hor.move(3)
        self.ship_vert.move(2)
        self.assertEqual(self.ship_hor.get_start_coords(), (4, 2))
        self.assertEqual(self.ship_vert.get_start_coords(), (2, 7))

    def test___get_place_and_around_coordinates(self):
        self.assertEqual(self.ship_hor._get_place_and_around_coordinates(self.ship_hor._tp, self.ship_hor),
                         ({(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (4, 3), (3, 3), (2, 3),
                           (1, 3), (0, 3), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}, {(1, 2), (2, 2), (3, 2), (4, 2)}))

    def test_is_collide(self):
        self.assertEqual(self.ship_hor.is_collide(self.ship_vert), False)

    def test_is_out_pole(self):
        self.assertEqual(self.ship_hor.is_out_pole(5), False)

    def test__check_index(self):
        self.assertEqual(self.ship_vert._check_index(2), True)
        self.assertEqual(self.ship_vert._check_index(3), False)

    def test_broken_ship_state(self):
        self.assertEqual(bool(self.ship_hor), True)
        self.ship_hor._cells = [2 for _ in range(self.ship_hor.length)]  # все палубы разрушены
        self.assertEqual(bool(self.ship_hor), False)

    def test_raise_type_error_set_coord_float(self):
        with self.assertRaises(TypeError) as te:
            self.ship_hor.__setattr__('_x', 2.5)

        self.assertEqual('Координаты и длина должны быть целыми положительными числами', te.exception.args[0])

    def test_raise_type_error_set_coord_negative(self):
        with self.assertRaises(TypeError) as te:
            self.ship_hor.__setattr__('_x', -2)

        self.assertEqual('Координаты и длина должны быть целыми положительными числами', te.exception.args[0])

    def test_raise_value_error_set_orientation(self):
        with self.assertRaises(ValueError) as ve:
            self.ship_hor.__setattr__('_tp', 3)

        self.assertEqual('Значение ориентации должно быть 1 или 2', ve.exception.args[0])


class TestGamePole(TestCase):

    def setUp(self) -> None:
        self.field = Sea_Battle_Game.GamePole(10)

        self.ship1 = Sea_Battle_Game.Ship(4, 1, 1, 2)
        self.ship2 = Sea_Battle_Game.Ship(3, 2, 6, 4)
        self.ship3 = Sea_Battle_Game.Ship(3, 1, 5, 9)
        self.ship4 = Sea_Battle_Game.Ship(2, 1, 2, 0)
        self.ship5 = Sea_Battle_Game.Ship(2, 1, 7, 1)
        self.ship6 = Sea_Battle_Game.Ship(2, 1, 2, 7)
        self.ship7 = Sea_Battle_Game.Ship(1, 2, 1, 9)
        self.ship8 = Sea_Battle_Game.Ship(1, 1, 1, 4)
        self.ship9 = Sea_Battle_Game.Ship(1, 2, 8, 7)
        self.ship10 = Sea_Battle_Game.Ship(1, 2, 9, 3)

        self.field._ships = [self.ship1, self.ship2, self.ship3,
                             self.ship4, self.ship5, self.ship6,
                             self.ship7, self.ship8,
                             self.ship9, self.ship10]

        for ship in self.field._ships:
            x, y, tp, length = ship.x, ship.y, ship.tp, ship.length
            if ship.tp == ship.HORIZONTAL:
                k = 0
                for j in range(x, x + length):
                    self.field._field[y][j] = ship[k]  # установка корабля на поле с k-палубами
                    k += 1
            elif ship.tp == ship.VERTICAL:
                k = 0
                for i in range(y, y + length):
                    self.field._field[i][x] = ship[k]
                    k += 1

    def test__check_ships_around_no_ships(self):
        result = self.field._check_ships_around(2, (4, 4), 2)  # кораблей нет вокруг
        self.assertEqual(result, 0)

    def test__check_ships_around_one_ship(self):
        result = self.field._check_ships_around(2, (4, 5), 1)  # есть один корабль
        self.assertEqual(result, 3)

    def test_get_ships(self):
        result = self.field.get_ships()
        self.assertListEqual(result, [self.ship1, self.ship2, self.ship3, self.ship4, self.ship5, self.ship6,
                                      self.ship7, self.ship8, self.ship9, self.ship10])

    def test_update_game_field(self):
        new_position = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                        [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]

        self.ship1.set_start_coords(0, 2)
        self.ship2.set_start_coords(6, 5)
        self.ship3.set_start_coords(6, 9)
        self.ship4.set_start_coords(1, 0)
        self.ship5.set_start_coords(6, 1)
        self.ship6.set_start_coords(3, 7)
        self.ship7.set_start_coords(1, 8)
        self.ship8.set_start_coords(2, 4)
        self.ship9.set_start_coords(8, 6)
        self.ship10.set_start_coords(9, 4)

        self.field.update_game_field()

        self.assertEqual(self.field._field, new_position)

    def test_get_pole(self):
        self.assertEqual(self.field.get_pole(), ((0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
                                                 (0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                                                 (0, 1, 1, 1, 1, 0, 0, 0, 0, 0),
                                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                                                 (0, 1, 0, 0, 0, 0, 1, 0, 0, 0),
                                                 (0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
                                                 (0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
                                                 (0, 0, 1, 1, 0, 0, 0, 0, 1, 0),
                                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                                 (0, 1, 0, 0, 0, 1, 1, 1, 0, 0)))


class TestSeaBattle(TestCase):

    def setUp(self):
        self.battle = Sea_Battle_Game.SeaBattle(10)

        self.ship1 = Sea_Battle_Game.Ship(4, 1, 1, 2)
        self.ship2 = Sea_Battle_Game.Ship(3, 2, 6, 4)
        self.ship3 = Sea_Battle_Game.Ship(3, 1, 5, 9)
        self.ship4 = Sea_Battle_Game.Ship(2, 1, 2, 0)
        self.ship5 = Sea_Battle_Game.Ship(2, 1, 7, 1)
        self.ship6 = Sea_Battle_Game.Ship(2, 1, 2, 7)
        self.ship7 = Sea_Battle_Game.Ship(1, 2, 1, 9)
        self.ship8 = Sea_Battle_Game.Ship(1, 1, 1, 4)
        self.ship9 = Sea_Battle_Game.Ship(1, 2, 8, 7)
        self.ship10 = Sea_Battle_Game.Ship(1, 2, 9, 3)

        self.battle.human._ships = [self.ship1, self.ship2, self.ship3, self.ship4, self.ship5,
                                    self.ship6, self.ship7, self.ship8, self.ship9, self.ship10]

        self.battle._human_ships_coord = self.battle.get_all_ships_parts_coord(self.battle.human)

    def test_get_all_ships_parts_coord(self):
        result = self.battle.get_all_ships_parts_coord(self.battle.human)
        self.assertDictEqual(result, {self.ship1: [(1, 2), (2, 2), (3, 2), (4, 2)],
                                      self.ship2: [(6, 4), (6, 5), (6, 6)],
                                      self.ship3: [(5, 9), (6, 9), (7, 9)],
                                      self.ship4: [(2, 0), (3, 0)],
                                      self.ship5: [(7, 1), (8, 1)],
                                      self.ship6: [(2, 7), (3, 7)],
                                      self.ship7: [(1, 9)],
                                      self.ship8: [(1, 4)],
                                      self.ship9: [(8, 7)],
                                      self.ship10: [(9, 3)]})

    def test_recognize_shell_place_not_none(self):
        result = self.battle.recognize_shell_place((4, 2), self.battle.computer)
        self.assertIsNotNone(result)

    def test_recognize_shell_place_none(self):
        result = self.battle.recognize_shell_place((4, 5), self.battle.computer)
        self.assertIsNone(result)

    def test__marked_broken_ship_part(self):
        self.battle._marked_broken_ship_part(self.battle.computer, self.ship1, (2, 2))
        self.assertEqual(self.battle.computer.count_dead_ships, 0)
        self.assertEqual(self.ship1.is_move, False)
        self.assertEqual(self.ship1._cells[1], 2)

    def test_count_dead_ships(self):
        for i in range(1, len(self.ship1._cells) + 1):
            self.battle._marked_broken_ship_part(self.battle.computer, self.ship1, (i, 2))

        self.assertEqual(self.battle.computer.count_dead_ships, 1)


if __name__ == '__main__':
    main()
