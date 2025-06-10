import pygame
import os
import sys
import platform

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.system_fonts = []
        self.default_font = None
        self.load_system_fonts()
    
    def load_system_fonts(self):
        """載入系統中文字體"""
        # 初始化pygame字體系統
        pygame.font.init()
        
        # 不同作業系統的中文字體路徑
        system = platform.system()
        
        if system == "Windows":
            font_paths = [
                "C:/Windows/Fonts/msjh.ttc",      # 微軟正黑體
                "C:/Windows/Fonts/msyh.ttc",      # 微軟雅黑
                "C:/Windows/Fonts/simsun.ttc",    # 宋體
                "C:/Windows/Fonts/simhei.ttf",    # 黑體
                "C:/Windows/Fonts/kaiu.ttf",      # 標楷體
            ]
        elif system == "Darwin":  # macOS
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",           # 蘋方
                "/System/Library/Fonts/Helvetica.ttc",          # Helvetica
                "/Library/Fonts/Arial Unicode MS.ttf",          # Arial Unicode
                "/System/Library/Fonts/STHeiti Medium.ttc",     # 黑體
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
        
        # 檢查自定義字體資料夾
        custom_font_dir = "assets/fonts"
        if os.path.exists(custom_font_dir):
            for font_file in os.listdir(custom_font_dir):
                if font_file.lower().endswith(('.ttf', '.ttc', '.otf')):
                    font_paths.insert(0, os.path.join(custom_font_dir, font_file))
        
        # 尋找可用的字體
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    # 測試字體是否支援中文
                    test_font = pygame.font.Font(font_path, 16)
                    test_surface = test_font.render("測試中文", True, (255, 255, 255))
                    if test_surface.get_width() > 0:
                        self.system_fonts.append(font_path)
                        if self.default_font is None:
                            self.default_font = font_path
                        print(f"找到中文字體: {font_path}")
                except:
                    continue
        
        # 如果沒找到任何字體，使用pygame預設字體
        if not self.system_fonts:
            print("警告: 未找到中文字體，將使用預設字體")
            self.default_font = None
            # 嘗試使用系統預設字體
            try:
                available_fonts = pygame.font.get_fonts()
                chinese_fonts = [f for f in available_fonts if any(cn in f.lower() for cn in ['chinese', 'cjk', 'han', 'zh'])]
                if chinese_fonts:
                    self.default_font = chinese_fonts[0]
            except:
                pass
    
    def get_font(self, size, bold=False):
        """獲取指定大小的字體"""
        font_key = (size, bold)
        
        if font_key not in self.fonts:
            font_path = self.default_font
            
            try:
                if font_path and os.path.exists(font_path):
                    font = pygame.font.Font(font_path, size)
                else:
                    # 使用pygame預設字體
                    font = pygame.font.Font(None, size)
                    
                # 設定粗體
                if bold:
                    font.set_bold(True)
                
                self.fonts[font_key] = font
                
            except Exception as e:
                print(f"字體載入失敗: {e}")
                # 最後的備用方案
                try:
                    font = pygame.font.Font(None, size)
                    if bold:
                        font.set_bold(True)
                    self.fonts[font_key] = font
                except:
                    # 如果連預設字體都失敗，建立一個空字體物件
                    self.fonts[font_key] = pygame.font.Font(None, 16)
        
        return self.fonts[font_key]
    
    def render_text(self, text, size, color, bold=False, antialias=True):
        """渲染文字，支援中文"""
        font = self.get_font(size, bold)
        
        try:
            # 嘗試渲染文字
            surface = font.render(text, antialias, color)
            
            # 檢查是否正確渲染（寬度大於0）
            if surface.get_width() > 0:
                return surface
            else:
                # 如果渲染失敗，嘗試使用其他字體
                return self.fallback_render(text, size, color, bold, antialias)
                
        except Exception as e:
            print(f"文字渲染失敗: {text}, 錯誤: {e}")
            return self.fallback_render(text, size, color, bold, antialias)
    
    def fallback_render(self, text, size, color, bold=False, antialias=True):
        """備用渲染方法"""
        try:
            # 嘗試使用系統預設字體
            default_font = pygame.font.Font(None, size)
            if bold:
                default_font.set_bold(True)
            
            surface = default_font.render(text, antialias, color)
            return surface
            
        except:
            # 最後的備用方案：建立一個空白surface
            surface = pygame.Surface((len(text) * size // 2, size))
            surface.fill((0, 0, 0))
            surface.set_colorkey((0, 0, 0))
            
            # 用簡單的矩形代替文字
            pygame.draw.rect(surface, color, (0, 0, len(text) * size // 3, size // 2))
            
            return surface
    
    def render_multiline_text(self, text, size, color, max_width, bold=False):
        """渲染多行文字"""
        font = self.get_font(size, bold)
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = self.render_text(test_line, size, color, bold)
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # 渲染每一行
        surfaces = []
        for line in lines:
            if line.strip():
                surface = self.render_text(line, size, color, bold)
                surfaces.append(surface)
        
        return surfaces
    
    def get_text_size(self, text, size, bold=False):
        """獲取文字尺寸"""
        font = self.get_font(size, bold)
        return font.size(text)
    
    def install_chinese_font(self):
        """安裝中文字體的輔助函數"""
        print("正在檢查中文字體...")
        
        if not self.system_fonts:
            print("系統中未找到中文字體。")
            print("建議:")
            print("1. Windows: 確保系統已安裝微軟正黑體或其他中文字體")
            print("2. macOS: 系統應該內建中文字體支援")
            print("3. Linux: 安裝中文字體包")
            print("   Ubuntu/Debian: sudo apt-get install fonts-wqy-microhei")
            print("   CentOS/RHEL: sudo yum install wqy-microhei-fonts")
            print("4. 或將TTF中文字體檔案放入 assets/fonts/ 資料夾")
            
            return False
        else:
            print(f"找到 {len(self.system_fonts)} 個中文字體")
            for font in self.system_fonts:
                print(f"  - {font}")
            return True

# 全域字體管理器實例
font_manager = FontManager()

def get_font(size, bold=False):
    """快速獲取字體的函數"""
    return font_manager.get_font(size, bold)

def render_text(text, size, color, bold=False):
    """快速渲染文字的函數"""
    return font_manager.render_text(text, size, color, bold)