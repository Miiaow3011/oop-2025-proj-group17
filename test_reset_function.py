import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_game_reset(self):
        """測試遊戲重置功能"""
        # 設置各種狀態為True
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.game_over = True
        self.ui.dialogue_active = True
        self.ui.show_inventory = True
        self.ui.show_map = True
        self.ui.message_display_time = 100
        self.ui.current_message = "測試訊息"
        
        # 調用重置方法
        self.ui.reset_game()
        
        # 驗證所有狀態已重置
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertFalse(self.ui.game_over)
        self.assertFalse(self.ui.dialogue_active)
        self.assertFalse(self.ui.show_inventory)
        self.assertFalse(self.ui.show_map)
        self.assertEqual(self.ui.message_display_time, 0)
        self.assertEqual(self.ui.current_message, "")

    def test_dialogue_reset(self):
        """測試對話重置功能"""
        # 設置對話狀態
        self.ui.dialogue_active = True
        self.ui.dialogue_data = {"type": "shop", "id": "A"}
        self.ui.dialogue_text = "測試對話"
        self.ui.dialogue_options = ["選項1", "選項2"]
        self.ui.selected_option = 1
        
        # 調用結束對話方法
        self.ui.end_dialogue()
        
        # 驗證對話狀態已重置
        self.assertFalse(self.ui.dialogue_active)
        self.assertIsNone(self.ui.dialogue_data)
        self.assertEqual(self.ui.dialogue_text, "")
        self.assertEqual(self.ui.dialogue_options, [])
        self.assertEqual(self.ui.selected_option, 0)

if __name__ == '__main__':
    unittest.main()
