---
title: 撰寫內容
author: Richard Chien
created: 2017-03-20
updated: 2017-06-02
language: zh-hant
---

VeriPress 支援三種內容形式：文章（post）、自訂頁面（page）、頁面部件（widget）。其中，文章（post）是指可以通過 `/post/<year>/<month>/<day>/<post_name>/` 形式的 URL 訪問的頁面；自訂頁面（page）是指直接在根 URL 後加上頁面路徑來訪問的頁面，如 `/hello/` 或 `/my-custom/page.html`；頁面部件（widget）是指常駐頁面的小部件，需要主題支援，預設主題只支援一種部件，也就是側邊欄部件。

## 通用

### 檔案格式

除了之前的 [開始使用](getting-started.html) 中提到的 Markdown 格式，目前還支持 TXT 格式，後續還會加入其它格式的支持。VeriPress 通過檔副檔名來區分格式，並通過相應格式的解析器將正文解析成 HTML 並傳給主題來顯示。下面是目前支持的格式列表：

| 格式名稱     | 支援的副檔名                     |
| -------- | -------------------------- |
| markdown | `.md`、`.mdown`、`.markdown` |
| txt      | `.txt`                     |

其中，Markdown 格式採用「Markdown Extra」擴展，該擴展在 [標準 Markdown 語法](https://daringfireball.net/projects/markdown/syntax) 的基礎上，加入了一些其它實用語法，具體見 [PHP Markdown Extra](https://michelf.ca/projects/php-markdown/extra/)。

無論使用什麼格式書寫內容，檔的開頭都使用 YAML 來標記元資訊，並在其上下分別用 `---` 來分隔，例如：

```
---
title: 文章的標題
author: 作者
---

正文內容，可使用不同的格式／標記語言書寫。
```

### YAML 頭部

YAML 頭部用於標記文章、頁面、部件的一些基本元資訊，比如標題、作者、標籤、分類等，這裡的元資訊將被傳到主題的範本檔中，因此具體這些資訊有哪些被顯示出來、以什麼形式顯示，都取決於你使用的主題，後面對三種內容形式的分別闡述中，將主要給出 VeriPress 原生支持的（或者說預設主題支援的）元資訊項。

另外，三種內容形式都支援的一個元資訊是 `is_draft`，用於表示該篇內容是否為草稿，例如，如果有一篇文章內容如下：

```
---
title: 標題
is_draft: true
---

正文內容
```

則它將不會顯示在文章清單中，也無法通過具體路徑訪問（API 也無法訪問）。`is_draft` 的預設值是 `false`，因此如果不填，默認認為不是草稿，會將其發佈。這個元資訊的效果是由 VeriPress 核心程式所保證的，因此不會受主題的影響。

另外，所有官方主題（即 [veripress/themes](https://github.com/veripress/themes) 倉庫中的主題），均支援 `language` 元資訊（三種內容形式都支援），此元資訊項的值，會覆蓋 `site.json` 中的同名項，見 [修改網站資訊](getting-started.html#修改網站資訊)。

## 文章（Post）

文章可通過形如 `/post/<year>/<month>/<day>/<post_name>/` 的 URL 訪問，檔放在 `posts` 目錄中，命名格式形如 `2017-03-20-post-name.md`，因為文章其實就是博客的「博文」，發佈時間非常重要，因此在檔案名中指出創建日期將有助於管理，同時也在 YAML 頭部沒有指定創建日期時作為默認的創建日期。

### 支援的 YAML 元資訊

文章預設支援的 YAML 元資訊如下：

| 項            | 預設值                                      | 說明                                       |
| ------------ | ---------------------------------------- | ---------------------------------------- |
| `title`      | 檔案名的 `post-name` 中 `-` 換成空格並讓每個單詞首字母大寫，如 `Post Name` | 文章標題                                     |
| `layout`     | `post`                                   | 文章的頁面配置，VeriPress 會在主題的範本目錄中尋找和這個項同名的範本檔來渲染頁面，一般情況下保持預設即可 |
| `author`     | `site.json` 中的 `author` 項                | 文章的作者名                                   |
| `email`      | `site.json` 中的 `email` 項                 | 文章的作者 email                              |
| `created`    | 檔案名中的日期的 00:00:00                        | 創建時間                                     |
| `updated`    | 等於 `created`                             | 更新時間                                     |
| `tags`       | 空列表                                      | 文章所屬標籤，可使用 YAML 字串或清單，如 `tags: Hello` 或 `tags: [TagA, TagB]` |
| `categories` | 空列表                                      | 文章所屬分類，同樣可使用 YAML 字串或清單                 |

### 劃分預覽部分

文章還支援在正文中劃分預覽部分，從而在文章清單中僅顯示預覽部分，以節省頁面空間。不同的檔案格式，使用不同的預覽分隔標記（或稱閱讀更多標記），如下：

| 格式名稱     | 預覽分隔標記／閱讀更多標記 |
| -------- | ------------- |
| markdown | `<!--more-->` |
| txt      | `---more---`  |

預覽分隔標記之前的內容將被作為預覽部分顯示在首頁文章清單中（需要主題支援），並顯示一個 `READ MORE` 連結，而沒有預覽分隔標記的文章將預設把全部正文作為預覽部分，這時將不顯示 `READ MORE` 連結（這是預設主題的行為，協力廠商主題未必這樣）。

注意：分隔標記前後都需要換行才有效。

## 自訂頁面（Page）

自訂頁面有時候被直接稱為「頁面」，它們可通過形如 `/hello/` 或 `/my-custom/page.html` 的 URL 訪問，檔放在 `pages` 目錄中，命名格式形如 `page-name.md`。

### 頁面訪問邏輯

之所以稱為自訂頁面，是因為這種內容形式自訂性比較強，你可以在 `pages` 中創建多級目錄來組織自訂頁面，甚至可以直接將 HTML 檔或其它靜態檔放在裡面。

對於使用非 HTML、且 VeriPress 支持的檔案格式，可以通過 `.html` 尾碼的 URL 來訪問，比如有一個自訂頁面的檔路徑是 `/pages/a/b/c/d.md`，你將可以通過 `/a/b/c/d.html` 來訪問這個頁面，與此同時，你還可以直接通過 `/a/b/c/d.md` 來訪問這個原始 Markdown 檔（前提是設定檔中的 `PAGE_SOURCE_ACCESSIBLE` 設置為 `True`，見 [設定檔](configuration-file.html#PAGE-SOURCE-ACCESSIBLE)）。如果這裡的 Markdown 檔案名是 `index`，例如 `/pages/a/b/c/index.md`，你還可以通過 `/a/b/c/` 來訪問。

而如果直接使用 HTML 檔，邏輯則更加簡單：只要這個檔存在，就會直接返回，例如你可以通過 URL `/abc/index.html` 或 `/abc/` 來訪問檔 `/pages/abc/index.html`。

如果你直接在 `pages` 目錄中創建了一個 `index.md` 或 `index.html` 或其它所支援的檔案格式，這個自訂頁面將會覆蓋首頁，也就是當你訪問 URL `/` 的時候，訪問的實際上是這個自訂頁面，而不是預設的文章列表。

### 支援的 YAML 元資訊

自訂頁面預設支援的 YAML 元資訊如下：

| 項         | 預設值                                      | 說明                                       |
| --------- | ---------------------------------------- | ---------------------------------------- |
| `title`   | 檔案名的中 `-` 換成空格並讓每個單詞首字母大寫，對於 `index.xx` 將對它的上一級目錄進行轉換，如 `hello-world/index.md` 的默認標題為 `Hello World`，`hello.md` 預設為 `Hello` | 頁面的標題                                    |
| `layout`  | `page`                                   | 自訂頁面的頁面配置，VeriPress 會在主題的範本目錄中尋找和這個項同名的範本檔來渲染頁面，一般情況下保持預設即可 |
| `author`  | `site.json` 中的 `author` 項                | 頁面的作者名                                   |
| `email`   | `site.json` 中的 `email` 項                 | 頁面的作者 email                              |
| `created` | 空                                        | 創建時間                                     |
| `updated` | 等於 `created`                             | 更新時間                                     |

## 頁面部件（Widget）

頁面部件是指常駐頁面的小部件，例如出現在側邊欄、頂欄、footer 等，但這需要主題支援，預設主題只支援側邊欄部件（sidebar）。

### 支援的 YAML 元資訊

頁面部件預設支援的 YAML 元資訊如下：

| 項          | 預設值  | 說明                                       |
| ---------- | ---- | ---------------------------------------- |
| `position` | 空    | 部件應該出現的位置，例如預設主題支援 `sidebar`，所有 `position` 為 `sidebar` 的部件將顯示在側邊欄 |
| `order`    | 空    | 部件在其位置上的順序，主題在獲取部件清單時將按此項從小到大排序          |

對於頁面部件來說，上面兩個元資訊基本上都是必填（除非顯示順序不重要或主題不區分位置）。
