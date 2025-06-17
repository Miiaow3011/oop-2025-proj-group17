#!/usr/bin/env python3
# setup_sounds.py - 音樂和音效資料夾設置腳本

import os
import sys

def create_sounds_structure():
    """創建音效資料夾結構"""
    print("🎵 設置音樂和音效資料夾結構...")
    
    # 基本路徑
    base_path = "assets"
    sounds_path = os.path.join(base_path, "sounds")
    
    # 創建資料夾
    os.makedirs(sounds_path, exist_ok=True)
    print(f"📁 創建資料夾: {sounds_path}")
    
    # 音樂文件列表
    music_files = [
        "intro_music.mp3",
        "character_select.mp3",
        "exploration_music.mp3",
        "combat_music.mp3",
        "dialogue_music.mp3",
        "victory_music.mp3",
        "game_over_music.mp3"
    ]
    
    # 音效文件列表
    sfx_files = [
        "move.wav",
        "interact.wav",
        "collect_item.wav",
        "combat_hit.wav",
        "combat_defend.wav",
        "level_up.wav",
        "dialogue_beep.wav",
        "error.wav",
        "success.wav",
        "stairs.wav",
        "door.wav"
    ]
    
    # 創建說明文件
    readme_content = """# 末世第二餐廳 - 音樂和音效文件說明

## 音樂文件 (MP3格式)
這些文件應該放在 assets/sounds/ 資料夾中：

### 背景音樂
- intro_music.mp3          : 開場介紹音樂 (循環播放)
- character_select.mp3     : 角色選擇音樂 (循環播放)
- exploration_music.mp3    : 探索模式音樂 (循環播放)
- combat_music.mp3         : 戰鬥音樂 (循環播放)
- dialogue_music.mp3       : 對話音樂 (循環播放，音量較低)
- victory_music.mp3        : 勝利音樂 (單次播放)
- game_over_music.mp3      : 遊戲結束音樂 (單次播放)

## 音效文件 (WAV格式)
這些文件應該放在 assets/sounds/ 資料夾中：

### 遊戲音效
- move.wav                 : 移動音效 (玩家移動時)
- interact.wav             : 互動音效 (按空白鍵時)
- collect_item.wav         : 收集物品音效 (撿到物品時)
- combat_hit.wav           : 攻擊音效 (戰鬥中攻擊時)
- combat_defend.wav        : 防禦音效 (戰鬥中防禦時)
- level_up.wav             : 升級音效 (等級提升時)
- dialogue_beep.wav        : 對話嗶嗶聲 (對話選項時)
- error.wav                : 錯誤音效 (操作失敗時)
- success.wav              : 成功音效 (操作成功時)
- stairs.wav               : 樓梯音效 (使用樓梯時)
- door.wav                 : 開門音效 (使用鑰匙卡時)

## 音樂建議
建議的音樂風格和來源：

### 背景音樂
- 開場音樂: 末世感的陰沉音樂
- 角色選擇: 輕鬆的選擇音樂
- 探索音樂: 緊張但不急迫的背景音樂
- 戰鬥音樂: 快節奏、緊張的戰鬥音樂
- 對話音樂: 安靜、輕柔的對話背景音樂
- 勝利音樂: 歡快的勝利音樂
- 失敗音樂: 沉重的失敗音樂

### 音效
- 建議使用簡短（0.5-2秒）的音效
- WAV格式確保最佳兼容性
- 音量適中，不要過於響亮

## 音樂控制
遊戲中的音樂控制：
- F6: 切換背景音樂開關
- F7: 切換音效開關
- F8: 調整音樂音量 (20%, 40%, 60%, 80%, 100%)
- F9: 調整音效音量 (20%, 40%, 60%, 80%, 100%)

## 免費音樂資源
推薦的免費音樂和音效網站：
- Freesound.org (音效)
- OpenGameArt.org (遊戲音樂和音效)
- Zapsplat.com (需註冊)
- Pixabay Music (免費音樂)
- YouTube Audio Library

## 注意事項
1. 確保音樂文件格式正確 (MP3 for music, WAV for SFX)
2. 文件名必須完全符合上述列表
3. 如果沒有某個音樂文件，遊戲仍可正常運行
4. 音樂文件大小建議不超過 10MB
5. 確保音樂文件沒有版權問題

## 測試
啟動遊戲後：
1. 檢查控制台輸出中的音樂文件載入狀態
2. 按F1開啟除錯模式查看音效系統狀態
3. 測試各種音效和音樂切換功能
"""
    
    readme_path = os.path.join(sounds_path, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"📄 創建說明文件: {readme_path}")
    
    # 創建音樂文件列表
    music_list_content = "# 音樂文件列表\n\n## 需要的音樂文件:\n\n"
    for music_file in music_files:
        file_path = os.path.join(sounds_path, music_file)
        music_list_content += f"- {music_file}\n"
        if not os.path.exists(file_path):
            music_list_content += f"  ❌ 尚未添加\n"
        else:
            music_list_content += f"  ✅ 已存在\n"
    
    music_list_content += "\n## 需要的音效文件:\n\n"
    for sfx_file in sfx_files:
        file_path = os.path.join(sounds_path, sfx_file)
        music_list_content += f"- {sfx_file}\n"
        if not os.path.exists(file_path):
            music_list_content += f"  ❌ 尚未添加\n"
        else:
            music_list_content += f"  ✅ 已存在\n"
    
    list_path = os.path.join(sounds_path, "file_list.md")
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write(music_list_content)
    print(f"📋 創建文件列表: {list_path}")
    
    # 檢查現有文件
    existing_files = []
    missing_files = []
    
    print("\n🔍 檢查音樂文件狀態:")
    for music_file in music_files:
        file_path = os.path.join(sounds_path, music_file)
        if os.path.exists(file_path):
            existing_files.append(music_file)
            print(f"  ✅ {music_file}")
        else:
            missing_files.append(music_file)
            print(f"  ❌ {music_file}")
    
    print("\n🔍 檢查音效文件狀態:")
    for sfx_file in sfx_files:
        file_path = os.path.join(sounds_path, sfx_file)
        if os.path.exists(file_path):
            existing_files.append(sfx_file)
            print(f"  ✅ {sfx_file}")
        else:
            missing_files.append(sfx_file)
            print(f"  ❌ {sfx_file}")
    
    # 創建空白文件作為佔位符（可選）
    create_placeholders = input("\n❓ 是否創建空白佔位符文件？(y/n): ").strip().lower()
    if create_placeholders in ['y', 'yes', 'Y', 'YES']:
        print("\n📝 創建佔位符文件...")
        for missing_file in missing_files:
            placeholder_path = os.path.join(sounds_path, f"{missing_file}.placeholder")
            with open(placeholder_path, 'w') as f:
                f.write(f"# 這是 {missing_file} 的佔位符文件\n")
                f.write(f"# 請用真正的音樂/音效文件替換此文件\n")
                f.write(f"# 文件格式: {'MP3' if missing_file.endswith('.mp3') else 'WAV'}\n")
            print(f"  📝 {placeholder_path}")
    
    # 總結
    print(f"\n✅ 音效資料夾設置完成！")
    print(f"📁 音效資料夾: {sounds_path}")
    print(f"✅ 已存在文件: {len(existing_files)}")
    print(f"❌ 缺少文件: {len(missing_files)}")
    
    if missing_files:
        print(f"\n🎵 接下來的步驟:")
        print(f"1. 到免費音樂網站下載合適的音樂和音效")
        print(f"2. 將文件重命名為上述列表中的名稱")
        print(f"3. 將文件放入 {sounds_path} 資料夾")
        print(f"4. 重新執行此腳本檢查狀態")
        print(f"5. 啟動遊戲測試音效系統")
    else:
        print(f"\n🎉 所有音效文件都已就位！可以啟動遊戲了！")
    
    print(f"\n📖 詳細說明請查看: {readme_path}")

def main():
    """主函數"""
    print("🎮 末世第二餐廳 - 音效設置工具")
    print("=" * 50)
    
    try:
        create_sounds_structure()
        
        print("\n" + "=" * 50)
        print("🎵 音效設置完成！")
        print("💡 提示:")
        print("   - 遊戲即使沒有音樂文件也能正常運行")
        print("   - 建議先下載一些免費的音效文件")
        print("   - 使用 F6-F9 鍵控制音效設定")
        print("   - 啟動遊戲時會顯示音效文件載入狀態")
        
    except Exception as e:
        print(f"❌ 設置過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()