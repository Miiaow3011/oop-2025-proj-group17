import unittest
from unittest.mock import MagicMock, patch
import pickle
from ui import UI

class TestSaveSystem(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.ui = UI(self.mock_screen)
        
        # 設置遊戲狀態
        self.ui.has_keycard = True
        self.ui.has_antidote = False
        self.ui.game_completed = False
        self.ui.show_inventory = True

    @patch('builtins.open')
    @patch('pickle.dump')
    def test_save_game(self, mock_pickle, mock_open):
        """測試遊戲存檔功能"""
        from game import save_game_state  # 假設有這個函數
        
        save_game_state(self.ui, "test_save.dat")
        
        # 驗證文件被打開
        mock_open.assert_called_with("test_save.dat", 'wb')
        
        # 驗證pickle被調用
        mock_pickle.assert_called()
        
        # 獲取保存的數據
        saved_data = mock_pickle.call_args[0][0]
        self.assertTrue(saved_data['has_keycard'])
        self.assertFalse(saved_data['has_antidote'])

    @patch('builtins.open')
    @patch('pickle.load')
    def test_load_game(self, mock_pickle, mock_open):
        """測試遊戲讀檔功能"""
        from game import load_game_state  # 假設有這個函數
        
        # 設置模擬的存檔數據
        mock_pickle.return_value = {
            'has_keycard': False,
            'has_antidote': True,
            'game_completed': False
        }
        
        load_game_state(self.ui, "test_save.dat")
        
        # 驗證狀態被正確載入
        self.assertFalse(self.ui.has_keycard)
        self.assertTrue(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)

    def test_reset_game_state(self):
        """測試重置遊戲狀態"""
        # 設置各種狀態
        self.ui.has_keycard = True
        self.ui.has_antidote = True
        self.ui.game_completed = True
        self.ui.dialogue_active = True
        
        # 執行重置
        self.ui.reset_game()
        
        # 驗證狀態已重置
        self.assertFalse(self.ui.has_keycard)
        self.assertFalse(self.ui.has_antidote)
        self.assertFalse(self.ui.game_completed)
        self.assertFalse(self.ui.dialogue_active)

if __name__ == '__main__':
    unittest.main()
