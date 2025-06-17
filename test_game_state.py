import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_victory_conditions(self):
        """測試不同勝利條件組合"""
        test_cases = [
            # (has_keycard, has_antidote, level, hp, expected)
            (True, True, 3, 80, True),    # 滿足所有條件
            (True, False, 3, 80, False),  # 缺少解藥
            (True, True, 2, 80, False),    # 等級不足
            (True, True, 3, 30, False)     # HP不足
        ]
        
        for keycard, antidote, level, hp, expected in test_cases:
            with self.subTest(keycard=keycard, antidote=antidote, level=level, hp=hp):
                self.ui.has_keycard = keycard
                self.ui.has_antidote = antidote
                self.mock_game_state.player_stats = {
                    "hp": hp,
                    "max_hp": 100,
                    "level": level,
                    "exp": 100
                }
                self.ui.check_victory_condition(self.mock_game_state)
                self.assertEqual(self.ui.game_completed, expected)

    def test_game_over_conditions(self):
        """測試遊戲結束條件"""
        self.mock_game_state.player_stats = {"hp": 0, "max_hp": 100}
        self.ui.check_game_over(self.mock_game_state)
        self.assertTrue(self.ui.game_over)
        
        self.mock_game_state.player_stats = {"hp": 1, "max_hp": 100}
        self.ui.check_game_over(self.mock_game_state)
        self.assertFalse(self.ui.game_over)

    def test_exp_gain_scenarios(self):
        """測試不同場景的經驗值獲取"""
        # 設置初始狀態
        self.mock_game_state.player_stats = {
            "hp": 80,
            "max_hp": 100,
            "level": 1,
            "exp": 0
        }
        
        # 測試購買醫療用品
        shop_data = {"type": "shop", "id": "A"}
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 選擇"購買醫療用品"
        
        # 驗證經驗值增加
        self.mock_game_state.add_exp.assert_called_with(10)

if __name__ == '__main__':
    unittest.main()