import unittest
from unittest.mock import MagicMock
from ui import UI

class TestResetFunction(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_quest_reset(self):
        """測試任務進度重置"""
        self.ui.active_quests = ["Q1", "Q2"]
        self.ui.completed_quests = ["Q3"]
        self.ui.reset_game()
        self.assertEqual(len(self.ui.active_quests), 0)
        self.assertEqual(len(self.ui.completed_quests), 0)

if __name__ == '__main__':
    unittest.main()
