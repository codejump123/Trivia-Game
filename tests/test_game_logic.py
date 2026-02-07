import unittest

from server.game_logic import apply_answer, update_stats, validate_wager


class GameLogicTests(unittest.TestCase):
    def test_validate_wager(self):
        ok, _ = validate_wager(100, 10)
        self.assertTrue(ok)

        ok, _ = validate_wager(100, -1)
        self.assertFalse(ok)

        ok, _ = validate_wager(100, 0)
        self.assertFalse(ok)

        ok, _ = validate_wager(50, 60)
        self.assertFalse(ok)

        ok, _ = validate_wager(50, "10")
        self.assertFalse(ok)

    def test_apply_answer(self):
        points, delta = apply_answer(100, 10, True)
        self.assertEqual(points, 110)
        self.assertEqual(delta, 10)

        points, delta = apply_answer(100, 20, False)
        self.assertEqual(points, 80)
        self.assertEqual(delta, -20)

        points, delta = apply_answer(5, 10, False)
        self.assertEqual(points, 0)
        self.assertEqual(delta, -10)

    def test_update_stats(self):
        stats = {
            "points": 100,
            "games_played": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
        }
        update_stats(stats, True)
        self.assertEqual(stats["games_played"], 1)
        self.assertEqual(stats["correct_answers"], 1)
        self.assertEqual(stats["incorrect_answers"], 0)


if __name__ == "__main__":
    unittest.main()
