import unittest
from unittest.mock import MagicMock, patch
from ui import UI

class TestUIRendering(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    @patch('pygame.draw.rect')
    def test_radiation_meter(self, mock_draw):
        """测试辐射值计量表渲染"""
        self.mock_game_state.player_stats = {
            "radiation": 60,
            "max_radiation": 100
        }
        
        self.ui.render_hud(self.mock_game_state, None)
        
        # 验证辐射条绘制
        args, _ = mock_draw.call_args_list[2]  # 第三个绘制条
        self.assertAlmostEqual(args[0].width, 200 * (60/100), delta=1)

    @patch('pygame.Surface')
    def test_sandstorm_effect(self, mock_surface):
        """测试沙尘暴特效渲染"""
        self.mock_game_state.environment = {"weather": "sandstorm"}
        self.ui.render(self.mock_game_state, None, None)
        mock_surface.assert_called_with((self.ui.screen_width, self.ui.screen_height), pygame.SRCALPHA)

    @patch('font_manager.render_text')
    def test_quest_marker(self, mock_render):
        """测试任务标记渲染"""
        self.ui.active_quests = ["寻找发电机零件"]
        self.ui.render_quest_markers()
        mock_render.assert_called_with("寻找发电机零件", 16, (255, 255, 0))

if __name__ == '__main__':
    unittest.main()