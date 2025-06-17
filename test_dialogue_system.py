import unittest
from unittest.mock import MagicMock
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_black_market(self):
        """测试黑市商店的隐藏交易"""
        shop_data = {
            "type": "shop",
            "id": "BM",
            "name": "黑市商人",
            "requires_reputation": 50,
            "secret_items": ["消音手枪", "夜视镜"]
        }
        
        # 测试声望不足
        self.mock_game_state.player_stats = {"reputation": 30}
        self.ui.start_dialogue(shop_data)
        self.assertIn("你还不够资格", self.ui.dialogue_text)
        
        # 测试声望足够
        self.mock_game_state.player_stats = {"reputation": 60}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买消音手枪")

    def test_hospital_emergency(self):
        """测试急诊室的限时治疗"""
        shop_data = {
            "type": "shop",
            "id": "ER",
            "name": "急诊室",
            "time_sensitive": True,
            "treatment_cost": 80
        }
        
        self.mock_game_state.player_stats = {"hp": 40, "max_hp": 100, "money": 100}
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 选择紧急治疗
        
        # 验证治疗和扣款
        self.mock_game_state.player_stats.__setitem__.assert_any_call("hp", 90)
        self.mock_game_state.player_stats.__setitem__.assert_any_call("money", 20)

if __name__ == '__main__':
    unittest.main()