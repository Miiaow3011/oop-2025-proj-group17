import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_game_state = MagicMock()
        self.ui.set_game_state_reference(self.mock_game_state)

    def test_scientist_research_progress(self):
        """测试科研进度追踪系统"""
        npc_data = {
            "type": "npc",
            "id": "DR_WANG",
            "name": "王博士",
            "research_progress": {
                "materials": 0,
                "stages": ["收集材料", "数据分析", "制作原型"]
            }
        }
        
        # 初始阶段
        self.ui.start_dialogue(npc_data)
        self.assertIn("收集材料", self.ui.dialogue_text)
        
        # 提交材料后
        npc_data["research_progress"]["materials"] = 1
        self.ui.setup_npc_dialogue(npc_data)
        self.assertIn("数据分析", self.ui.dialogue_text)

    def test_prisoner_interrogation_techniques(self):
        """测试多种审讯技术效果"""
        npc_data = {
            "type": "npc",
            "id": "PRISONER_X",
            "name": "战俘X",
            "techniques": {
                "threaten": {"stress": 20, "info": 30},
                "bargain": {"stress": -10, "info": 50}
            }
        }
        
        # 测试威胁技术
        self.ui.start_dialogue(npc_data)
        self.ui.select_dialogue_option(0)  # 选择威胁
        self.assertEqual(self.ui.dialogue_data["stress"], 20)
        
        # 测试交易技术
        self.ui.select_dialogue_option(1)  # 选择交易
        self.assertEqual(self.ui.dialogue_data["stress"], 10)

    def test_merchant_supply_demand(self):
        """测试商人供需经济系统"""
        npc_data = {
            "type": "npc",
            "id": "MERCHANT_Y",
            "name": "旅行商人Y",
            "supply_factor": {
                "antibiotics": 1.8  # 稀缺系数
            }
        }
        
        self.mock_game_state.economy = {"antibiotics_demand": "high"}
        self.ui.start_dialogue(npc_data)
        self.assertIn("抗生素紧缺", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()