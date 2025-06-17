import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_military_depot_access(self):
        """测试军事仓库的权限等级系统"""
        shop_data = {
            "type": "shop",
            "id": "DEPOT",
            "name": "军事仓库",
            "access_level": 3,
            "inventory": ["突击步枪", "防弹衣"]
        }
        
        # 权限不足
        self.mock_game_state.player_stats = {"clearance": 2}
        self.ui.start_dialogue(shop_data)
        self.assertIn("需要3级权限", self.ui.dialogue_text)
        
        # 权限足够
        self.mock_game_state.player_stats = {"clearance": 3}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买突击步枪")

    def test_medical_clinic_restock(self):
        """测试医疗诊所的库存刷新机制"""
        shop_data = {
            "type": "shop",
            "id": "CLINIC",
            "name": "应急诊所",
            "restock_hours": 6,
            "stock": ["抗生素", "止痛药"]
        }
        
        # 首次访问
        self.ui.start_dialogue(shop_data)
        self.assertEqual(len(self.ui.dialogue_options), 2)
        
        # 模拟立即再次访问
        shop_data["last_restock"] = 0  # 未到补货时间
        self.ui.start_dialogue(shop_data)
        self.assertIn("库存不足", self.ui.dialogue_text)

    def test_trader_barter_ui(self):
        """测试商人的实物交易界面"""
        shop_data = {
            "type": "shop",
            "id": "TRADER",
            "name": "流浪商人",
            "barter": [("子弹", "抗生素", 30)]
        }
        
        self.mock_inventory = MagicMock()
        self.mock_inventory.get_items.return_value = [{"name": "子弹", "quantity": 50}]
        self.ui.set_inventory_reference(self.mock_inventory)
        
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "用30子弹换抗生素")

if __name__ == '__main__':
    unittest.main()