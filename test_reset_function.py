import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_new_game_reset(self):
        """测试新游戏重置"""
        # 设置游戏状态
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.active_quests = ["q1", "q2"]
        self.ui.radiation_sickness_stage = 2
        self.ui.moral_choices = ["save1", "steal2"]
        
        # 执行重置
        self.ui.reset_game()
        
        # 验证重置结果
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertEqual(self.ui.radiation_sickness_stage, 0)
        self.assertEqual(len(self.ui.moral_choices), 0)

    def test_quest_reset(self):
        """测试任务进度重置"""
        self.ui.active_quests = ["find1", "repair2"]
        self.ui.completed_quests = ["help3"]
        
        self.ui.reset_quests()
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertEqual(len(self.ui.completed_quests), 0)

    def test_environment_reset(self):
        """测试环境状态重置"""
        self.ui.weather_effects = ["rain"]
        self.ui.temperature_effects = ["cold"]
        
        self.ui.reset_environment()
        self.assertEqual(len(self.ui.weather_effects), 0)
        self.assertEqual(len(self.ui.temperature_effects), 0)

if __name__ == '__main__':
    unittest.main()