import sys
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
import time

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 模擬 pygame（如果需要）
if 'pygame' not in sys.modules:
    pygame_mock = MagicMock()
    pygame_mock.init = MagicMock()
    pygame_mock.display.set_mode = MagicMock(return_value=MagicMock())
    pygame_mock.display.set_caption = MagicMock()
    pygame_mock.time.Clock = MagicMock(return_value=MagicMock())
    pygame_mock.QUIT = 12
    pygame_mock.KEYDOWN = 2
    pygame_mock.K_SPACE = 32
    pygame_mock.K_UP = 273
    pygame_mock.K_DOWN = 274
    pygame_mock.K_LEFT = 276
    pygame_mock.K_RIGHT = 275
    pygame_mock.K_i = 105
    pygame_mock.K_m = 109
    pygame_mock.K_1 = 49
    pygame_mock.K_2 = 50
    pygame_mock.K_3 = 51
    pygame_mock.key.name = MagicMock(return_value="test_key")
    sys.modules['pygame'] = pygame_mock