import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestCombatUI(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    @patch('pygame.draw.rect')
    def test_enemy_health_bar(self, mock_draw):
        """測試敵人血條渲染"""
        enemy = {
            "name": "變異殭屍",
            "hp": 120,
            "max_hp": 200,
            "level": 3
        }
        
        self.ui.render_enemy_health(enemy, 100, 100)
        
        # 驗證血條繪製
        args, _ = mock_draw.call_args_list[1]  # 獲取血量條部分
        self.assertAlmostEqual(args[0].width, 200 * (120/200), delta=1)

    def test_combat_options(self):
        """測試戰鬥選項顯示"""
        combat_data = {
            "type": "combat",
            "enemy": "變異殭屍",
            "options": ["攻擊", "防禦", "使用物品", "逃跑"]
        }
        
        self.ui.start_dialogue(combat_data)
        self.assertEqual(len(self.ui.dialogue_options), 4)
        self.assertEqual(self.ui.dialogue_options[0], "攻擊")

    @patch('pygame.Surface')
    def test_combat_result(self, mock_surface):
        """測試戰鬥結果顯示"""
        self.ui.show_combat_result("勝利!", "擊敗了變異殭屍", 150)
        mock_surface.assert_called()  # 驗證有創建結果畫面

if __name__ == '__main__':
    unittest.main()
