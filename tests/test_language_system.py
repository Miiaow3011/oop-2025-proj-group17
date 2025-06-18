import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestLanguageSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_language_switch(self):
        """測試語言切換功能"""
        # 初始為中文
        shop_data = {
            "type": "shop",
            "id": "A",
            "name": "7-11",
            "text": {
                "zh": "歡迎光臨",
                "en": "Welcome"
            }
        }
        
        self.ui.current_language = "zh"
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_text, "歡迎光臨")
        
        # 切換為英文
        self.ui.current_language = "en"
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_text, "Welcome")

    def test_fallback_language(self):
        """測試語言回退機制"""
        npc_data = {
            "type": "npc",
            "id": "test",
            "name": "測試NPC",
            "text": {
                "zh": "中文文本",
                "ja": "日本語テキスト"
            }
        }
        
        # 請求不存在的語言，應回退到中文
        self.ui.current_language = "fr"
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "中文文本")

    @patch('pygame.draw.rect')
    def test_language_menu(self, mock_draw):
        """測試語言選單渲染"""
        self.ui.show_language_menu = True
        self.ui.render(self.mock_game_state, None, None)
        
        # 驗證語言選項繪製
        self.assertGreaterEqual(mock_draw.call_count, 3)

if __name__ == '__main__':
    unittest.main()
