import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestUIRendering(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        
        # 設置模擬對象
        self.mock_game_state = MagicMock()
        self.mock_player = MagicMock()
        self.mock_inventory = MagicMock()
        
        self.mock_game_state.player_stats = {
            "hp": 80,
            "max_hp": 100,
            "level": 2,
            "exp": 50
        }
        self.mock_player.get_character_name.return_value = "測試角色"
        self.mock_player.get_character_stats.return_value = {"speed": 8}
        
        self.ui.set_game_state_reference(self.mock_game_state)
        self.ui.set_player_reference(self.mock_player)
        self.ui.set_inventory_reference(self.mock_inventory)

    @patch('pygame.draw.rect')
    @patch('font_manager.render_text')
    def test_hud_rendering(self, mock_render_text, mock_draw_rect):
        """測試HUD渲染"""
        self.ui.render_hud(self.mock_game_state, self.mock_player)
        
        # 驗證基本渲染函數被調用
        self.assertTrue(mock_draw_rect.called)
        self.assertTrue(mock_render_text.called)
        
        # 驗證角色信息顯示
        self.mock_player.get_character_name.assert_called()
        self.mock_player.get_character_stats.assert_called()

    @patch('pygame.draw.rect')
    @patch('font_manager.render_text')
    def test_inventory_rendering(self, mock_render_text, mock_draw_rect):
        """測試背包渲染"""
        # 設置背包物品
        self.mock_inventory.get_items.return_value = [
            {"name": "醫療包", "quantity": 2},
            {"name": "罐頭", "quantity": 5}
        ]
        
        self.ui.show_inventory = True
        self.ui.render(self.mock_game_state, self.mock_player, self.mock_inventory)
        
        # 驗證渲染函數被調用
        self.assertTrue(mock_draw_rect.called)
        self.assertTrue(mock_render_text.called)
        self.mock_inventory.get_items.assert_called()

    @patch('pygame.draw.rect')
    @patch('font_manager.render_text')
    def test_map_rendering(self, mock_render_text, mock_draw_rect):
        """測試地圖渲染"""
        self.ui.show_map = True
        self.ui.render(self.mock_game_state, self.mock_player, self.mock_inventory)
        
        # 驗證渲染函數被調用
        self.assertTrue(mock_draw_rect.called)
        self.assertTrue(mock_render_text.called)

    @patch('pygame.Surface')
    def test_game_over_rendering(self, mock_surface):
        """測試遊戲結束畫面渲染"""
        self.ui.game_over = True
        self.ui.render(self.mock_game_state, self.mock_player, self.mock_inventory)
        
        # 驗證Surface被創建用於覆蓋層
        mock_surface.assert_called()

if __name__ == '__main__':
    unittest.main()
