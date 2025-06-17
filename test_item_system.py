import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_radio_assembly(self):
        """測試無線電組裝系統"""
        required_parts = ["電路板", "電池", "天線"]
        self.mock_inventory.get_items.return_value = [
            {"name": "電路板", "quantity": 1},
            {"name": "電池", "quantity": 3}
        ]
        
        # 測試缺少零件
        self.assertFalse(self.ui.check_assembly(required_parts))
        
        # 測試零件齊全
        self.mock_inventory.get_items.return_value.append({"name": "天線", "quantity": 1})
        self.assertTrue(self.ui.check_assembly(required_parts))

    def test_medicine_combine(self):
        """測試藥物合成系統"""
        self.mock_inventory.get_items.return_value = [
            {"name": "草藥", "quantity": 3},
            {"name": "酒精", "quantity": 1}
        ]
        
        result = self.ui.combine_items(["草藥", "酒精"], "急救包")
        self.assertTrue(result)
        self.mock_inventory.remove_item.assert_any_call("草藥", 2)
        self.mock_inventory.remove_item.assert_any_call("酒精", 1)
        self.mock_inventory.add_item.assert_called_with("急救包", 1)

if __name__ == '__main__':
    unittest.main()