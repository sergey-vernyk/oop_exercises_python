from unittest import TestCase, main
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


if __name__ == '__main__':
    main()
