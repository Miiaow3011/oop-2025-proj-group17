# story.py - 劇情管理系統
import json
import random

class StoryManager:
    def __init__(self):
        self.current_event = None
        self.current_choice = 0
        self.story_flags = {}  # 劇情標記
        self.events = self.load_story_events()
        self.triggered_events = set()  # 已觸發的事件
    
    def load_story_events(self):
        """載入劇情事件"""
        return {
            # 開場事件
            "intro": {
                "id": "intro",
                "location": (5, 5),
                "type": "story",
                "auto_trigger": True,
                "title": "末日的開始",
                "text": "你是這家便利商店的臨時員工。突然，外面傳來巨大的爆炸聲，緊接著是尖叫聲...",
                "choices": [
                    {"text": "查看窗外情況", "next": "window_check"},
                    {"text": "躲在櫃台後面", "next": "hide_counter"},
                    {"text": "檢查店內物資", "next": "check_supplies"}
                ]
            },
            
            # 查看窗外
            "window_check": {
                "id": "window_check",
                "type": "story",
                "title": "窗外的恐怖",
                "text": "透過窗戶你看到街道上一片混亂，有些人似乎在攻擊其他人，而且行動很怪異...",
                "choices": [
                    {"text": "鎖上店門", "next": "lock_door", "flag": "door_locked"},
                    {"text": "準備武器", "next": "find_weapon"}
                ]
            },
            
            # 冷凍櫃事件
            "freezer_event": {
                "id": "freezer_event",
                "location": (16, 4),
                "type": "story",
                "title": "冷凍櫃中的發現",
                "text": "你打開冷凍櫃，發現裡面除了冷凍食品外，還有一些醫療用品...",
                "choices": [
                    {"text": "拿取醫療用品", "action": "get_medkit"},
                    {"text": "拿些食物", "action": "get_food"},
                    {"text": "什麼都不拿", "next": None}
                ]
            },
            
            # 儲藏室事件
            "storage_event": {
                "id": "storage_event",
                "location": (3, 10),
                "type": "story",
                "title": "儲藏室探索", 
                "text": "儲藏室很暗，你聽到裡面有奇怪的聲音...",
                "choices": [
                    {"text": "小心進入", "type": "combat", "enemy_type": "mutant_rat"},
                    {"text": "大聲呼喊", "next": "storage_noise"},
                    {"text": "離開", "next": None}
                ]
            },
            
            # 門口事件
            "door_event": {
                "id": "door_event", 
                "location": (1, 12),
                "type": "story",
                "title": "門外的訪客",
                "text": "有人在敲門，但從窗戶看起來不太對勁...",
                "choices": [
                    {"text": "開門", "type": "combat", "enemy_type": "zombie"},
                    {"text": "假裝沒人", "next": "ignore_door"},
                    {"text": "從後門逃跑", "next": "back_door_escape"}
                ]
            },
            
            # 隨機事件
            "random_encounter": {
                "id": "random_encounter",
                "type": "random",
                "encounters": [
                    {
                        "text": "你聽到奇怪的抓撓聲...",
                        "type": "combat",
                        "enemy_type": "zombie"
                    },
                    {
                        "text": "你發現地上有些有用的物品",
                        "action": "random_item"
                    },
                    {
                        "text": "你感到一陣暈眩...",
                        "action": "lose_hp"
                    }
                ]
            }
        }
    
    def get_event_by_location(self, x, y, tile_type):
        """根據位置獲取事件"""
        # 檢查特定位置事件
        for event_id, event in self.events.items():
            if event.get("location") == (x, y) and event_id not in self.triggered_events:
                return event
        
        # 檢查區域性事件
        if tile_type == 5:  # FREEZER
            return self.events.get("freezer_event")
        elif tile_type == 6:  # STORAGE
            return self.events.get("storage_event")
        elif tile_type == 4:  # DOOR
            return self.events.get("door_event")
        
        return None
    
    def get_auto_event(self, x, y, tile_type):
        """獲取自動觸發事件"""
        # 開場事件
        if x == 5 and y == 5 and "intro" not in self.triggered_events:
            return self.events.get("intro")
        
        # 隨機遭遇（10%機率）
        if random.random() < 0.1:
            return self.events.get("random_encounter")
        
        return None
    
    def trigger_event(self, event_id):
        """觸發事件"""
        if event_id in self.events:
            self.current_event = self.events[event_id]
            self.triggered_events.add(event_id)
            return True
        return False
    
    def choose_option(self, choice_index):
        """選擇選項"""
        if not self.current_event or choice_index >= len(self.current_event.get("choices", [])):
            return None
        
        choice = self.current_event["choices"][choice_index]
        
        # 處理選擇結果
        if "next" in choice and choice["next"]:
            return self.trigger_event(choice["next"])
        elif "action" in choice:
            return self.handle_action(choice["action"])
        elif "type" in choice:
            return choice
        
        self.current_event = None
        return None
    
    def handle_action(self, action):
        """處理動作"""
        if action == "get_medkit":
            return {"type": "item", "item": "medkit", "message": "你獲得了醫療包"}
        elif action == "get_food":
            return {"type": "item", "item": "food", "message": "你獲得了食物"}
        elif action == "random_item":
            items = ["medkit", "food", "weapon"]
            item = random.choice(items)
            return {"type": "item", "item": item, "message": f"你獲得了{item}"}
        elif action == "lose_hp":
            return {"type": "damage", "amount": 10, "message": "你失去了10點生命值"}
        
        return None
    
    def set_flag(self, flag_name, value=True):
        """設置劇情標記"""
        self.story_flags[flag_name] = value
    
    def get_flag(self, flag_name):
        """獲取劇情標記"""
        return self.story_flags.get(flag_name, False)
    
    def is_story_finished(self):
        """檢查當前劇情是否結束"""
        return self.current_event is None
