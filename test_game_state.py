import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_radiation_poisoning(self):
        """测试辐射中毒阶段系统"""
        test_cases = [
            (30, 1, "轻微症状"),
            (70, 2, "中度症状"),
            (100, 3, "严重症状")
        ]
        
        for level, stage, message in test_cases:
            with self.subTest(level=level):
                self.mock_game_state.player_stats = {"radiation": level}
                self.ui.check_radiation_effects()
                self.assertEqual(self.ui.radiation_stage, stage)
                self.assertIn(message, self.ui.current_message)

    def test_temperature_effects(self):
        """测试极端温度影响系统"""
        self.mock_game_state.environment = {"temperature": -25}
        self.ui.check_environment_effects()
        self.mock_game_state.damage_player.assert_called_with(15)
        self.assertIn("冻伤", self.ui.current_message)

    def test_moral_system(self):
        """测试道德选择影响"""
        choices = [
            ("拯救平民", 20),
            ("掠夺物资", -30),
            ("分享食物", 10)
        ]
        
        for action, points in choices:
            with self.subTest(action=action):
                self.mock_game_state.player_stats = {"morality": 50}
                self.ui.record_moral_choice(action, points)
                self.assertEqual(self.mock_game_state.player_stats["morality"], 50 + points)

if __name__ == '__main__':
    unittest.main()