import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_new_game_plus(self):
        """测试新游戏+模式重置"""
        # 设置NG+状态
        self.ui.completed_game = True
        self.ui.ng_plus = True
        self.ui.carried_over_items = ["传奇武器", "研究数据"]
        
        # 执行NG+重置
        self.ui.reset_for_new_game_plus()
        
        # 验证保留内容
        self.assertIn("传奇武器", self.ui.carried_over_items)
        self.assertEqual(self.ui.difficulty, "hard")

    def test_hardcore_mode_reset(self):
        """测试硬核模式重置"""
        self.ui.hardcore_mode = True
        self.ui.player_deaths = 3
        
        self.ui.hard_reset()
        self.assertEqual(self.ui.player_deaths, 0)
        self.assertTrue(self.ui.permadeath)

    def test_sector_based_reset(self):
        """测试区域进度重置"""
        self.ui.completed_sectors = ["A", "B"]
        self.ui.current_sector = "C"
        
        self.ui.reset_sector_progress()
        self.assertEqual(len(self.ui.completed_sectors), 0)
        self.assertEqual(self.ui.current_sector, "A")

if __name__ == '__main__':
    unittest.main()