import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_durability(self):
        """测试武器耐久度系统"""
        self.mock_inventory.get_items.return_value = [
            {"name": "手枪", "durability": 30},
            {"name": "维修套件", "quantity": 1}
        ]
        
        # 测试可维修状态
        self.assertTrue(self.ui.can_repair("手枪"))
        
        # 测试耐久度满的情况
        self.mock_inventory.get_items.return_value[0]["durability"] = 100
        self.assertFalse(self.ui.can_repair("手枪"))

    def test_medicine_quality(self):
        """测试药品品质系统"""
        self.mock_inventory.get_items.return_value = [
            {"name": "抗生素", "quality": 80},
            {"name": "过期止痛药", "quality": 10}
        ]
        
        # 测试有效药品
        self.assertTrue(self.ui.is_effective("抗生素"))
        
        # 测试失效药品
        self.assertFalse(self.ui.is_effective("过期止痛药"))

    def test_crafting_system(self):
        """测试物品合成系统"""
        recipe = {
            "inputs": [("金属", 2), ("零件", 1)],
            "output": ("陷阱", 1)
        }
        
        self.mock_inventory.get_items.return_value = [
            {"name": "金属", "quantity": 3},
            {"name": "零件", "quantity": 1}
        ]
        
        success = self.ui.craft_item(recipe)
        self.assertTrue(success)
        self.mock_inventory.remove_item.assert_any_call("金属", 2)
        self.mock_inventory.remove_item.assert_any_call("零件", 1)
        self.mock_inventory.add_item.assert_called_with("陷阱", 1)

if __name__ == '__main__':
    unittest.main()