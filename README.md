# yc-datapack

YC Startup School Taipei 2026 現場資料包的檔案結構與欄位定義。結構以 Franck 的 DOC-791 資料包架構與收集項目 database 為準，檔名、資料夾名與欄位名一律英文。

## 結構

```txt
schema/                       欄位定義的唯一來源
├─ files.csv                  每個檔案：路徑、中文名稱、版本、一列代表什麼、主鍵、來源設備
├─ fields.csv                 每個欄位：型別、必填、單位、允許值、定義、範例
├─ parameters.csv             定義中用到的門檻與權重、值、是否已定案、負責分類
├─ owners.csv                 工作分類與負責人
└─ franck_v0_mapping.md       與 Franck v0 架構版 zip 的逐欄對照
tools/
├─ build.py                   由 schema 產生 CSV 標題列、manifest.csv、file_owners.csv 與 docs/field_reference.md
├─ validate.py                檢查 datapack 裡的 CSV 是否符合 schema（含 UTF-8 BOM）
└─ package.py                 驗證後打包發布用 zip，排除內部檔案
datapack/                     資料包本體（用 tools/package.py 打包）
├─ 00_README.md
├─ 01_transcript_segmented.md
├─ CHANGELOG.md
├─ manifest.csv
├─ file_owners.csv            檔案負責人對照表（內部用，打包時排除）
├─ content/                   台上：議程、逐字稿、簡報、段落類別、提到台灣、提到工具
├─ notes/                     一場一份現場筆記
├─ reactions/                 台下：聲音事件、高峰、舉手機、舉手、現場調查、每分鐘總表
├─ presence/                  台下：可見人數、坐著、站著、離席、回座、坐滿順序、Wifi 人流
├─ after_talk/                講完被圍住
├─ questions/                 台上 Q&A、活動前問題、沒問出口的、你記得哪一刻
├─ startups/                  創業題目
├─ speakers/                  講者公開資料、新聞、公開專案、過去講法
├─ social/                    講者與 YC 貼文、貼文對到現場時刻
├─ online/                    活動後貼文、搜尋量
├─ side_events/               周邊活動報名人數
├─ outside/                   進出場、看了看板沒進場
├─ rankings/                  冷知識排行榜
├─ scene/                     場景描述（只有文字）
├─ derivatives/               二創回灌
└─ docs/                      欄位說明、設備與機位、量不到什麼、場地平面圖
```

每個欄位的完整定義見 [`datapack/docs/field_reference.md`](datapack/docs/field_reference.md)。

資料包只放 CSV 與 Markdown；`build.py` 會擋下其他格式。CSV 一律 UTF-8 含 BOM（繁體中文用 Excel 直接開不會亂碼），Markdown 不含 BOM。

## 怎麼改欄位

1. 改 `schema/fields.csv`（或 `files.csv`、`parameters.csv`）。值裡不要用半形逗號，允許值以 `|` 分隔。
2. 執行 `python3 tools/build.py`，重新產生 CSV 標題列、`manifest.csv`、`file_owners.csv` 與 `docs/field_reference.md`。
3. 執行 `python3 tools/validate.py`，確認資料包符合 schema。
4. 在 `datapack/CHANGELOG.md` 記下改了什麼。
5. 發布時執行 `python3 tools/package.py <版本>`，產生 `dist/datapack_yc_taipei_1112_<版本>.zip`。

`build.py` 會覆寫 CSV 的標題列、`manifest.csv` 與 `file_owners.csv`；已經填入資料後，改用 `validate.py` 檢查，不要再跑 `build.py`。手寫的 Markdown 不會被覆寫。

## 與 Franck 原始命名的對照

| Franck（DOC-791） | 本 repo |
| --- | --- |
| `00_先看這個.md` | `00_README.md` |
| `01_全場逐字稿_分段.md` | `01_transcript_segmented.md` |
| `notes/NN-講者.md` | `notes/{segment_id}_{speaker_id}.md` |
| `docs/欄位說明.md` | `docs/field_reference.md` |
| `docs/設備與機位.md` | `docs/devices_and_positions.md` |
| `docs/量不到什麼.md` | `docs/limitations.md` |
| `docs/場地平面圖` | `docs/venue_map.md`（文字，不附圖） |
| `scene/photos/`、3D 模型 | `scene/scene_description.md`（文字） |
| 設備 R、D | 改由 `X5`（Insta360）取代 |

其他檔案沿用 DOC-791 收集項目 database 的檔名。標「不做」與「不進資料包」的項目沒有收錄。

## 負責人

每個檔案的負責人見 `datapack/file_owners.csv`，由 `schema/owners.csv`（分類）與 `schema/files.csv` 的 `owner_area`、`owners_override` 產生。

| 分類 | 負責人 | 範圍 |
| --- | --- | --- |
| 聲音 | Ray | 聲音事件、逐字稿與由逐字稿衍生的表 |
| Insta360 影片處理 | Ivan、Leon、Jack | 舉手、舉手機、在座、反應高峰、每分鐘總表、現場手持與場外人流；簡報換頁與簡報筆記由 Jack、場景描述由 Leon |
| 網路與表單資料蒐集 | Edward | 講者資料、貼文、搜尋量、周邊活動、報名表與問卷 |
| 二創與影片串流 | Mike | 二創回灌 |
| 資料包統整 | Emerson | 入口說明、版本紀錄、目錄、議程、冷知識與 docs/ |

## 已決定

- 版本：v0.5（活動前）→ v1（散場 2 小時內）→ v1.1（當晚或隔天）→ v2（一週內）。
- 不適合二創的句子：`text` 改成「[不公開]」，保留時間與句子編號。
- Wifi CSI：放進 v1.1，列為延伸；TK-2801 驗收通過才發布。
- 已定的參數：Insta360 每秒取 2 張；高峰權重掌聲 1、笑聲 2、舉手機 1；講者 1.5 公尺內至少 3 人算圍住；看板前停 3 秒算停下。

## 待確認

- **Wifi 人流負責人**：`presence/csi.csv` 還沒有負責人。
- **測試門檻**：`schema/parameters.csv` 中 `to_test` 的值是建議起始值，試錄後由該參數 `owner_area` 的負責人調整。
- **場地細節**：`docs/venue_map.md` 的分區與 X5 架設高度，踩點後回填。
- **與 v0 刻意不同的地方**：台下影像只用 X5、舉手與舉手機分開、舉手機改為一次事件一列、只放文字、每分鐘總表放原句不摘要。對照與原因見 [`schema/franck_v0_mapping.md`](schema/franck_v0_mapping.md)，要和 Franck 確認。
