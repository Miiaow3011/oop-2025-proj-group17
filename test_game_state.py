import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        
        # 設置模擬遊戲狀態
        self.mock_game_state = MagicMock()
        self.mock_game_state.player_stats = {
            "hp": 80,
            "max_hp": 100,
            "level": 2,
            "exp": 50
        }
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_victory_condition(self):
        """測試勝利條件檢查"""
        # 設置勝利條件
        self.ui.has_antidote = True
        self.mock_game_state.player_stats["level"] = 3
        self.mock_game_state.player_stats["hp"] = 80
        
        # 檢查勝利條件
        self.ui.check_victory_condition(self.mock_game_state)
        self.assertTrue(self.ui.game_completed)

    def test_game_over_condition(self):
        """測試遊戲結束條件檢查"""
        # 設置HP為0
        self.mock_game_state.player_stats["hp"] = 0
        
        # 檢查遊戲結束
        self.ui.check_game_over(self.mock_game_state)
        self.assertTrue(self.ui.game_over)

    def test_message_display(self):
        """測試訊息顯示功能"""
        test_message = "測試訊息"
        self.ui.show_message(test_message)
        
        self.assertEqual(self.ui.current_message, test_message)
        self.assertEqual(self.ui.message_display_time, 180)
        
        # 測試訊息更新
        self.ui.update_messages()
        self.assertEqual(self.ui.message_display_time, 179)

    def test_get_game_state(self):
        """測試獲取遊戲狀態"""
        # 有設置參考的情況
        result = self.ui.get_game_state()
        self.assertEqual(result, self.mock_game_state)
        
        # 無參考的情況（使用模擬狀態）
        self.ui.game_state_reference = None
        result = self.ui.get_game_state()
        self.assertEqual(result.player_stats["hp"], 80)  # 來自模擬狀態

if __name__ == '__main__':
    unittest.main()
