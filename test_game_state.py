import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_radiation_effect(self):
        """測試輻射區狀態影響"""
        self.mock_game_state.in_radiation_zone = True
        self.ui.render_hud(self.mock_game_state, None)
        self.assertIn("輻射", self.ui.current_message)

if __name__ == '__main__':
    unittest.main()