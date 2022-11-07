from unittest import TestCase, main
from git_repo.oop_exercises_python import Sea_Battle_Game


class TestShip(TestCase):
    def setUp(self) -> None:
        self.ship_hor = Sea_Battle_Game.Ship(4, x=1, y=2)
        self.ship_vert = Sea_Battle_Game.Ship(3, tp=2, x=2, y=5)

    """Positive Test Cases"""

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

    def test_raise_type_error_set_coord(self):
        with self.assertRaises(TypeError) as te:
            self.ship_hor.__setattr__('_x', 2.5)

        self.assertEqual('Координаты и длина должны быть целыми числами', te.exception.args[0])

    def test_raise_value_error_set_orientation(self):
        with self.assertRaises(ValueError) as ve:
            self.ship_hor.__setattr__('_tp', 3)

        self.assertEqual('Значение ориентации должно быть 1 или 2', ve.exception.args[0])

    """Negative Test Cases"""


if __name__ == '__main__':
    main()
