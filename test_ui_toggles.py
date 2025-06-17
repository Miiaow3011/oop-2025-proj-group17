import unittest
from unittest.mock import MagicMock
from ui import UI

class TestUIToggles(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_inventory_toggle(self):
        """測試背包切換功能"""
        # 初始狀態
        self.assertFalse(self.ui.show_inventory)
        
        # 第一次切換
        self.ui.toggle_inventory()
        self.assertTrue(self.ui.show_inventory)
        self.assertFalse(self.ui.show_map)  # 地圖應保持關閉
        
        # 第二次切換
        self.ui.toggle_inventory()
        self.assertFalse(self.ui.show_inventory)

    def test_map_toggle(self):
        """測試地圖切換功能"""
        # 初始狀態
        self.assertFalse(self.ui.show_map)
        
        # 第一次切換
        self.ui.toggle_map()
        self.assertTrue(self.ui.show_map)
        self.assertFalse(self.ui.show_inventory)  # 背包應保持關閉
        
        # 第二次切換
        self.ui.toggle_map()
        self.assertFalse(self.ui.show_map)

    def test_ui_status_check(self):
        """測試UI狀態檢查"""
        # 初始無UI開啟
        self.assertFalse(self.ui.is_any_ui_open())
        
        # 開啟背包後檢查
        self.ui.toggle_inventory()
        self.assertTrue(self.ui.is_any_ui_open())
        
        # 關閉所有UI
        self.ui.close_all_ui()
        self.assertFalse(self.ui.is_any_ui_open())
        self.assertFalse(self.ui.show_inventory)
        self.assertFalse(self.ui.show_map)

    def test_close_all_ui(self):
        """測試關閉所有UI功能"""
        # 開啟所有UI
        self.ui.show_inventory = True
        self.ui.show_map = True
        self.ui.dialogue_active = True
        
        # 關閉所有UI
        self.ui.close_all_ui()
        
        # 驗證
        self.assertFalse(self.ui.show_inventory)
        self.assertFalse(self.ui.show_map)
        self.assertFalse(self.ui.dialogue_active)

if __name__ == '__main__':
    unittest.main()
