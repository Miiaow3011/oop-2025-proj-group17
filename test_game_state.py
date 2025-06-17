import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_toxin_accumulation(self):
        """测试毒素累积阶段系统"""
        stages = {
            30: "轻度中毒",
            70: "器官损伤",
            100: "生命危险"
        }
        
        for level, effect in stages.items():
            with self.subTest(level=level):
                self.mock_game_state.player_stats = {"toxin": level}
                self.ui.check_toxin_effects()
                self.assertIn(effect, self.ui.current_message)

    def test_weather_impact_system(self):
        """测试复合天气影响系统"""
        weather_cases = [
            ("sandstorm", {"visibility": 0.3, "damage": 5}),
            ("blizzard", {"stamina": 0.5, "damage": 8})
        ]
        
        for weather, effects in weather_cases:
            with self.subTest(weather=weather):
                self.mock_game_state.environment = {"weather": weather}
                self.ui.check_weather_impact()
                self.mock_game_state.apply_effects.assert_called_with(effects)

    def test_faction_relations(self):
        """测试阵营关系影响"""
        actions = [
            ("帮派任务", {"gang": +10}),
            ("袭击哨站", {"military": -20})
        ]
        
        for action, impact in actions:
            with self.subTest(action=action):
                self.mock_game_state.factions = {"gang": 50, "military": 50}
                self.ui.record_faction_action(action, impact)
                self.assertEqual(
                    self.mock_game_state.factions[list(impact.keys())[0]],
                    50 + list(impact.values())[0]
                )

if __name__ == '__main__':
    unittest.main()