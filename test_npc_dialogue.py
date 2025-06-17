import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_scientist_research_tree(self):
        """测试科学家研究任务树"""
        npc_data = {
            "type": "npc",
            "id": "SCIENTIST",
            "name": "张博士",
            "research_tree": {
                "stage1": "需要病毒样本...",
                "stage2": "分析中...",
                "stage3": "这是抗病毒血清！"
            }
        }
        
        # 第一阶段对话
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "需要病毒样本...")
        
        # 第三阶段对话
        self.ui.dialogue_data["stage"] = "stage3"
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("抗病毒血清", self.ui.dialogue_text)

    def test_prisoner_interrogation(self):
        """测试战俘审讯压力系统"""
        npc_data = {
            "type": "npc",
            "id": "PRISONER",
            "name": "敌方士兵",
            "stress": 0,
            "break_point": 3
        }
        
        # 施加压力
        self.ui.start_dialogue(npc_data)
        self.ui.select_dialogue_option(1)  # 选择威胁选项
        self.assertEqual(self.ui.dialogue_data["stress"], 1)
        
        # 达到崩溃点
        self.ui.dialogue_data["stress"] = 3
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("我投降！", self.ui.dialogue_text)

    def test_merchant_dynamic_pricing(self):
        """测试商人的动态定价系统"""
        npc_data = {
            "type": "npc",
            "id": "MERCHANT",
            "name": "黑市商人",
            "price_factors": {
                "抗生素": {"base": 50, "scarcity": 1.5}
            }
        }
        
        self.mock_game_state = MagicMock()
        self.mock_game_state.economy = {"antibiotic_scarcity": True}
        self.ui.set_game_state_reference(self.mock_game_state)
        
        self.ui.start_dialogue(npc_data)
        self.assertIn("抗生素:75", self.ui.dialogue_text)  # 50*1.5

if __name__ == '__main__':
    unittest.main()