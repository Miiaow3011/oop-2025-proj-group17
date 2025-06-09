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
            },

            "hide_counter": {
                "id": "hide_counter",
                "type": "story",
                "title": "Silent Tension",
                "text": (
                    "You crouch behind the counter, holding your breath. The noise outside intensifies — "
                    "shrieks, footsteps, and something banging on the glass. Minutes crawl by like hours."
                ),
                "choices": [
                    {"text": "Stay hidden a bit longer", "next": None},
                    {"text": "Peek outside carefully", "next": "window_check"}
                ]
            },

            "check_supplies": {
                "id": "check_supplies",
                "type": "story",
                "title": "Emergency Stockpile",
                "text": (
                    "You quickly scan the shelves — snacks, bottled water, bandages, and a battered flashlight. "
                    "This might be all you have to survive the next few hours."
                ),
                "choices": [
                    {"text": "Take all you can carry", "action": "random_item"},
                    {"text": "Focus on medical supplies", "action": "get_medkit"},
                    {"text": "Head toward the freezer for food", "next": "freezer_event"}
                ]
            },

            "lock_door": {
                "id": "lock_door",
                "type": "story",
                "title": "Barricading the Front",
                "text": (
                    "You shove shelves and crates against the front door. The glass rattles under pressure, "
                    "but for now, it holds. You take a moment to catch your breath."
                ),
                "choices": [
                    {"text": "Look for other exits", "next": "back_door_escape"},
                    {"text": "Search the store again", "next": "check_supplies"}
                ]
            },

            "find_weapon": {
                "id": "find_weapon",
                "type": "story",
                "title": "Improvised Arsenal",
                "text": (
                    "You grab a metal umbrella and a box cutter from the counter. Not ideal, but better than nothing."
                ),
                "choices": [
                    {"text": "Get ready to defend yourself", "next": None},
                    {"text": "Try to sneak out the back", "next": "back_door_escape"}
                ]
            },

            "storage_noise": {
                "id": "storage_noise",
                "type": "story",
                "title": "It Heard You",
                "text": (
                    "As you shout, the breathing stops — then turns into a growl. Something rushes toward the door from inside!"
                ),
                "choices": [
                    {"text": "Hold the door shut!", "type": "combat", "enemy_type": "infected_staff"},
                    {"text": "Back away slowly", "next": None}
                ]
            },

            "ignore_door": {
                "id": "ignore_door",
                "type": "story",
                "title": "Unwelcome Guest",
                "text": (
                    "You crouch behind a shelf, heart pounding. The girl outside continues to slam the glass, "
                    "then suddenly stops. Did she leave — or is she still watching?"
                ),
                "choices": [
                    {"text": "Risk a look outside", "next": "window_check"},
                    {"text": "Stay hidden and wait", "next": None}
                ]
            },

            "back_door_escape": {
                "id": "back_door_escape",
                "type": "story",
                "title": "Back Alley Breakout",
                "text": (
                    "You slip through the back door into a narrow alley. The campus is eerily quiet now, "
                    "but danger could be around any corner."
                ),
                "choices": [
                    {"text": "Head toward the cafeteria", "next": None},
                    {"text": "Try to find other survivors", "next": "storage_event"}
                ]
            },

            "upstairs_entry": {
                "id": "upstairs_entry",
                "type": "story",
                "title": "Up the Stairs",
                "text": "你找到一個通往二樓的樓梯口，並確認身上帶有基本生存資源。你迅速衝上樓，暫時脫離了危險。",
                "choices": [
                    {"text": "繼續前進（進入二樓）", "next": None}
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
