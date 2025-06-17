import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_store_attitude_system(self):
        """测试武器店态度系统（基于玩家声望）"""
        shop_data = {
            "type": "shop",
            "id": "GUNSHOP",
            "name": "枪械商店",
            "attitude_thresholds": {
                "friendly": 70,
                "neutral": 30
            }
        }
        
        # 测试敌对态度
        self.mock_game_state.player_stats = {"reputation": 20}
        self.ui.start_dialogue(shop_data)
        self.assertIn("不欢迎你", self.ui.dialogue_text)
        
        # 测试友好态度
        self.mock_game_state.player_stats = {"reputation": 80}
        self.ui.start_dialogue(shop_data)
        self.assertIn("老朋友", self.ui.dialogue_text)

    def test_hospital_emergency_triage(self):
        """测试医院急诊分诊系统"""
        shop_data = {
            "type": "shop",
            "id": "HOSPITAL",
            "name": "战地医院",
            "triage_levels": {
                "critical": 20,
                "serious": 50
            }
        }
        
        # 测试危急状态优先治疗
        self.mock_game_state.player_stats = {"hp": 15}
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "立即抢救（优先）")
        
        # 测试轻伤状态
        self.mock_game_state.player_stats = {"hp": 60}
        self.ui.start_dialogue(shop_data)
        self.assertIn("请排队", self.ui.dialogue_text)

    @patch('random.randint')
    def test_black_market_dynamic_pricing(self, mock_rand):
        """测试黑市动态随机定价"""
        mock_rand.return_value = 80  # 模拟随机数
        shop_data = {
            "type": "shop",
            "id": "BLACK",
            "name": "黑市",
            "price_range": {"min": 50, "max": 100}
        }
        
        self.ui.start_dialogue(shop_data)
        self.assertIn("价格:80", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()