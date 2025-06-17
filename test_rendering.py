import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestUIRendering(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    @patch('pygame.draw.rect')
    def test_quest_marker_rendering(self, mock_draw):
        """測試任務標記渲染"""
        self.ui.active_quests = ["尋找醫療包"]
        self.ui.render_quest_markers()
        self.assertTrue(mock_draw.called)

if __name__ == '__main__':
    unittest.main()