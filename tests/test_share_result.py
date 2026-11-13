import unittest

from connections_tui import GameState, Group, format_share_result, submit_selection


class ShareResultTest(unittest.TestCase):
    def setUp(self):
        self.state = GameState(
            date_str="2026-11-12",
            puzzle_id=1251,
            groups=[
                Group("Yellow", {"Y1", "Y2", "Y3", "Y4"}, difficulty=0),
                Group("Green", {"G1", "G2", "G3", "G4"}, difficulty=1),
                Group("Blue", {"B1", "B2", "B3", "B4"}, difficulty=2),
                Group("Purple", {"P1", "P2", "P3", "P4"}, difficulty=3),
            ],
            remaining_words=[
                "G1",
                "G2",
                "G3",
                "G4",
                "Y1",
                "Y2",
                "Y3",
                "Y4",
                "B1",
                "B2",
                "B3",
                "B4",
                "P1",
                "P2",
                "P3",
                "P4",
            ],
        )

    def guess(self, *words):
        self.state.selection_idx = {
            self.state.remaining_words.index(word) for word in words
        }
        return submit_selection(self.state)

    def submit(self, *words):
        matched, _ = self.guess(*words)
        self.assertTrue(matched)

    def test_formats_completed_game_in_guess_order(self):
        self.submit("G1", "G2", "G3", "G4")
        self.submit("Y1", "Y2", "Y3", "Y4")
        self.submit("B1", "B2", "B3", "B4")
        self.submit("P1", "P2", "P3", "P4")

        self.assertEqual(
            format_share_result(self.state),
            "Connections\n"
            "Puzzle #1251\n"
            "🟩🟩🟩🟩\n"
            "🟨🟨🟨🟨\n"
            "🟦🟦🟦🟦\n"
            "🟪🟪🟪🟪",
        )

    def test_includes_incorrect_guesses_in_board_order(self):
        matched, _ = self.guess("G1", "Y1", "Y2", "Y3")
        self.assertFalse(matched)
        self.submit("G1", "G2", "G3", "G4")
        self.submit("Y1", "Y2", "Y3", "Y4")
        self.submit("B1", "B2", "B3", "B4")
        self.submit("P1", "P2", "P3", "P4")

        self.assertEqual(
            format_share_result(self.state),
            "Connections\n"
            "Puzzle #1251\n"
            "🟩🟨🟨🟨\n"
            "🟩🟩🟩🟩\n"
            "🟨🟨🟨🟨\n"
            "🟦🟦🟦🟦\n"
            "🟪🟪🟪🟪",
        )

if __name__ == "__main__":
    unittest.main()
