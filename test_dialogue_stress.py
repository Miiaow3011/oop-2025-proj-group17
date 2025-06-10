#!/usr/bin/env python3
"""
連續對話壓力測試
測試多次對話後是否會卡住
"""

import pygame
import sys
import time
from font_manager import font_manager

class DialogueStressTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("連續對話壓力測試")
        self.clock = pygame.time.Clock()
        
        # 測試統計
        self.test_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.test_results = []
        self.current_test_status = "準備中"
        
        # 模擬對話系統
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
        self.game_state = "exploration"  # exploration, dialogue
        
        # 測試用對話數據
        self.test_dialogues = [
            {
                "name": "驚慌學生",
                "text": "救命！外面到處都是殭屍！",
                "options": ["冷靜一點", "樓上有什麼", "離開"]
            },
            {
                "name": "受傷職員", 
                "text": "我被咬了...聽說三樓有解藥...",
                "options": ["解藥在哪", "你還好嗎", "離開"]
            },
            {
                "name": "7-11商店",
                "text": "歡迎來到7-11！需要什麼嗎？",
                "options": ["購買醫療用品", "詢問情況", "離開"]
            }
        ]
        
        self.running = True
        self.auto_test_mode = False
        self.auto_test_delay = 1.0  # 自動測試間隔(秒)
        self.last_auto_test = time.time()
    
    def start_dialogue(self, dialogue_data):
        """開始對話"""
        print(f"📞 開始對話: {dialogue_data['name']}")
        self.dialogue_active = True
        self.dialogue_text = dialogue_data["text"]
        self.dialogue_options = dialogue_data["options"].copy()
        self.selected_option = 0
        self.game_state = "dialogue"
        return True
    
    def select_option(self, option_index):
        """選擇對話選項"""
        if not self.dialogue_active:
            print("❌ 對話未活躍")
            return False
            
        if 0 <= option_index < len(self.dialogue_options):
            selected_text = self.dialogue_options[option_index]
            print(f"✅ 選擇選項 {option_index + 1}: {selected_text}")
            
            # 模擬處理選項
            self.end_dialogue()
            return True
        else:
            print(f"❌ 無效選項: {option_index}")
            return False
    
    def end_dialogue(self):
        """結束對話"""
        print("🏁 結束對話")
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
        self.game_state = "exploration"
        return True
    
    def run_single_test(self):
        """執行單次對話測試"""
        self.test_count += 1
        test_start_time = time.time()
        
        print(f"\n🧪 開始測試 #{self.test_count}")
        
        try:
            # 隨機選擇一個對話
            import random
            dialogue = random.choice(self.test_dialogues)
            
            # 步驟1: 開始對話
            if not self.start_dialogue(dialogue):
                raise Exception("無法開始對話")
            
            # 檢查狀態
            if not self.dialogue_active or self.game_state != "dialogue":
                raise Exception("對話狀態異常")
            
            # 步驟2: 選擇選項
            option_index = random.randint(0, len(dialogue["options"]) - 1)
            if not self.select_option(option_index):
                raise Exception("選項選擇失敗")
            
            # 檢查結束狀態
            if self.dialogue_active or self.game_state != "exploration":
                raise Exception("對話結束狀態異常")
            
            # 測試成功
            test_duration = time.time() - test_start_time
            self.success_count += 1
            result = {
                "test_id": self.test_count,
                "status": "成功",
                "dialogue": dialogue["name"],
                "option": option_index,
                "duration": test_duration,
                "error": None
            }
            self.test_results.append(result)
            self.current_test_status = f"測試 #{self.test_count} 成功"
            print(f"✅ 測試 #{self.test_count} 成功 ({test_duration:.3f}s)")
            
        except Exception as e:
            # 測試失敗
            test_duration = time.time() - test_start_time
            self.fail_count += 1
            result = {
                "test_id": self.test_count,
                "status": "失敗",
                "dialogue": dialogue["name"] if 'dialogue' in locals() else "未知",
                "option": -1,
                "duration": test_duration,
                "error": str(e)
            }
            self.test_results.append(result)
            self.current_test_status = f"測試 #{self.test_count} 失敗: {e}"
            print(f"❌ 測試 #{self.test_count} 失敗: {e}")
            
            # 強制重置狀態
            self.force_reset()
    
    def force_reset(self):
        """強制重置狀態"""
        print("🔧 強制重置狀態")
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
        self.game_state = "exploration"
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 單次測試
                    self.run_single_test()
                elif event.key == pygame.K_a:
                    # 切換自動測試模式
                    self.auto_test_mode = not self.auto_test_mode
                    print(f"🤖 自動測試模式: {'開啟' if self.auto_test_mode else '關閉'}")
                elif event.key == pygame.K_r:
                    # 重置統計
                    self.reset_statistics()
                elif event.key == pygame.K_s:
                    # 顯示詳細結果
                    self.show_detailed_results()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def reset_statistics(self):
        """重置測試統計"""
        self.test_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.test_results = []
        self.current_test_status = "統計已重置"
        print("🔄 測試統計已重置")
    
    def show_detailed_results(self):
        """顯示詳細結果"""
        print("\n" + "="*60)
        print("📊 詳細測試結果")
        print("="*60)
        
        for result in self.test_results[-10:]:  # 顯示最近10次
            status_icon = "✅" if result["status"] == "成功" else "❌"
            print(f"{status_icon} 測試 #{result['test_id']:03d}: {result['dialogue']} "
                  f"選項{result['option']+1 if result['option'] >= 0 else 'N/A'} "
                  f"({result['duration']:.3f}s)")
            if result["error"]:
                print(f"    錯誤: {result['error']}")
        
        print("="*60)
        
        if self.test_count > 0:
            success_rate = (self.success_count / self.test_count) * 100
            avg_duration = sum(r["duration"] for r in self.test_results) / len(self.test_results)
            print(f"成功率: {success_rate:.1f}% ({self.success_count}/{self.test_count})")
            print(f"平均耗時: {avg_duration:.3f}秒")
            
            # 分析失敗原因
            if self.fail_count > 0:
                print(f"\n失敗分析:")
                error_counts = {}
                for result in self.test_results:
                    if result["status"] == "失敗" and result["error"]:
                        error = result["error"]
                        error_counts[error] = error_counts.get(error, 0) + 1
                
                for error, count in error_counts.items():
                    print(f"  • {error}: {count}次")
        
        print("="*60 + "\n")
    
    def update(self):
        # 自動測試模式
        if self.auto_test_mode:
            current_time = time.time()
            if current_time - self.last_auto_test >= self.auto_test_delay:
                self.run_single_test()
                self.last_auto_test = current_time
    
    def render(self):
        self.screen.fill((30, 30, 50))  # 深藍背景
        
        # 標題
        title = font_manager.render_text("連續對話壓力測試", 32, (255, 255, 255))
        title_rect = title.get_rect(center=(500, 50))
        self.screen.blit(title, title_rect)
        
        # 統計資訊
        stats_y = 120
        if self.test_count > 0:
            success_rate = (self.success_count / self.test_count) * 100
            stats_text = [
                f"總測試次數: {self.test_count}",
                f"成功: {self.success_count} 次",
                f"失敗: {self.fail_count} 次", 
                f"成功率: {success_rate:.1f}%"
            ]
        else:
            stats_text = ["尚未開始測試"]
        
        for text in stats_text:
            color = (0, 255, 0) if "成功" in text else (255, 0, 0) if "失敗" in text else (255, 255, 255)
            surface = font_manager.render_text(text, 20, color)
            self.screen.blit(surface, (50, stats_y))
            stats_y += 30
        
        # 當前狀態
        status_surface = font_manager.render_text(f"狀態: {self.current_test_status}", 18, (255, 255, 0))
        self.screen.blit(status_surface, (50, stats_y + 20))
        
        # 模式指示
        mode_text = "🤖 自動測試中..." if self.auto_test_mode else "手動測試模式"
        mode_color = (0, 255, 255) if self.auto_test_mode else (200, 200, 200)
        mode_surface = font_manager.render_text(mode_text, 18, mode_color)
        self.screen.blit(mode_surface, (50, stats_y + 50))
        
        # 最近測試結果
        results_y = 350
        results_title = font_manager.render_text("最近測試結果:", 22, (255, 255, 255))
        self.screen.blit(results_title, (50, results_y))
        results_y += 40
        
        # 顯示最近5次測試
        recent_results = self.test_results[-5:] if self.test_results else []
        for result in recent_results:
            status_icon = "✅" if result["status"] == "成功" else "❌"
            result_text = f"{status_icon} #{result['test_id']:03d}: {result['dialogue']} ({result['duration']:.2f}s)"
            color = (0, 255, 0) if result["status"] == "成功" else (255, 100, 100)
            
            result_surface = font_manager.render_text(result_text, 16, color)
            self.screen.blit(result_surface, (70, results_y))
            results_y += 25
            
            # 顯示錯誤訊息
            if result["error"]:
                error_surface = font_manager.render_text(f"    錯誤: {result['error']}", 14, (255, 150, 150))
                self.screen.blit(error_surface, (90, results_y))
                results_y += 20
        
        # 操作說明
        instructions_y = 580
        instructions = [
            "空白鍵 - 執行單次測試",
            "A鍵 - 切換自動測試模式", 
            "R鍵 - 重置統計",
            "S鍵 - 顯示詳細結果",
            "ESC - 退出"
        ]
        
        instructions_title = font_manager.render_text("操作說明:", 18, (255, 255, 255))
        self.screen.blit(instructions_title, (50, instructions_y))
        instructions_y += 30
        
        for instruction in instructions:
            inst_surface = font_manager.render_text(instruction, 14, (200, 200, 200))
            self.screen.blit(inst_surface, (70, instructions_y))
            instructions_y += 20
        
        pygame.display.flip()
    
    def run(self):
        print("🧪 連續對話壓力測試開始")
        print("這個測試用來檢測多次對話後是否會卡住")
        print("操作說明:")
        print("  空白鍵 - 執行單次測試")
        print("  A鍵 - 自動測試模式")
        print("  R鍵 - 重置統計")
        print("  S鍵 - 詳細結果")
        print("-" * 40)
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        # 最終報告
        self.show_final_report()
        pygame.quit()
    
    def show_final_report(self):
        """顯示最終測試報告"""
        print(f"\n🏁 測試完成報告")
        print("="*50)
        
        if self.test_count > 0:
            success_rate = (self.success_count / self.test_count) * 100
            print(f"總測試次數: {self.test_count}")
            print(f"成功次數: {self.success_count}")
            print(f"失敗次數: {self.fail_count}")
            print(f"成功率: {success_rate:.1f}%")
            
            if self.test_results:
                avg_duration = sum(r["duration"] for r in self.test_results) / len(self.test_results)
                print(f"平均耗時: {avg_duration:.3f}秒")
            
            # 結論
            if success_rate >= 95:
                print("🎉 測試結論: 對話系統穩定")
            elif success_rate >= 80:
                print("⚠️ 測試結論: 對話系統基本穩定，有少數問題")
            else:
                print("❌ 測試結論: 對話系統不穩定，需要修復")
                
            # 問題分析
            if self.fail_count > 0:
                print(f"\n🔍 問題分析:")
                error_counts = {}
                for result in self.test_results:
                    if result["status"] == "失敗" and result["error"]:
                        error = result["error"]
                        error_counts[error] = error_counts.get(error, 0) + 1
                
                for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / self.fail_count) * 100
                    print(f"  • {error}: {count}次 ({percentage:.1f}%)")
        else:
            print("未執行任何測試")
        
        print("="*50)

def main():
    try:
        test = DialogueStressTest()
        test.run()
    except Exception as e:
        print(f"測試程式發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()