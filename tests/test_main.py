import sys
import os
import pytest
from unittest.mock import Mock, patch, MagicMock

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 模擬 pygame 模組（如果需要）
if 'pygame' not in sys.modules:
    pygame_mock = MagicMock()
    pygame_mock.init = MagicMock()
    pygame_mock.display.set_mode = MagicMock(return_value=MagicMock())
    pygame_mock.display.set_caption = MagicMock()
    pygame_mock.time.Clock = MagicMock(return_value=MagicMock())
    pygame_mock.QUIT = 12  # pygame.QUIT 的實際值
    pygame_mock.KEYDOWN = 2  # pygame.KEYDOWN 的實際值
    pygame_mock.K_ESCAPE = 27
    pygame_mock.K_SPACE = 32
    pygame_mock.K_UP = 273
    pygame_mock.K_DOWN = 274
    pygame_mock.K_LEFT = 276
    pygame_mock.K_RIGHT = 275
    pygame_mock.K_i = 105
    pygame_mock.K_m = 109
    pygame_mock.K_r = 114
    pygame_mock.K_F1 = 282
    pygame_mock.K_F12 = 293
    pygame_mock.key.name = MagicMock(return_value="test_key")
    sys.modules['pygame'] = pygame_mock

# 模擬依賴模組
class MockGameState:
    def __init__(self):
        self.current_state = "exploration"
        self.player_stats = {"hp": 100, "max_hp": 100, "attack": 10, "defense": 5, "level": 1, "exp": 0}
        self.enemies = [{"name": "Test Enemy", "hp": 30, "attack": 8, "defense": 2}]
        self.flags = {}
    
    def set_state(self, state):
        self.current_state = state
    
    def get_flag(self, flag):
        return self.flags.get(flag, False)
    
    def set_flag(self, flag, value):
        self.flags[flag] = value
    
    def add_exp(self, exp):
        self.player_stats["exp"] += exp