#!/usr/bin/env python3
"""
遊戲除錯工具
用於診斷和修復遊戲卡住的問題
"""

import pygame
import sys
from main import Game

class DebugGame(Game):
    def __init__(self):
        super().__init__()
        self.debug_mode = True
        self.debug_info = []
        self.last_state = ""
        self.state_change_count = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 除錯快捷鍵
                if event.key == pygame.K_F1:
                    self.print_debug_info()
                elif event.key == pygame.K_F2:
                    self.force_exploration_state()
                elif event.key == pygame.K_F3:
                    self.toggle_debug_overlay()
                elif event.key == pygame.K_F4:
                    self.reset_player_position()
                elif event.key == pygame.K_F5:
                    self.print_interaction_debug()
                
                # 原有的事件處理
                if self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        self.log_debug("遊戲開始")
                        
                elif self.game_state.current_state == "exploration":
                    self.handle_exploration_input(event)
                    
                elif self.game_state.current_state == "combat":
                    self.handle_combat_input(event)
                    
                elif self.game_state.current_state == "dialogue":
                    self.handle_dialogue_input(event)
    
    def log_debug(self, message):
        """記錄除錯訊息"""
        self.debug_info.append(f"[{len(self.debug_info):03d}] {message}")
        print(f"🐛 {message}")
        
        # 只保留最近50條記錄
        if len(self.debug_info) > 50:
            self.debug_info.pop(0)
    
    def print_debug_info(self):
        """顯示當前遊戲狀態"""
        print("\n" + "="*50)
        print("🔍 遊戲狀態除錯資訊")
        print("="*50)
        print(f"遊戲狀態: {self.game_state.current_state}")
        print(f"對話活躍: {self.ui.dialogue_active}")
        print(f"背包開啟: {self.ui.show_inventory}")
        print(f"地圖開啟: {self.ui.show_map}")
        print(f"戰鬥中: {self.combat_system.in_combat}")
        print(f"玩家位置: ({self.player.x}, {self.player.y})")
        print(f"當前樓層: {self.map_manager.current_floor}")
        print(f"玩家移動中: {self.player.is_moving}")
        print(f"狀態改變次數: {self.state_change_count}")
        print("-"*50)
        print("最近的除錯記錄:")
        for record in self.debug_info[-10:]:
            print(f"  {record}")
        print("="*50)
        print("除錯快捷鍵:")
        print("F1 - 顯示此資訊")
        print("F2 - 強制恢復exploration狀態")
        print("F3 - 切換除錯顯示")
        print("F4 - 重置玩家位置")
        print("F5 - 顯示互動除錯資訊")
        print("="*50 + "\n")
    
    def force_exploration_state(self):
        """強制恢復exploration狀態"""
        self.log_debug("🔧 強制恢復exploration狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.combat_system.in_combat = False
        self.log_debug("✅ 狀態已強制恢復")
    
    def toggle_debug_overlay(self):
        """切換除錯顯示"""
        self.debug_mode = not self.debug_mode
        self.log_debug(f"除錯顯示: {'開啟' if self.debug_mode else '關閉'}")
    
    def reset_player_position(self):
        """重置玩家位置"""
        self.player.set_position(400, 300)
        self.log_debug("🚶 玩家位置已重置")
    
    def print_interaction_debug(self):
        """顯示互動除錯資訊"""
        current_floor = self.map_manager.get_current_floor()
        interaction = self.map_manager.check_interaction(
            self.player.x, self.player.y, current_floor
        )
        
        print(f"\n🔍 互動除錯資訊:")
        print(f"玩家位置: ({self.player.x}, {self.player.y})")
        print(f"當前樓層: {current_floor}")
        
        if interaction:
            print(f"找到互動: {interaction}")
        else:
            print("沒有找到互動物件")
            
            # 顯示附近的互動物件
            floor_data = self.map_manager.floor_data.get(current_floor, {})
            print(f"\n此樓層的互動物件:")
            
            for shop_id, shop in floor_data.get("shops", {}).items():
                distance = ((self.player.x - shop["pos"][0])**2 + (self.player.y - shop["pos"][1])**2)**0.5
                print(f"  商店 {shop_id}: {shop['chinese_name']} - 距離 {distance:.1f}")
            
            for npc in floor_data.get("npcs", []):
                distance = ((self.player.x - npc["pos"][0])**2 + (self.player.y - npc["pos"][1])**2)**0.5
                print(f"  NPC: {npc['name']} - 距離 {distance:.1f}")
            
            for item in floor_data.get("items", []):
                distance = ((self.player.x - item["pos"][0])**2 + (self.player.y - item["pos"][1])**2)**0.5
                print(f"  物品: {item['item']['name']} - 距離 {distance:.1f}")
        print()
    
    def handle_dialogue_input(self, event):
        """重寫對話輸入處理，添加詳細除錯"""
        self.log_debug(f"🎮 對話輸入: {pygame.key.name(event.key)}")
        self.log_debug(f"📊 當前狀態 - 遊戲:{self.game_state.current_state}, UI對話:{self.ui.dialogue_active}")
        
        # 呼叫父類方法
        super().handle_dialogue_input(event)
        
        # 檢查狀態一致性
        self.check_state_consistency()
    
    def check_state_consistency(self):
        """檢查狀態一致性"""
        game_state = self.game_state.current_state
        ui_dialogue = self.ui.dialogue_active
        
        if game_state == "dialogue" and not ui_dialogue:
            self.log_debug("⚠️ 狀態不一致: 遊戲為dialogue但UI對話已結束")
        elif game_state != "dialogue" and ui_dialogue:
            self.log_debug("⚠️ 狀態不一致: UI對話活躍但遊戲狀態不是dialogue")
        elif game_state == "exploration" and not ui_dialogue:
            self.log_debug("✅ 狀態一致: 都處於exploration")
        elif game_state == "dialogue" and ui_dialogue:
            self.log_debug("✅ 狀態一致: 都處於dialogue")
    
    def start_npc_dialogue(self, npc_info):
        """重寫NPC對話，添加狀態追蹤"""
        self.log_debug(f"👤 開始NPC對話: {npc_info['name']}")
        self.log_debug(f"📊 對話前狀態 - 遊戲:{self.game_state.current_state}, UI:{self.ui.dialogue_active}")
        
        super().start_npc_dialogue(npc_info)
        
        self.log_debug(f"📊 對話後狀態 - 遊戲:{self.game_state.current_state}, UI:{self.ui.dialogue_active}")
    
    def update(self):
        """重寫更新函數，添加狀態監控"""
        # 記錄狀態變化
        current_state = self.game_state.current_state
        current_ui_dialogue = self.ui.dialogue_active
        
        if current_state != self.last_state:
            self.log_debug(f"🔄 遊戲狀態變化: {self.last_state} → {current_state}")
            self.last_state = current_state
            self.state_change_count += 1
        
        # 檢查對話狀態變化
        if hasattr(self, 'last_ui_dialogue'):
            if current_ui_dialogue != self.last_ui_dialogue:
                self.log_debug(f"💬 UI對話狀態變化: {self.last_ui_dialogue} → {current_ui_dialogue}")
        
        self.last_ui_dialogue = current_ui_dialogue
        
        # 每隔一段時間檢查狀態一致性
        if hasattr(self, '_consistency_check_counter'):
            self._consistency_check_counter += 1
        else:
            self._consistency_check_counter = 0
        
        if self._consistency_check_counter % 180 == 0:  # 每3秒檢查一次
            self.check_state_consistency()
        
        super().update()
    
    def render(self):
        """重寫渲染函數添加除錯顯示"""
        super().render()
        
        if self.debug_mode and not self.show_intro:
            self.render_debug_overlay()
    
    def render_debug_overlay(self):
        """渲染除錯顯示"""
        # 除錯資訊背景
        debug_rect = pygame.Rect(10, 10, 300, 150)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), debug_rect)
        pygame.draw.rect(self.screen, (255, 255, 0), debug_rect, 1)
        
        # 除錯文字
        debug_lines = [
            f"狀態: {self.game_state.current_state}",
            f"對話: {self.ui.dialogue_active}",
            f"背包: {self.ui.show_inventory}",
            f"戰鬥: {self.combat_system.in_combat}",
            f"位置: ({self.player.x}, {self.player.y})",
            f"樓層: {self.map_manager.current_floor}樓",
            f"移動: {self.player.is_moving}",
            "F1:資訊 F2:修復 F3:顯示"
        ]
        
        y_offset = 20
        for line in debug_lines:
            from font_manager import font_manager
            text_surface = font_manager.render_text(line, 14, (255, 255, 0))
            self.screen.blit(text_surface, (15, y_offset))
            y_offset += 18

def main():
    """啟動除錯版遊戲"""
    print("🐛 啟動除錯版《末世第二餐廳》")
    print("除錯快捷鍵:")
    print("F1 - 顯示詳細狀態資訊")
    print("F2 - 強制恢復正常狀態")
    print("F3 - 切換除錯顯示")
    print("F4 - 重置玩家位置")
    print("F5 - 顯示互動除錯資訊")
    print("-" * 40)
    
    try:
        game = DebugGame()
        game.run()
    except Exception as e:
        print(f"遊戲異常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()