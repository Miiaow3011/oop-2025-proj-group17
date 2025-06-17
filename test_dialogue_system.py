import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_reputation_based_discounts(self):
        """测试基于声望的动态折扣系统"""
        shop_data = {
            "type": "shop",
            "id": "TOWN_STORE",
            "name": "城镇商店",
            "rep_tiers": [
                {"level": 50, "discount": 0.1},
                {"level": 100, "discount": 0.2}
            ]
        }
        
        # 测试不同声望等级的折扣
        test_cases = [
            (30, "原价"),
            (60, "9折优惠"),
            (110, "8折优惠")
        ]
        
        for rep, expected in test_cases:
            with self.subTest(rep=rep):
                self.mock_game_state.player_stats = {"reputation": rep}
                self.ui.start_dialogue(shop_data)
                self.assertIn(expected, self.ui.dialogue_text)

    def test_supply_chain_disruption(self):
        """测试供应链中断场景"""
        shop_data = {
            "type": "shop",
            "id": "RURAL_CLINIC",
            "name": "乡村诊所",
            "supply_chain": {
                "disrupted": True,
                "alternatives": ["草药", "自制绷带"]
            }
        }
        
        # 测试供应链中断状态
        self.mock_game_state.world_events = {"supply_disruption": True}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买草药")

    @patch('ui.random.random')
    def test_black_market_raid_risk(self, mock_random):
        """测试黑市交易被突袭风险"""
        mock_random.return_value = 0.05  # 5%风险触发
        shop_data = {
            "type": "shop",
            "id": "BLACK_MARKET",
            "name": "黑市",
            "raid_risk": 0.1
        }
        
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 选择交易
        self.assertIn("警察突袭", self.ui.current_message)

if __name__ == '__main__':
    unittest.main()