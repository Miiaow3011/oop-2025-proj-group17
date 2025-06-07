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
        "intro": {
            "id": "intro",
            "location": (5, 5),
            "type": "story",
            "auto_trigger": True,
            "title": "人類文明的崩壞",
            "text": (
                "你是國立陽明交通大學的一名大一學生，今天中午到便利商店買午餐時，"
                "忽然外面傳來一連串爆炸聲與驚慌尖叫。你從店內望出去，發現整個校園陷入混亂，"
                "人們奔逃、互相攻擊，還有許多人口吐白沫、瘋狂撕咬他人。"
            ),
            "choices": [
                {"text": "查看窗外發生什麼事", "next": "window_check"},
                {"text": "躲到櫃台後方靜觀其變", "next": "hide_counter"},
                {"text": "趕快檢查便利商店裡的資源", "next": "check_supplies"}
            ]
        },

        "window_check": {
            "id": "window_check",
            "type": "story",
            "title": "噩夢的起點",
            "text": (
                "你看到幾名學生被追趕、撕咬，街道上滿是血跡。一名身穿研究服的學生嘶喊著："
                "『疫苗在二餐三樓⋯快⋯去⋯！』隨即被撲倒。你意識到自己可能是少數倖存者之一。"
            ),
            "choices": [
                {"text": "立刻封死店門", "next": "lock_door", "flag": "door_locked"},
                {"text": "拿起可用的物品準備防身", "next": "find_weapon"}
            ]
        },

        "freezer_event": {
            "id": "freezer_event",
            "location": (16, 4),
            "type": "story",
            "title": "冷藏中的物資",
            "text": "你打開冷凍櫃，裡面除了幾盒微波食品，還意外發現一個簡易醫療包。",
            "choices": [
                {"text": "拿取醫療包", "action": "get_medkit"},
                {"text": "只拿食物", "action": "get_food"},
                {"text": "什麼都不拿", "next": None}
            ]
        },

        "storage_event": {
            "id": "storage_event",
            "location": (3, 10),
            "type": "story",
            "title": "儲藏室的動靜",
            "text": "你打開儲藏室，裡面傳來低沉的喘息聲，像是什麼東西躲藏其中。",
            "choices": [
                {"text": "慢慢靠近查看", "type": "combat", "enemy_type": "infected_staff"},
                {"text": "大聲喊出：有人在嗎？", "next": "storage_noise"},
                {"text": "立刻關門離開", "next": None}
            ]
        },

        "door_event": {
            "id": "door_event",
            "location": (1, 12),
            "type": "story",
            "title": "敲門聲",
            "text": (
                "便利商店的大門傳來急促的敲打聲，你透過玻璃看到一個神情痛苦的女生，"
                "但她的雙眼泛白，嘴角流出不明液體。她仍不停拍打玻璃，嘴裡發出低吼。"
            ),
            "choices": [
                {"text": "開門看看", "type": "combat", "enemy_type": "zombie"},
                {"text": "靜靜躲起來，假裝沒人", "next": "ignore_door"},
                {"text": "從後門試著離開便利商店", "next": "back_door_escape"}
            ]
        },

        "random_encounter": {
            "id": "random_encounter",
            "type": "random",
            "encounters": [
                {"text": "你聽見貨架後有東西摩擦地板的聲音...", "type": "combat", "enemy_type": "zombie"},
                {"text": "你在收銀台下發現一瓶飲料與一把剪刀", "action": "random_item"},
                {"text": "一陣頭暈目眩襲來，你靠著牆站穩。", "action": "lose_hp"}
            ]
        }
    }

def get_event_by_location(self, x, y, tile_type):
    """根據位置獲取事件"""
    for event_id, event in self.events.items():
        if event.get("location") == (x, y) and event_id not in self.triggered_events:
            return event

    if tile_type == 5:
        return self.events.get("freezer_event")
    elif tile_type == 6:
        return self.events.get("storage_event")
    elif tile_type == 4:
        return self.events.get("door_event")
    return None

def get_auto_event(self, x, y, tile_type):
    """獲取自動觸發事件"""
    if x == 5 and y == 5 and "intro" not in self.triggered_events:
        return self.events.get("intro")
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
    """查看當前劇情是否結束"""
    return self.current_event is None
