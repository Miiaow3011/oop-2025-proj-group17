import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestDialogueSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        
        # 設置模擬參考
        self.mock_game_state = MagicMock()
        self.mock_player = MagicMock()
        self.mock_inventory = MagicMock()
        
        self.ui.set_game_state_reference(self.mock_game_state)
        self.ui.set_player_reference(self.mock_player)
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_shop_dialogue_setup(self):
        """測試商店對話設置"""
        shop_data = {
            "type": "shop",
            "id": "A",
            "name": "7-11"
        }
        
        self.ui.start_dialogue(shop_data)
        
        self.assertTrue(self.ui.dialogue_active)
        self.assertEqual(self.ui.dialogue_data, shop_data)
        self.assertEqual(self.ui.dialogue_step, 0)
        self.assertIn("歡迎來到7-11", self.ui.dialogue_text)
        self.assertEqual(len(self.ui.dialogue_options), 3)

    def test_npc_dialogue_setup(self):
        """測試NPC對話設置"""
        npc_data = {
            "type": "npc",
            "id": "npc1",
            "name": "驚慌學生"
        }
        
        self.ui.start_dialogue(npc_data)
        
        self.assertTrue(self.ui.dialogue_active)
        self.assertEqual(self.ui.dialogue_data, npc_data)
        self.assertEqual(self.ui.dialogue_step, 0)
        self.assertIn("救命！外面到處都是殭屍", self.ui.dialogue_text)
        self.assertEqual(len(self.ui.dialogue_options), 3)

    def test_dialogue_selection(self):
        """測試對話選項選擇"""
        # 設置商店對話
        shop_data = {"type": "shop", "id": "A", "name": "7-11"}
        self.ui.start_dialogue(shop_data)
        
        # 選擇第一個選項
        self.ui.select_dialogue_option(0)
        self.assertEqual(self.ui.selected_option, 0)
        
        # 驗證遊戲狀態更新
        self.mock_game_state.player_stats.__getitem__.return_value = 80  # 當前HP
        self.mock_game_state.player_stats.__setitem__.assert_called()
        self.mock_game_state.add_exp.assert_called()

    def test_dialogue_end(self):
        """測試結束對話"""
        shop_data = {"type": "shop", "id": "A", "name": "7-11"}
        self.ui.start_dialogue(shop_data)
        
        self.ui.end_dialogue()
        
        self.assertFalse(self.ui.dialogue_active)
        self.assertIsNone(self.ui.dialogue_data)
        self.assertEqual(self.ui.dialogue_text, "")
        self.assertEqual(self.ui.dialogue_options, [])

    @patch('pygame.draw.rect')
    @patch('font_manager.render_text')
    def test_dialogue_rendering(self, mock_render_text, mock_draw_rect):
        """測試對話框渲染"""
        shop_data = {"type": "shop", "id": "A", "name": "7-11"}
        self.ui.start_dialogue(shop_data)
        
        self.ui.render_dialogue()
        
        # 驗證渲染函數被調用
        self.assertTrue(mock_draw_rect.called)
        self.assertTrue(mock_render_text.called)

if __name__ == '__main__':
    unittest.main()
