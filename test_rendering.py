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
    def test_sanity_bar_rendering(self, mock_draw):
        """測試精神值條渲染"""
        self.mock_game_state.player_stats = {
            "sanity": 60,
            "max_sanity": 100
        }
        
        self.ui.render_hud(self.mock_game_state, None)
        
        # 驗證精神值條繪製
        args, _ = mock_draw.call_args_list[2]  # 第三個繪製條
        self.assertAlmostEqual(args[0].width, 200 * (60/100), delta=1)

    @patch('pygame.Surface')
    def test_weather_overlay(self, mock_surface):
        """測試天氣覆蓋層渲染"""
        self.mock_game_state.weather = "sandstorm"
        self.ui.render(self.mock_game_state, None, None)
        mock_surface.assert_called_with((self.ui.screen_width, self.ui.screen_height), pygame.SRCALPHA)

if __name__ == '__main__':
    unittest.main()