import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_scientist_rescue(self):
        """測試科學家救援任務多階段對話"""
        npc_data = {
            "type": "npc",
            "id": "sci1",
            "name": "被困科學家",
            "phases": {
                "start": "請幫我找實驗筆記...",
                "progress": "筆記在3樓實驗室",
                "complete": "你救了我一命！"
            }
        }
        
        # 初始階段
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "請幫我找實驗筆記...")
        
        # 進度更新階段
        self.ui.dialogue_data["phase"] = "progress"
        self.ui.setup_npc_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "筆記在3樓實驗室")

    def test_trader_barter(self):
        """測試商人以物易物系統"""
        npc_data = {
            "type": "npc",
            "id": "trd1",
            "name": "流浪商人",
            "barter_items": ["罐頭", "電池", "藥品"]
        }
        
        self.mock_inventory.get_items.return_value = [
            {"name": "罐頭", "quantity": 5},
            {"name": "子彈", "quantity": 20}
        ]
        
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_options[0], "交易罐頭(庫存:5)")

if __name__ == '__main__':
    unittest.main()