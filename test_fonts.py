#!/usr/bin/env python3
"""
中文字體測試工具
用於檢測系統是否能正確顯示中文
"""

import pygame
import sys
import os

def test_font_display():
    """測試字體顯示"""
    print("=== 中文字體測試工具 ===\n")
    
    # 初始化pygame
    try:
        pygame.init()
        print("✅ Pygame初始化成功")
    except Exception as e:
        print(f"❌ Pygame初始化失敗: {e}")
        return False
    
    # 測試字體管理器
    try:
        from font_manager import font_manager
        print("✅ 字體管理器載入成功")
    except Exception as e:
        print(f"❌ 字體管理器載入失敗: {e}")
        return False
    
    # 檢查字體檢測結果
    print("\n--- 字體檢測結果 ---")
    font_manager.install_chinese_font()
    
    # 創建測試視窗
    try:
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("中文字體測試")
        print("✅ 測試視窗創建成功")
    except Exception as e:
        print(f"❌ 無法創建測試視窗: {e}")
        return False
    
    # 測試文字列表
    test_texts = [
        ("遊戲標題", "《末世第二餐廳》", 32),
        ("基本中文", "你好世界！歡迎來到遊戲", 24),
        ("遊戲內容", "殭屍、解藥、拯救世界", 20),
        ("繁體字", "臺灣、學生、餐廳", 20),
        ("標點符號", "「這是測試」：成功！", 18),
        ("數字混合", "第1樓 HP:100/100 Lv.5", 16),
    ]
    
    print(f"\n--- 文字渲染測試 ---")
    
    # 測試每個文字
    rendered_surfaces = []
    y_offset = 50
    
    for label, text, size in test_texts:
        try:
            # 渲染文字
            surface = font_manager.render_text(text, size, (255, 255, 255))
            
            # 檢查渲染結果
            if surface.get_width() > 0 and surface.get_height() > 0:
                print(f"✅ {label}: '{text}' (大小:{size}) - 渲染成功")
                rendered_surfaces.append((surface, 50, y_offset, label))
                y_offset += size + 10
            else:
                print(f"❌ {label}: '{text}' (大小:{size}) - 渲染失敗（空白）")
                
        except Exception as e:
            print(f"❌ {label}: '{text}' (大小:{size}) - 渲染錯誤: {e}")
    
    # 顯示測試結果
    print(f"\n--- 顯示測試結果 ---")
    
    # 繪製測試畫面
    screen.fill((40, 40, 40))  # 深灰背景
    
    # 標題
    title_surface = font_manager.render_text("中文字體測試", 28, (255, 255, 0))
    title_rect = title_surface.get_rect(center=(300, 25))
    screen.blit(title_surface, title_rect)
    
    # 繪製測試文字
    for surface, x, y, label in rendered_surfaces:
        screen.blit(surface, (x, y))
    
    # 說明文字
    info_texts = [
        "如果上方文字顯示正常，表示中文字體工作正常",
        "如果看到方塊字或亂碼，請安裝中文字體",
        "按任意鍵關閉視窗..."
    ]
    
    info_y = 320
    for info in info_texts:
        info_surface = font_manager.render_text(info, 14, (200, 200, 200))
        screen.blit(info_surface, (50, info_y))
        info_y += 20
    
    pygame.display.flip()
    
    # 等待用戶輸入
    print("測試視窗已開啟，請檢查中文是否正確顯示")
    print("按任意鍵關閉視窗...")
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
    
    pygame.quit()
    print("✅ 測試完成")
    return True

def check_font_files():
    """檢查字體檔案"""
    print("\n--- 字體檔案檢查 ---")
    
    font_dir = "assets/fonts"
    
    if not os.path.exists(font_dir):
        print(f"❌ 字體資料夾不存在: {font_dir}")
        print("建議: 執行 python setup.py 創建資料夾")
        return False
    
    font_files = []
    for file in os.listdir(font_dir):
        if file.lower().endswith(('.ttf', '.ttc', '.otf')):
            font_files.append(file)
    
    if font_files:
        print(f"✅ 找到 {len(font_files)} 個字體檔案:")
        for font_file in font_files:
            file_path = os.path.join(font_dir, font_file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  - {font_file} ({file_size:.1f} MB)")
    else:
        print(f"⚠️ {font_dir} 資料夾是空的")
        print("建議: 下載中文字體檔案並放入此資料夾")
    
    return len(font_files) > 0

def system_font_check():
    """檢查系統字體"""
    print("\n--- 系統字體檢查 ---")
    
    import platform
    system = platform.system()
    
    if system == "Windows":
        font_paths = [
            ("微軟正黑體", "C:/Windows/Fonts/msjh.ttc"),
            ("微軟雅黑", "C:/Windows/Fonts/msyh.ttc"),
            ("宋體", "C:/Windows/Fonts/simsun.ttc"),
        ]
    elif system == "Darwin":  # macOS
        font_paths = [
            ("蘋方", "/System/Library/Fonts/PingFang.ttc"),
            ("黑體", "/System/Library/Fonts/STHeiti Medium.ttc"),
        ]
    else:  # Linux
        font_paths = [
            ("文泉驛微米黑", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
            ("思源黑體", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        ]
    
    found_fonts = 0
    for name, path in font_paths:
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
            found_fonts += 1
        else:
            print(f"❌ {name}: 未找到")
    
    if found_fonts == 0:
        print("⚠️ 未找到任何系統中文字體")
        if system == "Linux":
            print("建議安裝: sudo apt-get install fonts-wqy-microhei")
    else:
        print(f"✅ 找到 {found_fonts} 個系統中文字體")
    
    return found_fonts > 0

def main():
    """主程序"""
    print("開始字體檢測...\n")
    
    # 檢查字體檔案
    has_custom_fonts = check_font_files()
    
    # 檢查系統字體
    has_system_fonts = system_font_check()
    
    # 執行顯示測試
    if has_custom_fonts or has_system_fonts:
        print("\n正在啟動字體顯示測試...")
        test_success = test_font_display()
    else:
        print("\n❌ 沒有找到任何中文字體")
        print("請先安裝中文字體再進行測試")
        test_success = False
    
    # 總結
    print(f"\n=== 檢測總結 ===")
    print(f"自訂字體: {'✅' if has_custom_fonts else '❌'}")
    print(f"系統字體: {'✅' if has_system_fonts else '❌'}")
    print(f"顯示測試: {'✅' if test_success else '❌'}")
    
    if not (has_custom_fonts or has_system_fonts):
        print(f"\n🔧 解決建議:")
        print(f"1. 下載中文字體檔案 (.ttf) 放入 assets/fonts/ 資料夾")
        print(f"2. 或安裝系統中文字體")
        print(f"3. 詳細說明請參考 '字體安裝指南.md'")
    
    print(f"\n測試完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n測試被用戶中斷")
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        print("請檢查是否正確安裝了 pygame 和相關依賴")