# HTML 打包工具使用說明

## 功能說明

這個工具可以將多個 Markdown 文件打包成 HTML 網頁，並自動生成一個漂亮的索引頁面，讓您可以點擊瀏覽每個文件。

## 使用方法

### 基本使用

```bash
python3 tools/pack_to_html.py <MD文件目錄> [輸出目錄] [標題]
```

### 範例

```bash
# 將 test 目錄下的所有 MD 文件打包到 docs 目錄
python3 tools/pack_to_html.py ./test ./docs "PSS 專案文件"

# 使用預設輸出目錄 (./docs)
python3 tools/pack_to_html.py ./test

# 使用預設標題
python3 tools/pack_to_html.py ./test ./output
```

## 功能特色

✨ **自動轉換** - 自動將所有 MD 文件轉換成 HTML
📑 **索引頁面** - 自動生成漂亮的卡片式索引頁面
🎨 **美觀設計** - 現代化的漸層背景和卡片設計
📱 **響應式** - 支援手機、平板、電腦各種螢幕
🔍 **完整目錄** - 每個 HTML 頁面都有完整的目錄導航

## 輸出結果

執行後會在輸出目錄中生成：

```
docs/
├── index.html          # 索引頁面（主入口）
├── 專案功能清單.html   # 轉換後的文件 1
├── 安裝指南.html       # 轉換後的文件 2
└── API文件.html        # 轉換後的文件 3
```

## 快速開始

```bash
# 1. 確認有 pandoc
which pandoc

# 2. 如果沒有，安裝 pandoc
# Ubuntu/Debian: sudo apt-get install pandoc
# macOS: brew install pandoc

# 3. 執行打包
python3 tools/pack_to_html.py ./test ./docs "我的專案文件"

# 4. 在瀏覽器中開啟
# 直接開啟 docs/index.html
```

## 部署到網頁伺服器

打包後的 docs 目錄可以直接部署到任何網頁伺服器：

### GitHub Pages

```bash
# 將 docs 目錄推送到 GitHub
git add docs/
git commit -m "Add documentation"
git push

# 在 GitHub repo 設定中啟用 GitHub Pages，選擇 docs 目錄
```

### 本地預覽

```bash
# 使用 Python 內建的 HTTP 伺服器
cd docs
python3 -m http.server 8000

# 然後在瀏覽器開啟: http://localhost:8000
```

## 自訂樣式

如果您想修改索引頁面的樣式，可以編輯 `tools/pack_to_html.py` 中的 CSS 部分。

## 注意事項

- 需要安裝 pandoc
- MD 文件需要使用 UTF-8 編碼
- 圖片路徑建議使用相對路徑或絕對 URL
- 輸出目錄會自動創建，如果已存在會覆蓋同名文件

http://localhost/html/doc/root/PSS_WEB_APP/

python3 tools/root_to_html.py

python3 tools/pack_html.py 

python3 tools/pack_md_to_html.py others/SUPPORT/MANTIS.md

把 PowerMoat管理系統維運手冊_v20250827裡 使用者帳號維護的內容獨立出來到  root/使用者管理設定/使用者帳號維護.md 把圖放在images/U0001

把 PowerMoat管理系統維運手冊_v20250827裡 列印審核中 部門審核者進行審核作業 的內容獨立出來到 root/列印審核/部門審核者進行審核作業.md 把圖放在images/PRTAD0004

