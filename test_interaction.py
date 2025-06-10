#!/usr/bin/env python3
"""
互動系統測試工具
專門測試多次互動是否會失效
"""

import pygame
import sys
import time
from font_manager import font_manager

class InteractionTester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("互動系統測試")
        self.clock = pygame.time.Clock()
        
        # 測試統計
        self.interaction_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.test_log = []
        
        # 模擬互動物件
        self.test_objects = [
            {"name": "7-11", "type": "shop", "pos": (200, 200), "size": (100, 80)},
            {"name": "NPC學生", "type": "npc", "pos": (400, 200), "size": (50, 50)},
            {"name": "醫療包", "type": "item", "pos": (300, 350), "size": (30, 30)},
            {"name": "樓梯", "type": "stairs", "pos": (500, 400), "size": (60, 40)}
        ]
        
        # 玩家位置
        self.player_x = 100
        self.player_y = 100
        
        # 互動狀態
        self.in_interaction = False
        self.interaction_cooldown = 0
        
        self.running = True
        
        print("🧪 互動系統測試工具")
        print("操作說明:")
        print("- 方向鍵移動玩家")
        print("- 空白鍵進行互動")
        print("- R鍵重置測試")
        print("- ESC退出")
        print("-" * 30)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_test()
                elif event.key == pygame.K_SPACE:
                    self.test_interaction()
                elif event.key == pygame.K_UP:
                    self.player_y -= 20
                elif event.key == pygame.K_DOWN:
                    self.player_y += 20
                elif event.key == pygame.K_LEFT:
                    self.player_x -= 20
                elif event.key == pygame.K_RIGHT:
                    self.player_x += 20
    
    def test_interaction(self):
        """測試互動功能"""
        if self.interaction_cooldown > 0:
            print(f"⏰ 冷卻中，剩餘 {self.interaction_cooldown:.1f} 秒")
            return
        
        self.interaction_count += 1
        current_time = time.time()
        
        # 檢查是否與物件接觸
        interacted_object = None
        for obj in self.test_objects:
            if self.check_collision(obj):
                interacted_object = obj
                break
        
        if interacted_object:
            if self.in_interaction:
                # 結束互動
                self.end_interaction(interacted_object)
            else:
                # 開始互動
                self.start_interaction(interacted_object)
        else:
            # 沒有找到互動物件
            self.log_test(f"第{self.interaction_count}次", "失敗", "沒有找到互動物件", current_time)
            self.fail_count += 1
            print(f"❌ 第{self.interaction_count}次互動失敗: 沒有找到物件")
    
    def start_interaction(self, obj):
        """開始互動"""
        current_time = time.time()
        
        if obj["type"] == "item":
            # 物品類型：直接收集
            self.collect_item(obj)
            self.log_test(f"第{self.interaction_count}次", "成功", f"收集物品: {obj['name']}", current_time)
            self.success_count += 1
            print(f"✅ 第{self.interaction_count}次互動成功: 收集了{obj['name']}")
        else:
            # 其他類型：進入互動狀態
            self.in_interaction = True
            self.interaction_cooldown = 1.0  # 1秒冷卻
            self.log_test(f"第{self.interaction_count}次", "成功", f"開始互動: {obj['name']}", current_time)
            self.success_count += 1
            print(f"✅ 第{self.interaction_count}次互動成功: 開始與{obj['name']}互動")
    
    def end_interaction(self, obj):
        """結束互動"""
        current_time = time.time()
        self.in_interaction = False
        self.interaction_cooldown = 0.5  # 0.5秒冷卻
        
        self.log_test(f"第{self.interaction_count}次", "成功", f"結束互動: {obj['name']}", current_time)
        self.success_count += 1
        print(f"✅ 第{self.interaction_count}次互動成功: 結束與{obj['name']}的互動")
    
    def collect_item(self, obj):
        """收集物品（移除物品）"""
        if obj in self.test_objects:
            self.test_objects.remove(obj)
            print(f"📦 {obj['name']} 已被收集並移除")
    
    def check_collision(self, obj):
        """檢查玩家是否與物件碰撞"""
        obj_x, obj_y = obj["pos"]
        obj_w, obj_h = obj["size"]
        
        return (obj_x <= self.player_x <= obj_x + obj_w and
                obj_y <= self.player_y <= obj_y + obj_h)
    
    def log_test(self, test_id, status, description, timestamp):
        """記錄測試結果"""
        log_entry = {
            "id": test_id,
            "status": status,
            "description": description,
            "timestamp": timestamp
        }
        self.test_log.append(log_entry)
        
        # 只保留最近10次記錄
        if len(self.test_log) > 10:
            self.test_log.pop(0)
    
    def reset_test(self):
        """重置測試"""
        self.interaction_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.test_log.clear()
        self.in_interaction = False
        self.interaction_cooldown = 0
        
        # 重置物件
        self.test_objects = [
            {"name": "7-11", "type": "shop", "pos": (200, 200), "size": (100, 80)},
            {"name": "NPC學生", "type": "npc", "pos": (400, 200), "size": (50, 50)},
            {"name": "醫療包", "type": "item", "pos": (300, 350), "size": (30, 30)},
            {"name": "樓梯", "type": "stairs", "pos": (500, 400), "size": (60, 40)}
        ]
        
        print("🔄 測試已重置")
    
    def update(self):
        # 更新冷卻時間
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= 1/60  # 60 FPS
            if self.interaction_cooldown <= 0:
                self.interaction_cooldown = 0
    
    def render(self):
        self.screen.fill((40, 40, 60))
        
        # 繪製標題
        title = font_manager.render_text("互動系統測試", 24, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 30))
        self.screen.blit(title, title_rect)
        
        # 繪製統計
        stats_y = 70
        stats = [
            f"互動次數: {self.interaction_count}",
            f"成功: {self.success_count}",
            f"失敗: {self.fail_count}",
            f"成功率: {(self.success_count/max(1,self.interaction_count)*100):.1f}%"
        ]
        
        for stat in stats:
            stat_surface = font_manager.render_text(stat, 16, (255, 255, 255))
            self.screen.blit(stat_surface, (20, stats_y))
            stats_y += 25
        
        # 繪製互動狀態
        status_text = "互動中" if self.in_interaction else "探索中"
        status_color = (255, 255, 0) if self.in_interaction else (0, 255, 0)
        status_surface = font_manager.render_text(f"狀態: {status_text}", 16, status_color)
        self.screen.blit(status_surface, (20, stats_y + 10))
        
        # 繪製冷卻時間
        if self.interaction_cooldown > 0:
            cooldown_surface = font_manager.render_text(f"冷卻: {self.interaction_cooldown:.1f}s", 16, (255, 100, 100))
            self.screen.blit(cooldown_surface, (20, stats_y + 35))
        
        # 繪製玩家
        pygame.draw.rect(self.screen, (0, 255, 255), (self.player_x-10, self.player_y-10, 20, 20))
        
        # 繪製互動物件
        for obj in self.test_objects:
            color = (100, 255, 100) if obj["type"] == "item" else (255, 200, 100)
            
            # 檢查是否在範圍內
            if self.check_collision(obj):
                color = (255, 255, 255)  # 高亮顯示
            
            obj_x, obj_y = obj["pos"]
            obj_w, obj_h = obj["size"]
            pygame.draw.rect(self.screen, color, (obj_x, obj_y, obj_w, obj_h))
            
            # 物件名稱
            name_surface = font_manager.render_text(obj["name"], 12, (255, 255, 255))
            self.screen.blit(name_surface, (obj_x, obj_y - 20))
        
        # 繪製測試日誌
        log_y = 400
        log_title = font_manager.render_text("測試日誌 (最近5次):", 14, (255, 255, 255))
        self.screen.blit(log_title, (20, log_y))
        log_y += 25
        
        recent_logs = self.test_log[-5:]
        for log in recent_logs:
            status_icon = "✅" if log["status"] == "成功" else "❌"
            log_text = f"{status_icon} {log['id']}: {log['description']}"
            color = (0, 255, 0) if log["status"] == "成功" else (255, 100, 100)
            
            log_surface = font_manager.render_text(log_text, 12, color)
            self.screen.blit(log_surface, (20, log_y))
            log_y += 18
        
        # 操作說明
        instructions_y = 520
        instructions = [
            "方向鍵: 移動玩家",
            "空白鍵: 互動",
            "R鍵: 重置測試",
            "ESC: 退出"
        ]
        
        for instruction in instructions:
            inst_surface = font_manager.render_text(instruction, 12, (200, 200, 200))
            self.screen.blit(inst_surface, (500, instructions_y))
            instructions_y += 16
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        # 顯示最終報告
        self.show_final_report()
        pygame.quit()
    
    def show_final_report(self):
        """顯示最終測試報告"""
        print("\n" + "="*40)
        print("🏁 互動測試最終報告")
        print("="*40)
        print(f"總互動次數: {self.interaction_count}")
        print(f"成功次數: {self.success_count}")
        print(f"失敗次數: {self.fail_count}")
        
        if self.interaction_count > 0:
            success_rate = (self.success_count / self.interaction_count) * 100
            print(f"成功率: {success_rate:.1f}%")
            
            if success_rate >= 95:
                print("🎉 結論: 互動系統穩定")
            elif success_rate >= 80:
                print("⚠️ 結論: 互動系統基本穩定，有少數問題")
            else:
                print("❌ 結論: 互動系統不穩定，需要修復")
        else:
            print("未進行任何互動測試")
        
        print("="*40)

def main():
    try:
        tester = InteractionTester()
        tester.run()
    except Exception as e:
        print(f"測試工具錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()