import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_mayor_quest(self):
        """测试市长多阶段任务对话"""
        npc_data = {
            "type": "npc",
            "id": "mayor",
            "name": "避难所市长",
            "quest_stages": {
                1: "我们需要建立防御工事...",
                2: "请收集10个钢材",
                3: "太感谢你了！"
            }
        }
        
        # 第一阶段
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "我们需要建立防御工事...")
        
        # 模拟任务进展
        self.ui.dialogue_data["stage"] = 2
        self.ui.setup_npc_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "请收集10个钢材")

    def test_prisoner_negotiation(self):
        """测试囚犯谈判系统"""
        npc_data = {
            "type": "npc",
            "id": "prisoner",
            "name": "被俘士兵",
            "negotiation_options": [
                "释放他（需要开锁器）",
                "审问情报",
                "要求加入队伍"
            ]
        }
        
        self.ui.start_dialogue(npc_data)
        self.assertEqual(len(self.ui.dialogue_options), 3)
        self.assertEqual(self.ui.dialogue_options[1], "审问情报")

if __name__ == '__main__':
    unittest.main()