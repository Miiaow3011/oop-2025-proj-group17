import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_weapon_store_rank_access(self):
        """测试武器商店的军衔准入系统"""
        shop_data = {
            "type": "shop",
            "id": "ARMORY",
            "name": "军械库",
            "required_rank": 5
        }
        
        # 军衔不足
        self.mock_game_state.player_stats = {"rank": 3}
        self.ui.start_dialogue(shop_data)
        self.assertIn("需要上尉军衔", self.ui.dialogue_text)
        
        # 军衔足够
        self.mock_game_state.player_stats = {"rank": 6}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买突击步枪")

    def test_pharmacy_medicine_restock(self):
        """测试药局的药品补货机制"""
        shop_data = {
            "type": "shop",
            "id": "PHARM",
            "name": "应急药局",
            "restock_timer": 24
        }
        
        # 首次访问
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买抗生素")
        
        # 模拟立即再次访问
        self.ui.start_dialogue(shop_data)
        self.assertIn("补货中", self.ui.dialogue_text)

    def test_black_market_currency(self):
        """测试黑市的特殊货币系统"""
        shop_data = {
            "type": "shop",
            "id": "BLACK",
            "name": "黑市",
            "currency": "信用点"
        }
        
        self.mock_game_state.player_stats = {"credits": 150}
        self.ui.start_dialogue(shop_data)
        self.assertIn("当前信用点:150", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()