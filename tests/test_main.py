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

class MockInventory:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        if len(self.items) < 10:  # 假設背包容量為10
            self.items.append(item)
            return True
        return False
    
    def get_items(self):
        return self.items
    
    def has_item(self, item_name):
        return any(item.get("name") == item_name for item in self.items)

class MockFontManager:
    def install_chinese_font(self):
        return True
    
    def render_text(self, text, size, color):
        mock_surface = Mock()
        mock_surface.get_rect.return_value = Mock(center=Mock())
        return mock_surface
    
# 模擬模組
sys.modules['game_state'] = Mock(GameState=MockGameState)
sys.modules['map_manager'] = Mock(MapManager=MockMapManager)
sys.modules['player'] = Mock(Player=MockPlayer)
sys.modules['ui'] = Mock(UI=MockUI)
sys.modules['combat'] = Mock(CombatSystem=MockCombatSystem)
sys.modules['inventory'] = Mock(Inventory=MockInventory)
sys.modules['font_manager'] = Mock(font_manager=MockFontManager())

class TestGame:
    """Game 類別的測試"""
    
    def setup_method(self):
        """每個測試方法執行前的設置"""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'):
            # 導入並創建遊戲實例
            import main
            self.game_class = main.Game
    
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_game_initialization(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試遊戲初始化"""
        mock_font.install_chinese_font.return_value = True
        mock_display.return_value = Mock()
        mock_clock.return_value = Mock()
        
        game = self.game_class()
        
        assert game.SCREEN_WIDTH == 1024
        assert game.SCREEN_HEIGHT == 768
        assert game.FPS == 60
        assert game.running == True
        assert game.show_intro == True
        assert game.debug_mode == False
        assert game.interaction_cooldown == 0.5

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_toggle_debug_mode(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試除錯模式切換"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        assert game.debug_mode == False
        
        game.toggle_debug_mode()
        assert game.debug_mode == True
        
        game.toggle_debug_mode()
        assert game.debug_mode == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_force_exploration_state(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試強制探索狀態"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 設置非探索狀態
        game.game_state.current_state = "combat"
        game.ui.show_inventory = True
        game.player.is_moving = True
        
        game.force_exploration_state()
        
        assert game.game_state.current_state == "exploration"
        assert game.ui.show_inventory == False
        assert game.ui.show_map == False
        assert game.ui.dialogue_active == False
        assert game.player.is_moving == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_inventory_toggle(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試背包切換"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        assert game.ui.show_inventory == False
        
        game.handle_inventory_toggle()
        assert game.ui.show_inventory == True
        
        game.handle_inventory_toggle()
        assert game.ui.show_inventory == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_map_toggle(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試地圖切換"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        assert game.ui.show_map == False
        
        game.handle_map_toggle()
        assert game.ui.show_map == True
        
        game.handle_map_toggle()
        assert game.ui.show_map == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_reset_player_position(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試重置玩家位置"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 設置玩家到其他位置
        game.player.x = 100
        game.player.y = 200
        
        game.reset_player_position()
        
        assert game.player.x == 400
        assert game.player.y == 300

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_toggle_combat_zone_debug(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥區域除錯切換"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        assert game.map_manager.debug_show_combat_zones == False
        
        game.toggle_combat_zone_debug()
        assert game.map_manager.debug_show_combat_zones == True
        
        game.toggle_combat_zone_debug()
        assert game.map_manager.debug_show_combat_zones == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    @patch('time.time')
    def test_interact_cooldown(self, mock_time, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試互動冷卻機制"""
        mock_font.install_chinese_font.return_value = True
        mock_time.side_effect = [0, 0.2, 0.6]  # 模擬時間序列
        
        game = self.game_class()
        game.last_interaction_time = 0
        
        # 第一次互動 - 應該成功
        game.interact()
        assert game.last_interaction_time == 0
        
        # 立即第二次互動 - 應該被冷卻阻止
        game.interact()
        # 由於冷卻，last_interaction_time 不應該更新
        
        # 等待冷卻時間後再次互動 - 應該成功
        game.interact()
        assert game.last_interaction_time == 0.6

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_use_stairs(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試樓梯使用"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 測試從1樓上2樓
        stairs_info = {"direction": "up", "target_floor": 2}
        game.map_manager.current_floor = 1
        
        game.use_stairs(stairs_info)
        
        assert game.map_manager.current_floor == 2
        assert game.player.x == 450
        assert game.player.y == 600

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_use_stairs_need_keycard(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試需要鑰匙卡的樓梯"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 測試從2樓上3樓（沒有鑰匙卡）
        stairs_info = {"direction": "up", "target_floor": 3}
        game.map_manager.current_floor = 2
        
        game.use_stairs(stairs_info)
        
        # 沒有鑰匙卡，應該還在2樓
        assert game.map_manager.current_floor == 2
        
        # 給玩家鑰匙卡
        game.ui.has_keycard = True
        
        game.use_stairs(stairs_info)
        
        # 有鑰匙卡，應該能上3樓
        assert game.map_manager.current_floor == 3

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_start_combat_in_zone(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試在戰鬥區域開始戰鬥"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        combat_zone = {
            "name": "危險區域",
            "enemies": ["zombie_student"]
        }
        
        game.start_combat_in_zone(combat_zone)
        
        assert game.game_state.current_state == "combat"
        assert game.combat_system.in_combat == True
        assert hasattr(game, 'current_combat_zone')
        assert game.current_combat_zone == combat_zone

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_combat_end_win(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥勝利結束"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 設置戰鬥狀態
        game.combat_system.combat_result = "win"
        game.combat_system.in_combat = True
        game.game_state.current_state = "combat"
        
        game.handle_combat_end()
        
        assert game.combat_system.in_combat == False
        assert game.combat_system.combat_result == None
        assert game.game_state.current_state == "exploration"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_collect_item_new(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試新的物品收集方法"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        item_pickup = {
            "item": {"name": "測試物品", "type": "healing", "value": 20},
            "item_id": "test_item_1"
        }
        
        # 確保背包有空間
        assert len(game.inventory.items) == 0
        
        game.collect_item_new(item_pickup)
        
        # 檢查物品是否添加到背包
        assert len(game.inventory.items) == 1
        assert game.inventory.items[0]["name"] == "測試物品"
        
        # 檢查物品是否標記為已收集
        assert "test_item_1" in game.map_manager.collected_items

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_restart_game(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試重新開始遊戲"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 修改一些狀態
        game.player.x = 100
        game.player.y = 200
        game.ui.show_inventory = True
        game.ui.has_keycard = True
        game.map_manager.current_floor = 3
        game.map_manager.collected_items.add("test_item")
        
        game.restart_game()
        
        # 檢查狀態是否重置
        assert game.player.x == 400
        assert game.player.y == 300
        assert game.ui.show_inventory == False
        assert game.ui.has_keycard == False
        assert game.map_manager.current_floor == 1
        assert len(game.map_manager.collected_items) == 0

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_get_item_exp_reward(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試物品經驗值獎勵計算"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 測試不同類型物品的經驗值
        healing_item = {"type": "healing"}
        key_item = {"type": "key"}
        special_item = {"type": "special"}
        unknown_item = {"type": "unknown"}
        
        assert game.get_item_exp_reward(healing_item) == 5
        assert game.get_item_exp_reward(key_item) == 20
        assert game.get_item_exp_reward(special_item) == 50
        assert game.get_item_exp_reward(unknown_item) == 3

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_exploration_input(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試探索模式輸入處理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 模擬按鍵事件
        mock_event = Mock()
        mock_event.key = 273  # pygame.K_UP
        
        original_y = game.player.y
        
        game.handle_exploration_input(mock_event)
        
        # 檢查玩家是否開始移動
        assert game.player.is_moving == True
        assert game.player.move_target_y == original_y - 32

class TestGameEvents:
    """測試遊戲事件處理"""
    
    def setup_method(self):
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'):
            import main
            self.game_class = main.Game

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_events_escape_key(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試ESC鍵處理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 設置戰鬥狀態
        game.game_state.current_state = "combat"
        game.combat_system.in_combat = True
        
        # 模擬ESC鍵事件
        mock_event = Mock()
        mock_event.type = 2  # pygame.KEYDOWN
        mock_event.key = 27  # pygame.K_ESCAPE
        
        with patch('pygame.event.get', return_value=[mock_event]):
            game.handle_events()
        
        # 檢查是否強制結束戰鬥
        assert game.game_state.current_state == "exploration"
        assert game.combat_system.in_combat == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_events_inventory_key(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試I鍵（背包）處理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 模擬I鍵事件
        mock_event = Mock()
        mock_event.type = 2  # pygame.KEYDOWN
        mock_event.key = 105  # pygame.K_i
        
        assert game.ui.show_inventory == False
        
        with patch('pygame.event.get', return_value=[mock_event]):
            game.handle_events()
        
        assert game.ui.show_inventory == True

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_events_debug_keys(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試除錯快捷鍵處理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 測試F1鍵（除錯模式切換）
        mock_event = Mock()
        mock_event.type = 2  # pygame.KEYDOWN
        mock_event.key = 282  # pygame.K_F1
        
        assert game.debug_mode == False
        
        with patch('pygame.event.get', return_value=[mock_event]):
            game.handle_events()
        
        assert game.debug_mode == True

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_handle_events_intro_space(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試介紹畫面空白鍵處理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = True
        
        # 模擬空白鍵事件
        mock_event = Mock()
        mock_event.type = 2  # pygame.KEYDOWN
        mock_event.key = 32  # pygame.K_SPACE
        
        with patch('pygame.event.get', return_value=[mock_event]):
            game.handle_events()
        
        assert game.show_intro == False

class TestGameUpdate:
    """測試遊戲更新邏輯"""
    
    def setup_method(self):
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'):
            import main
            self.game_class = main.Game

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_update_exploration_state(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試探索狀態更新"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        game.game_state.current_state = "exploration"
        
        # 模擬沒有UI開啟
        game.ui.show_inventory = False
        game.ui.show_map = False
        game.ui.dialogue_active = False
        
        game.update()
        
        # 檢查是否正常更新（沒有錯誤）
        assert game.game_state.current_state == "exploration"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_update_combat_state(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥狀態更新"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        game.game_state.current_state = "combat"
        game.combat_system.in_combat = True
        
        game.update()
        
        # 檢查戰鬥系統是否被更新
        assert game.game_state.current_state == "combat"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_update_intro_state(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試介紹狀態更新"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = True
        
        game.update()
        
        # 介紹狀態下不應該更新遊戲邏輯
        assert game.show_intro == True

class TestGameRender:
    """測試遊戲渲染邏輯"""
    
    def setup_method(self):
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'):
            import main
            self.game_class = main.Game

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    @patch('pygame.display.flip')
    def test_render_intro(self, mock_flip, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試介紹畫面渲染"""
        mock_font.install_chinese_font.return_value = True
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        
        game = self.game_class()
        game.show_intro = True
        
        game.render()
        
        # 檢查是否調用了畫面填充和翻轉
        mock_screen.fill.assert_called()
        mock_flip.assert_called()

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    @patch('pygame.display.flip')
    def test_render_exploration(self, mock_flip, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試探索畫面渲染"""
        mock_font.install_chinese_font.return_value = True
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        
        game = self.game_class()
        game.show_intro = False
        game.game_state.current_state = "exploration"
        
        game.render()
        
        # 檢查是否調用了畫面填充和翻轉
        mock_screen.fill.assert_called()
        mock_flip.assert_called()

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    @patch('pygame.display.flip')
    def test_render_combat(self, mock_flip, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥畫面渲染"""
        mock_font.install_chinese_font.return_value = True
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        
        game = self.game_class()
        game.show_intro = False
        game.game_state.current_state = "combat"
        
        game.render()
        
        # 檢查是否調用了畫面填充和翻轉
        mock_screen.fill.assert_called()
        mock_flip.assert_called()

# 主程序 - 在所有類別定義之後
if __name__ == "__main__":
    print("🚀 開始運行主程式測試...")
    
    # 手動運行每個測試類別
    test_classes = [TestGame, TestGameEvents, TestGameUpdate, TestGameRender]
    
    total_passed = 0
    total_failed = 0
    
    for test_class in test_classes:
        print(f"\n📦 測試類別: {test_class.__name__}")
        print("=" * 50)
        
        # 獲取測試方法
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        class_passed = 0
        class_failed = 0
        
        for method_name in test_methods:
            try:
                print(f"🧪 運行測試: {method_name}")
                
                # 創建測試實例並運行測試
                test_instance = test_class()
                test_instance.setup_method()
                test_method = getattr(test_instance, method_name)
                test_method()
                
                print(f"✅ {method_name} 通過")
                class_passed += 1
                total_passed += 1
                
            except Exception as e:
                import traceback
                print(f"❌ {method_name} 失敗:")
                print(f"   錯誤: {e}")
                if hasattr(e, '__traceback__'):
                    tb_lines = traceback.format_tb(e.__traceback__)
                    # 只顯示最後幾行錯誤訊息
                    for line in tb_lines[-2:]:
                        print(f"   {line.strip()}")
                class_failed += 1
                total_failed += 1
        
        print(f"\n📊 {test_class.__name__} 結果:")
        print(f"✅ 通過: {class_passed}")
        print(f"❌ 失敗: {class_failed}")
        if class_passed + class_failed > 0:
            print(f"📈 成功率: {class_passed/(class_passed+class_failed)*100:.1f}%")
    
    print(f"\n" + "=" * 70)
    print(f"📊 總體測試結果:")
    print(f"✅ 通過: {total_passed}")
    print(f"❌ 失敗: {total_failed}")
    if total_passed + total_failed > 0:
        print(f"📈 總成功率: {total_passed/(total_passed+total_failed)*100:.1f}%")
    
    if total_failed == 0:
        print("\n🎉 所有測試通過！")
    else:
        print(f"\n⚠️  有 {total_failed} 個測試失敗")
    
    print("\n💡 你也可以用 pytest 運行:")
    print("   pytest tests/test_main.py -v")
    print("   pytest tests/ -v  # 運行所有測試")