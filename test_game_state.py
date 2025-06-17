import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_sanity_mechanic(self):
        """測試精神值系統影響"""
        self.mock_game_state.player_stats = {
            "sanity": 30,  # 低於50會產生幻覺
            "max_sanity": 100
        }
        
        self.ui.check_sanity_effects()
        self.assertTrue(self.ui.hallucination_active)
        self.assertIn("幻覺", self.ui.current_message)

    def test_weather_effects(self):
        """測試天氣系統影響"""
        self.mock_game_state.weather = "acid_rain"
        self.ui.render_weather_effects()
        self.assertIn("酸雨", self.ui.current_message)
        self.mock_game_state.damage_player.assert_called_with(5)

if __name__ == '__main__':
    unittest.main()