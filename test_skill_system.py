import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestSkillSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_skill_tree_display(self):
        """測試技能樹顯示"""
        skills = {
            "醫療": {"level": 2, "max": 5},
            "戰鬥": {"level": 3, "max": 5},
            "潛行": {"level": 1, "max": 5}
        }
        
        self.mock_game_state.player_skills = skills
        self.ui.show_skill_tree = True
        
        with patch('pygame.draw.rect') as mock_draw:
            self.ui.render(self.mock_game_state, None, None)
            
            # 驗證技能項目繪製
            self.assertGreaterEqual(mock_draw.call_count, 3)

    def test_skill_upgrade(self):
        """測試技能升級互動"""
        npc_data = {
            "type": "npc",
            "id": "trainer",
            "name": "技能導師",
            "can_train": True
        }
        
        self.mock_game_state.player_stats = {"exp": 500}
        self.ui.start_dialogue(npc_data)
        
        # 測試升級選項
        self.assertEqual(self.ui.dialogue_options[0], "提升醫療技能")
        self.assertEqual(self.ui.dialogue_options[1], "提升戰鬥技能")

    @patch('pygame.Surface')
    def test_skill_effect_display(self, mock_surface):
        """測試技能效果顯示"""
        self.ui.show_skill_effect("醫療", "治療效果+20%")
        mock_surface.assert_called()  # 驗證有效果顯示

if __name__ == '__main__':
    unittest.main()
