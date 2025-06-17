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
    def test_stamina_bar(self, mock_draw):
        """测试耐力条动态渲染"""
        self.mock_game_state.player_stats = {
            "stamina": 40,
            "max_stamina": 100
        }
        
        self.ui.render_hud(self.mock_game_state, None)
        
        # 验证耐力条长度和颜色
        args, _ = mock_draw.call_args_list[1]
        self.assertAlmostEqual(args[0].width, 200 * 0.4, delta=1)
        self.assertEqual(args[2], (0, 200, 255))  # 蓝色耐力条

    @patch('pygame.Surface')
    def test_rain_effect(self, mock_surface):
        """测试下雨特效渲染"""
        self.mock_game_state.environment = {"weather": "rain"}
        self.ui.render(self.mock_game_state, None, None)
        mock_surface.assert_called_with(
            (self.ui.screen_width, self.ui.screen_height), 
            pygame.SRCALPHA
        )

    @patch('font_manager.render_text')
    def test_interaction_prompt(self, mock_render):
        """测试交互提示渲染"""
        self.ui.show_interaction_prompt("按E打开")
        mock_render.assert_called_with(
            "按E打开", 
            20, 
            (255, 255, 0),  # 黄色提示
            font_name="Arial"
        )

if __name__ == '__main__':
    unittest.main()