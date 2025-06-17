# sound_manager.py - 音樂和音效管理器
import pygame
import os
import random

class SoundManager:
    def __init__(self):
        # 初始化音樂系統
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # 音樂文件路徑
        self.sounds_path = "assets/sounds"
        
        # 確保音樂資料夾存在
        if not os.path.exists(self.sounds_path):
            os.makedirs(self.sounds_path)
            print(f"📁 創建音樂資料夾: {self.sounds_path}")
        
        # 音樂設定
        self.music_volume = 0.6  # 背景音樂音量 (0.0-1.0)
        self.sfx_volume = 0.8    # 音效音量 (0.0-1.0)
        self.current_mode = None
        self.is_music_enabled = True
        self.is_sfx_enabled = True
        
        # 音樂文件映射 - 針對不同遊戲狀態
        self.music_files = {
            "intro": "intro_music.mp3",           # 開場介紹音樂
            "character_select": "character_select.mp3",  # 角色選擇音樂
            "exploration": "exploration_music.mp3",      # 探索模式音樂
            "combat": "combat_music.mp3",               # 戰鬥音樂
            "dialogue": "dialogue_music.mp3",           # 對話音樂 (輕柔版本)
            "victory": "victory_music.mp3",             # 勝利音樂
            "game_over": "game_over_music.mp3"          # 遊戲結束音樂
        }
        
        # 音效文件映射
        self.sfx_files = {
            "move": "move.wav",                 # 移動音效
            "interact": "interact.wav",         # 互動音效
            "collect_item": "collect_item.wav", # 收集物品音效
            "combat_hit": "combat_hit.wav",     # 戰鬥攻擊音效
            "combat_defend": "combat_defend.wav", # 防禦音效
            "level_up": "level_up.wav",         # 升級音效
            "dialogue_beep": "dialogue_beep.wav", # 對話嗶嗶聲
            "error": "error.wav",               # 錯誤音效
            "success": "success.wav",           # 成功音效
            "stairs": "stairs.wav",             # 樓梯音效
            "door": "door.wav",                 # 開門音效
        }
        
        # 載入的音效緩存
        self.loaded_sfx = {}
        
        # 載入音效
        self.load_sound_effects()
        
        print("🎵 音樂管理器初始化完成")
        self.print_available_files()
    
    def print_available_files(self):
        """顯示可用的音樂文件"""
        print(f"🎵 檢查音樂文件...")
        
        # 檢查音樂文件
        for mode, filename in self.music_files.items():
            filepath = os.path.join(self.sounds_path, filename)
            if os.path.exists(filepath):
                print(f"   ✅ {mode}: {filename}")
            else:
                print(f"   ❌ {mode}: {filename} (未找到)")
        
        # 檢查音效文件
        print(f"🔊 檢查音效文件...")
        for sfx_name, filename in self.sfx_files.items():
            filepath = os.path.join(self.sounds_path, filename)
            if os.path.exists(filepath):
                print(f"   ✅ {sfx_name}: {filename}")
            else:
                print(f"   ❌ {sfx_name}: {filename} (未找到)")
    
    def load_sound_effects(self):
        """載入所有音效到記憶體中"""
        print("🔊 載入音效檔案...")
        
        for sfx_name, filename in self.sfx_files.items():
            filepath = os.path.join(self.sounds_path, filename)
            try:
                if os.path.exists(filepath):
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(self.sfx_volume)
                    self.loaded_sfx[sfx_name] = sound
                    print(f"   ✅ 載入音效: {sfx_name}")
                else:
                    print(f"   ⚠️ 音效檔案不存在: {filepath}")
            except Exception as e:
                print(f"   ❌ 載入音效失敗 {sfx_name}: {e}")
        
        print(f"✅ 音效載入完成，共載入 {len(self.loaded_sfx)} 個音效")
    
    def play_music(self, mode, loop=True, fade_in_time=1000):
        """播放指定模式的背景音樂"""
        if not self.is_music_enabled:
            return
        
        # 如果已經在播放相同模式的音樂，就不需要重新播放
        if self.current_mode == mode and pygame.mixer.music.get_busy():
            return
        
        # 停止當前音樂
        self.stop_music(fade_out_time=500)
        
        # 獲取音樂文件路徑
        if mode not in self.music_files:
            print(f"⚠️ 未知的音樂模式: {mode}")
            return
        
        music_file = self.music_files[mode]
        music_path = os.path.join(self.sounds_path, music_file)
        
        # 檢查文件是否存在
        if not os.path.exists(music_path):
            print(f"⚠️ 音樂檔案不存在: {music_path}")
            return
        
        try:
            # 載入並播放音樂
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            
            # 設定播放次數 (-1 表示無限循環)
            play_count = -1 if loop else 0
            
            # 播放音樂 (fade_in_time 毫秒漸入)
            pygame.mixer.music.play(play_count, fade_ms=fade_in_time)
            
            self.current_mode = mode
            print(f"🎵 播放音樂: {mode} ({music_file})")
            
        except Exception as e:
            print(f"❌ 播放音樂失敗 {mode}: {e}")
    
    def stop_music(self, fade_out_time=1000):
        """停止背景音樂"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_out_time)
            print(f"🔇 停止音樂 (淡出 {fade_out_time}ms)")
        self.current_mode = None
    
    def play_sfx(self, sfx_name):
        """播放音效 - 增強除錯版"""
        print(f"🔊 收到播放音效請求: {sfx_name}")
        
        if not self.is_sfx_enabled:
            print(f"⚠️ 音效已關閉，跳過播放: {sfx_name}")
            return
        
        if sfx_name in self.loaded_sfx:
            try:
                print(f"🔊 找到音效文件: {sfx_name}")
                sound = self.loaded_sfx[sfx_name]
                print(f"🔊 音效音量: {sound.get_volume()}")
                
                # 播放音效
                channel = sound.play()
                if channel:
                    print(f"✅ 音效播放成功: {sfx_name}")
                else:
                    print(f"⚠️ 音效播放失敗（可能是通道已滿）: {sfx_name}")
                    
            except Exception as e:
                print(f"❌ 播放音效異常 {sfx_name}: {e}")
        else:
            print(f"❌ 音效不存在於已載入列表: {sfx_name}")
            print(f"📋 可用音效: {list(self.loaded_sfx.keys())}")
            
            # 嘗試直接載入並播放
            filepath = os.path.join(self.sounds_path, self.sfx_files.get(sfx_name, f"{sfx_name}.wav"))
            if os.path.exists(filepath):
                try:
                    print(f"🔄 嘗試直接載入: {filepath}")
                    temp_sound = pygame.mixer.Sound(filepath)
                    temp_sound.set_volume(self.sfx_volume)
                    temp_sound.play()
                    print(f"✅ 直接播放成功: {sfx_name}")
                except Exception as e:
                    print(f"❌ 直接播放失敗 {sfx_name}: {e}")
            else:
                print(f"❌ 音效文件不存在: {filepath}")
    
    def set_music_volume(self, volume):
        """設定背景音樂音量 (0.0-1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"🎵 設定音樂音量: {self.music_volume}")
    
    def set_sfx_volume(self, volume):
        """設定音效音量 (0.0-1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # 更新所有已載入音效的音量
        for sound in self.loaded_sfx.values():
            sound.set_volume(self.sfx_volume)
        print(f"🔊 設定音效音量: {self.sfx_volume}")
    
    def toggle_music(self):
        """切換背景音樂開關"""
        self.is_music_enabled = not self.is_music_enabled
        if not self.is_music_enabled:
            self.stop_music()
        print(f"🎵 背景音樂: {'開啟' if self.is_music_enabled else '關閉'}")
        return self.is_music_enabled
    
    def toggle_sfx(self):
        """切換音效開關"""
        self.is_sfx_enabled = not self.is_sfx_enabled
        print(f"🔊 音效: {'開啟' if self.is_sfx_enabled else '關閉'}")
        return self.is_sfx_enabled
    
    def get_status(self):
        """獲取音效系統狀態"""
        return {
            "music_enabled": self.is_music_enabled,
            "sfx_enabled": self.is_sfx_enabled,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "current_mode": self.current_mode,
            "music_playing": pygame.mixer.music.get_busy(),
            "loaded_sfx_count": len(self.loaded_sfx)
        }
    
    def cleanup(self):
        """清理音效系統"""
        self.stop_music()
        pygame.mixer.quit()
        print("🔇 音效系統已關閉")

# 全域音效管理器實例
sound_manager = SoundManager()