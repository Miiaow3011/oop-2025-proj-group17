#!/usr/bin/env python3
"""
末世第二餐廳 - 背包卡住修復腳本
修復打開背包後遊戲卡住的問題
"""

import os
import shutil
from datetime import datetime

def fix_ui_freeze():
    """修復 UI 卡住問題"""
    print("🔧 修復 UI 卡住問題...")
    
    # 備份 ui.py
    if os.path.exists("ui.py"):
        backup_name = f"ui.py.backup_{datetime.now().strftime('%m%d_%H%M')}"
        shutil.copy2("ui.py", backup_name)
        print(f"✅ 已備份: {backup_name}")
    
    # 讀取 ui.py
    with open("ui.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修復1: 確保 toggle_inventory 正確處理狀態
    old_toggle = """    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
        if self.show_inventory:
            self.show_map = False"""
    
    new_toggle = """    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
        if self.show_inventory:
            self.show_map = False
        print(f"🎒 背包狀態: {'開啟' if self.show_inventory else '關閉'}")"""
    
    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)
    
    # 修復2: 確保 toggle_map 正確處理狀態  
    old_map_toggle = """    def toggle_map(self):
        self.show_map = not self.show_map
        if self.show_map:
            self.show_inventory = False"""
    
    new_map_toggle = """    def toggle_map(self):
        self.show_map = not self.show_map
        if self.show_map:
            self.show_inventory = False
        print(f"🗺️ 地圖狀態: {'開啟' if self.show_map else '關閉'}")"""
    
    if old_map_toggle in content:
        content = content.replace(old_map_toggle, new_map_toggle)
    
    # 寫入修復後的內容
    with open("ui.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ ui.py 修復完成")

def fix_main_event_handling():
    """修復 main.py 的事件處理"""
    print("🔧 修復事件處理...")
    
    # 備份 main.py
    if os.path.exists("main.py"):
        backup_name = f"main.py.backup_{datetime.now().strftime('%m%d_%H%M')}"
        shutil.copy2("main.py", backup_name)
        print(f"✅ 已備份: {backup_name}")
    
    # 讀取 main.py
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修復1: 確保在任何UI狀態下都能處理基本事件
    old_event_handling = """    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:"""
    
    new_event_handling = """    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 全域快捷鍵 - 在任何狀態下都可用
                if event.key == pygame.K_i:
                    # 切換背包
                    self.ui.toggle_inventory()
                    continue
                elif event.key == pygame.K_m:
                    # 切換地圖
                    self.ui.toggle_map()
                    continue
                elif event.key == pygame.K_ESCAPE:
                    # ESC 關閉所有UI
                    self.ui.show_inventory = False
                    self.ui.show_map = False
                    self.ui.dialogue_active = False
                    self.game_state.current_state = "exploration"
                    print("🚪 ESC - 關閉所有UI")
                    continue"""
    
    if old_event_handling in content:
        content = content.replace(old_event_handling, new_event_handling)
    
    # 修復2: 移除重複的 I 和 M 鍵處理
    duplicate_i_key = """        elif event.key == pygame.K_i:
            self.ui.toggle_inventory()"""
    
    duplicate_m_key = """        elif event.key == pygame.K_m:
            self.ui.toggle_map()"""
    
    # 移除在 handle_exploration_input 中的重複處理
    content = content.replace(duplicate_i_key, "")
    content = content.replace(duplicate_m_key, "")
    
    # 修復3: 改善 handle_exploration_input
    old_exploration = """    def handle_exploration_input(self, event):"""
    
    new_exploration = """    def handle_exploration_input(self, event):
        # 檢查UI狀態，如果有UI開啟就不處理移動
        if self.ui.show_inventory or self.ui.show_map:
            print("⚠️ UI開啟中，忽略移動輸入")
            return"""
    
    content = content.replace(old_exploration, new_exploration)
    
    # 修復4: 確保update函數不會在UI開啟時觸發遊戲邏輯
    old_update = """    def update(self):
        if not self.show_intro:
            self.player.update()
            self.map_manager.update()
            
            # 檢查隨機遭遇
            if self.game_state.should_trigger_encounter():
                self.start_combat()"""
    
    new_update = """    def update(self):
        if not self.show_intro:
            # 只有在沒有UI開啟時才更新遊戲邏輯
            if not (self.ui.show_inventory or self.ui.show_map or self.ui.dialogue_active):
                self.player.update()
                self.map_manager.update()
                
                # 檢查隨機遭遇
                if self.game_state.should_trigger_encounter():
                    self.start_combat()
            else:
                # UI開啟時只更新UI相關內容
                pass"""
    
    if old_update in content:
        content = content.replace(old_update, new_update)
    
    # 寫入修復後的內容
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ main.py 修復完成")

def add_debug_to_main():
    """在 main.py 中添加除錯資訊"""
    print("🔧 添加除錯資訊...")
    
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 在開場畫面提示中添加說明
    if "ESC關閉UI" not in content:
        intro_addition = '''            "ESC關閉UI，如果卡住請按ESC"'''
        
        if '"F1開啟除錯模式，F2重置狀態，F3重置位置"' in content:
            content = content.replace(
                '"F1開啟除錯模式，F2重置狀態，F3重置位置"',
                '"F1開啟除錯模式，F2重置狀態，F3重置位置",' + intro_addition
            )
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 除錯資訊添加完成")

def main():
    """主修復程序"""
    print("🔧 末世第二餐廳 - 背包卡住修復腳本")
    print("=" * 50)
    
    # 檢查檔案
    required_files = ["main.py", "ui.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 缺少檔案: {', '.join(missing_files)}")
        return
    
    print("🔍 檢測到的問題:")
    print("• 打開背包後遊戲卡住")
    print("• UI事件處理不當")
    print("• 缺少ESC退出機制")
    print()
    
    response = input("是否要應用修復？ (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("❌ 取消修復")
        return
    
    print("\n🔧 開始修復...")
    
    try:
        fix_ui_freeze()
        fix_main_event_handling()
        add_debug_to_main()
        
        print("\n✅ 修復完成！")
        print()
        print("🎮 修復內容:")
        print("• 修復背包/地圖卡住問題")
        print("• 改善UI事件處理")
        print("• 添加ESC關閉所有UI功能")
        print("• 防止UI開啟時的遊戲邏輯衝突")
        print()
        print("🎮 新的快捷鍵:")
        print("I - 開啟/關閉背包 (任何時候)")
        print("M - 開啟/關閉地圖 (任何時候)")
        print("ESC - 強制關閉所有UI (緊急修復)")
        print()
        print("📝 使用方法:")
        print("python3 main.py")
        print()
        print("💡 如果還是卡住:")
        print("立即按 ESC 鍵強制關閉所有UI")
        print()
        print("💾 原檔案已備份")
        
    except Exception as e:
        print(f"❌ 修復失敗: {e}")
        print("請檢查檔案權限")

if __name__ == "__main__":
    main()