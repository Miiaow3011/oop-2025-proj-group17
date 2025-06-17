import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_scared_student(self):
        """測試驚慌學生對話"""
        npc_data = {
            "type": "npc",
            "id": "npc1",
            "name": "驚慌學生"
        }
        self.ui.start_dialogue(npc_data)
        
        self.assertIn("救命！外面到處都是殭屍", self.ui.dialogue_text)
        self.assertEqual(len(self.ui.dialogue_options), 3)

    def test_injured_staff(self):
        """測試受傷職員對話"""
        npc_data = {
            "type": "npc",
            "id": "npc2",
            "name": "受傷職員"
        }
        self.ui.start_dialogue(npc_data)
        
        self.assertIn("我被咬了...但還沒完全感染", self.ui.dialogue_text)
        self.assertEqual(len(self.ui.dialogue_options), 4)

    def test_researcher_dialogue(self):
        """測試研究員對話（有鑰匙卡和無鑰匙卡兩種狀態）"""
        npc_data = {
            "type": "npc", 
            "id": "npc3",
            "name": "神秘研究員"
        }
        
        # 測試無鑰匙卡狀態
        self.ui.has_keycard = False
        self.ui.start_dialogue(npc_data)
        self.assertIn("你也在找解藥嗎", self.ui.dialogue_text)
        
        # 測試有鑰匙卡狀態
        self.ui.has_keycard = True
        self.ui.start_dialogue(npc_data)
        self.assertIn("鑰匙卡", self.ui.dialogue_text)

if __name__ == '__main__':
    unittest.main()
