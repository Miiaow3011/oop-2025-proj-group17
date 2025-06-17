import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_infection_progression(self):
        """测试感染状态系统"""
        self.mock_game_state.player_stats = {
            "infection_level": 60,  # 超过50会有症状
            "max_infection": 100
        }
        
        self.ui.check_infection_effects()
        self.assertTrue(self.ui.showing_symptoms)
        self.assertIn("感染症状", self.ui.current_message)

    def test_temperature_effects(self):
        """测试极端温度影响"""
        self.mock_game_state.environment = {
            "temperature": -15,  # 极寒状态
            "weather": "blizzard"
        }
        
        self.ui.check_environment_effects()
        self.mock_game_state.damage_player.assert_called_with(10)
        self.assertIn("极寒", self.ui.current_message)

if __name__ == '__main__':
    unittest.main()