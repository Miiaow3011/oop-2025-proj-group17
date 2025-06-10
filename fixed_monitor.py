#!/usr/bin/env python3
"""
修復版監控器 - 避免複雜的繼承問題
直接修改主遊戲的關鍵方法
"""

import pygame
import sys
import time

# 首先導入所有需要的模組
from game_state import GameState
from map_manager import MapManager
from player import Player
from ui import UI
from combat import CombatSystem
from inventory import Inventory
from font_manager import font_manager

class FixedMonitorGame:
    def __init__(self):
        pygame.init()
        
        # 檢查中文字體
        if not font_manager.install_chinese_font():
            print("警告: 中文字體可能無法正常顯示")
        
        # 遊戲設定
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # 初始化畫面
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("末世第二餐廳 - 狀態監控版")
        self.clock = pygame.time.Clock()
        
        # 遊戲狀態
        self.game_state = GameState()
        
        # 初始化遊戲組件
        self.map_manager = MapManager()
        self.player = Player(x=400, y=300)
        self.ui = UI(self.screen)
        self.combat_system = CombatSystem()
        self.inventory = Inventory()
        
        # 遊戲標誌
        self.running = True
        self.show_intro = True
        
        # 監控相關
        self.state_changes = []
        self.encounter_blocks = 0
        self.last_state_check_time = time.time()
        
        print("🔍 修復版狀態監控器啟動")
        print("監控功能:")
        print("- F6: 顯示狀態歷史")
        print("- F7: 顯示統計")
        print("- F1: 當前狀態")
        print("- F2: 強制修復")
        print("-" * 40)
    
    def log_state_change(self, old_state, new_state, reason):
        """記錄狀態變化"""
        change = {
            "time": time.time(),
            "old_state": old_state,
            "new_state": new_state,
            "reason": reason,
            "dialogue_active": self.ui.dialogue_active
        }
        
        self.state_changes.append(change)
        
        # 只保留最近20次
        if len(self.state_changes) > 20:
            self.state_changes.pop(0)
        
        print(f"📊 狀態變化: {old_state} → {new_state} ({reason})")
        
        # 檢測異常
        if old_state == "dialogue" and new_state == "combat":
            print(f"🚨 異常檢測: 對話期間觸發戰鬥！對話狀態={self.ui.dialogue_active}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_final_report()
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 監控快捷鍵
                if event.key == pygame.K_F6:
                    self.show_state_history()
                    continue
                elif event.key == pygame.K_F7:
                    self.show_statistics()
                    continue
                elif event.key == pygame.K_F1:
                    print(f"🔍 當前狀態: 遊戲={self.game_state.current_state}, 對話={self.ui.dialogue_active}")
                    continue
                elif event.key == pygame.K_F2:
                    self.force_fix_state()
                    continue
                
                # 記錄狀態變化
                old_state = self.game_state.current_state
                
                # 處理正常遊戲事件
                if self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        
                elif self.game_state.current_state == "exploration":
                    self.handle_exploration_input(event)
                    
                elif self.game_state.current_state == "combat":
                    self.handle_combat_input(event)
                    
                elif self.game_state.current_state == "dialogue":
                    self.handle_dialogue_input(event)
                
                # 檢查狀態是否改變
                new_state = self.game_state.current_state
                if old_state != new_state:
                    key_name = pygame.key.name(event.key)
                    self.log_state_change(old_state, new_state, f"按鍵: {key_name}")
    
    def handle_exploration_input(self, event):
        if event.key == pygame.K_UP:
            self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            self.player.move(32, 0)
        elif event.key == pygame.K_SPACE:
            self.interact()
        elif event.key == pygame.K_i:
            self.ui.toggle_inventory()
        elif event.key == pygame.K_m:
            self.ui.toggle_map()
    
    def handle_combat_input(self, event):
        if event.key == pygame.K_1:
            self.combat_system.player_action("attack")
        elif event.key == pygame.K_2:
            self.combat_system.player_action("defend")
        elif event.key == pygame.K_3:
            self.combat_system.player_action("escape")
    
    def handle_dialogue_input(self, event):
        print(f"🎮 對話輸入: {pygame.key.name(event.key)} (對話活躍: {self.ui.dialogue_active})")
        
        if not self.ui.dialogue_active:
            print("⚠️ 對話未活躍，切換到exploration狀態")
            self.game_state.current_state = "exploration"
            return
        
        if event.key == pygame.K_1 and len(self.ui.dialogue_options) >= 1:
            self.ui.select_dialogue_option(0)
        elif event.key == pygame.K_2 and len(self.ui.dialogue_options) >= 2:
            self.ui.select_dialogue_option(1)
        elif event.key == pygame.K_3 and len(self.ui.dialogue_options) >= 3:
            self.ui.select_dialogue_option(2)
        elif event.key == pygame.K_SPACE:
            self.ui.continue_dialogue()
        elif event.key == pygame.K_ESCAPE:
            print("🚪 ESC強制退出對話")
            self.ui.end_dialogue()
            self.game_state.current_state = "exploration"
        
        # 每次對話輸入後檢查狀態
        if not self.ui.dialogue_active and self.game_state.current_state == "dialogue":
            print("🔄 對話結束，恢復exploration狀態")
            self.game_state.current_state = "exploration"
    
    def interact(self):
        current_floor = self.map_manager.get_current_floor()
        interaction = self.map_manager.check_interaction(
            self.player.x, self.player.y, current_floor
        )
        
        if interaction:
            if interaction["type"] == "shop":
                old_state = self.game_state.current_state
                self.game_state.current_state = "dialogue"
                self.ui.start_dialogue(interaction)
                self.log_state_change(old_state, "dialogue", f"商店互動: {interaction['name']}")
                
            elif interaction["type"] == "npc":
                old_state = self.game_state.current_state
                self.game_state.current_state = "dialogue"
                self.ui.start_dialogue(interaction)
                self.log_state_change(old_state, "dialogue", f"NPC對話: {interaction['name']}")
    
    def update(self):
        if not self.show_intro:
            # 記錄更新前狀態
            old_state = self.game_state.current_state
            
            # 同步UI和遊戲狀態
            self.sync_states()
            
            # 更新各系統
            self.player.update()
            self.map_manager.update()
            self.ui.update_messages()
            
            # 根據當前狀態執行對應邏輯
            if self.game_state.current_state == "exploration":
                self.update_exploration()
            elif self.game_state.current_state == "combat":
                self.update_combat()
            
            # 更新遊戲狀態訊息
            self.game_state.update_messages()
            
            # 檢查狀態變化
            new_state = self.game_state.current_state
            if old_state != new_state:
                self.log_state_change(old_state, new_state, "update週期")
    
    def sync_states(self):
        """同步UI和遊戲狀態"""
        if not self.ui.dialogue_active and self.game_state.current_state == "dialogue":
            print("🔄 同步: 對話已結束，切換到exploration")
            self.game_state.current_state = "exploration"
        elif self.ui.dialogue_active and self.game_state.current_state != "dialogue":
            print(f"🔄 同步: UI對話活躍，修正遊戲狀態到dialogue")
            self.game_state.current_state = "dialogue"
    
    def update_exploration(self):
        """安全的exploration更新，阻止對話期間的遭遇"""
        # 檢查是否應該阻止隨機遭遇
        if (self.ui.dialogue_active or 
            self.ui.show_inventory or 
            self.ui.show_map):
            
            # 如果遭遇系統想要觸發，阻止它
            if self.game_state.should_trigger_encounter():
                self.encounter_blocks += 1
                print(f"🚫 阻止遭遇 #{self.encounter_blocks}: UI介面開啟中")
                self.game_state.last_encounter_time = time.time()  # 重置計時器
            return
        
        # 正常檢查隨機遭遇
        if self.game_state.should_trigger_encounter():
            print("✅ 觸發隨機遭遇")
            old_state = self.game_state.current_state
            self.game_state.current_state = "combat"
            enemy = self.game_state.get_random_enemy()
            self.combat_system.start_combat(enemy)
            self.log_state_change(old_state, "combat", "隨機遭遇")
    
    def update_combat(self):
        """更新戰鬥狀態"""
        self.combat_system.update(self.game_state)
        
        if not self.combat_system.in_combat:
            old_state = self.game_state.current_state
            self.game_state.current_state = "exploration"
            self.log_state_change(old_state, "exploration", "戰鬥結束")
    
    def force_fix_state(self):
        """強制修復狀態"""
        print("🔧 強制修復狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.combat_system.in_combat = False
        print("✅ 狀態已強制修復到exploration")
    
    def show_state_history(self):
        """顯示狀態歷史"""
        print("\n" + "="*60)
        print("📚 狀態變化歷史 (最近10次)")
        print("="*60)
        
        recent = self.state_changes[-10:]
        for i, change in enumerate(recent):
            timestamp = time.strftime("%H:%M:%S", time.localtime(change["time"]))
            print(f"{i+1:2d}. [{timestamp}] {change['old_state']} → {change['new_state']}")
            print(f"     原因: {change['reason']}")
            print(f"     對話狀態: {change['dialogue_active']}")
            
            if change["old_state"] == "dialogue" and change["new_state"] == "combat":
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
        
        # 分析異常
        dialogue_to_combat = sum(1 for c in self.state_changes 
                               if c["old_state"] == "dialogue" and c["new_state"] == "combat")
        
        if dialogue_to_combat > 0:
            print(f"🚨 對話→戰鬥異常: {dialogue_to_combat}次")
        else:
            print("✅ 未發現對話→戰鬥異常")
        
        print("="*50 + "\n")
    
    def show_final_report(self):
        """最終報告"""
        print("\n🏁 監控結束報告")
        self.show_statistics()
        self.show_state_history()
    
    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.show_intro:
            self.render_intro()
        else:
            # 渲染地圖
            self.map_manager.render(self.screen)
            
            # 渲染玩家
            self.player.render(self.screen)
            
            # 渲染UI
            self.ui.render(self.game_state, self.player, self.inventory)
            
            # 渲染戰鬥
            if self.game_state.current_state == "combat":
                self.combat_system.render(self.screen, self.game_state)
            
            # 渲染監控資訊
            self.render_monitor_info()
        
        pygame.display.flip()
    
    def render_intro(self):
        intro_text = [
            "《末世第二餐廳》- 狀態監控版",
            "",
            "沒有人知道這一切是怎麼開始的。",
            "有一天，一種可怕的殭屍病毒突然席捲全球。",
            "只要被咬傷，感染者便會在三分鐘內失去理智...",
            "",
            "傳聞中，一群國立陽明交通大學的天才學生，",
            "憑著超凡的智慧，研發出了一種能夠治癒病毒的神秘藥劑。",
            "他們已將解藥藏於交大第二餐廳三樓的某個隱密角落...",
            "",
            "而你，作為同樣來自交大的普通學生，",
            "原本只是在便利商店買午餐，",
            "卻在殭屍攻進校園的瞬間被困其中。",
            "",
            "現在，全人類的命運，落在你手中。",
            "",
            "按 [空白鍵] 開始遊戲"
        ]
        
        y_offset = 50
        for line in intro_text:
            if line:
                text_surface = font_manager.render_text(line, 24, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, y_offset))
                self.screen.blit(text_surface, text_rect)
            y_offset += 30
    
    def render_monitor_info(self):
        """渲染監控資訊"""
        info_rect = pygame.Rect(10, 10, 200, 80)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), info_rect)
        pygame.draw.rect(self.screen, (255, 255, 0), info_rect, 1)
        
        info_lines = [
            f"狀態: {self.game_state.current_state}",
            f"對話: {self.ui.dialogue_active}",
            f"變化: {len(self.state_changes)}次",
            f"阻止: {self.encounter_blocks}次",
            "F6:歷史 F7:統計"
        ]
        
        y_offset = 15
        for line in info_lines:
            text_surface = font_manager.render_text(line, 12, (255, 255, 0))
            self.screen.blit(text_surface, (15, y_offset))
            y_offset += 12
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

def main():
    try:
        game = FixedMonitorGame()
        game.run()
    except Exception as e:
        print(f"遊戲錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()