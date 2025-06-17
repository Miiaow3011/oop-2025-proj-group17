import unittest
from unittest.mock import MagicMock
from ui import UI

class TestNPCDialogue(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)

    def test_military_soldier(self):
        """測試軍人NPC多階段對話"""
        npc_data = {
            "type": "npc",
            "id": "mil1",
            "name": "受傷軍人",
            "phases": {
                "start": "我們需要醫療支援...",
                "helped": "感謝你的協助"
            }
        }
        self.ui.start_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "我們需要醫療支援...")
        
        # 模擬完成幫助後
        self.ui.dialogue_data["phase"] = "helped"
        self.ui.setup_npc_dialogue(npc_data)
        self.assertEqual(self.ui.dialogue_text, "感謝你的協助")

if __name__ == '__main__':
    unittest.main()
