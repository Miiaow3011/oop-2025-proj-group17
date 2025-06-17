import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestShopDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_faction_locked_vendor(self):
        """测试阵营专属商店访问控制"""
        shop_data = {
            "type": "shop",
            "id": "FACTION_ARMORY",
            "name": "阵营军械库",
            "required_faction": "resistance",
            "inventory": ["原型武器"]
        }
        
        # 测试阵营不符
        self.mock_game_state.player_faction = "bandits"
        self.ui.start_dialogue(shop_data)
        self.assertIn("拒绝进入", self.ui.dialogue_text)
        
        # 测试阵营匹配
        self.mock_game_state.player_faction = "resistance"
        self.ui.start_dialogue(shop_data)
        self.assertEqual(self.ui.dialogue_options[0], "购买原型武器")

    def test_dynamic_stock_rotation(self):
        """测试动态库存轮换系统"""
        shop_data = {
            "type": "shop",
            "id": "TRAVELING_MERCHANT",
            "name": "旅行商人",
            "stock_rotation": {
                "days": [1, 3, 5],
                "items": ["稀有零件", "古董武器"]
            }
        }
        
        # 测试库存更新日
        self.mock_game_state.game_time = {"day": 3}
        self.ui.start_dialogue(shop_data)
        self.assertIn("稀有零件", self.ui.dialogue_text)
        
        # 测试非库存日
        self.mock_game_state.game_time = {"day": 2}
        self.ui.start_dialogue(shop_data)
        self.assertIn("下次到货", self.ui.dialogue_text)

    @patch('ui.random.randint')
    def test_haggling_system(self, mock_rand):
        """测试议价系统成功率"""
        mock_rand.return_value = 65  # 设置随机数
        shop_data = {
            "type": "shop",
            "id": "MARKET",
            "name": "集市",
            "haggle_difficulty": 60
        }
        
        self.mock_game_state.player_skills = {"barter": 70}
        self.ui.start_dialogue(shop_data)
        self.ui.select_dialogue_option(0)  # 选择议价
        self.assertIn("议价成功", self.ui.current_message)

if __name__ == '__main__':
    unittest.main()