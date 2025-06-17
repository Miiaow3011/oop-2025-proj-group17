import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_hard_reset(self):
        """测试硬重置所有游戏系统"""
        # 设置各种状态
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.active_quests = ["q1", "q2"]
        self.ui.showing_symptoms = True
        self.ui.environment_effects = ["blizzard"]
        
        # 执行重置
        self.ui.hard_reset_game()
        
        # 验证所有状态重置
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertFalse(self.ui.showing_symptoms)
        self.assertEqual(len(self.ui.environment_effects), 0)

if __name__ == '__main__':
    unittest.main()