#!/usr/bin/env python3
"""
簡化的狀態監控器
修復import問題並簡化邏輯
"""

import pygame
import sys
import time
from main import Game

class SimpleStateMonitor(Game):
    def __init__(self):
        super().__init__()
        
        # 狀態追蹤
        self.last_game_state = ""
        self.last_ui_dialogue = False
        self.state_changes = []
        self.encounter_blocks = 0
        
        print("🔍 簡化狀態監控器啟動")
        print("監控功能:")
        print("- 自動記錄狀態變化")
        print("- 檢測對話→戰鬥異常轉換")
        print("- 阻止對話期間的隨機遭遇")
        print("- F6: 顯示狀態歷史")
        print("- F7: 顯示統計")
        print("-" * 40)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_final_report()
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 監控專用快捷鍵
                if event.key == pygame.K_F6:
                    self.show_state_history()
                    continue
                elif event.key == pygame.K_F7:
                    self.show_statistics()
                    continue
                
                # 記錄按鍵和狀態變化
                key_name = pygame.key.name(event.key)
                old_state = self.game_state.current_state
                old_dialogue = self.ui.dialogue_active
                
                # 呼叫原始事件處理
                super().handle_events_for_single_event(event)
                
                # 檢查狀態變化
                new_state = self.game_state.current_state
                new_dialogue = self.ui.dialogue_active
                
                if old_state != new_state or old_dialogue != new_dialogue:
                    self.record_state_change(old_state, new_state, old_dialogue, new_dialogue, f"按鍵: {key_name}")
    
    def handle_events_for_single_event(self, event):
        """處理單個事件的原始邏輯"""
        if self.show_intro:
            if event.key == pygame.K_SPACE:
                self.show_intro = False
                
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
    
    def update(self):
        # 記錄更新前的狀態
        old_state = self.game_state.current_state
        old_dialogue = self.ui.dialogue_active
        
        # 執行原始更新
        super().update()
        
        # 檢查更新後的狀態變化
        new_state = self.game_state.current_state
        new_dialogue = self.ui.dialogue_active
        
        if old_state != new_state or old_dialogue != new_dialogue:
            self.record_state_change(old_state, new_state, old_dialogue, new_dialogue, "update週期")
    
    def update_exploration(self):
        """重寫exploration更新，添加遭遇保護"""
        # 檢查是否應該阻止隨機遭遇
        if (self.ui.dialogue_active or 
            self.ui.show_inventory or 
            self.ui.show_map or
            self.game_state.current_state != "exploration"):
            
            # 阻止隨機遭遇
            if self.game_state.should_trigger_encounter():
                self.encounter_blocks += 1
                ui_state = []
                if self.ui.dialogue_active: ui_state.append("對話")
                if self.ui.show_inventory: ui_state.append("背包")
                if self.ui.show_map: ui_state.append("地圖")
                
                block_reason = f"遊戲狀態={self.game_state.current_state}, UI={'+'.join(ui_state) or '無'}"
                print(f"🚫 阻止隨機遭遇 #{self.encounter_blocks}: {block_reason}")
                return
        
        # 正常執行exploration更新
        if self.game_state.should_trigger_encounter():
            print("✅ 允許隨機遭遇觸發")
            self.start_combat()
    
    def record_state_change(self, old_game_state, new_game_state, old_dialogue, new_dialogue, reason):
        """記錄狀態變化"""
        change_info = {
            "time": time.time(),
            "old_game_state": old_game_state,
            "new_game_state": new_game_state,
            "old_dialogue": old_dialogue,
            "new_dialogue": new_dialogue,
            "reason": reason
        }
        
        self.state_changes.append(change_info)
        
        # 只保留最近20次變化
        if len(self.state_changes) > 20:
            self.state_changes.pop(0)
        
        # 輸出狀態變化
        if old_game_state != new_game_state:
            print(f"📊 遊戲狀態: {old_game_state} → {new_game_state} ({reason})")
            
            # 檢測異常轉換
            if old_game_state == "dialogue" and new_game_state == "combat":
                print(f"🚨 異常檢測: 對話期間觸發戰鬥！UI對話={new_dialogue}")
        
        if old_dialogue != new_dialogue:
            print(f"💬 對話狀態: {old_dialogue} → {new_dialogue} ({reason})")
    
    def show_state_history(self):
        """顯示狀態歷史"""
        print("\n" + "="*60)
        print("📚 狀態變化歷史 (最近10次)")
        print("="*60)
        
        recent = self.state_changes[-10:]
        for i, change in enumerate(recent):
            timestamp = time.strftime("%H:%M:%S", time.localtime(change["time"]))
            print(f"{i+1:2d}. [{timestamp}] {change['reason']}")
            
            if change["old_game_state"] != change["new_game_state"]:
                print(f"     遊戲狀態: {change['old_game_state']} → {change['new_game_state']}")
            
            if change["old_dialogue"] != change["new_dialogue"]:
                print(f"     對話狀態: {change['old_dialogue']} → {change['new_dialogue']}")
            
            # 標記異常
            if (change["old_game_state"] == "dialogue" and 
                change["new_game_state"] == "combat"):
                print("     🚨 異常: 對話→戰鬥轉換")
            
            print()
        
        print("="*60 + "\n")
    
    def show_statistics(self):
        """顯示統計"""
        print("\n" + "="*50)
        print("📈 監控統計")
        print("="*50)
        
        print(f"狀態變化次數: {len(self.state_changes)}")
        print(f"阻止遭遇次數: {self.encounter_blocks}")
        
        # 分析異常轉換
        dialogue_to_combat = 0
        for change in self.state_changes:
            if (change["old_game_state"] == "dialogue" and 
                change["new_game_state"] == "combat"):
                dialogue_to_combat += 1
        
        if dialogue_to_combat > 0:
            print(f"🚨 對話→戰鬥異常: {dialogue_to_combat}次")
        else:
            print("✅ 未發現對話→戰鬥異常")
        
        print("="*50 + "\n")
    
    def show_final_report(self):
        """顯示最終報告"""
        print("\n🏁 監控結束報告")
        self.show_statistics()
        self.show_state_history()
        
        # 結論
        dialogue_to_combat = sum(1 for c in self.state_changes 
                               if c["old_game_state"] == "dialogue" and c["new_game_state"] == "combat")
        
        if dialogue_to_combat == 0:
            print("🎉 結論: 對話系統穩定，未發現異常狀態轉換")
        else:
            print(f"⚠️ 結論: 發現 {dialogue_to_combat} 次對話→戰鬥異常轉換，需要修復")

def main():
    try:
        monitor = SimpleStateMonitor()
        monitor.run()
    except Exception as e:
        print(f"監控器錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()