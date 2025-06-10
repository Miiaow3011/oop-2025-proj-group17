#!/usr/bin/env python3
"""
對話系統測試工具
用於測試NPC對話功能是否正常
"""

import pygame
import sys
from font_manager import font_manager

class DialogueTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("對話系統測試")
        self.clock = pygame.time.Clock()
        
        # 測試對話數據
        self.test_dialogues = [
            {
                "name": "驚慌學生",
                "text": "救命！外面到處都是殭屍！我看到研究生們往樓上跑了！",
                "options": [
                    "冷靜一點，告訴我更多",
                    "樓上有什麼？",
                    "離開"
                ]
            },
            {
                "name": "受傷職員", 
                "text": "我被咬了...但還沒完全感染。聽說三樓有解藥...",
                "options": [
                    "解藥在哪裡？",
                    "你還好嗎？",
                    "離開"
                ]
            },
            {
                "name": "7-11商店",
                "text": "歡迎來到7-11！雖然外面很危險，但這裡還算安全。需要什麼嗎？",
                "options": [
                    "購買醫療用品",
                    "詢問情況",
                    "離開"
                ]
            }
        ]
        
        self.current_dialogue = 0
        self.dialogue_active = True
        self.selected_option = 0
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.dialogue_active:
                    if event.key == pygame.K_1:
                        self.select_option(0)
                    elif event.key == pygame.K_2:
                        self.select_option(1)
                    elif event.key == pygame.K_3:
                        self.select_option(2)
                    elif event.key == pygame.K_ESCAPE:
                        self.end_dialogue()
                    elif event.key == pygame.K_UP:
                        self.selected_option = max(0, self.selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        max_options = len(self.test_dialogues[self.current_dialogue]["options"])
                        self.selected_option = min(max_options - 1, self.selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        self.select_option(self.selected_option)
                else:
                    if event.key == pygame.K_n:
                        self.next_dialogue()
                    elif event.key == pygame.K_r:
                        self.restart_dialogue()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
    
    def select_option(self, option_index):
        dialogue = self.test_dialogues[self.current_dialogue]
        if 0 <= option_index < len(dialogue["options"]):
            selected_text = dialogue["options"][option_index]
            print(f"✅ 選擇了選項 {option_index + 1}: {selected_text}")
            
            # 模擬回應
            responses = {
                "冷靜一點，告訴我更多": "學生: 我看到他們拿著什麼東西往樓上跑...",
                "樓上有什麼？": "學生: 聽說研究生們在三樓做實驗...",
                "解藥在哪裡？": "職員: 三樓...咖啡廳附近...快去...",
                "你還好嗎？": "職員: 還撐得住...你快去找解藥...",
                "購買醫療用品": "店員: 這是醫療包，50元。",
                "詢問情況": "店員: 外面很危險，最好待在室內。",
                "離開": "對話結束"
            }
            
            response = responses.get(selected_text, f"你選擇了：{selected_text}")
            print(f"💬 回應: {response}")
            
            self.end_dialogue()
    
    def end_dialogue(self):
        print("🔚 對話結束")
        self.dialogue_active = False
    
    def next_dialogue(self):
        self.current_dialogue = (self.current_dialogue + 1) % len(self.test_dialogues)
        self.restart_dialogue()
    
    def restart_dialogue(self):
        self.dialogue_active = True
        self.selected_option = 0
        print(f"🔄 開始對話: {self.test_dialogues[self.current_dialogue]['name']}")
    
    def render(self):
        self.screen.fill((40, 40, 60))  # 深藍背景
        
        if self.dialogue_active:
            self.render_dialogue()
        else:
            self.render_menu()
        
        pygame.display.flip()
    
    def render_dialogue(self):
        dialogue = self.test_dialogues[self.current_dialogue]
        
        # 對話框背景
        dialogue_rect = pygame.Rect(50, 350, 700, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), dialogue_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), dialogue_rect, 2)
        
        # NPC名稱
        name_surface = font_manager.render_text(dialogue["name"], 20, (255, 255, 0))
        self.screen.blit(name_surface, (60, 360))
        
        # 對話文字
        text_lines = self.wrap_text(dialogue["text"], 680)
        y_offset = 390
        for line in text_lines:
            text_surface = font_manager.render_text(line, 18, (255, 255, 255))
            self.screen.blit(text_surface, (60, y_offset))
            y_offset += 25
        
        # 選項
        y_offset += 10
        for i, option in enumerate(dialogue["options"]):
            if i == self.selected_option:
                color = (255, 255, 0)
                pygame.draw.rect(self.screen, (50, 50, 50), (55, y_offset - 2, 690, 22))
            else:
                color = (200, 200, 200)
            
            option_text = f"{i+1}. {option}"
            option_surface = font_manager.render_text(option_text, 16, color)
            self.screen.blit(option_surface, (70, y_offset))
            y_offset += 25
        
        # 操作提示
        hint_text = "按 1/2/3 或 方向鍵+Enter 選擇，ESC 退出對話"
        hint_surface = font_manager.render_text(hint_text, 14, (150, 150, 150))
        self.screen.blit(hint_surface, (60, 520))
    
    def render_menu(self):
        # 標題
        title_surface = font_manager.render_text("對話系統測試", 32, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(400, 100))
        self.screen.blit(title_surface, title_rect)
        
        # 當前對話
        current_name = self.test_dialogues[self.current_dialogue]["name"]
        current_surface = font_manager.render_text(f"當前測試: {current_name}", 24, (255, 255, 0))
        current_rect = current_surface.get_rect(center=(400, 200))
        self.screen.blit(current_surface, current_rect)
        
        # 操作說明
        instructions = [
            "R - 重新開始當前對話",
            "N - 切換到下一個對話",
            "ESC - 退出測試"
        ]
        
        y_offset = 300
        for instruction in instructions:
            inst_surface = font_manager.render_text(instruction, 18, (200, 200, 200))
            inst_rect = inst_surface.get_rect(center=(400, y_offset))
            self.screen.blit(inst_surface, inst_rect)
            y_offset += 40
        
        # 對話列表
        list_title = font_manager.render_text("可測試對話:", 20, (255, 255, 255))
        self.screen.blit(list_title, (50, 480))
        
        y_offset = 510
        for i, dialogue in enumerate(self.test_dialogues):
            marker = "→ " if i == self.current_dialogue else "  "
            text = f"{marker}{i+1}. {dialogue['name']}"
            color = (255, 255, 0) if i == self.current_dialogue else (150, 150, 150)
            
            dialogue_surface = font_manager.render_text(text, 16, color)
            self.screen.blit(dialogue_surface, (70, y_offset))
            y_offset += 25
    
    def wrap_text(self, text, max_width):
        """文字換行"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = font_manager.render_text(test_line, 18, (255, 255, 255))
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def run(self):
        print("=== 對話系統測試開始 ===")
        print("這個工具用來測試對話選項功能")
        print("如果選擇選項後沒有反應，表示有bug")
        print()
        
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        print("測試結束")

def main():
    try:
        test = DialogueTest()
        test.run()
    except Exception as e:
        print(f"測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()