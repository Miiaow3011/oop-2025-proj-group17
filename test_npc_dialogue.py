import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_weapon_jamming(self):
        """测试武器卡弹概率系统"""
        weapons = [
            {"name": "AK47", "jam_chance": 0.15, "condition": 70},
            {"name": "保养良好的手枪", "jam_chance": 0.02, "condition": 95}
        ]
        self.mock_inventory.get_items.return_value = weapons
        
        # 测试卡弹概率计算
        self.assertAlmostEqual(
            self.ui.calculate_jam_chance("AK47"),
            0.15 * (1 - 0.7),
            delta=0.01
        )
        
        # 测试保养良好的武器
        self.assertLess(
            self.ui.calculate_jam_chance("保养良好的手枪"),
            0.05
        )

    def test_food_spoilage_rate(self):
        """测试食物腐败速率系统"""
        environment_conditions = [
            {"temp": 30, "humidity": 0.8, "expected_rate": 1.5},
            {"temp": 10, "humidity": 0.3, "expected_rate": 0.5}
        ]
        
        for cond in environment_conditions:
            with self.subTest(temp=cond["temp"]):
                self.mock_game_state.environment = {
                    "temperature": cond["temp"],
                    "humidity": cond["humidity"]
                }
                self.assertEqual(
                    self.ui.calculate_spoilage_rate(),
                    cond["expected_rate"]
                )

    def test_chemical_stability(self):
        """测试化学品稳定性系统"""
        chemicals = [
            {"name": "硝酸甘油", "stability": 0.3, "temp_sensitive": True},
            {"name": "食盐", "stability": 1.0, "temp_sensitive": False}
        ]
        
        # 测试不稳定化学品
        self.mock_game_state.environment = {"temperature": 35}
        self.assertTrue(self.ui.check_chemical_stability("硝酸甘油"))
        
        # 测试稳定物品
        self.assertFalse(self.ui.check_chemical_stability("食盐"))

if __name__ == '__main__':
    unittest.main()