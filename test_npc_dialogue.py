import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_memory_system(self):
        """测试NPC记忆系统（基于历史交互）"""
        npc_data = {
            "type": "npc",
            "id": "OLD_MAN",
            "name": "老杰克",
            "memory": {
                "last_met": 5,
                "favor": 30
            }
        }
        
        # 测试记忆影响对话
        self.mock_game_state.game_time = {"day": 10}
        self.ui.start_dialogue(npc_data)
        self.assertIn("5天没见了", self.ui.dialogue_text)
        
        # 测试好感度影响
        npc_data["memory"]["favor"] = 80
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("老朋友", self.ui.dialogue_text)

    def test_skill_check_dialogue(self):
        """测试技能检查对话选项"""
        npc_data = {
            "type": "npc",
            "id": "ENGINEER",
            "name": "工程师",
            "skill_checks": {
                "repair": 60,
                "hack": 40
            }
        }
        
        # 测试技能不足
        self.mock_game_state.player_skills = {"repair": 50}
        self.ui.start_dialogue(npc_data)
        self.assertIn("技术不够", self.ui.dialogue_text)
        
        # 测试技能足够
        self.mock_game_state.player_skills = {"hack": 45}
        self.ui.setup_npc_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_options[0], "尝试破解")

    def test_conditional_branches(self):
        """测试条件分支对话系统"""
        npc_data = {
            "type": "npc",
            "id": "INFORMANT",
            "name": "线人",
            "branches": [
                {"condition": "has_item('证据')", "text": "感谢证据"},
                {"condition": "default", "text": "需要证据"}
            ]
        }
        
        # 测试条件分支
        self.mock_inventory = MagicMock()
        self.mock_inventory.has_item.return_value = True
        self.ui.set_inventory_reference(self.mock_inventory)
        
        self.ui.start_dialogue(npc_data)
        self.assertIn("感谢证据", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()