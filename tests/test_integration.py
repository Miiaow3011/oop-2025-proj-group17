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

class TestGameIntegration:
    """遊戲整合測試 - 測試各系統間的互動"""
    
    def setup_method(self):
        """設置測試環境"""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'), \
             patch('main.font_manager'):
            import main
            self.game_class = main.Game

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_complete_game_flow(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試完整遊戲流程"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        
        # 1. 開始時應該顯示介紹
        assert game.show_intro == True
        assert game.game_state.current_state == "exploration"
        
        # 2. 跳過介紹
        game.show_intro = False
        
        # 3. 測試玩家移動
        initial_x = game.player.x
        game.player.move(32, 0)
        assert game.player.move_target_x == initial_x + 32
        
        # 4. 測試UI切換
        game.handle_inventory_toggle()
        assert game.ui.show_inventory == True
        
        game.handle_map_toggle()
        assert game.ui.show_map == True
        
        # 5. 測試強制重置
        game.force_exploration_state()
        assert game.ui.show_inventory == False
        assert game.ui.show_map == False
        assert game.game_state.current_state == "exploration"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_player_movement_and_interaction(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試玩家移動和互動"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試移動
        original_x = game.player.x
        original_y = game.player.y
        
        # 向右移動
        success = game.player.move(32, 0)
        assert success == True
        assert game.player.move_target_x == original_x + 32
        
        # 完成移動
        game.player.x = game.player.move_target_x
        game.player.y = game.player.move_target_y
        game.player.is_moving = False
        
        # 向上移動
        success = game.player.move(0, -32)
        assert success == True
        assert game.player.move_target_y == original_y - 32

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    @patch('time.time')
    def test_interaction_cooldown_system(self, mock_time, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試互動冷卻系統"""
        mock_font.install_chinese_font.return_value = True
        mock_time.side_effect = [0, 0.2, 0.6, 1.2]  # 模擬時間進行
        
        game = self.game_class()
        game.show_intro = False
        
        # 第一次互動
        game.interact()
        first_interaction_time = game.last_interaction_time
        
        # 立即第二次互動（應該被冷卻阻止）
        game.interact()
        # 時間不應該更新（因為被冷卻阻止）
        
        # 等待冷卻時間後互動
        game.interact()
        # 現在應該能夠互動

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_floor_navigation_system(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試樓層導航系統"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 初始在1樓
        assert game.map_manager.current_floor == 1
        
        # 上2樓（自由通行）
        stairs_up = {"direction": "up", "target_floor": 2}
        game.use_stairs(stairs_up)
        assert game.map_manager.current_floor == 2
        assert game.player.x == 450
        assert game.player.y == 600
        
        # 嘗試上3樓（需要鑰匙卡）
        stairs_up_3f = {"direction": "up", "target_floor": 3}
        game.use_stairs(stairs_up_3f)
        assert game.map_manager.current_floor == 2  # 應該還在2樓
        
        # 給予鑰匙卡並再次嘗試
        game.ui.has_keycard = True
        game.use_stairs(stairs_up_3f)
        assert game.map_manager.current_floor == 3
        
        # 下樓測試
        stairs_down = {"direction": "down", "target_floor": 2}
        game.use_stairs(stairs_down)
        assert game.map_manager.current_floor == 2
        assert game.player.x == 450
        assert game.player.y == 100

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_combat_system_integration(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥系統整合"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 模擬進入戰鬥區域
        combat_zone = {
            "name": "測試戰鬥區域",
            "enemies": ["zombie_student"]
        }
        
        # 開始戰鬥
        game.start_combat_in_zone(combat_zone)
        
        assert game.game_state.current_state == "combat"
        assert game.combat_system.in_combat == True
        assert hasattr(game, 'current_combat_zone')
        
        # 模擬戰鬥行動
        game.combat_system.combat_result = "win"
        
        # 處理戰鬥結束
        game.handle_combat_end()
        
        assert game.game_state.current_state == "exploration"
        assert game.combat_system.in_combat == False
        assert game.combat_system.combat_result == None

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_item_collection_system(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試物品收集系統整合"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試收集不同類型的物品
        items_to_test = [
            {
                "item": {"name": "醫療包", "type": "healing", "value": 20},
                "item_id": "healing_1"
            },
            {
                "item": {"name": "鑰匙卡", "type": "key"},
                "item_id": "key_1"
            },
            {
                "item": {"name": "解藥", "type": "special"},
                "item_id": "special_1"
            }
        ]
        
        initial_exp = game.game_state.player_stats["exp"]
        
        for item_pickup in items_to_test:
            game.collect_item_new(item_pickup)
            
            # 檢查物品是否添加到背包
            assert item_pickup["item"]["name"] in [item["name"] for item in game.inventory.items]
            
            # 檢查物品是否標記為已收集
            assert item_pickup["item_id"] in game.map_manager.collected_items
        
        # 檢查經驗值是否增加
        assert game.game_state.player_stats["exp"] > initial_exp
        
        # 檢查特殊物品標記
        assert game.ui.has_keycard == True
        assert game.ui.has_antidote == True

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_ui_state_management(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試UI狀態管理"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試UI狀態切換
        assert game.ui.is_any_ui_open() == False
        
        # 開啟背包
        game.handle_inventory_toggle()
        assert game.ui.show_inventory == True
        assert game.ui.is_any_ui_open() == True
        
        # 開啟地圖（背包應該還開著）
        game.handle_map_toggle()
        assert game.ui.show_map == True
        assert game.ui.show_inventory == True
        assert game.ui.is_any_ui_open() == True
        
        # 關閉所有UI
        game.ui.close_all_ui()
        assert game.ui.show_inventory == False
        assert game.ui.show_map == False
        assert game.ui.dialogue_active == False
        assert game.ui.is_any_ui_open() == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_debug_mode_functionality(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試除錯模式功能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試除錯模式切換
        assert game.debug_mode == False
        assert game.map_manager.debug_show_combat_zones == False
        
        # 開啟除錯模式
        game.toggle_debug_mode()
        assert game.debug_mode == True
        
        # 測試戰鬥區域除錯切換
        game.toggle_combat_zone_debug()
        assert game.map_manager.debug_show_combat_zones == True
        
        game.toggle_combat_zone_debug()
        assert game.map_manager.debug_show_combat_zones == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_game_restart_functionality(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試遊戲重新開始功能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 修改遊戲狀態
        game.player.x = 100
        game.player.y = 200
        game.map_manager.current_floor = 3
        game.ui.show_inventory = True
        game.ui.has_keycard = True
        game.ui.has_antidote = True
        game.map_manager.collected_items.add("test_item")
        game.inventory.add_item({"name": "測試物品", "type": "test"})
        
        # 重新開始遊戲
        game.restart_game()
        
        # 檢查狀態是否重置
        assert game.player.x == 400
        assert game.player.y == 300
        assert game.map_manager.current_floor == 1
        assert game.ui.show_inventory == False
        assert game.ui.has_keycard == False
        assert game.ui.has_antidote == False
        assert len(game.map_manager.collected_items) == 0
        assert len(game.inventory.items) == 0

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_event_handling_integration(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試事件處理整合"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試探索模式下的移動事件
        mock_event = Mock()
        mock_event.key = 273  # K_UP
        
        original_y = game.player.y
        game.handle_exploration_input(mock_event)
        
        assert game.player.is_moving == True
        assert game.player.move_target_y == original_y - 32
        
        # 測試戰鬥模式下的事件
        game.game_state.current_state = "combat"
        game.combat_system.in_combat = True
        game.combat_system.player_turn = True
        
        mock_combat_event = Mock()
        mock_combat_event.key = 49  # K_1 (攻擊)
        
        game.handle_combat_input(mock_combat_event)
        
        # 檢查戰鬥行動是否執行
        assert game.combat_system.player_turn == False

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_error_recovery_mechanisms(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試錯誤恢復機制"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 模擬錯誤狀態
        game.game_state.current_state = "invalid_state"
        game.player.is_moving = True
        game.ui.show_inventory = True
        game.ui.dialogue_active = True
        
        # 使用強制恢復
        game.force_exploration_state()
        
        # 檢查是否恢復正常
        assert game.game_state.current_state == "exploration"
        assert game.player.is_moving == False
        assert game.ui.show_inventory == False
        assert game.ui.dialogue_active == False

# 主程序
if __name__ == "__main__":
    print("🚀 開始運行整合測試...")
    
    # 獲取測試方法
    test_class = TestGameIntegration
    test_methods = [method for method in dir(test_class) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print(f"📦 整合測試類別: {test_class.__name__}")
    print("=" * 60)
    
    for method_name in test_methods:
        try:
            print(f"🧪 運行測試: {method_name}")
            
            # 創建測試實例並運行測試
            test_instance = test_class()
            test_instance.setup_method()
            test_method = getattr(test_instance, method_name)
            test_method()
            
            print(f"✅ {method_name} 通過")
            passed += 1
            
        except Exception as e:
            import traceback
            print(f"❌ {method_name} 失敗:")
            print(f"   錯誤: {e}")
            # 顯示簡化的錯誤訊息
            tb_lines = traceback.format_tb(e.__traceback__)
            for line in tb_lines[-2:]:
                print(f"   {line.strip()}")
            failed += 1
    
    print(f"\n📊 整合測試結果:")
    print(f"✅ 通過: {passed}")
    print(f"❌ 失敗: {failed}")
    if passed + failed > 0:
        print(f"📈 成功率: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有整合測試通過！")
        print("🔧 系統各組件之間的互動正常")
    else:
        print(f"\n⚠️  有 {failed} 個整合測試失敗")
        print("🔧 建議檢查系統組件間的互動邏輯")
    
    print("\n💡 你也可以用 pytest 運行:")
    print("   pytest tests/test_integration.py -v")
    print("   pytest tests/ -v  # 運行所有測試")