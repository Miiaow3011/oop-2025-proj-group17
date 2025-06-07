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
                "title": "The Fall of Civilization",
                "text": (
                    "You're a freshman at National Yang Ming Chiao Tung University. While grabbing lunch at the campus convenience store, "
                    "a sudden series of explosions and terrified screams erupt outside. Looking out the store window, you witness chaos unfold — "
                    "people running in panic, attacking each other, some foaming at the mouth and violently biting others."
                ),
                "choices": [
                    {"text": "Check what's happening outside", "next": "window_check"},
                    {"text": "Hide behind the counter and stay quiet", "next": "hide_counter"},
                    {"text": "Quickly search the store for supplies", "next": "check_supplies"}
                ]
            },

            "window_check": {
                "id": "window_check",
                "type": "story",
                "title": "The Nightmare Begins",
                "text": (
                    "You see students being chased and mauled. Blood is everywhere. A student in a lab coat shouts, "
                    "'The vaccine... it’s on the 3rd floor... of the cafeteria... hurry!' before being tackled by a crazed figure. "
                    "You realize you might be one of the few left uninfected."
                ),
                "choices": [
                    {"text": "Barricade the store entrance immediately", "next": "lock_door", "flag": "door_locked"},
                    {"text": "Grab anything that can be used as a weapon", "next": "find_weapon"}
                ]
            },

            "freezer_event": {
                "id": "freezer_event",
                "location": (16, 4),
                "type": "story",
                "title": "Supplies in the Freezer",
                "text": "You open the freezer. Aside from some microwaveable meals, you find a basic first-aid kit stashed inside.",
                "choices": [
                    {"text": "Take the medkit", "action": "get_medkit"},
                    {"text": "Just grab the food", "action": "get_food"},
                    {"text": "Leave everything", "next": None}
                ]
            },

            "storage_event": {
                "id": "storage_event",
                "location": (3, 10),
                "type": "story",
                "title": "Suspicious Sounds in Storage",
                "text": "You open the storage room door. Inside, you hear raspy breathing — something’s lurking in the shadows.",
                "choices": [
                    {"text": "Approach carefully to investigate", "type": "combat", "enemy_type": "infected_staff"},
                    {"text": "Shout: Is anyone in there?", "next": "storage_noise"},
                    {"text": "Close the door and walk away", "next": None}
                ]
            },

            "door_event": {
                "id": "door_event",
                "location": (1, 12),
                "type": "story",
                "title": "Knocking at the Door",
                "text": (
                    "The store's glass door shakes under frantic knocking. Outside, a girl appears in pain — "
                    "her eyes are clouded white and strange fluids drip from her mouth. Still, she keeps pounding the glass and growling."
                ),
                "choices": [
                    {"text": "Open the door and see what's going on", "type": "combat", "enemy_type": "zombie"},
                    {"text": "Stay hidden and pretend no one's inside", "next": "ignore_door"},
                    {"text": "Try escaping through the back door", "next": "back_door_escape"}
                ]
            },

            "random_encounter": {
                "id": "random_encounter",
                "type": "random",
                "encounters": [
                    {"text": "You hear something dragging along the floor behind the shelves...", "type": "combat", "enemy_type": "zombie"},
                    {"text": "You find a bottle of drink and a pair of scissors under the checkout counter", "action": "random_item"},
                    {"text": "A wave of dizziness hits you. You lean against the wall to keep your balance.", "action": "lose_hp"}
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
