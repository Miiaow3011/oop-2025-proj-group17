import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_chapter_based_reset(self):
        """测试章节进度重置系统"""
        self.ui.completed_chapters = [1, 2]
        self.ui.current_chapter = 3
        self.ui.chapter_reset()
        
        self.assertEqual(len(self.ui.completed_chapters), 0)
        self.assertEqual(self.ui.current_chapter, 1)

    def test_permadeath_reset(self):
        """测试永久死亡模式重置"""
        self.ui.permadeath_mode = True
        self.ui.character_progression = {"level": 10}
        
        self.ui.hard_reset()
        self.assertEqual(self.ui.character_progression, {})

    def test_difficulty_scaling(self):
        """测试难度缩放重置"""
        difficulties = {
            "easy": {"enemy_health": 0.8},
            "hard": {"enemy_damage": 1.5}
        }
        
        for mode, scaling in difficulties.items():
            with self.subTest(mode=mode):
                self.ui.difficulty = mode
                self.ui.reset_difficulty()
                self.assertEqual(
                    self.ui.game_scaling,
                    scaling
                )

if __name__ == '__main__':
    unittest.main()