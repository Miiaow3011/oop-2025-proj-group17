#!/usr/bin/env python3
"""
末世第二餐廳 - 簡化修復腳本
專門修復 main.py 的移動卡住問題
"""

import os
import shutil
from datetime import datetime

def backup_and_fix_player():
    """修復 player.py 的移動問題"""
    print("🔧 修復 player.py...")
    
    # 備份
    if os.path.exists("player.py"):
        backup_name = f"player.py.backup_{datetime.now().strftime('%m%d_%H%M')}"
        shutil.copy2("player.py", backup_name)
        print(f"✅ 已備份: {backup_name}")
    
    # 讀取當前內容
    with open("player.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修復1: 增加速度
    content = content.replace("self.speed = 4", "self.speed = 8")
    
    # 修復2: 添加容錯距離
    if "self.move_threshold" not in content:
        # 在移動狀態部分添加容錯距離
        content = content.replace(
            "self.move_target_y = y",
            "self.move_target_y = y\n        self.move_threshold = 2  # 到達目標的容錯距離"
        )
    
    # 修復3: 改善 move 函數的返回值
    old_move_func = """    def move(self, dx, dy):
        # 計算新位置
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 邊界檢查
        new_x = max(self.min_x, min(new_x, self.max_x))
        new_y = max(self.min_y, min(new_y, self.max_y))
        
        # 設定移動目標
        self.move_target_x = new_x
        self.move_target_y = new_y
        self.is_moving = True"""
    
    new_move_func = """    def move(self, dx, dy):
        # 如果玩家正在移動中，忽略新的移動指令
        if self.is_moving:
            return False
        
        # 計算新位置
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 邊界檢查
        new_x = max(self.min_x, min(new_x, self.max_x))
        new_y = max(self.min_y, min(new_y, self.max_y))
        
        # 檢查是否真的移動了
        if new_x == self.x and new_y == self.y:
            return False
        
        # 設定移動目標
        self.move_target_x = new_x
        self.move_target_y = new_y
        self.is_moving = True"""
    
    content = content.replace(old_move_func, new_move_func)
    
    # 修復4: 改善 update 函數的距離判斷
    old_update = """            # 如果距離目標很近，直接到達
            if abs(dx) < self.speed and abs(dy) < self.speed:
                self.x = self.move_target_x
                self.y = self.move_target_y
                self.is_moving = False"""
    
    new_update = """            # 計算距離
            distance = (dx**2 + dy**2)**0.5
            
            # 如果距離目標很近，直接到達
            if distance <= getattr(self, 'move_threshold', 2):
                self.x = self.move_target_x
                self.y = self.move_target_y
                self.is_moving = False"""
    
    content = content.replace(old_update, new_update)
    
    # 修復5: 添加輔助函數
    if "def force_stop_movement" not in content:
        helper_functions = """
    def force_stop_movement(self):
        \"\"\"強制停止移動\"\"\"
        self.is_moving = False
        self.move_target_x = self.x
        self.move_target_y = self.y
    
    def get_movement_info(self):
        \"\"\"獲取移動狀態資訊\"\"\"
        return {
            "position": (self.x, self.y),
            "target": (self.move_target_x, self.move_target_y),
            "is_moving": self.is_moving,
            "direction": self.direction,
            "distance_to_target": ((self.move_target_x - self.x)**2 + (self.move_target_y - self.y)**2)**0.5
        }"""
        
        # 在 get_rect 函數前添加
        content = content.replace("    def get_rect(self):", helper_functions + "\n    def get_rect(self):")
    
    # 確保 move 函數有返回值
    if "return True" not in content.split("def move(self, dx, dy):")[1].split("def ")[0]:
        # 在設定朝向後添加 return True
        content = content.replace(
            '            self.direction = "up"',
            '            self.direction = "up"\n        \n        return True'
        )
    
    # 寫入修復後的內容
    with open("player.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ player.py 修復完成")

def fix_main_py():
    """修復 main.py 的移動處理"""
    print("🔧 修復 main.py...")
    
    # 備份
    if os.path.exists("main.py"):
        backup_name = f"main.py.backup_{datetime.now().strftime('%m%d_%H%M')}"
        shutil.copy2("main.py", backup_name)
        print(f"✅ 已備份: {backup_name}")
    
    # 讀取當前內容
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修復1: 添加除錯模式和狀態重置功能
    if "self.debug_mode = False" not in content:
        # 在 __init__ 方法的最後添加除錯模式
        init_addition = """        
        # 除錯模式
        self.debug_mode = False"""
        
        content = content.replace(
            "self.interaction_cooldown = 0.5  # 0.5秒冷卻時間",
            "self.interaction_cooldown = 0.5  # 0.5秒冷卻時間" + init_addition
        )
    
    # 修復2: 添加 F1, F2, F3 快捷鍵處理
    if "elif event.key == pygame.K_F1:" not in content:
        hotkey_code = """                
                # 全域快捷鍵 (任何狀態都可用)
                if event.key == pygame.K_F1:
                    self.toggle_debug_mode()
                elif event.key == pygame.K_F2:
                    # 強制恢復exploration狀態
                    self.force_exploration_state()
                elif event.key == pygame.K_F3:
                    # 重置玩家位置
                    self.reset_player_position()"""
        
        # 在現有的 F1 處理前添加（如果沒有的話）
        if "if event.key == pygame.K_F1:" in content:
            # 替換現有的 F1 處理
            old_f1 = """                if event.key == pygame.K_F1:
                    print(f"除錯: 當前狀態 = {self.game_state.current_state}")
                    print(f"除錯: 對話活躍 = {self.ui.dialogue_active}")
                    print(f"除錯: 玩家位置 = ({self.player.x}, {self.player.y})")
                elif event.key == pygame.K_F2:
                    # 強制恢復exploration狀態
                    self.force_exploration_state()"""
            content = content.replace(old_f1, hotkey_code)
        else:
            # 在對話輸入處理後添加
            content = content.replace(
                "self.handle_dialogue_input(event)",
                "self.handle_dialogue_input(event)" + hotkey_code
            )
    
    # 修復3: 添加缺失的輔助函數
    helper_functions = """
    def toggle_debug_mode(self):
        \"\"\"切換除錯模式\"\"\"
        self.debug_mode = not self.debug_mode
        print(f"🔧 除錯模式: {'開啟' if self.debug_mode else '關閉'}")
        if self.debug_mode:
            self.print_debug_info()
    
    def print_debug_info(self):
        \"\"\"顯示除錯資訊\"\"\"
        move_info = self.player.get_movement_info() if hasattr(self.player, 'get_movement_info') else {}
        print(f"🔍 除錯資訊:")
        print(f"   遊戲狀態: {self.game_state.current_state}")
        print(f"   對話活躍: {self.ui.dialogue_active}")
        print(f"   玩家位置: ({self.player.x}, {self.player.y})")
        print(f"   玩家移動: {self.player.is_moving}")
        if move_info:
            print(f"   目標位置: {move_info.get('target', 'N/A')}")
    
    def reset_player_position(self):
        \"\"\"重置玩家位置\"\"\"
        old_pos = (self.player.x, self.player.y)
        self.player.set_position(400, 300)
        print(f"🔄 重置玩家位置: {old_pos} → (400, 300)")"""
    
    # 檢查是否已有這些函數
    if "def toggle_debug_mode" not in content:
        # 在 force_exploration_state 函數前添加
        if "def force_exploration_state" in content:
            content = content.replace("    def force_exploration_state", helper_functions + "\n    def force_exploration_state")
        else:
            # 在 handle_events 函數後添加
            content = content.replace("    def handle_events(self):", helper_functions + "\n    def handle_events(self):")
    
    # 修復4: 改善 handle_exploration_input 函數
    old_exploration_input = """    def handle_exploration_input(self, event):
        if event.key == pygame.K_UP:
            self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            self.player.move(32, 0)"""
    
    new_exploration_input = """    def handle_exploration_input(self, event):
        \"\"\"處理探索模式的輸入 - 修復版\"\"\"
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"🎮 按鍵: {pygame.key.name(event.key)}, 玩家移動中: {self.player.is_moving}")
        
        # 移動處理
        movement_successful = False
        
        if event.key == pygame.K_UP:
            movement_successful = self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            movement_successful = self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            movement_successful = self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            movement_successful = self.player.move(32, 0)"""
    
    content = content.replace(old_exploration_input, new_exploration_input)
    
    # 修復5: 改善 force_exploration_state 函數
    if "def force_exploration_state" in content:
        old_force_exploration = """    def force_exploration_state(self):
        \"\"\"強制恢復到exploration狀態\"\"\"
        print("🔧 強制恢復exploration狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.player.is_moving = False
        print("✅ 狀態已恢復")"""
        
        new_force_exploration = """    def force_exploration_state(self):
        \"\"\"強制恢復到exploration狀態\"\"\"
        print("🔧 強制恢復exploration狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
        
        # 強制停止玩家移動
        if hasattr(self.player, 'force_stop_movement'):
            self.player.force_stop_movement()
        else:
            self.player.is_moving = False
            
        print("✅ 狀態已恢復")"""
        
        content = content.replace(old_force_exploration, new_force_exploration)
    
    # 修復6: 在開場畫面添加說明
    if "F1開啟除錯模式" not in content:
        intro_addition = '''            "",
            "遊戲說明:",
            "方向鍵移動，空白鍵互動，I打開背包，M打開地圖",
            "F1開啟除錯模式，F2重置狀態，F3重置位置"'''
        
        content = content.replace(
            '"按 [空白鍵] 開始遊戲"',
            '"按 [空白鍵] 開始遊戲",' + intro_addition
        )
    
    # 寫入修復後的內容
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ main.py 修復完成")

def main():
    """主修復程序"""
    print("🔧 末世第二餐廳 - 移動問題修復腳本")
    print("=" * 50)
    
    # 檢查檔案
    if not os.path.exists("main.py"):
        print("❌ 找不到 main.py")
        return
    
    if not os.path.exists("player.py"):
        print("❌ 找不到 player.py")
        return
    
    print("🔍 檢測到的問題:")
    print("• 玩家移動卡住")
    print("• 移動速度過慢")
    print("• 缺少狀態重置功能")
    print()
    
    response = input("是否要應用修復？ (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("❌ 取消修復")
        return
    
    print("\n🔧 開始修復...")
    
    try:
        # 修復檔案
        backup_and_fix_player()
        fix_main_py()
        
        print("\n✅ 修復完成！")
        print()
        print("🎮 修復內容:")
        print("• 修復了玩家移動卡住問題")
        print("• 增加移動速度 (4 → 8)")
        print("• 添加除錯模式 (F1)")
        print("• 添加狀態重置 (F2)")
        print("• 添加位置重置 (F3)")
        print()
        print("📝 使用方法:")
        print("python3 main.py")
        print()
        print("🎮 遊戲內快捷鍵:")
        print("F1 - 開啟/關閉除錯模式")
        print("F2 - 強制重置遊戲狀態")
        print("F3 - 重置玩家位置")
        print()
        print("💾 原檔案已備份為 *.backup_* 檔案")
        
    except Exception as e:
        print(f"❌ 修復失敗: {e}")
        print("請檢查檔案權限")

if __name__ == "__main__":
    main()