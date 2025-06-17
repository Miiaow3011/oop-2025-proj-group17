import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_hardware_store(self):
        """測試五金行特殊對話"""
        shop_data = {
            "type": "shop",
            "id": "HW",
            "name": "緊急五金行",
            "special_items": ["鐵鎚", "鐵絲", "鎖具"]
        }
        self.ui.start_dialogue(shop_data)
        self.assertIn("五金行貨架", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[0], "購買工具")

    def test_pharmacy_night(self):
        """測試夜間藥局限制"""
        shop_data = {
            "type": "shop",
            "id": "PH",
            "name": "24小時藥局",
            "night_only": True
        }
        self.mock_game_state.is_night = False
        self.ui.start_dialogue(shop_data)
        self.assertIn("晚上8點後營業", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()