#!/usr/bin/env python3
"""
遊戲診斷工具
逐步檢查每個模組的初始化過程
"""

import sys
import traceback

def test_imports():
    """測試所有模組的導入"""
    print("🔍 測試模組導入...")
    
    modules_to_test = [
        ("pygame", "pygame"),
        ("遊戲狀態", "game_state"),
        ("地圖管理", "map_manager"), 
        ("玩家", "player"),
        ("使用者介面", "ui"),
        ("戰鬥系統", "combat"),
        ("背包系統", "inventory"),
        ("字體管理", "font_manager"),
    ]
    
    for name, module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {name} 模組導入成功")
        except Exception as e:
            print(f"❌ {name} 模組導入失敗: {e}")
            traceback.print_exc()
            return False
    
    return True

def test_pygame_init():
    """測試Pygame初始化"""
    print("\n🔍 測試Pygame初始化...")
    
    try:
        import pygame
        pygame.init()
        print("✅ Pygame初始化成功")
        
        # 測試顯示器
        screen = pygame.display.set_mode((800, 600))
        print("✅ 顯示器創建成功")
        
        pygame.display.set_caption("診斷測試")
        print("✅ 視窗標題設定成功")
        
        pygame.quit()
        print("✅ Pygame正常關閉")
        return True
        
    except Exception as e:
        print(f"❌ Pygame初始化失敗: {e}")
        traceback.print_exc()
        return False

def test_font_manager():
    """測試字體管理器"""
    print("\n🔍 測試字體管理器...")
    
    try:
        from font_manager import font_manager
        print("✅ 字體管理器導入成功")
        
        # 測試字體安裝檢查
        result = font_manager.install_chinese_font()
        if result:
            print("✅ 中文字體檢查通過")
        else:
            print("⚠️ 中文字體檢查未通過，但可能不影響遊戲運行")
        
        # 測試字體渲染
        import pygame
        pygame.init()
        test_surface = font_manager.render_text("測試", 24, (255, 255, 255))
        print("✅ 文字渲染測試成功")
        pygame.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ 字體管理器測試失敗: {e}")
        traceback.print_exc()
        return False

def test_game_components():
    """測試遊戲組件初始化"""
    print("\n🔍 測試遊戲組件初始化...")
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        # 測試各個組件
        print("正在測試遊戲狀態...")
        from game_state import GameState
        game_state = GameState()
        print("✅ 遊戲狀態創建成功")
        
        print("正在測試地圖管理器...")
        from map_manager import MapManager
        map_manager = MapManager()
        print("✅ 地圖管理器創建成功")
        
        print("正在測試玩家...")
        from player import Player
        player = Player(x=400, y=300)
        print("✅ 玩家創建成功")
        
        print("正在測試UI系統...")
        from ui import UI
        ui = UI(screen)
        print("✅ UI系統創建成功")
        
        print("正在測試戰鬥系統...")
        from combat import CombatSystem
        combat_system = CombatSystem()
        print("✅ 戰鬥系統創建成功")
        
        print("正在測試背包系統...")
        from inventory import Inventory
        inventory = Inventory()
        print("✅ 背包系統創建成功")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 遊戲組件測試失敗: {e}")
        traceback.print_exc()
        return False

def test_main_game():
    """測試主遊戲類別"""
    print("\n🔍 測試主遊戲類別...")
    
    try:
        from main import Game
        print("✅ Game類別導入成功")
        
        print("正在創建Game實例...")
        game = Game()
        print("✅ Game實例創建成功")
        
        # 檢查關鍵屬性
        print("檢查遊戲屬性...")
        assert hasattr(game, 'screen'), "缺少screen屬性"
        assert hasattr(game, 'game_state'), "缺少game_state屬性"
        assert hasattr(game, 'player'), "缺少player屬性"
        print("✅ 遊戲屬性檢查通過")
        
        return True
        
    except Exception as e:
        print(f"❌ 主遊戲測試失敗: {e}")
        traceback.print_exc()
        return False

def test_simple_run():
    """測試簡單運行"""
    print("\n🔍 測試遊戲簡單運行...")
    
    try:
        from main import Game
        game = Game()
        
        print("測試遊戲循環（2秒）...")
        import time
        start_time = time.time()
        
        # 運行短暫的遊戲循環
        while time.time() - start_time < 2.0:
            # 處理事件（但不處理退出）
            import pygame
            for event in pygame.event.get():
                if event.type != pygame.QUIT:
                    pass
            
            # 更新和渲染
            game.update()
            game.render()
            game.clock.tick(60)
        
        print("✅ 遊戲循環測試成功")
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 遊戲運行測試失敗: {e}")
        traceback.print_exc()
        return False

def main():
    """主診斷程序"""
    print("🏥 遊戲診斷工具啟動")
    print("=" * 50)
    
    all_tests = [
        ("模組導入", test_imports),
        ("Pygame初始化", test_pygame_init),
        ("字體管理器", test_font_manager),
        ("遊戲組件", test_game_components),
        ("主遊戲類別", test_main_game),
        ("簡單運行", test_simple_run)
    ]
    
    passed_tests = 0
    total_tests = len(all_tests)
    
    for test_name, test_func in all_tests:
        print(f"\n📋 執行測試: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed_tests += 1
                print(f"🎉 {test_name} 測試通過")
            else:
                print(f"💥 {test_name} 測試失敗")
                break
        except Exception as e:
            print(f"💥 {test_name} 測試異常: {e}")
            traceback.print_exc()
            break
    
    # 最終報告
    print("\n" + "=" * 50)
    print("🏁 診斷結果")
    print("=" * 50)
    print(f"通過測試: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 所有測試通過！遊戲應該可以正常運行。")
        print("\n建議:")
        print("- 直接運行: python3 main.py")
        print("- 如果還是沒有視窗，檢查是否有防火牆或顯示問題")
    elif passed_tests == 0:
        print("💥 基礎測試都未通過，有嚴重問題。")
        print("\n建議:")
        print("- 檢查Python環境")
        print("- 重新安裝pygame: pip install pygame")
        print("- 檢查所有遊戲檔案是否存在")
    else:
        print(f"⚠️ 部分測試未通過，問題出現在第{passed_tests+1}個測試。")
        print("\n建議:")
        print("- 查看上面的錯誤訊息")
        print("- 修復失敗的組件")
        print("- 重新運行診斷")
    
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n診斷被用戶中斷")
    except Exception as e:
        print(f"\n診斷工具本身發生錯誤: {e}")
        traceback.print_exc()