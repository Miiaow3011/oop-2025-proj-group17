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
    def test_toxin_meter_rendering(self, mock_draw):
        """测试毒素计量表颜色变化"""
        self.mock_game_state.player_stats = {
            "toxin": 65,
            "max_toxin": 100
        }
        
        self.ui.render_hud(self.mock_game_state, None)
        
        # 验证毒素条颜色
        args, _ = mock_draw.call_args_list[3]
        self.assertEqual(args[2], (200, 0, 0))  # 红色毒素条

    @patch('pygame.Surface')
    def test_weather_overlay_intensity(self, mock_surface):
        """测试天气特效强度控制"""
        self.mock_game_state.environment = {
            "weather": "rain",
            "intensity": 0.7
        }
        
        self.ui.render_weather_effects()
        mock_surface.assert_called_with(
            (self.ui.screen_width, self.ui.screen_height),
            pygame.SRCALPHA
        )

    @patch('font_manager.render_text')
    def test_dynamic_quest_markers(self, mock_render):
        """测试动态任务标记颜色"""
        self.ui.active_quests = [
            {"name": "主线任务", "priority": "high"},
            {"name": "支线任务", "priority": "low"}
        ]
        
        self.ui.render_quest_markers()
        
        # 验证不同优先级颜色
        mock_render.assert_any_call("主线任务", 18, (255, 0, 0))  # 红色高优先级
        mock_render.assert_any_call("支线任务", 16, (150, 150, 150))  # 灰色低优先级

if __name__ == '__main__':
    unittest.main()