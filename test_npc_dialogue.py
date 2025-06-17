import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_trauma_system(self):
        """测试NPC创伤记忆系统"""
        npc_data = {
            "type": "npc",
            "id": "WAR_VETERAN",
            "name": "老兵",
            "trauma_triggers": ["枪声", "爆炸"],
            "calm_methods": ["安抚", "给酒"]
        }
        
        # 测试触发创伤状态
        self.ui.dialogue_data = {"triggered": True}
        self.ui.setup_npc_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_options[0], "安抚")

    def test_language_barrier(self):
        """测试语言障碍沟通系统"""
        npc_data = {
            "type": "npc",
            "id": "FOREIGNER",
            "name": "外国商人",
            "language": "russian",
            "comprehension": 0.4
        }
        
        # 测试语言技能不足
        self.mock_game_state.player_skills = {"russian": 30}
        self.ui.start_dialogue(npc_data)
        self.assertIn("理解困难", self.ui.dialogue_text)
        
        # 测试语言技能足够
        self.mock_game_state.player_skills = {"russian": 80}
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("沟通顺畅", self.ui.dialogue_text)

    def test_negotiation_minigame(self):
        """测试谈判小游戏系统"""
        npc_data = {
            "type": "npc",
            "id": "HOSTAGE_TAKER",
            "name": "绑匪",
            "negotiation": {
                "rounds": 3,
                "win_condition": 2
            }
        }
        
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_data["rounds"], 3)
        self.assertEqual(self.ui.dialogue_data["wins_required"], 2)

if __name__ == '__main__':
    unittest.main()