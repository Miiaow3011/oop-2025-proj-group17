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
    def test_compound_status_bars(self, mock_draw):
        """测试复合状态条渲染（健康+辐射）"""
        self.mock_game_state.player_stats = {
            "hp": 70,
            "max_hp": 100,
            "radiation": 30,
            "max_radiation": 100
        }
        
        self.ui.render_compound_health_bar(10, 10)
        
        # 验证双状态条叠加渲染
        self.assertEqual(mock_draw.call_count, 4)  # 背景+两个状态条+分割线

    @patch('pygame.Surface')
    def test_dynamic_damage_overlay(self, mock_surface):
        """测试动态伤害覆盖层（根据伤害来源）"""
        damage_types = {
            "bullet": (200, 0, 0),  # 红色
            "poison": (0, 200, 0)   # 绿色
        }
        
        for dtype, color in damage_types.items():
            with self.subTest(type=dtype):
                self.ui.last_damage_type = dtype
                self.ui.render_damage_overlay()
                mock_surface.assert_called_with(
                    (self.ui.screen_width, self.ui.screen_height),
                    pygame.SRCALPHA
                )

    @patch('font_manager.render_text')
    def test_contextual_interaction_prompts(self, mock_render):
        """测试情境交互提示（根据环境变化）"""
        contexts = [
            ("water", "按F取水"),
            ("locked_door", "按E撬锁")
        ]
        
        for context, prompt in contexts:
            with self.subTest(context=context):
                self.ui.current_context = context
                self.ui.render_interaction_prompt()
                mock_render.assert_called_with(
                    prompt,
                    22,
                    (255, 255, 255),
                    font_name="Arial"
                )

if __name__ == '__main__':
    unittest.main()