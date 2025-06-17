import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_full_reset(self):
        """测试完整游戏状态重置"""
        # 设置各种游戏状态
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.active_quests = ["q1", "q2"]
        self.ui.radiation_stage = 2
        self.ui.moral_choices = ["save1", "steal2"]
        
        # 执行重置
        self.ui.full_reset()
        
        # 验证重置结果
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertEqual(self.ui.radiation_stage, 0)
        self.assertEqual(len(self.ui.moral_choices), 0)

    def test_quest_reset(self):
        """测试任务系统独立重置"""
        self.ui.active_quests = ["find1", "repair2"]
        self.ui.completed_quests = ["help3"]
        
        self.ui.reset_quests()
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertEqual(len(self.ui.completed_quests), 0)

    def test_inventory_reset(self):
        """测试背包系统独立重置"""
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)
        
        self.ui.reset_inventory()
        self.mock_inventory.clear.assert_called_once()

if __name__ == '__main__':
    unittest.main()