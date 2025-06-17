import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_scientist_research_help(self):
        """测试科学家研究协助的多阶段对话"""
        npc_data = {
            "type": "npc",
            "id": "DR_LEE",
            "name": "李博士",
            "research_stages": {
                1: "需要3个病毒样本...",
                2: "分析中...",
                3: "这是疫苗配方！"
            }
        }
        
        # 第一阶段
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "需要3个病毒样本...")
        
        # 第三阶段
        self.ui.dialogue_data["stage"] = 3
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("疫苗配方", self.ui.dialogue_text)

    def test_prisoner_interrogation(self):
        """测试审讯囚犯的压力系统"""
        npc_data = {
            "type": "npc",
            "id": "PRISONER",
            "name": "战俘",
            "stress_level": 0,
            "break_point": 5
        }
        
        # 首次审讯
        self.ui.start_dialogue(npc_data)
        self.ui.select_dialogue_option(1)  # 选择施压选项
        self.assertEqual(self.ui.dialogue_data["stress_level"], 1)
        
        # 达到崩溃点
        self.ui.dialogue_data["stress_level"] = 5
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("我全说！", self.ui.dialogue_text)

    def test_merchant_barter_system(self):
        """测试商人的以物易物系统"""
        npc_data = {
            "type": "npc",
            "id": "MERCHANT",
            "name": "旅行商人",
            "barter_items": {
                "抗生素": ["子弹", 30],
                "防弹衣": ["医疗包", 2]
            }
        }
        
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_options[0], "用30子弹换抗生素")

if __name__ == '__main__':
    unittest.main()