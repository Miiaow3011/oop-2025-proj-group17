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
    def test_infection_bar_rendering(self, mock_draw):
        """测试感染条渲染"""
        self.mock_game_state.player_stats = {
            "infection_level": 75,
            "max_infection": 100
        }
        
        self.ui.render_hud(self.mock_game_state, None)
        
        # 验证感染条绘制
        args, _ = mock_draw.call_args_list[3]  # 第四个绘制条
        self.assertAlmostEqual(args[0].width, 200 * (75/100), delta=1)

    @patch('pygame.Surface')
    def test_blizzard_overlay(self, mock_surface):
        """测试暴风雪覆盖层渲染"""
        self.mock_game_state.environment = {"weather": "blizzard"}
        self.ui.render(self.mock_game_state, None, None)
        mock_surface.assert_called_with((self.ui.screen_width, self.ui.screen_height), pygame.SRCALPHA)

if __name__ == '__main__':
    unittest.main()