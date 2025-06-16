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
    
    # Player 模擬
    class MockPlayer:
        def __init__(self, x=400, y=300):
            self.x = x
            self.y = y
            self.is_moving = False
            self.move_target_x = x
            self.move_target_y = y
        
        def update(self):
            pass
        
        def render(self, screen):
            pass
        
        def move(self, dx, dy):
            if not self.is_moving:
                self.move_target_x = self.x + dx
                self.move_target_y = self.y + dy
                self.is_moving = True
                return True
            return False
        
        def set_position(self, x, y):
            self.x = x
            self.y = y
            self.move_target_x = x
            self.move_target_y = y
            self.is_moving = False
        
        def reset(self):
            self.set_position(400, 300)
        
        def force_stop_movement(self):
            self.is_moving = False
            self.move_target_x = self.x
            self.move_target_y = self.y

    # UI 模擬
    class MockUI:
        def __init__(self, screen):
            self.screen = screen
            self.show_inventory = False
            self.show_map = False
            self.dialogue_active = False
            self.dialogue_options = []
            self.has_keycard = False
            self.has_antidote = False
            self.game_completed = False
            self.game_over = False
            self.player = None
            self.game_state = None
            self.inventory = None
        
        def render(self, game_state, player, inventory):
            pass
        
        def set_player_reference(self, player):
            self.player = player
        
        def set_game_state_reference(self, game_state):
            self.game_state = game_state
        
        def set_inventory_reference(self, inventory):
            self.inventory = inventory
        
        def toggle_inventory(self):
            self.show_inventory = not self.show_inventory
        
        def toggle_map(self):
            self.show_map = not self.show_map
        
        def is_any_ui_open(self):
            return self.show_inventory or self.show_map or self.dialogue_active
        
        def close_all_ui(self):
            self.show_inventory = False
            self.show_map = False
            self.dialogue_active = False
        
        def get_ui_status(self):
            return f"inventory={self.show_inventory}, map={self.show_map}, dialogue={self.dialogue_active}"
        
        def show_message(self, message):
            pass
        
        def start_dialogue(self, dialogue_info):
            self.dialogue_active = True
        
        def select_dialogue_option(self, index):
            pass
        
        def continue_dialogue(self):
            pass
        
        def reset_game(self):
            self.show_inventory = False
            self.show_map = False
            self.dialogue_active = False
            self.has_keycard = False
            self.has_antidote = False
            self.game_completed = False
            self.game_over = False

    # CombatSystem 模擬
    class MockCombatSystem:
        def __init__(self):
            self.in_combat = False
            self.combat_result = None
            self.current_enemy = None
            self.player_turn = True
            self.animation_timer = 0
            self.combat_log = []
        
        def start_combat(self, enemy):
            self.in_combat = True
            self.current_enemy = enemy.copy()
            self.combat_result = None
            self.player_turn = True
            self.combat_log = [f"遭遇 {enemy['name']}！"]
        
        def update(self, game_state):
            if self.animation_timer > 0:
                self.animation_timer -= 1
        
        def render(self, screen, game_state):
            pass
        
        def player_action(self, action):
            if not self.in_combat or not self.player_turn or self.combat_result:
                return None
            
            if action == "attack":
                self.combat_result = "win"  # 簡化測試
            elif action == "escape":
                self.combat_result = "escape"
            elif action == "defend":
                pass
            
            self.player_turn = False