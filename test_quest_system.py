import unittest
from unittest.mock import MagicMock
from ui import UI

class TestQuestSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        self.mock_inventory = MagicMock()
        self.ui.set_inventory_reference(self.mock_inventory)

    def test_fetch_quest(self):
        """測試物品收集任務"""
        npc_data = {
            "type": "npc",
            "id": "quest1",
            "name": "研究主任",
            "requires_items": {"醫療包": 3}
        }
        
        # 測試物品不足
        self.mock_inventory.get_items.return_value = [{"name": "醫療包", "quantity": 2}]
        self.ui.start_dialogue(npc_data)
        self.assertIn("還需要1個醫療包", self.ui.dialogue_text)
        
        # 測試物品足夠
        self.mock_inventory.get_items.return_value = [{"name": "醫療包", "quantity": 3}]
        self.ui.start_dialogue(npc_data)
        self.assertIn("感謝你帶來這些物品", self.ui.dialogue_text)

    def test_escort_quest(self):
        """測試護送任務"""
        npc_data = {
            "type": "npc",
            "id": "quest2",
            "name": "受傷科學家",
            "quest_type": "escort"
        }
        
        self.ui.start_dialogue(npc_data)
        self.assertIn("能帶我離開這裡嗎", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[-1], "接受護送任務")

    def test_boss_key_quest(self):
        """測試Boss鑰匙任務"""
        npc_data = {
            "type": "npc",
            "id": "quest3",
            "name": "守衛隊長",
            "key_quest": True
        }
        
        self.ui.start_dialogue(npc_data)
        self.assertIn("實驗室主鑰匙", self.ui.dialogue_text)
        self.assertEqual(self.ui.dialogue_options[0], "詢問鑰匙位置")

if __name__ == '__main__':
    unittest.main()
