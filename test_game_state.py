import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_radiation_sickness(self):
        """测试辐射病阶段发展"""
        self.mock_game_state.player_stats = {
            "radiation": 75,
            "max_radiation": 100
        }
        
        self.ui.check_radiation_effects()
        self.assertEqual(self.ui.radiation_sickness_stage, 2)
        self.assertIn("中度辐射症状", self.ui.current_message)

    def test_temperature_effects(self):
        """测试极端温度影响"""
        test_cases = [
            (-20, "冻伤", 15),  # 极寒
            (45, "中暑", 10)    # 极热
        ]
        
        for temp, effect, damage in test_cases:
            with self.subTest(temp=temp):
                self.mock_game_state.environment = {"temperature": temp}
                self.ui.check_environment_effects()
                self.assertIn(effect, self.ui.current_message)
                self.mock_game_state.damage_player.assert_called_with(damage)

    def test_moral_system(self):
        """测试道德选择影响"""
        self.mock_game_state.player_stats = {"morality": 50}
        
        # 道德选择
        self.ui.make_moral_choice("拯救平民", 20)
        self.assertEqual(self.mock_game_state.player_stats["morality"], 70)
        
        # 不道德选择
        self.ui.make_moral_choice("抢夺物资", -30)
        self.assertEqual(self.mock_game_state.player_stats["morality"], 40)

if __name__ == '__main__':
    unittest.main()