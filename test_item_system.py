import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_quest_item_usage(self):
        """測試任務關鍵道具使用"""
        self.mock_inventory.get_items.return_value = [
            {"name": "實驗室磁卡", "quantity": 1, "quest_item": True}
        ]
        self.ui.has_keycard = False
        self.ui.check_quest_items()
        self.assertTrue(self.ui.has_keycard)

if __name__ == '__main__':
    unittest.main()