import sys
import os
import pytest
from unittest.mock import Mock, patch, MagicMock, create_autospec
import time

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 完整模擬 pygame
pygame_mock = MagicMock()
pygame_mock.init = MagicMock()
pygame_mock.display.set_mode = MagicMock(return_value=MagicMock())
pygame_mock.display.set_caption = MagicMock()
pygame_mock.display.flip = MagicMock()
pygame_mock.time.Clock = MagicMock(return_value=MagicMock())
pygame_mock.event.get = MagicMock(return_value=[])
pygame_mock.draw.rect = MagicMock()
pygame_mock.Rect = MagicMock(return_value=MagicMock())
pygame_mock.QUIT = 12
pygame_mock.KEYDOWN = 2
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
pygame_mock.K_1 = 49
pygame_mock.K_2 = 50
pygame_mock.K_3 = 51
pygame_mock.key.name = MagicMock(return_value="test_key")
pygame_mock.quit = MagicMock()
sys.modules['pygame'] = pygame_mock

# 在導入 main 之前設置所有必要的模擬
def setup_mocks():
    """設置所有必要的模擬對象"""
    
    # GameState 模擬
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
    
    # MapManager 模擬
    class MockMapManager:
        def __init__(self):
            self.current_floor = 1
            self.use_sprites = False
            self.use_floor_sprites = False
            self.use_shop_sprites = False
            self.debug_show_combat_zones = False
            self.collected_items = set()
        
        def render(self, screen):
            pass
        
        def update(self):
            pass
        
        def get_current_floor(self):
            return self.current_floor
        
        def check_interaction(self, x, y, floor):
            return None
        
        def check_item_pickup(self, x, y, floor):
            return None
        
        def check_combat_zone(self, x, y, floor):
            return None
        
        def change_floor(self, floor):
            self.current_floor = floor
        
        def debug_print_stairs(self):
            pass
        
        def debug_print_floor_info(self):
            pass
        
        def debug_print_items(self):
            pass
        
        def debug_print_combat_zones(self):
            pass
        
        def debug_print_shop_info(self):
            pass
        
        def reload_stairs_images(self):
            pass
        
        def reload_floor_images(self):
            pass
        
        def reload_shop_images(self):
            pass
        
        def reset_items(self):
            self.collected_items.clear()
        
        def toggle_combat_zone_debug(self):
            self.debug_show_combat_zones = not self.debug_show_combat_zones
            return self.debug_show_combat_zones
        
        def collect_item(self, item_id):
            self.collected_items.add(item_id)
        
        def remove_combat_zone(self, zone, floor):
            pass
    