import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_repair_kit(self):
        """测试武器维修套件的使用条件"""
        self.mock_inventory.get_items.return_value = [
            {"name": "维修套件", "quantity": 1, "durability": 100},
            {"name": "AK-47", "durability": 30}
        ]
        
        # 测试可以维修
        self.assertTrue(self.ui.can_repair("AK-47"))
        
        # 测试耐久度已满
        self.mock_inventory.get_items.return_value[1]["durability"] = 100
        self.assertFalse(self.ui.can_repair("AK-47"))

    def test_medicine_expiration(self):
        """测试药品过期系统"""
        self.mock_inventory.get_items.return_value = [
            {"name": "抗生素", "expiry": 3},
            {"name": "止痛药", "expiry": 0}
        ]
        
        # 测试过期药品
        self.assertFalse(self.ui.is_usable("止痛药"))
        
        # 测试有效药品
        self.assertTrue(self.ui.is_usable("抗生素"))

    def test_radio_assembly(self):
        """测试无线电组装系统"""
        required_parts = ["电路板", "电池", "天线"]
        self.mock_inventory.get_items.return_value = [
            {"name": "电路板", "quantity": 2},
            {"name": "电池", "quantity": 1},
            {"name": "电线", "quantity": 3}
        ]
        
        # 缺少天线
        self.assertFalse(self.ui.check_assembly(required_parts))
        
        # 添加天线后
        self.mock_inventory.get_items.return_value.append({"name": "天线", "quantity": 1})
        self.assertTrue(self.ui.check_assembly(required_parts))

if __name__ == '__main__':
    unittest.main()