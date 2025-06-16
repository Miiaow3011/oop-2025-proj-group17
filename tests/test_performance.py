import sys
import os
import time
import pytest
from unittest.mock import Mock, patch, MagicMock
import gc
import psutil
import threading

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
    pygame_mock.event.get = MagicMock(return_value=[])
    sys.modules['pygame'] = pygame_mock