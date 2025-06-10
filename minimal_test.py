#!/usr/bin/env python3
"""
最小化遊戲測試
只測試基本的Pygame視窗
"""

import pygame
import sys

def minimal_test():
    """最基本的遊戲測試"""
    print("🔍 開始最小化測試...")
    
    try:
        # 初始化Pygame
        print("1. 初始化Pygame...")
        pygame.init()
        print("✅ Pygame初始化成功")
        
        # 創建視窗
        print("2. 創建視窗...")
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("最小化測試")
        print("✅ 視窗創建成功")
        
        # 創建時鐘
        print("3. 創建時鐘...")
        clock = pygame.time.Clock()
        print("✅ 時鐘創建成功")
        
        print("\n🎮 測試視窗已開啟！")
        print("- 你應該看到一個800x600的黑色視窗")
        print("- 按ESC或關閉視窗結束測試")
        print("- 如果沒有看到視窗，可能是顯示問題")
        
        # 主循環
        running = True
        frame_count = 0
        
        while running:
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("📝 用戶關閉視窗")
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("📝 用戶按下ESC")
                        running = False
            
            # 清除螢幕
            screen.fill((0, 0, 0))  # 黑色背景
            
            # 繪製一些測試內容
            frame_count += 1
            color_value = int((frame_count % 120) / 120 * 255)
            pygame.draw.circle(screen, (color_value, 100, 255-color_value), (400, 300), 50)
            
            # 更新顯示
            pygame.display.flip()
            clock.tick(60)
            
            # 每60幀輸出一次狀態（1秒）
            if frame_count % 60 == 0:
                print(f"📊 運行正常，已渲染 {frame_count} 幀")
        
        print("🏁 測試結束")
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_font_rendering():
    """測試字體渲染"""
    print("\n🔍 測試字體渲染...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("字體測試")
        
        # 測試基本字體
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Basic Font Test", True, (255, 255, 255))
        print("✅ 基本字體渲染成功")
        
        # 測試中文字體
        try:
            from font_manager import font_manager
            chinese_text = font_manager.render_text("中文測試", 24, (255, 255, 0))
            print("✅ 中文字體渲染成功")
        except:
            print("⚠️ 中文字體渲染失敗，但不影響基本功能")
        
        # 顯示測試
        clock = pygame.time.Clock()
        for i in range(180):  # 3秒測試
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            
            screen.fill((50, 50, 100))
            screen.blit(text_surface, (50, 50))
            
            try:
                screen.blit(chinese_text, (50, 100))
            except:
                pass
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        print("✅ 字體測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 字體測試失敗: {e}")
        return False

def main():
    """主測試程序"""
    print("🧪 最小化遊戲測試工具")
    print("=" * 40)
    
    # 基本視窗測試
    print("\n📋 測試1: 基本視窗功能")
    if not minimal_test():
        print("💥 基本視窗測試失敗，遊戲無法運行")
        return
    
    # 字體測試
    print("\n📋 測試2: 字體渲染")
    if not test_font_rendering():
        print("⚠️ 字體測試失敗，但遊戲可能仍可運行")
    
    print("\n🎉 測試完成！")
    print("如果你看到了測試視窗，說明Pygame工作正常")
    print("如果main.py還是無法運行，問題可能在遊戲邏輯中")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 測試工具異常: {e}")
        import traceback
        traceback.print_exc()