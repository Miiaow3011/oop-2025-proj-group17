import unittest
from unittest.mock import MagicMock
from ui import UI

class TestSpecialShops(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_locked_lab_shop(self):
        """測試需要鑰匙卡的實驗室商店"""
        shop_data = {
            "type": "shop",
            "id": "LAB",
            "name": "秘密實驗室",
            "requires_keycard": True
        }
        
        # 無鑰匙卡狀態
        self.ui.has_keycard = False
        self.ui.start_dialogue(shop_data)
        self.assertIn("需要特殊通行證", self.ui.dialogue_text)
        
        # 有鑰匙卡狀態
        self.ui.has_keycard = True
        self.ui.start_dialogue(shop_data)
        self.assertIn("實驗室控制面板", self.ui.dialogue_text)

    def test_medical_center(self):
        """測試醫療中心特殊互動"""
        shop_data = {
            "type": "shop",
            "id": "MED",
            "name": "醫療中心",
            "can_heal": True
        }
        
        self.mock_game_state.player_stats = {"hp": 50, "max_hp": 100}
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 選擇治療
        
        self.mock_game_state.player_stats.__setitem__.assert_called_with("hp", 100)

    def test_weapon_upgrade_shop(self):
        """測試武器升級商店"""
        shop_data = {
            "type": "shop",
            "id": "WPN",
            "name": "武器工坊",
            "upgrades": ["傷害+", "射速+", "容量+"]
        }
        
        self.ui.start_dialogue(shop_data)
        self.assertEqual(len(self.ui.dialogue_options), 4)  # 3升級選項+離開

if __name__ == '__main__':
    unittest.main()
