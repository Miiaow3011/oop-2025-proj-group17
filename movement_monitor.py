#!/usr/bin/env python3
"""
移動卡住監控器
專門監控玩家移動和狀態問題
"""

import pygame
import sys
import time
from main import Game

class MovementMonitor(Game):
    def __init__(self):
        super().__init__()
        
        # 移動監控
        self.last_position = (self.player.x, self.player.y)
        self.position_history = []
        self.movement_attempts = 0
        self.successful_movements = 0
        self.stuck_count = 0
        self.last_movement_time = time.time()
        
        # 狀態監控
        self.state_monitor = {
            "game_state": self.game_state.current_state,
            "dialogue_active": self.ui.dialogue_active,
            "show_inventory": self.ui.show_inventory,
            "show_map": self.ui.show_map,
            "player_moving": self.player.is_moving
        }
        
        print("🔍 移動監控器啟動")
        print("實時監控移動問題和狀態異常")
        print("-" * 40)
    
    def handle_exploration_input(self, event):
        """重寫移動輸入處理，添加詳細監控"""
        old_pos = (self.player.x, self.player.y)
        
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            self.movement_attempts += 1
            current_time = time.time()
            
            print(f"🎮 移動嘗試 #{self.movement_attempts}: {pygame.key.name(event.key)}")
            print(f"   當前位置: ({self.player.x}, {self.player.y})")
            print(f"   遊戲狀態: {self.game_state.current_state}")
            print(f"   對話狀態: {self.ui.dialogue_active}")
            print(f"   玩家移動中: {self.player.is_moving}")
        
        # 執行原始移動邏輯
        if event.key == pygame.K_UP:
            self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            self.player.move(32, 0)
        elif event.key == pygame.K_SPACE:
            print("🤝 嘗試互動")
            self.interact()
        elif event.key == pygame.K_i:
            print("🎒 切換背包")
            self.ui.toggle_inventory()
        elif event.key == pygame.K_m:
            print("🗺️ 切換地圖")
            self.ui.toggle_map()
        
        # 檢查移動結果
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            new_pos = (self.player.x, self.player.y)
            
            if new_pos != old_pos:
                self.successful_movements += 1
                self.last_movement_time = current_time
                print(f"✅ 移動成功: {old_pos} → {new_pos}")
                
                # 記錄移動歷史
                self.position_history.append({
                    "time": current_time,
                    "from": old_pos,
                    "to": new_pos,
                    "key": pygame.key.name(event.key)
                })
                
                # 只保留最近10次移動
                if len(self.position_history) > 10:
                    self.position_history.pop(0)
                    
            else:
                self.stuck_count += 1
                print(f"❌ 移動失敗 #{self.stuck_count}: 位置未改變")
                
                # 如果連續多次移動失敗，診斷問題
                if self.stuck_count >= 3:
                    self.diagnose_stuck_problem()
    
    def diagnose_stuck_problem(self):
        """診斷卡住問題"""
        print("\n🚨 檢測到移動問題，開始診斷...")
        print("=" * 50)
        
        # 檢查遊戲狀態
        print(f"🎮 遊戲狀態檢查:")
        print(f"   current_state: {self.game_state.current_state}")
        print(f"   dialogue_active: {self.ui.dialogue_active}")
        print(f"   show_inventory: {self.ui.show_inventory}")
        print(f"   show_map: {self.ui.show_map}")
        print(f"   player.is_moving: {self.player.is_moving}")
        
        # 檢查玩家狀態
        print(f"👤 玩家狀態檢查:")
        print(f"   位置: ({self.player.x}, {self.player.y})")
        print(f"   目標位置: ({self.player.move_target_x}, {self.player.move_target_y})")
        print(f"   移動中: {self.player.is_moving}")
        print(f"   邊界: min({self.player.min_x}, {self.player.min_y}) max({self.player.max_x}, {self.player.max_y})")
        
        # 可能的問題分析
        possible_issues = []
        
        if self.game_state.current_state != "exploration":
            possible_issues.append(f"遊戲狀態不是exploration: {self.game_state.current_state}")
        
        if self.ui.dialogue_active:
            possible_issues.append("對話還在進行中")
        
        if self.ui.show_inventory:
            possible_issues.append("背包介面開啟中")
            
        if self.ui.show_map:
            possible_issues.append("地圖介面開啟中")
            
        if self.player.is_moving:
            possible_issues.append("玩家還在移動動畫中")
        
        # 邊界檢查
        if (self.player.x <= self.player.min_x or self.player.x >= self.player.max_x or
            self.player.y <= self.player.min_y or self.player.y >= self.player.max_y):
            possible_issues.append("玩家位置超出邊界")
        
        print(f"\n🔍 可能的問題:")
        if possible_issues:
            for i, issue in enumerate(possible_issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("   未發現明顯問題")
        
        print(f"\n💡 建議修復:")
        print(f"   按 F2 - 強制重置狀態")
        print(f"   按 F3 - 重置玩家位置")
        print(f"   按 F4 - 強制設為exploration狀態")
        
        print("=" * 50)
        
        # 重置卡住計數器
        self.stuck_count = 0
    
    def handle_events(self):
        """重寫事件處理，添加額外快捷鍵"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_movement_report()
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 監控專用快捷鍵
                if event.key == pygame.K_F3:
                    self.reset_player_position()
                elif event.key == pygame.K_F4:
                    self.force_exploration()
                elif event.key == pygame.K_F5:
                    self.show_current_status()
                elif event.key == pygame.K_F6:
                    self.show_movement_history()
                
                # 原始事件處理
                elif self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        print("📖 跳過開場動畫")
                        
                elif self.game_state.current_state == "exploration":
                    self.handle_exploration_input(event)
                    
                elif self.game_state.current_state == "combat":
                    self.handle_combat_input(event)
                    
                elif self.game_state.current_state == "dialogue":
                    self.handle_dialogue_input(event)
                
                # 全域快捷鍵
                if event.key == pygame.K_F1:
                    print(f"🔍 當前狀態: 遊戲={self.game_state.current_state}, 對話={self.ui.dialogue_active}")
                elif event.key == pygame.K_F2:
                    self.force_exploration_state()
    
    def reset_player_position(self):
        """重置玩家位置"""
        old_pos = (self.player.x, self.player.y)
        self.player.set_position(400, 300)
        print(f"🔄 重置玩家位置: {old_pos} → (400, 300)")
        self.stuck_count = 0
    
    def force_exploration(self):
        """強制設為exploration狀態"""
        print("🔧 強制設為exploration狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.player.is_moving = False
        self.stuck_count = 0
        print("✅ 狀態已強制重置")
    
    def show_current_status(self):
        """顯示當前詳細狀態"""
        print("\n📊 當前詳細狀態:")
        print(f"   遊戲狀態: {self.game_state.current_state}")
        print(f"   對話活躍: {self.ui.dialogue_active}")
        print(f"   背包開啟: {self.ui.show_inventory}")
        print(f"   地圖開啟: {self.ui.show_map}")
        print(f"   玩家位置: ({self.player.x}, {self.player.y})")
        print(f"   玩家移動: {self.player.is_moving}")
        print(f"   移動嘗試: {self.movement_attempts}")
        print(f"   成功移動: {self.successful_movements}")
        print(f"   卡住次數: {self.stuck_count}")
        
        if self.movement_attempts > 0:
            success_rate = (self.successful_movements / self.movement_attempts) * 100
            print(f"   成功率: {success_rate:.1f}%")
    
    def show_movement_history(self):
        """顯示移動歷史"""
        print("\n📚 移動歷史 (最近10次):")
        if not self.position_history:
            print("   無移動記錄")
            return
        
        for i, move in enumerate(self.position_history[-10:], 1):
            timestamp = time.strftime("%H:%M:%S", time.localtime(move["time"]))
            print(f"   {i:2d}. [{timestamp}] {move['key']}: {move['from']} → {move['to']}")
    
    def render(self):
        """重寫渲染，添加監控資訊"""
        super().render()
        
        # 渲染監控資訊
        if not self.show_intro:
            self.render_movement_info()
    
    def render_movement_info(self):
        """渲染移動監控資訊"""
        info_rect = pygame.Rect(220, 10, 300, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), info_rect)
        pygame.draw.rect(self.screen, (255, 255, 0), info_rect, 1)
        
        from font_manager import font_manager
        
        info_lines = [
            "移動監控",
            f"位置: ({self.player.x}, {self.player.y})",
            f"嘗試: {self.movement_attempts}",
            f"成功: {self.successful_movements}",
            f"卡住: {self.stuck_count}",
            f"移動中: {self.player.is_moving}",
            "F3:重置位置 F4:強制exploration"
        ]
        
        y_offset = 15
        for line in info_lines:
            color = (255, 100, 100) if "卡住" in line and self.stuck_count > 0 else (255, 255, 0)
            text_surface = font_manager.render_text(line, 12, color)
            self.screen.blit(text_surface, (225, y_offset))
            y_offset += 14
    
    def show_movement_report(self):
        """顯示移動報告"""
        print("\n📊 移動監控報告")
        print("=" * 40)
        print(f"總移動嘗試: {self.movement_attempts}")
        print(f"成功移動: {self.successful_movements}")
        print(f"失敗次數: {self.movement_attempts - self.successful_movements}")
        print(f"卡住次數: {self.stuck_count}")
        
        if self.movement_attempts > 0:
            success_rate = (self.successful_movements / self.movement_attempts) * 100
            print(f"成功率: {success_rate:.1f}%")
            
            if success_rate < 80:
                print("⚠️ 移動成功率偏低，可能有問題")
            else:
                print("✅ 移動系統正常")
        
        print("=" * 40)

def main():
    print("🔍 啟動移動監控版《末世第二餐廳》")
    print("額外快捷鍵:")
    print("F3 - 重置玩家位置")
    print("F4 - 強制exploration狀態")
    print("F5 - 顯示詳細狀態")
    print("F6 - 顯示移動歷史")
    print("-" * 40)
    
    try:
        monitor = MovementMonitor()
        monitor.run()
    except Exception as e:
        print(f"監控器異常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()