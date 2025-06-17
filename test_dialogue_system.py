import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_7eleven_shop(self):
        """測試7-11商店對話"""
        shop_data = {
            "type": "shop",
            "id": "A",
            "name": "7-11"
        }
        self.ui.start_dialogue(shop_data)
        
        self.assertIn("歡迎來到7-11", self.ui.dialogue_text)
        self.assertEqual(len(self.ui.dialogue_options), 3)
        self.assertEqual(self.ui.dialogue_options[0], "購買醫療用品")

    def test_subway_shop(self):
        """測試Subway商店對話"""
        shop_data = {
            "type": "shop",
            "id": "B",
            "name": "Subway"
        }
        self.ui.start_dialogue(shop_data)
        
        self.assertIn("Subway已經沒有新鮮食材", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[0], "購買罐頭食品")

    def test_tea_shop(self):
        """測試茶壜商店對話"""
        shop_data = {
            "type": "shop",
            "id": "C",
            "name": "茶壜"
        }
        self.ui.start_dialogue(shop_data)
        
        self.assertIn("茶壜的飲料機還在運作", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[0], "搜尋飲料")

if __name__ == '__main__':
    unittest.main()