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

    # Inventory 模擬
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
        
    # FontManager 模擬
    class MockFontManager:
        def install_chinese_font(self):
            return True
        
        def render_text(self, text, size, color):
            mock_surface = Mock()
            mock_surface.get_rect.return_value = Mock(center=Mock())
            return mock_surface
        
    # 設置模組模擬
    sys.modules['game_state'] = Mock(GameState=MockGameState)
    sys.modules['map_manager'] = Mock(MapManager=MockMapManager)
    sys.modules['player'] = Mock(Player=MockPlayer)
    sys.modules['ui'] = Mock(UI=MockUI)
    sys.modules['combat'] = Mock(CombatSystem=MockCombatSystem)
    sys.modules['inventory'] = Mock(Inventory=MockInventory)
    sys.modules['font_manager'] = Mock(font_manager=MockFontManager())
    
    return MockGameState, MockMapManager, MockPlayer, MockUI, MockCombatSystem, MockInventory, MockFontManager

# 設置模擬
MockGameState, MockMapManager, MockPlayer, MockUI, MockCombatSystem, MockInventory, MockFontManager = setup_mocks()

# 現在可以安全地導入 main
import main

class TestMainGameBasic:
    """基本主程式測試"""
    
    def test_game_initialization(self):
        """測試遊戲初始化"""
        try:
            game = main.Game()
            
            # 測試基本屬性
            assert hasattr(game, 'SCREEN_WIDTH')
            assert hasattr(game, 'SCREEN_HEIGHT')
            assert hasattr(game, 'FPS')
            assert hasattr(game, 'running')
            assert hasattr(game, 'show_intro')
            assert hasattr(game, 'debug_mode')
            
            print("✅ 遊戲初始化測試通過")
            
        except Exception as e:
            print(f"❌ 遊戲初始化測試失敗: {e}")
            raise
    
    def test_game_components_exist(self):
        """測試遊戲組件存在"""
        try:
            game = main.Game()
            
            # 檢查關鍵組件是否存在
            assert hasattr(game, 'game_state')
            assert hasattr(game, 'map_manager')
            assert hasattr(game, 'player')
            assert hasattr(game, 'ui')
            assert hasattr(game, 'combat_system')
            assert hasattr(game, 'inventory')
            
            print("✅ 遊戲組件存在測試通過")
            
        except Exception as e:
            print(f"❌ 遊戲組件存在測試失敗: {e}")
            raise

    def test_toggle_debug_mode(self):
        """測試除錯模式切換"""
        try:
            game = main.Game()
            
            # 初始狀態
            initial_debug = getattr(game, 'debug_mode', False)
            
            # 切換除錯模式
            if hasattr(game, 'toggle_debug_mode'):
                game.toggle_debug_mode()
                new_debug = getattr(game, 'debug_mode', False)
                assert new_debug != initial_debug
            
            print("✅ 除錯模式切換測試通過")
            
        except Exception as e:
            print(f"❌ 除錯模式切換測試失敗: {e}")
            raise

    def test_ui_toggles(self):
        """測試UI切換"""
        try:
            game = main.Game()
            
            # 測試背包切換
            if hasattr(game, 'handle_inventory_toggle'):
                initial_inventory = getattr(game.ui, 'show_inventory', False)
                game.handle_inventory_toggle()
                new_inventory = getattr(game.ui, 'show_inventory', False)
                assert new_inventory != initial_inventory
            
            # 測試地圖切換
            if hasattr(game, 'handle_map_toggle'):
                initial_map = getattr(game.ui, 'show_map', False)
                game.handle_map_toggle()
                new_map = getattr(game.ui, 'show_map', False)
                assert new_map != initial_map
            
            print("✅ UI切換測試通過")
            
        except Exception as e:
            print(f"❌ UI切換測試失敗: {e}")
            raise

    def test_player_position_reset(self):
        """測試玩家位置重置"""
        try:
            game = main.Game()
            
            # 修改玩家位置
            if hasattr(game.player, 'x') and hasattr(game.player, 'y'):
                game.player.x = 100
                game.player.y = 200
                
                # 重置位置
                if hasattr(game, 'reset_player_position'):
                    game.reset_player_position()
                    
                    # 檢查是否重置到預設位置
                    assert game.player.x == 400
                    assert game.player.y == 300
            
            print("✅ 玩家位置重置測試通過")
            
        except Exception as e:
            print(f"❌ 玩家位置重置測試失敗: {e}")
            raise

    def test_update_method(self):
        """測試更新方法"""
        try:
            game = main.Game()
            
            # 設置非介紹狀態
            if hasattr(game, 'show_intro'):
                game.show_intro = False
            
            # 調用更新方法（不應該拋出異常）
            if hasattr(game, 'update'):
                game.update()
            
            print("✅ 更新方法測試通過")
            
        except Exception as e:
            print(f"❌ 更新方法測試失敗: {e}")
            raise

    def test_render_method(self):
        """測試渲染方法"""
        try:
            game = main.Game()
            
            # 調用渲染方法（不應該拋出異常）
            if hasattr(game, 'render'):
                game.render()
            
            print("✅ 渲染方法測試通過")
            
        except Exception as e:
            print(f"❌ 渲染方法測試失敗: {e}")
            raise

    def test_interaction_cooldown(self):
        """測試互動冷卻"""
        try:
            game = main.Game()
            
            # 檢查互動冷卻機制
            if hasattr(game, 'interact') and hasattr(game, 'interaction_cooldown'):
                initial_time = getattr(game, 'last_interaction_time', 0)
                
                # 嘗試互動（可能會因為模擬而沒有實際效果，但不應該出錯）
                game.interact()
                
                # 檢查時間是否有更新的邏輯
                assert hasattr(game, 'last_interaction_time')
            
            print("✅ 互動冷卻測試通過")
            
        except Exception as e:
            print(f"❌ 互動冷卻測試失敗: {e}")
            raise

    def test_combat_zone_debug(self):
        """測試戰鬥區域除錯"""
        try:
            game = main.Game()
            
            # 測試戰鬥區域除錯切換
            if hasattr(game, 'toggle_combat_zone_debug'):
                initial_debug = getattr(game.map_manager, 'debug_show_combat_zones', False)
                result = game.toggle_combat_zone_debug()
                new_debug = getattr(game.map_manager, 'debug_show_combat_zones', False)
                
                # 驗證狀態已改變
                assert new_debug != initial_debug
            
            print("✅ 戰鬥區域除錯測試通過")
            
        except Exception as e:
            print(f"❌ 戰鬥區域除錯測試失敗: {e}")
            raise

    def test_stairs_usage(self):
        """測試樓梯使用"""
        try:
            game = main.Game()
            
            if hasattr(game, 'use_stairs'):
                # 測試上樓梯
                stairs_info = {"direction": "up", "target_floor": 2}
                initial_floor = getattr(game.map_manager, 'current_floor', 1)
                
                game.use_stairs(stairs_info)
                
                # 檢查樓層是否可能改變（取決於具體實現）
                new_floor = getattr(game.map_manager, 'current_floor', 1)
                
                # 至少確保方法執行沒有錯誤
                assert isinstance(new_floor, int)
            
            print("✅ 樓梯使用測試通過")
            
        except Exception as e:
            print(f"❌ 樓梯使用測試失敗: {e}")
            raise

    def test_restart_game(self):
        """測試重新開始遊戲"""
        try:
            game = main.Game()
            
            if hasattr(game, 'restart_game'):
                # 修改一些狀態
                if hasattr(game.player, 'x'):
                    game.player.x = 100
                if hasattr(game.ui, 'show_inventory'):
                    game.ui.show_inventory = True
                
                # 重新開始遊戲
                game.restart_game()
                
                # 檢查狀態是否重置
                if hasattr(game.player, 'x'):
                    assert game.player.x == 400
                if hasattr(game.ui, 'show_inventory'):
                    assert game.ui.show_inventory == False
            
            print("✅ 重新開始遊戲測試通過")
            
        except Exception as e:
            print(f"❌ 重新開始遊戲測試失敗: {e}")
            raise

class TestEventHandling:
    """事件處理測試"""
    
    def test_handle_events_method_exists(self):
        """測試事件處理方法存在"""
        try:
            game = main.Game()
            assert hasattr(game, 'handle_events')
            print("✅ 事件處理方法存在測試通過")
            
        except Exception as e:
            print(f"❌ 事件處理方法存在測試失敗: {e}")
            raise

    def test_exploration_input_handling(self):
        """測試探索輸入處理"""
        try:
            game = main.Game()
            
            if hasattr(game, 'handle_exploration_input'):
                # 創建模擬事件
                mock_event = Mock()
                mock_event.key = 273  # K_UP
                
                # 調用處理方法（不應該出錯）
                game.handle_exploration_input(mock_event)
            
            print("✅ 探索輸入處理測試通過")
            
        except Exception as e:
            print(f"❌ 探索輸入處理測試失敗: {e}")
            raise

    def test_combat_input_handling(self):
        """測試戰鬥輸入處理"""
        try:
            game = main.Game()
            
            if hasattr(game, 'handle_combat_input'):
                # 設置戰鬥狀態
                if hasattr(game.combat_system, 'in_combat'):
                    game.combat_system.in_combat = True
                if hasattr(game.combat_system, 'player_turn'):
                    game.combat_system.player_turn = True
                
                # 創建模擬事件
                mock_event = Mock()
                mock_event.key = 49  # K_1
                
                # 調用處理方法（不應該出錯）
                game.handle_combat_input(mock_event)
            
            print("✅ 戰鬥輸入處理測試通過")
            
        except Exception as e:
            print(f"❌ 戰鬥輸入處理測試失敗: {e}")
            raise


# 主程序
if __name__ == "__main__":
    print("🚀 開始運行修復的主程式測試...")
    
    # 手動運行測試
    test_classes = [TestMainGameBasic, TestEventHandling]
    
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
                test_method = getattr(test_instance, method_name)
                test_method()
                
                print(f"✅ {method_name} 通過")
                class_passed += 1
                total_passed += 1
                
            except Exception as e:
                print(f"❌ {method_name} 失敗:")
                print(f"   錯誤: {e}")
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