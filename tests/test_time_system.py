import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestTimeSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    @patch('pygame.draw.rect')
    def test_day_night_indicator(self, mock_draw):
        """測試日夜指示器渲染"""
        # 測試白天
        self.mock_game_state.is_night = False
        self.ui.render_time_indicator(10, 10)
        
        # 測試夜晚
        self.mock_game_state.is_night = True
        self.ui.render_time_indicator(10, 10)
        
        # 驗證顏色變化
        day_color = mock_draw.call_args_list[0][0][2]
        night_color = mock_draw.call_args_list[2][0][2]
        self.assertNotEqual(day_color, night_color)

    def test_time_sensitive_shops(self):
        """測試時間敏感的商店"""
        shop_data = {
            "type": "shop",
            "id": "NIGHT",
            "name": "黑市商人",
            "night_only": True
        }
        
        # 白天測試
        self.mock_game_state.is_night = False
        self.ui.start_dialogue(shop_data)
        self.assertIn("晚上再來", self.ui.dialogue_text)
        
        # 夜晚測試
        self.mock_game_state.is_night = True
        self.ui.start_dialogue(shop_data)
        self.assertIn("想買什麼", self.ui.dialogue_text)

    def test_emergency_event(self):
        """測試緊急事件觸發"""
        event_data = {
            "type": "event",
            "name": "殭屍來襲",
            "time_limit": 60
        }
        
        self.ui.start_dialogue(event_data)
        self.assertIn("殭屍來襲", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[0], "準備戰鬥")

if __name__ == '__main__':
    unittest.main()
