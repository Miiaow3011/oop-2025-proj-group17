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

class PerformanceTimer:
    """性能計時器"""
    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        gc.collect()  # 清理垃圾回收
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time
        print(f"⏱️  {self.name}: {self.duration:.4f} 秒")
    
    def get_duration(self):
        return self.duration if hasattr(self, 'duration') else None
    
class MemoryProfiler:
    """記憶體分析器"""
    def __init__(self, name):
        self.name = name
        self.start_memory = None
        self.end_memory = None
        self.process = psutil.Process() if 'psutil' in sys.modules else None
    
    def __enter__(self):
        gc.collect()
        if self.process:
            self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        return self
    
    def __exit__(self, *args):
        gc.collect()
        if self.process:
            self.end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            memory_diff = self.end_memory - self.start_memory
            print(f"🧠 {self.name}: {memory_diff:+.2f} MB (開始: {self.start_memory:.2f} MB, 結束: {self.end_memory:.2f} MB)")
    
    def get_memory_diff(self):
        if hasattr(self, 'end_memory') and self.start_memory:
            return self.end_memory - self.start_memory
        return 0