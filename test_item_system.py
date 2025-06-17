import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_keycard_usage(self):
        """測試鑰匙卡使用場景"""
        # 設置咖啡廳商店數據
        shop_data = {
            "type": "shop",
            "id": "L",
            "name": "咖啡廳"
        }
        
        # 無鑰匙卡時的對話選項
        self.ui.has_keycard = False
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "仔細搜查")
        
        # 有鑰匙卡時的對話選項
        self.ui.has_keycard = True
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "深入搜查")

    def test_antidote_usage(self):
        """測試解藥使用場景"""
        # 設置最後研究者NPC數據
        npc_data = {
            "type": "npc",
            "id": "npc4",
            "name": "最後的研究者"
        }
        
        # 無解藥狀態
        self.ui.has_antidote = False
        self.ui.start_dialogue(npc_data)
        self.assertIn("解藥就在這裡", self.ui.dialogue_text)
        
        # 有解藥狀態
        self.ui.has_antidote = True
        self.ui.start_dialogue(npc_data)
        self.assertIn("你已經有解藥了", self.ui.dialogue_text)

    def test_medical_item_consumption(self):
        """測試醫療物品消耗"""
        # 模擬背包中有醫療物品
        self.mock_inventory.get_items.return_value = [
            {"name": "醫療包", "quantity": 3},
            {"name": "繃帶", "quantity": 5}
        ]
        
        # 測試檢查醫療物品
        has_medical = self.ui.check_has_medical_item(self.mock_inventory)
        self.assertTrue(has_medical)
        
        # 測試消耗醫療物品
        self.mock_inventory.remove_item.return_value = True
        result = self.ui.consume_medical_item(self.mock_inventory)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
