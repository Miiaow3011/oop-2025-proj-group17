import unittest
from unittest.mock import MagicMock
from ui import UI

class TestItemSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_equipment_set_bonus(self):
        """测试装备套装效果激活"""
        inventory = [
            {"name": "反抗军头盔", "set": "rebel"},
            {"name": "反抗军护甲", "set": "rebel"},
            {"name": "普通手套", "set": None}
        ]
        self.mock_inventory.get_items.return_value = inventory
        
        # 测试套装激活
        self.assertTrue(self.ui.check_set_bonus("rebel", 2))
        
        # 测试套装不完整
        self.assertFalse(self.ui.check_set_bonus("rebel", 3))

    def test_weapon_condition_impact(self):
        """测试武器状态影响伤害"""
        weapons = [
            {"name": "AK47", "condition": 80},
            {"name": "生锈手枪", "condition": 20}
        ]
        self.mock_inventory.get_items.return_value = weapons
        
        # 测试状态影响
        self.assertAlmostEqual(
            self.ui.calculate_damage("AK47", 100),
            100 * 0.8,
            delta=0.1
        )
        
        # 测试低状态武器
        self.assertLess(
            self.ui.calculate_damage("生锈手枪", 50),
            25
        )

    def test_chemical_mixing(self):
        """测试化学品混合危险性"""
        recipes = [
            {"inputs": ["硝酸", "甘油"], "danger": True},
            {"inputs": ["水", "盐"], "danger": False}
        ]
        
        # 测试危险组合
        self.assertTrue(self.ui.check_chemical_danger(["硝酸", "甘油"]))
        
        # 测试安全组合
        self.assertFalse(self.ui.check_chemical_danger(["水", "盐"]))

if __name__ == '__main__':
    unittest.main()