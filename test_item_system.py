import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_upgrade(self):
        """测试武器升级材料检查"""
        required_materials = {"金属零件": 3, "工具组": 1}
        self.mock_inventory.get_items.return_value = [
            {"name": "金属零件", "quantity": 5},
            {"name": "工具组", "quantity": 0}
        ]
        
        # 测试材料不足
        self.assertFalse(self.ui.check_upgrade_materials(required_materials))
        
        # 测试材料足够
        self.mock_inventory.get_items.return_value[1]["quantity"] = 2
        self.assertTrue(self.ui.check_upgrade_materials(required_materials))

    def test_medicine_crafting(self):
        """测试药物制作系统"""
        recipe = {
            "inputs": [("草药", 2), ("酒精", 1)],
            "output": ("消毒剂", 1)
        }
        
        self.mock_inventory.get_items.return_value = [
            {"name": "草药", "quantity": 3},
            {"name": "酒精", "quantity": 1}
        ]
        
        success = self.ui.craft_item(recipe)
        self.assertTrue(success)
        self.mock_inventory.remove_item.assert_any_call("草药", 2)
        self.mock_inventory.remove_item.assert_any_call("酒精", 1)
        self.mock_inventory.add_item.assert_called_with("消毒剂", 1)

if __name__ == '__main__':
    unittest.main()