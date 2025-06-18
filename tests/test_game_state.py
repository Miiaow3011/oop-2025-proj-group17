import unittest
from unittest.mock import MagicMock
from ui import UI

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_mental_health_system(self):
        """测试心理健康状态系统"""
        test_cases = [
            (30, "焦虑", {"accuracy": -0.2}),
            (70, "崩溃", {"speed": -0.5})
        ]
        
        for stress, effect, impacts in test_cases:
            with self.subTest(stress=stress):
                self.mock_game_state.player_stats = {"stress": stress}
                self.ui.check_mental_health()
                self.assertIn(effect, self.ui.current_message)
                self.mock_game_state.apply_effects.assert_called_with(impacts)

    def test_biome_effects(self):
        """测试不同生物群落影响"""
        biomes = {
            "wasteland": {"radiation": +0.1},
            "forest": {"stamina_regen": +0.3}
        }
        
        for biome, effects in biomes.items():
            with self.subTest(biome=biome):
                self.mock_game_state.environment = {"biome": biome}
                self.ui.check_biome_effects()
                self.mock_game_state.apply_effects.assert_called_with(effects)

    def test_day_night_cycle(self):
        """测试昼夜循环影响NPC行为"""
        self.mock_game_state.game_time = {"hour": 3}  # 凌晨
        self.ui.check_night_effects()
        self.mock_game_state.update_npc_status.assert_called_with("sleeping")

        self.mock_game_state.game_time = {"hour": 14}  # 下午
        self.ui.check_day_effects()
        self.mock_game_state.update_npc_status.assert_called_with("active")

if __name__ == '__main__':
    unittest.main()