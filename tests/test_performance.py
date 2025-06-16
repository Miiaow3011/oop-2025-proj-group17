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
    
class TestGamePerformance:
    """遊戲性能測試"""
    
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
    def test_game_initialization_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試遊戲初始化性能"""
        mock_font.install_chinese_font.return_value = True
        
        with PerformanceTimer("遊戲初始化") as timer:
            with MemoryProfiler("遊戲初始化記憶體") as memory:
                game = self.game_class()
        
        # 初始化應該在合理時間內完成
        assert timer.get_duration() < 2.0, f"初始化時間過長: {timer.get_duration():.4f}秒"
        
        # 檢查基本屬性是否正確設置
        assert game.SCREEN_WIDTH == 1024
        assert game.SCREEN_HEIGHT == 768
        assert game.running == True

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_update_loop_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試更新循環性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試多次更新的性能
        iterations = 1000
        
        with PerformanceTimer(f"更新循環 ({iterations} 次)") as timer:
            for _ in range(iterations):
                game.update()
        
        avg_time = timer.get_duration() / iterations
        print(f"   平均單次更新時間: {avg_time*1000:.4f} 毫秒")
        
        # 單次更新應該非常快
        assert avg_time < 0.001, f"單次更新時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_render_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試渲染性能"""
        mock_font.install_chinese_font.return_value = True
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試多次渲染的性能
        iterations = 100
        
        with PerformanceTimer(f"渲染循環 ({iterations} 次)") as timer:
            for _ in range(iterations):
                game.render()
        
        avg_time = timer.get_duration() / iterations
        print(f"   平均單次渲染時間: {avg_time*1000:.4f} 毫秒")
        
        # 渲染應該在合理時間內完成
        assert avg_time < 0.1, f"單次渲染時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_player_movement_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試玩家移動性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試大量移動操作
        moves = 1000
        
        with PerformanceTimer(f"玩家移動 ({moves} 次)") as timer:
            for i in range(moves):
                # 模擬移動完成
                game.player.is_moving = False
                # 執行新移動
                direction = i % 4
                if direction == 0:
                    game.player.move(32, 0)
                elif direction == 1:
                    game.player.move(-32, 0)
                elif direction == 2:
                    game.player.move(0, 32)
                else:
                    game.player.move(0, -32)
        
        avg_time = timer.get_duration() / moves
        print(f"   平均單次移動時間: {avg_time*1000:.4f} 毫秒")
        
        # 移動操作應該非常快
        assert avg_time < 0.001, f"單次移動時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_ui_toggle_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試UI切換性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試UI切換性能
        toggles = 1000
        
        with PerformanceTimer(f"UI切換 ({toggles} 次背包 + {toggles} 次地圖)") as timer:
            for _ in range(toggles):
                game.handle_inventory_toggle()
                game.handle_map_toggle()
        
        avg_time = timer.get_duration() / (toggles * 2)
        print(f"   平均單次UI切換時間: {avg_time*1000:.4f} 毫秒")
        
        # UI切換應該很快
        assert avg_time < 0.001, f"UI切換時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_combat_system_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試戰鬥系統性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試戰鬥開始性能
        combat_zone = {
            "name": "測試區域",
            "enemies": ["zombie_student"]
        }
        
        battles = 100
        
        with PerformanceTimer(f"戰鬥開始 ({battles} 次)") as timer:
            for _ in range(battles):
                game.start_combat_in_zone(combat_zone)
                # 立即結束戰鬥
                game.combat_system.combat_result = "win"
                game.handle_combat_end()
        
        avg_time = timer.get_duration() / battles
        print(f"   平均戰鬥開始+結束時間: {avg_time*1000:.4f} 毫秒")
        
        # 戰鬥開始應該很快
        assert avg_time < 0.01, f"戰鬥系統響應時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_item_collection_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試物品收集性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 測試大量物品收集
        items = 500
        
        with PerformanceTimer(f"物品收集 ({items} 個)") as timer:
            for i in range(items):
                item_pickup = {
                    "item": {"name": f"測試物品{i}", "type": "healing", "value": 10},
                    "item_id": f"test_item_{i}"
                }
                # 清空背包以避免滿背包影響性能測試
                if len(game.inventory.items) >= 10:
                    game.inventory.items.clear()
                
                game.collect_item_new(item_pickup)
        
        avg_time = timer.get_duration() / items
        print(f"   平均單次物品收集時間: {avg_time*1000:.4f} 毫秒")
        
        # 物品收集應該很快
        assert avg_time < 0.001, f"物品收集時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_memory_usage_stability(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試記憶體使用穩定性"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        initial_memory = None
        if 'psutil' in sys.modules:
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024
        
        # 執行大量操作來測試記憶體穩定性
        operations = 1000
        
        with MemoryProfiler("記憶體穩定性測試") as memory:
            for i in range(operations):
                # 模擬各種遊戲操作
                game.update()
                game.player.move(32, 0)
                game.player.is_moving = False
                game.handle_inventory_toggle()
                game.handle_inventory_toggle()
                
                # 每100次操作進行一次垃圾回收
                if i % 100 == 0:
                    gc.collect()
        
        memory_growth = memory.get_memory_diff()
        
        # 記憶體增長應該是有限的
        if memory_growth > 0:
            print(f"   記憶體增長: {memory_growth:.2f} MB")
            # 記憶體增長應該小於50MB
            assert memory_growth < 50, f"記憶體洩漏可能性: 增長了 {memory_growth:.2f} MB"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_event_handling_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試事件處理性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 創建模擬事件
        mock_events = []
        for i in range(1000):
            mock_event = Mock()
            mock_event.type = 2  # KEYDOWN
            mock_event.key = 273 + (i % 4)  # 方向鍵
            mock_events.append(mock_event)
        
        with PerformanceTimer("事件處理 (1000 個事件)") as timer:
            with patch('pygame.event.get', return_value=mock_events):
                game.handle_events()
        
        avg_time = timer.get_duration() / len(mock_events)
        print(f"   平均單個事件處理時間: {avg_time*1000:.4f} 毫秒")
        
        # 事件處理應該很快
        assert avg_time < 0.001, f"事件處理時間過長: {avg_time*1000:.4f}毫秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_concurrent_operations_performance(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試並發操作性能（模擬多線程場景）"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        def worker_function(worker_id, iterations):
            """工作線程函數"""
            for i in range(iterations):
                # 模擬遊戲操作
                game.update()
                time.sleep(0.001)  # 模擬實際遊戲幀間隔
        
        workers = 3
        iterations_per_worker = 100
        
        with PerformanceTimer(f"並發操作 ({workers} 線程 x {iterations_per_worker} 次)") as timer:
            threads = []
            for i in range(workers):
                thread = threading.Thread(target=worker_function, args=(i, iterations_per_worker))
                threads.append(thread)
            
            # 啟動所有線程
            for thread in threads:
                thread.start()
            
            # 等待所有線程完成
            for thread in threads:
                thread.join()
        
        total_operations = workers * iterations_per_worker
        avg_time = timer.get_duration() / total_operations
        print(f"   平均每操作時間: {avg_time*1000:.4f} 毫秒")
        
        # 並發操作不應該顯著降低性能
        assert timer.get_duration() < 30.0, f"並發操作總時間過長: {timer.get_duration():.4f}秒"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_fps_simulation(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試FPS模擬性能"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        target_fps = 60
        frames = 300  # 模擬5秒
        frame_time = 1.0 / target_fps
        
        with PerformanceTimer(f"FPS模擬 ({frames} 幀，目標 {target_fps} FPS)") as timer:
            for frame in range(frames):
                frame_start = time.perf_counter()
                
                # 模擬一幀的操作
                game.update()
                game.render()
                
                frame_end = time.perf_counter()
                frame_duration = frame_end - frame_start
                
                # 如果幀時間太短，等待以維持目標FPS
                if frame_duration < frame_time:
                    time.sleep(frame_time - frame_duration)
        
        actual_fps = frames / timer.get_duration()
        print(f"   實際FPS: {actual_fps:.2f}")
        print(f"   目標FPS: {target_fps}")
        print(f"   FPS達成率: {(actual_fps/target_fps)*100:.1f}%")
        
        # 實際FPS應該接近目標FPS
        assert actual_fps >= target_fps * 0.8, f"FPS性能不足: 實際 {actual_fps:.2f}, 目標 {target_fps}"

class TestStressTests:
    """壓力測試"""
    
    def setup_method(self):
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
    def test_long_running_stability(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試長時間運行穩定性"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 模擬長時間運行
        duration = 10  # 10秒
        start_time = time.time()
        frame_count = 0
        
        with MemoryProfiler("長時間運行穩定性") as memory:
            while time.time() - start_time < duration:
                game.update()
                game.render()
                frame_count += 1
                
                # 每秒進行一次垃圾回收
                if frame_count % 60 == 0:
                    gc.collect()
        
        actual_duration = time.time() - start_time
        avg_fps = frame_count / actual_duration
        
        print(f"   運行時間: {actual_duration:.2f} 秒")
        print(f"   總幀數: {frame_count}")
        print(f"   平均FPS: {avg_fps:.2f}")
        
        memory_growth = memory.get_memory_diff()
        if memory_growth > 0:
            print(f"   記憶體增長: {memory_growth:.2f} MB")
            # 長時間運行記憶體增長應該有限
            assert memory_growth < 100, f"長時間運行記憶體洩漏: {memory_growth:.2f} MB"

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('main.font_manager')
    def test_extreme_load(self, mock_font, mock_clock, mock_caption, mock_display, mock_init):
        """測試極限負載"""
        mock_font.install_chinese_font.return_value = True
        
        game = self.game_class()
        game.show_intro = False
        
        # 創建極限負載場景
        extreme_operations = 10000
        
        with PerformanceTimer(f"極限負載測試 ({extreme_operations} 次複合操作)") as timer:
            for i in range(extreme_operations):
                # 複合操作
                game.update()
                game.player.move(32, 0)
                game.player.is_moving = False
                game.handle_inventory_toggle()
                game.handle_map_toggle()
                game.ui.close_all_ui()
                
                # 每1000次操作清理一次
                if i % 1000 == 0:
                    gc.collect()
        
        avg_time = timer.get_duration() / extreme_operations
        print(f"   平均複合操作時間: {avg_time*1000:.4f} 毫秒")
        
        # 即使在極限負載下也應該保持響應
        assert avg_time < 0.01, f"極限負載下性能不足: {avg_time*1000:.4f}毫秒/操作"