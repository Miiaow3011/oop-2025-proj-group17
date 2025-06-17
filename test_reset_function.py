import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_full_reset(self):
        """測試完整遊戲重置"""
        # 設置各種遊戲狀態
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.active_quests = ["q1", "q2"]
        self.ui.hallucination_active = True
        self.ui.weather_effects = ["rain"]
        
        # 執行重置
        self.ui.reset_game()
        
        # 驗證所有狀態重置
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertFalse(self.ui.hallucination_active)
        self.assertEqual(len(self.ui.weather_effects), 0)

if __name__ == '__main__':
    unittest.main()