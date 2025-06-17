import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_attachment_compatibility(self):
        """测试武器配件兼容性系统"""
        inventory = [
            {"name": "AK47", "type": "rifle"},
            {"name": "红点瞄准镜", "compatible": ["rifle", "smg"]}
        ]
        self.mock_inventory.get_items.return_value = inventory
        
        # 测试兼容配件
        self.assertTrue(self.ui.check_compatibility("AK47", "红点瞄准镜"))
        
        # 测试不兼容情况
        self.mock_inventory.get_items.return_value[0]["name"] = "手枪"
        self.assertFalse(self.ui.check_compatibility("手枪", "红点瞄准镜"))

    def test_food_spoilage_system(self):
        """测试食物腐败度系统"""
        items = [
            {"name": "罐头", "spoilage": 0.1},
            {"name": "鲜肉", "spoilage": 0.8}
        ]
        self.mock_inventory.get_items.return_value = items
        
        # 测试可食用状态
        self.assertTrue(self.ui.is_edible("罐头"))
        
        # 测试腐败状态
        self.assertFalse(self.ui.is_edible("鲜肉"))

    def test_chemistry_crafting(self):
        """测试化学合成系统"""
        recipe = {
            "inputs": [("酒精", 1), ("草药", 3)],
            "output": ("消毒剂", 2),
            "skill": "chemistry"
        }
        
        self.mock_inventory.get_items.return_value = [
            {"name": "酒精", "quantity": 2},
            {"name": "草药", "quantity": 5}
        ]
        self.mock_game_state.player_skills = {"chemistry": 2}
        
        success = self.ui.chemistry_craft(recipe)
        self.assertTrue(success)
        self.mock_inventory.remove_item.assert_any_call("酒精", 1)
        self.mock_inventory.add_item.assert_called_with("消毒剂", 2)

if __name__ == '__main__':
    unittest.main()