#!/usr/bin/env python3
"""
末世第二餐廳 - 遊戲啟動器
提供遊戲啟動、設定和除錯功能
"""

import os
import sys
import pygame
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("末世第二餐廳 - 遊戲啟動器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 設定遊戲配置
        self.config = {
            "resolution": "1024x768",
            "fullscreen": False,
            "fps": 60,
            "volume": 0.8,
            "difficulty": "normal"
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """設定使用者介面"""
        # 主標題
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="末世第二餐廳", 
                              font=("Arial", 24, "bold"), fg="darkred")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Apocalypse Second Restaurant", 
                                 font=("Arial", 12), fg="gray")
        subtitle_label.pack()
        
        # 遊戲資訊
        info_frame = tk.LabelFrame(self.root, text="遊戲資訊", padx=10, pady=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """
你是交大學生，被困在第二餐廳的7-11中。
傳說三樓有能拯救世界的解藥...
你能找到它嗎？
        """
        
        info_label = tk.Label(info_frame, text=info_text, justify="left")
        info_label.pack()
        
        # 設定選項
        settings_frame = tk.LabelFrame(self.root, text="遊戲設定", padx=10, pady=10)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # 解析度設定
        res_frame = tk.Frame(settings_frame)
        res_frame.pack(fill="x", pady=5)
        
        tk.Label(res_frame, text="解析度:").pack(side="left")
        self.resolution_var = tk.StringVar(value=self.config["resolution"])
        resolution_combo = ttk.Combobox(res_frame, textvariable=self.resolution_var,
                                       values=["800x600", "1024x768", "1280x720", "1920x1080"],
                                       state="readonly", width=15)
        resolution_combo.pack(side="right")
        
        # 全螢幕設定
        self.fullscreen_var = tk.BooleanVar(value=self.config["fullscreen"])
        fullscreen_check = tk.Checkbutton(settings_frame, text="全螢幕模式",
                                         variable=self.fullscreen_var)
        fullscreen_check.pack(anchor="w", pady=5)
        
        # 難度設定
        diff_frame = tk.Frame(settings_frame)
        diff_frame.pack(fill="x", pady=5)
        
        tk.Label(diff_frame, text="難度:").pack(side="left")
        self.difficulty_var = tk.StringVar(value=self.config["difficulty"])
        difficulty_combo = ttk.Combobox(diff_frame, textvariable=self.difficulty_var,
                                       values=["easy", "normal", "hard"],
                                       state="readonly", width=15)
        difficulty_combo.pack(side="right")
        
        # 音量設定
        volume_frame = tk.Frame(settings_frame)
        volume_frame.pack(fill="x", pady=5)
        
        tk.Label(volume_frame, text="音量:").pack(side="left")
        self.volume_var = tk.DoubleVar(value=self.config["volume"])
        volume_scale = tk.Scale(volume_frame, from_=0.0, to=1.0, resolution=0.1,
                               orient="horizontal", variable=self.volume_var, length=200)
        volume_scale.pack(side="right")
        
        # 按鈕區域
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # 開始遊戲按鈕
        start_button = tk.Button(button_frame, text="開始遊戲", 
                                font=("Arial", 14, "bold"), bg="darkgreen", fg="white",
                                command=self.start_game, height=2)
        start_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # 檢查系統按鈕
        check_button = tk.Button(button_frame, text="系統檢查",
                                font=("Arial", 12), bg="darkblue", fg="white", 
                                command=self.check_system)
        check_button.pack(side="right", padx=(5, 0))
        
        # 狀態列
        self.status_var = tk.StringVar(value="準備就緒")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief="sunken", anchor="w")
        status_bar.pack(fill="x", side="bottom")
    
    def check_system(self):
        """檢查系統需求"""
        self.status_var.set("正在檢查系統...")
        self.root.update()
        
        issues = []
        
        # 檢查Python版本
        if sys.version_info < (3, 7):
            issues.append(f"Python版本過舊 (需要3.7+，目前{sys.version_info.major}.{sys.version_info.minor})")
        
        # 檢查Pygame
        try:
            import pygame
            pygame.init()
        except ImportError:
            issues.append("Pygame未安裝")
        except Exception as e:
            issues.append(f"Pygame初始化失敗: {e}")
        
        # 檢查遊戲檔案
        required_files = ["main.py", "game_state.py", "map_manager.py", 
                         "player.py", "ui.py", "combat.py", "inventory.py"]
        
        for file in required_files:
            if not os.path.exists(file):
                issues.append(f"缺少遊戲檔案: {file}")
        
        # 檢查assets資料夾
        if not os.path.exists("assets"):
            issues.append("缺少assets資料夾 (建議執行setup.py)")
        
        # 顯示結果
        if issues:
            issue_text = "\n".join([f"• {issue}" for issue in issues])
            messagebox.showerror("系統檢查失敗", 
                               f"發現以下問題:\n\n{issue_text}\n\n請修復後再試。")
            self.status_var.set("系統檢查失敗")
        else:
            messagebox.showinfo("系統檢查完成", "所有檢查通過！遊戲可以正常執行。")
            self.status_var.set("系統檢查通過")
    
    def start_game(self):
        """啟動遊戲"""
        self.status_var.set("正在啟動遊戲...")
        self.root.update()
        
        # 更新配置
        self.config["resolution"] = self.resolution_var.get()
        self.config["fullscreen"] = self.fullscreen_var.get()
        self.config["difficulty"] = self.difficulty_var.get()
        self.config["volume"] = self.volume_var.get()
        
        try:
            # 設定環境變數
            width, height = self.config["resolution"].split("x")
            os.environ["GAME_WIDTH"] = width
            os.environ["GAME_HEIGHT"] = height
            os.environ["GAME_FULLSCREEN"] = str(self.config["fullscreen"])
            os.environ["GAME_DIFFICULTY"] = self.config["difficulty"]
            os.environ["GAME_VOLUME"] = str(self.config["volume"])
            
            # 啟動遊戲
            self.root.withdraw()  # 隱藏啟動器
            
            # 執行主遊戲
            result = subprocess.run([sys.executable, "main.py"], 
                                  capture_output=True, text=True)
            
            # 遊戲結束後顯示啟動器
            self.root.deiconify()
            
            if result.returncode != 0:
                messagebox.showerror("遊戲錯誤", 
                                   f"遊戲異常結束:\n{result.stderr}")
                self.status_var.set("遊戲異常結束")
            else:
                self.status_var.set("遊戲正常結束")
                
        except FileNotFoundError:
            messagebox.showerror("啟動失敗", "找不到main.py檔案")
            self.status_var.set("啟動失敗")
        except Exception as e:
            messagebox.showerror("啟動失敗", f"啟動遊戲時發生錯誤:\n{e}")
            self.status_var.set("啟動失敗")
    
    def run(self):
        """執行啟動器"""
        self.root.mainloop()

def main():
    """主程序"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        print(f"啟動器錯誤: {e}")
        # 如果啟動器失敗，嘗試直接啟動遊戲
        try:
            import main
        except ImportError:
            print("無法找到遊戲主程式")

if __name__ == "__main__":
    main()