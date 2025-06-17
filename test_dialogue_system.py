import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_military_supply_store(self):
        """測試軍用品商店特殊選項"""
        shop_data = {
            "type": "shop",
            "id": "MS",
            "name": "軍用品商店",
            "requires_rank": 3
        }
        
        # 測試軍階不足
        self.mock_game_state.player_stats = {"rank": 2}
        self.ui.start_dialogue(shop_data)
        self.assertIn("權限不足", self.ui.dialogue_text)
        
        # 測試軍階足夠
        self.mock_game_state.player_stats = {"rank": 4}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "購買武器裝備")

    def test_underground_clinic(self):
        """測試地下診所治療功能"""
        shop_data = {
            "type": "shop",
            "id": "UC",
            "name": "地下診所",
            "can_heal": True,
            "cost": 50
        }
        
        self.mock_game_state.player_stats = {"hp": 30, "max_hp": 100, "money": 60}
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 選擇治療
        
        # 驗證治療效果和扣款
        self.mock_game_state.player_stats.__setitem__.assert_any_call("hp", 100)
        self.mock_game_state.player_stats.__setitem__.assert_any_call("money", 10)

if __name__ == '__main__':
    unittest.main()