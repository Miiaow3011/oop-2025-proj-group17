import unittest
from unittest.mock import MagicMock
from ui import UI

class TestUIInitialization(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.mock_screen.get_size.return_value = (800, 600)
        self.ui = UI(self.mock_screen)

    def test_initial_properties(self):
        """測試UI初始化屬性"""
        self.assertEqual(self.ui.screen_width, 800)
        self.assertEqual(self.ui.screen_height, 600)
        self.assertFalse(self.ui.show_inventory)
        self.assertFalse(self.ui.show_map)
        self.assertFalse(self.ui.dialogue_active)
        self.assertIsNone(self.ui.dialogue_data)
        self.assertEqual(self.ui.dialogue_text, "")
        self.assertEqual(self.ui.dialogue_options, [])
        self.assertEqual(self.ui.selected_option, 0)
        self.assertEqual(self.ui.dialogue_box_height, 150)
        self.assertEqual(self.ui.dialogue_box_y, 600 - 150 - 10)

    def test_reference_setters(self):
        """測試參考設置方法"""
        mock_player = MagicMock()
        mock_inventory = MagicMock()
        mock_game_state = MagicMock()
        
        self.ui.set_player_reference(mock_player)
        self.ui.set_inventory_reference(mock_inventory)
        self.ui.set_game_state_reference(mock_game_state)
        
        self.assertEqual(self.ui.player_reference, mock_player)
        self.assertEqual(self.ui.inventory_reference, mock_inventory)
        self.assertEqual(self.ui.game_state_reference, mock_game_state)

if __name__ == '__main__':
    unittest.main()
