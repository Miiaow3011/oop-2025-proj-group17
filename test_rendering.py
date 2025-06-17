import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestUIRendering(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.mock_player = MagicMock()
        self.mock_inventory = MagicMock()
        
        # 設置模擬數據
        self.mock_game_state.player_stats = {
            "hp": 75,
            "max_hp": 100,
            "level": 2,
            "exp": 50
        }
        self.mock_player.get_character_name.return_value = "測試角色"
        self.mock_player.get_character_stats.return_value = {"speed": 8}

    @patch('pygame.draw.rect')
    @patch('font_manager.render_text')
    def test_hud_rendering(self, mock_render, mock_draw):
        """測試HUD渲染"""
        self.ui.render_hud(self.mock_game_state, self.mock_player)
        
        # 驗證血量條繪製
        mock_draw.assert_called()
        
        # 驗證文字渲染
        mock_render.assert_any_call("HP: 75/100", 18, (255, 255, 255))
        mock_render.assert_any_call("Lv.2", 18, (255, 255, 255))
        mock_render.assert_any_call("測試角色", 16, (255, 150, 255))

    @patch('pygame.draw.rect')
    def test_dialogue_rendering(self, mock_draw):
        """測試對話框渲染"""
        # 設置對話數據
        self.ui.dialogue_active = True
        self.ui.dialogue_text = "測試對話內容"
        self.ui.dialogue_options = ["選項1", "選項2"]
        
        self.ui.render_dialogue()
        
        # 驗證對話框繪製
        mock_draw.assert_called()
        
        # 驗證對話框位置
        args, kwargs = mock_draw.call_args
        self.assertEqual(args[0].y, self.ui.dialogue_box_y)

    @patch('pygame.Surface')
    def test_game_over_rendering(self, mock_surface):
        """測試遊戲結束畫面渲染"""
        self.ui.game_over = True
        self.ui.render(self.mock_game_state, self.mock_player, self.mock_inventory)
        
        # 驗證創建了覆蓋層
        mock_surface.assert_called_with((self.ui.screen_width, self.ui.screen_height))

if __name__ == '__main__':
    unittest.main()