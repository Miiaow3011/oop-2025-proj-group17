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
        self.hp = 100  # 初始生命值


    def load_story_events(self):
        """載入劇情事件"""
        return {
            #一樓事件
            "intro": {
                "id": "intro",
                "location": (5, 5),
                "type": "story",
                "auto_trigger": True,
                "title": "末日的開始",
                "text": (
                    "你是這家便利商店的臨時員工。突然，外面傳來巨大的爆炸聲，緊接著是尖叫聲... "
                ),
                "choices": [
                    {"text": "查看窗外情況", "next": "window_check"},
                    {"text": "躲在櫃台後面", "next": "hide_counter"},
                    {"text": "躲在櫃台後面", "next": "check_supplies"}
                ]
            },

            "window_check": {
                "id": "window_check",
                "type": "story",
                "title": "窗外的恐怖",
                "text": (
                    "Y透過窗戶你看到街道上一片混亂，有些人似乎在攻擊其他人，而且行動很怪異..."
                ),
                "choices": [
                    {"text": "立刻鎖上店門", "next": "lock_door", "flag": "door_locked"},
                    {"text": "準備武器", "next": "find_weapon"}
                ]
            },

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

            "storage_event": {
                "id": "storage_event",
                "location": (3, 10),
                "type": "story",
                "title": "儲藏室探索",
                "text": "儲藏室很暗，你聽到裡面有奇怪的聲音...",
                "choices": [
                    {"text": "小心進入", "type": "combat", "enemy_type": "infected_staff"},
                    {"text": "大聲呼喊: 有人在嘛?", "next": "storage_noise"},
                    {"text": "關上門並離開", "next": None}
                ]
            },
            "door_event": {
                "id": "door_event",
                "location": (1, 12),
                "type": "story",
                "title": "門外的訪客",
                "text": "有人在敲門，但從窗戶看起來不太對勁...",
                "choices": [
                    {"text": "打開門看看發生了什麼事", "type": "combat", "enemy_type": "zombie"},
                    {"text": "躲起來假裝沒人在家", "next": "ignore_door"},
                    {"text": "嘗試從後門逃走", "next": "back_door_escape"}
                ]
            },

            "random_encounter": {
                "id": "random_encounter",
                "type": "random",
                "encounters": [
                    {"text": "你聽到有東西在架子後面拖行...", "type": "combat", "enemy_type": "zombie"},
                    {"text": "你在櫃檯下找到一瓶飲料和一把剪刀", "action": "random_item"},
                    {"text": "一陣眩暈襲來，你靠著牆站穩身體。", "action": "lose_hp"}
                ]
            },

            "hide_counter": {
                "id": "hide_counter",
                "type": "story",
                "title": "寂靜的緊張",
                "text": (
                    "你蹲在櫃檯後面，屏住呼吸。外頭的聲音越來越大——"
                    "尖叫聲、腳步聲，還有什麼東西撞著玻璃。時間過得異常緩慢。"
                ),
                "choices": [
                    {"text": "繼續躲著", "next": None},
                    {"text": "小心地偷看外面", "next": "window_check"}
                ]
            },

            "check_supplies": {
                "id": "check_supplies",
                "type": "story",
                "title": "應急物資",
                "text": (
                    "你快速查看貨架——零食、瓶裝水、繃帶和一支破舊的手電筒。"
                    "這些可能是你接下來幾小時唯一的依靠。"
                ),
                "choices": [
                    {"text": "拿走所有能帶的物資", "action": "random_item"},
                    {"text": "集中拿取醫療用品", "action": "get_medkit"},
                    {"text": "前往冷凍櫃找食物", "next": "freezer_event"}
                ]
            },

            "lock_door": {
                "id": "lock_door",
                "type": "story",
                "title": "封鎖前門",
                "text": (
                    "你把書架和箱子推到門口擋住門。玻璃在壓力下嘎嘎作響，"
                    "但目前還撐得住。你喘了口氣。"
                ),
                "choices": [
                    {"text": "尋找其他出口", "next": "back_door_escape"},
                    {"text": "再次搜尋店內", "next": "check_supplies"}
                ]
            },

            "find_weapon": {
                "id": "find_weapon",
                "type": "story",
                "title": "臨時武裝",
                "text": (
                    "你從櫃台抓起一把金屬雨傘和一把美工刀。雖然稱不上理想，"
                    "但總比空手好。"
                ),
                "choices": [
                    {"text": "準備戰鬥", "next": None},
                    {"text": "試著從後門溜出去", "next": "back_door_escape"}
                ]
            },

            "storage_noise": {
                "id": "storage_noise",
                "type": "story",
                "title": "它聽見你了",
                "text": (
                    "當你喊叫時，呼吸聲停止了——然後變成低吼。"
                    "什麼東西正從裡面衝向門口！"
                ),
                "choices": [
                    {"text": "緊緊頂住門！", "type": "combat", "enemy_type": "infected_staff"},
                    {"text": "慢慢後退", "next": None}
                ]
            },

            "ignore_door": {
                "id": "ignore_door",
                "type": "story",
                "title": "不速之客",
                "text": (
                    "你躲在貨架後，心臟怦怦跳。外頭的女孩繼續猛敲玻璃，"
                    "然後突然安靜下來。她走了嗎——還是正在盯著你？"
                ),
                "choices": [
                    {"text": "冒險偷看外面", "next": "window_check"},
                    {"text": "繼續躲藏等待", "next": None}
                ]
            },

            "back_door_escape": {
                "id": "back_door_escape",
                "type": "story",
                "title": "後巷逃脫",
                "text": (
                    "你從後門溜出，來到一條狹窄的巷子。整個校園異常寂靜，"
                    "但危險可能隨時出現。"
                ),
                "choices": [
                    {"text": "往餐廳方向前進", "next": None},
                    {"text": "試著尋找其他倖存者", "next": "storage_event"}
                ]
            },

            "upstairs_entry": {
                "id": "upstairs_entry",
                "type": "story",
                "title": "Up the Stairs",
                "text": "你到一個通往二樓的樓梯口，並確認身上帶有基本生存資源。你迅速衝上樓，暫時脫離了危險。",
                "choices": [
                    {"text": "keep going", "next": None}
                ]
            },
            #一樓事件結束
            "game_over": {
                "id": "game_over",
                "type": "story",
              "title": "Game Over",
              "text": (
                    "你的視線逐漸模糊，身體失去了力氣。周圍的聲音逐漸遠去。\n"
                   "在這場災難中，你無法存活下來……"
             ),
              "choices": []
            },

        }

    def get_event_by_location(self, x, y, tile_type):
        if (x, y) == (0, 0):
            if (
                self.get_flag("door_locked")
                and self.get_flag("has_medkit")
                and self.get_flag("has_weapon")
            ):
                return self.events.get("upstairs_entry")

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
        if x == 5 and y == 5 and "intro" not in self.triggered_events:
            return self.events.get("intro")
        if random.random() < 0.1:
            return self.events.get("random_encounter")
        return None

    def trigger_event(self, event_id):
        if event_id in self.events:
            self.current_event = self.events[event_id]
            self.triggered_events.add(event_id)
            return True
        return False

    def choose_option(self, choice_index):
        if not self.current_event or choice_index >= len(self.current_event.get("choices", [])):
            return None
        choice = self.current_event["choices"][choice_index]
        if "flag" in choice:
            self.set_flag(choice["flag"])
        if "next" in choice and choice["next"]:
            return self.trigger_event(choice["next"])
        elif "action" in choice:
            return self.handle_action(choice["action"])
        elif "type" in choice:
            return choice
        self.current_event = None
        return None

    def handle_action(self, action):
        if action == "get_medkit":
            self.set_flag("has_medkit")
            return {"type": "item", "item": "medkit", "message": "你獲得了醫療包"}
        elif action == "get_food":
            return {"type": "item", "item": "food", "message": "你獲得了食物"}
        elif action == "random_item":
            items = ["medkit", "food", "weapon"]
            item = random.choice(items)
            if item == "medkit":
                self.set_flag("has_medkit")
            elif item == "weapon":
                self.set_flag("has_weapon")
            return {"type": "item", "item": item, "message": f"你獲得了{item}"}
        elif action == "lose_hp":
            return {"type": "damage", "amount": 10, "message": "你失去了10點生命值"}
        return None

    def set_flag(self, flag_name, value=True):
        self.story_flags[flag_name] = value

    def get_flag(self, flag_name):
        return self.story_flags.get(flag_name, False)

    def is_story_finished(self):
        return self.current_event is None
