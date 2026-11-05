# 欄位說明

本檔由 `tools/build.py` 依 `schema/` 產生，請勿手動修改；要改欄位請改 `schema/fields.csv` 後重新產生。

## 共通規則

- **檔案格式**：CSV 一律 UTF-8 含 BOM（Excel 直接開繁體中文不會亂碼）、逗號分隔、換行為 LF、第一列為欄位名；含逗號、引號或換行的值用雙引號包起來（RFC 4180）。
- **命名**：檔名、資料夾名與欄位名一律英文小寫，以 `_` 連接。
- **時間軸**：`t_sec` 是從 T0 起算的秒數，T0 是開場第一段掌聲在主收音設備上的起點，T0 以前為負數；所有裝置以同一個聲音事件對時。`*_clock` 是同一時刻的台北時間。
- **區間**：`start_t_sec` 到 `end_t_sec` 是左閉右開區間 [start, end)。
- **空值與零**：沒測到、不適用或畫面不可用時留空；`0` 代表有測，結果是零。
- **計數是下限**：遮擋會造成低估，所有人數欄位代表「至少」。
- **只有文字**：資料包只放 CSV 與 Markdown，不放影片、音檔、照片與 3D 模型；場景以文字描述，見 `scene/scene_description.md`。
- **影像只數人**：台下的舉手、舉手機、坐著、站著、離席與回座都由 Insta360（X5）的 360 影片偵測；只輸出人數，不認臉、不保存也不輸出任何個人編號或軌跡；前後畫面的比對只用來判斷動作持續幾秒。
- **個資**：不收觀眾的姓名、臉、聯絡方式與帳號；姓名只限同意公開的講者；問題與題目改寫時移除身分線索。
- **不放判斷**：只放觀察值與照公開規則算出的結果；重點、金句等判斷放報告。
- **參數**：定義中出現的參數名（例如 `polite_window_sec`）見文末參數表。

## 欄位型別

| 型別 | 格式 |
| --- | --- |
| `string` | 文字 |
| `integer` | 整數 |
| `number` | 數字，小數點用 .，最多三位小數 |
| `boolean` | true 或 false（小寫） |
| `enum` | 只能填「允許值」中的一個 |
| `id` | 代號，格式見定義 |
| `id_list` | 多個代號，以 ; 分隔，不加空格 |
| `url` | 完整網址，含 https:// |
| `url_list` | 多個網址，以 ; 分隔 |
| `date` | YYYY-MM-DD |
| `datetime` | ISO 8601，含時區 +08:00，例如 2026-11-12T13:05:00+08:00 |

必填欄：`yes` 必填；`no` 可留空；`conditional` 條件必填（條件寫在定義中）。

## 檔案總覽

| 檔案 | 中文名稱 | 版本 | 優先序 | 誰填 | 一列代表 | 主鍵 |
| --- | --- | --- | --- | --- | --- | --- |
| `00_README.md` | 資料包入口 | v0.5 | core | office | — | — |
| `01_transcript_segmented.md` | 全場逐字稿（分段） | v1 | core | pipeline | — | — |
| `CHANGELOG.md` | 版本紀錄 | v0.5 | core | office | — | — |
| `manifest.csv` | 資料包目錄 | v0.5 | core | office | 一個檔案或資料夾一列 | `path` |
| `content/agenda.csv` | 議程與講者名單 | v0.5 | core | office | 一個議程段落一列 | `segment_id` |
| `content/transcript.csv` | 逐字稿 | v1 | core | pipeline_reviewed | 一句話一列 | `sentence_id` |
| `content/slides_notes.csv` | 簡報頁標題與筆記 | v1 | core | office | 一個簡報頁一列 | `slide_id` |
| `content/slide_changes.csv` | 換頁時間 | v1 | core | pipeline | 一次換頁一列 | `change_seq` |
| `content/segment_function.csv` | 每段在做什麼 | v1 | core | pipeline_reviewed | 一個功能段落一列 | `block_id` |
| `content/taiwan_mentions.csv` | 講者提到台灣 | v1 | bonus | pipeline_reviewed | 一次提及一列 | `mention_id` |
| `content/tool_mentions.csv` | 講者提到的工具與公司 | v1 | bonus | pipeline | 一次提及一列 | `mention_id` |
| `notes/` | 現場筆記 | v1 | core | field_staff | 一場一份 | — |
| `reactions/sound_events.csv` | 掌聲、笑聲、全場安靜 | v1 | core | pipeline | 一個聲音事件一列 | `event_id` |
| `reactions/peaks.csv` | 反應高峰與高峰前三秒 | v1 | core | pipeline | 一個高峰一列 | `peak_id` |
| `reactions/phone_raise.csv` | 舉手機 | v1 | core | pipeline_reviewed | 一次舉手機事件一列 | `raise_id` |
| `reactions/hand_raise.csv` | 舉手 | v1 | core | pipeline_reviewed | 一次舉手事件一列 | `raise_id` |
| `reactions/stage_polls.csv` | 講者在台上做的現場調查 | v1 | core | pipeline_reviewed | 一次調查一列 | `poll_id` |
| `reactions/timeline_minute.csv` | 每分鐘總表 | v1 | core | pipeline | 一分鐘一列 | `minute_idx` |
| `presence/presence_minute.csv` | 在座、離席與站著聽 | v1.1 | core | pipeline | 一台鏡頭一區一分鐘一列 | `minute_idx+camera+zone` |
| `presence/fill_order.csv` | 各區坐滿順序 | v1.1 | reduced | pipeline | 一個區域群組一列 | `zone_group` |
| `presence/csi.csv` | Wifi 人流 | v1.1 | extension | pipeline | 一區一個時間窗一列 | `window_start_t_sec+zone` |
| `after_talk/crowd_after_talk.csv` | 講完被圍住 | v1.1 | core | manual_annotation | 一位講者一列 | `segment_id+speaker_id` |
| `questions/onsite_qa.csv` | 台上 Q&A | v1 | core | pipeline_reviewed | 一個問題一列 | `qa_id` |
| `questions/pre_event.csv` | 活動前收到的問題 | v1 | core | office | 一個問題一列 | `pre_q_id` |
| `questions/unasked.csv` | 想問但沒問到的問題 | v1.1 | core | field_staff | 一個問題一列 | `unasked_id` |
| `questions/remembered_moments.csv` | 你記得哪一刻 | v2 | core | office | 一則回覆一列 | `response_id` |
| `startups/topics.csv` | 創業題目分布 | v1.1 | core | office | 一個題目一列 | `topic_id` |
| `speakers/profiles.csv` | 講者公開資料 | v0.5 | core | office | 一位講者一列 | `speaker_id` |
| `speakers/news.csv` | 講者近期新聞 | v0.5 | core | office | 一則新聞一列 | `news_id` |
| `speakers/public_projects.md` | 講者公開專案 | v0.5 | core | office | — | — |
| `speakers/new_vs_old.csv` | 過去講法與這場對照 | v0.5 | bonus | office | 一個觀點一列 | `claim_id` |
| `social/speakers_yc_posts.csv` | 講者與 YC 的公開貼文 | v0.5 | core | office | 一則貼文一列 | `post_id` |
| `social/post_to_moment.csv` | 公開貼文對到現場時刻 | v2 | core | pipeline_reviewed | 一則對應一列 | `match_id` |
| `online/posts.csv` | 活動後公開貼文 | v2 | core | office | 一則貼文一列 | `post_id` |
| `online/search_lift.csv` | 提到後的搜尋量 | v2 | extension | office | 一個詞一列 | `mention_id` |
| `side_events/luma.csv` | 周邊活動報名人數 | v2 | bonus | office | 一個周邊活動一列 | `event_id` |
| `outside/entry_minute.csv` | 進場與出場人流 | v1.1 | bonus | pipeline | 一分鐘一列 | `minute_idx+camera` |
| `outside/passersby_10min.csv` | 看了看板卻沒進場 | v1.1 | bonus | pipeline_reviewed | 十分鐘一列 | `window_start_clock+camera` |
| `rankings/trivia.csv` | 冷知識排行榜 | v1.1 | bonus | office | 一則冷知識一列 | `trivia_id` |
| `scene/scene_description.md` | 場景描述 | v1 | core | field_staff | — | — |
| `derivatives/works.csv` | 二創回灌 | v2 | core | office | 一件作品一列 | `work_id` |
| `docs/field_reference.md` | 欄位說明 | v0.5 | core | pipeline | — | — |
| `docs/devices_and_positions.md` | 設備與機位 | v0.5 | core | office | — | — |
| `docs/limitations.md` | 量不到什麼 | v0.5 | core | office | — | — |
| `docs/venue_map.md` | 場地平面圖 | v0.5 | bonus | office | — | — |

## `manifest.csv`：資料包目錄

列出每個檔案是什麼、從哪來、怎麼產生、本版狀態。

版本：v0.5　優先序：core　誰填：office　一列代表：一個檔案或資料夾一列　主鍵：`path`

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `path` | string | 必填 |  |  | 資料包內的相對路徑，以 / 分隔；資料夾以 / 結尾 | `content/transcript.csv` |
| `title_zh` | string | 必填 |  |  | 檔案的中文名稱 | `逐字稿` |
| `description` | string | 必填 |  |  | 這個檔案在說什麼，一句話 | `逐句逐字稿` |
| `version_added` | enum | 必填 |  | `v0.5` / `v1` / `v1.1` / `v2` | 第一次出現在資料包的版本 | `v1` |
| `status` | enum | 必填 |  | `included` / `partial` / `pending` / `not_available` | 本版狀態：included 完整收錄；partial 部分收錄（缺漏寫在 docs/limitations.md）；pending 預計之後的版本加入；not_available 這次活動收不到 | `included` |
| `row_count` | integer | 可留空 | rows |  | CSV 的資料列數，不含標題列；非 CSV 留空 | `1834` |
| `source_devices` | id_list | 可留空 |  |  | 產生這個檔案的設備代號，以 ; 分隔，代號見 docs/devices_and_positions.md；線上來源填 online；表單填 form | `B;B2;A1` |
| `filled_by` | enum | 必填 |  | `pipeline` / `pipeline_reviewed` / `office` / `manual_annotation` / `field_staff` | 誰填：pipeline 流程自動；pipeline_reviewed 流程自動加人工確認或抽查；office 辦公室整理；manual_annotation 人工看畫面或聽音檔標記；field_staff 現場人員記錄 | `pipeline_reviewed` |
| `priority` | enum | 必填 |  | `core` / `bonus` / `reduced` / `extension` | 優先序：core 核心，一定要有；bonus 加分，做得到就放；reduced 降級，只做粗的版本；extension 延伸，測得出來才放 | `core` |
| `method` | string | 條件必填（條件寫在定義中） |  |  | 一句話說明怎麼產生：工具或模型名稱加人工步驟；status 不是 pending 時必填 | `Whisper large-v3 轉寫後多來源比對，不一致處人工聽音檔` |
| `updated_at` | datetime | 條件必填（條件寫在定義中） |  |  | 本檔最後一次更新的時間；status 不是 pending 時必填 | `2026-11-12T20:05:00+08:00` |
| `sha256` | string | 可留空 |  |  | 檔案內容的 SHA-256，小寫十六進位；資料夾留空 |  |
| `note` | string | 可留空 |  |  | 其他說明 |  |

## `content/agenda.csv`：議程與講者名單

活動段落、講者與實際起訖時間；v0.5 只有公開的講者名單與開門時間，v1 補上現場實際時間。

版本：v0.5　優先序：core　誰填：office　一列代表：一個議程段落一列　主鍵：`segment_id`　來源設備：online;B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `segment_id` | id | 必填 |  |  | 段落代號：S 加兩位數，依實際開始時間排序，從 S01 開始；v0.5 依公布順序暫編，v1 依實際順序重編並寫進 CHANGELOG | `S03` |
| `segment_type` | enum | 必填 |  | `opening` / `talk` / `fireside` / `panel` / `qa` / `break` / `closing` / `other` | 段落類型：演講後接著的問答不另立段落（問題記在 questions/onsite_qa.csv）；只有主辦方另外排的問答時段才標 qa | `talk` |
| `title` | string | 可留空 |  |  | 段落標題：主辦方公布或現場投影上的講題原文；沒有就留空 | `How to Build the Future` |
| `speaker_ids` | id_list | 可留空 |  |  | 本段台上的人，以 ; 分隔，對應 speakers/profiles.csv 的 speaker_id；主持人也列入；break 留空 | `garry-tan` |
| `scheduled_start_clock` | datetime | 可留空 |  |  | 主辦方事前公布的開始時間；未公布留空 | `2026-11-12T13:00:00+08:00` |
| `start_t_sec` | number | 條件必填（條件寫在定義中） | s |  | 實際開始：本段第一句話的 start_t_sec；break 為上一段的 end_t_sec；v0.5 尚無現場資料時留空 | `1520.4` |
| `end_t_sec` | number | 條件必填（條件寫在定義中） | s |  | 實際結束：本段最後一句話的 end_t_sec，不含下台與換場；break 為下一段的 start_t_sec；v0.5 留空 | `3310.8` |
| `start_clock` | datetime | 條件必填（條件寫在定義中） |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:20+08:00` |
| `end_clock` | datetime | 條件必填（條件寫在定義中） |  |  | end_t_sec 換算的台北時間 | `2026-11-12T12:55:10+08:00` |
| `source` | enum | 必填 |  | `published` / `observed` / `published_corrected` | published 只有事前公布的資訊；observed 由現場逐字稿與換頁推得；published_corrected 事前公布並依現場校正 | `published_corrected` |

## `content/transcript.csv`：逐字稿

每句話的講者、時間與定稿文字；含「不適合二創」標記。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一句話一列　主鍵：`sentence_id`　來源設備：B;B2;B3;A1

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `sentence_id` | id | 必填 |  |  | 句子代號：T 加五位數，依 start_t_sec 排序，從 T00001 開始 | `T00042` |
| `segment_id` | id | 必填 |  |  | 所屬段落，對應 content/agenda.csv；以句子的 start_t_sec 判定 | `S03` |
| `speaker_id` | string | 必填 |  | `speaker_id` / `host` / `audience` / `unknown` | 說話者：台上講者填 speaker_id；主持人未建檔填 host；台下的人一律填 audience，不記姓名；無法判斷填 unknown | `garry-tan` |
| `start_t_sec` | number | 必填 | s |  | 句子第一個字開始發音的時間 | `1532.18` |
| `end_t_sec` | number | 必填 | s |  | 句子最後一個字結束發音的時間 | `1536.90` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:32+08:00` |
| `text_raw` | string | 必填 |  |  | 轉寫原文：主要轉寫來源的模型輸出，未經人工修改；is_sensitive 為 true 時改為「[不公開]」 | `the best founders i know talk to users every week` |
| `text` | string | 必填 |  |  | 校對版：照原話，不改寫、不摘要；只修正錯字、人名與專有名詞，保留口語贅詞；is_sensitive 為 true 時改為「[不公開]」 | `The best founders I know talk to users every week.` |
| `lang` | enum | 必填 |  | `zh` / `en` / `mixed` | 句子語言：同一句中文與英文各至少一個實詞時填 mixed | `en` |
| `slide_id` | id | 可留空 |  |  | start_t_sec 當下投影幕上的簡報頁，對應 content/slides_notes.csv；沒有投影時留空 | `S03-P012` |
| `verification` | enum | 必填 |  | `agreed` / `resolved` / `single_source` / `unverified` | 定稿方式：agreed 三個以上來源文字一致；resolved 來源不一致、人工聽音檔後定稿；single_source 只有一個來源可用；unverified 尚未校對 | `agreed` |
| `source_count` | integer | 必填 |  |  | 這一句可用的轉寫來源數，來源見 manifest.csv 的 source_devices | `3` |
| `is_sensitive` | boolean | 必填 |  | `true` / `false` | 不適合二創：觀眾提到的個人狀況、未公開的公司內情、講者說不要外傳的內容；true 的句子不進 reactions/peaks.csv 的排名與二創範本 | `false` |
| `sensitive_reason` | enum | 條件必填（條件寫在定義中） |  | `personal` / `company_internal` / `off_record` / `other` | is_sensitive 為 true 時必填；false 時留空 |  |
| `asr_confidence` | number | 可留空 | 0–1 |  | 轉寫模型給的平均信心值；人工定稿後仍保留原值 | `0.91` |

## `content/slides_notes.csv`：簡報頁標題與筆記

每一頁簡報的標題與我們寫的筆記；不放簡報畫面與全文。

版本：v1　優先序：core　誰填：office　一列代表：一個簡報頁一列　主鍵：`slide_id`　來源設備：A;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `slide_id` | id | 必填 |  |  | 簡報頁代號：segment_id 加 -P 加三位數頁碼；拿不到頁碼時依首次出現順序編號 | `S03-P012` |
| `segment_id` | id | 必填 |  |  | 所屬段落，對應 content/agenda.csv | `S03` |
| `speaker_id` | string | 必填 |  |  | 這頁由誰講，同 content/transcript.csv | `garry-tan` |
| `page_no` | integer | 可留空 |  |  | 簡報檔上的頁碼；拿不到簡報檔時留空 | `12` |
| `page_title` | string | 可留空 |  |  | 投影上的標題原文；頁面沒有標題時留空 | `Talk to users` |
| `notes` | string | 可留空 |  |  | 我們寫的一到兩句筆記：這頁在講什麼；不複製頁面全文 | `用三個新創的例子說明每週訪談使用者的頻率` |
| `content_type` | enum | 必填 |  | `title` / `text` / `chart` / `table` / `image` / `video` / `demo` / `other` | 這頁主要的呈現方式；同時有多種時取面積最大者 | `chart` |
| `first_shown_t_sec` | number | 必填 | s |  | 第一次出現在投影幕上的時間 | `1610.0` |
| `total_dwell_sec` | number | 必填 | s |  | 這頁累計顯示秒數；同頁多次出現相加 | `95.5` |
| `show_count` | integer | 必填 |  |  | 這頁出現的次數 | `2` |

## `content/slide_changes.csv`：換頁時間

每一次換頁的時間與停留秒數；同一頁再次出現另起一列。

版本：v1　優先序：core　誰填：pipeline　一列代表：一次換頁一列　主鍵：`change_seq`　來源設備：A;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `change_seq` | integer | 必填 |  |  | 全場換頁序號：從 1 開始依 start_t_sec 遞增 | `57` |
| `from_slide_id` | id | 可留空 |  |  | 換頁前的簡報頁；段落第一頁留空 | `S03-P011` |
| `slide_id` | id | 必填 |  |  | 換到的簡報頁，對應 content/slides_notes.csv | `S03-P012` |
| `segment_id` | id | 必填 |  |  | 所屬段落，對應 content/agenda.csv | `S03` |
| `speaker_id` | string | 必填 |  |  | 換頁當下的講者 | `garry-tan` |
| `start_t_sec` | number | 必填 | s |  | 新頁第一次完整顯示的時間；動畫逐步出現的頁以第一個畫面為準，動畫中的變化不算換頁 | `1610.0` |
| `end_t_sec` | number | 必填 | s |  | 下一次換頁的 start_t_sec；段落最後一頁以段落的 end_t_sec 為準 | `1672.3` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:26:50+08:00` |
| `dwell_sec` | number | 必填 | s |  | end_t_sec 減 start_t_sec | `62.3` |
| `detect_method` | enum | 必填 |  | `manual` / `visual_diff` / `deck_match` | manual 人工標記；visual_diff 由投影畫面變化偵測；deck_match 與簡報檔逐頁比對 | `visual_diff` |
| `confidence` | number | 必填 | 0–1 |  | 偵測信心；manual 填 1 | `0.97` |
| `camera` | id | 必填 |  | `A` / `X5` | 拍到這次換頁的設備代號；X5 是備援 | `A` |

## `content/segment_function.csv`：每段在做什麼

把連續且同一類別的句子合併為功能段落，標出在給方法、講故事、回答問題等哪一類。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一個功能段落一列　主鍵：`block_id`　來源設備：B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `block_id` | id | 必填 |  |  | 功能段落代號：F 加四位數，依 start_t_sec 排序 | `F0031` |
| `segment_id` | id | 必填 |  |  | 所屬段落，對應 content/agenda.csv | `S03` |
| `speaker_id` | string | 必填 |  | `speaker_id` / `host` / `audience` / `unknown` | 這個功能段落的說話者；同 content/transcript.csv | `garry-tan` |
| `start_t_sec` | number | 必填 | s |  | 第一句的 start_t_sec | `1532.18` |
| `end_t_sec` | number | 必填 | s |  | 最後一句的 end_t_sec | `1601.40` |
| `sentence_ids` | id_list | 必填 |  |  | 包含的句子代號，以 ; 分隔，必須是同一段落內連續的句子 | `T00042;T00043;T00044` |
| `slide_ids` | id_list | 可留空 |  |  | 期間出現過的簡報頁，以 ; 分隔 | `S03-P011;S03-P012` |
| `function` | enum | 必填 |  | `method` / `concept` / `story` / `data` / `vision` / `audience_interaction` / `qa_answer` / `transition` | 定稿類別：有人工標時以 function_human 為準，否則用 function_ai。method 給方法（聽完可以照著做）；concept 講觀念（主張或框架、沒有步驟）；story 講故事（有時間、人物、發生的事）；data 給數字（數據、事實、市場現況）；vision 講願景（未來會怎樣）；audience_interaction 跟台下互動（請舉手、問台下、點名台灣）；qa_answer 回答提問；transition 開場與過場（自介、串場、感謝、公告） | `story` |
| `function_ai` | enum | 必填 |  | `method` / `concept` / `story` / `data` / `vision` / `audience_interaction` / `qa_answer` / `transition` | 模型標的類別；模型名稱寫在 manifest.csv 的 method | `story` |
| `function_human` | enum | 可留空 |  | `method` / `concept` / `story` / `data` / `vision` / `audience_interaction` / `qa_answer` / `transition` | 人工標的類別；沒有抽到人工標的段落留空 | `story` |
| `labels_agree` | boolean | 條件必填（條件寫在定義中） |  | `true` / `false` | function_ai 是否等於 function_human；function_human 為空時留空 | `true` |
| `char_count` | integer | 必填 | chars |  | 段落內所有句子 text 的字數：中文一字算 1，英文一個單字算 1，數字串算 1，不含標點與空白 | `186` |
| `char_share` | number | 必填 | 0–1 |  | char_count 除以同一 segment_id 所有功能段落 char_count 的總和 | `0.083` |
| `peak_count` | integer | 必填 |  |  | reactions/peaks.csv 中 peak_t_sec 落在本段起訖內的高峰數 | `1` |
| `phone_count_max` | integer | 可留空 | people |  | 本段期間 reactions/phone_raise.csv 事件 phone_count_peak 的最大值；沒有事件填 0；沒有影像時留空 | `18` |

## `content/taiwan_mentions.csv`：講者提到台灣

逐字稿中提到台灣的地名、食物、公司與創業環境。

版本：v1　優先序：bonus　誰填：pipeline_reviewed　一列代表：一次提及一列　主鍵：`mention_id`　來源設備：B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `mention_id` | id | 必填 |  |  | TW 加四位數，依 t_sec 排序 | `TW0003` |
| `sentence_id` | id | 必填 |  |  | 提到的句子，對應 content/transcript.csv | `T00208` |
| `segment_id` | id | 必填 |  |  | 所屬段落 | `S05` |
| `speaker_id` | string | 必填 |  |  | 說話者，同 content/transcript.csv | `garry-tan` |
| `sentence_text` | string | 必填 |  |  | 所在句子的 text，同 content/transcript.csv，方便不用另外查表 | `We love coming to Taipei because of TSMC.` |
| `t_sec` | number | 必填 | s |  | 所在句子的 start_t_sec | `4021.6` |
| `term` | string | 必填 |  |  | 逐字稿中的原詞 | `TSMC` |
| `normalized` | string | 必填 |  |  | 標準名稱：地名與機構用官方英文或中文全名，其他用最常見寫法 | `台灣積體電路製造` |
| `category` | enum | 必填 |  | `place` / `food` / `company` / `institution` / `culture` / `startup_ecosystem` / `other` | 提及的類別 | `company` |

## `content/tool_mentions.csv`：講者提到的工具與公司

逐字稿中提到的工具、公司、產品與開源專案。

版本：v1　優先序：bonus　誰填：pipeline　一列代表：一次提及一列　主鍵：`mention_id`　來源設備：B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `mention_id` | id | 必填 |  |  | TM 加四位數，依 t_sec 排序 | `TM0012` |
| `sentence_id` | id | 必填 |  |  | 提到的句子，對應 content/transcript.csv | `T00377` |
| `segment_id` | id | 必填 |  |  | 所屬段落 | `S06` |
| `speaker_id` | string | 必填 |  |  | 說話者，同 content/transcript.csv | `diana-hu` |
| `sentence_text` | string | 必填 |  |  | 所在句子的 text，同 content/transcript.csv，方便不用另外查表 | `Half the batch builds with Cursor now.` |
| `t_sec` | number | 必填 | s |  | 所在句子的 start_t_sec | `5133.0` |
| `term` | string | 必填 |  |  | 逐字稿中的原詞 | `cursor` |
| `normalized_name` | string | 必填 |  |  | 官方名稱 | `Cursor` |
| `entity_type` | enum | 必填 |  | `tool` / `company` / `product` / `open_source_project` / `other` | 提及對象的類型；公司與它的同名產品以講者語意判斷 | `tool` |
| `official_url` | url | 可留空 |  |  | 官方網站或 repo；查不到留空 | `https://cursor.com` |
| `is_yc_company` | boolean | 可留空 |  | `true` / `false` | 依 YC 官方公司目錄判定；查不到留空 | `false` |

## `reactions/sound_events.csv`：掌聲、笑聲、全場安靜

每一段掌聲、笑聲、台下討論聲或全場安靜的起訖時間與當下講到哪一句、哪一頁。

版本：v1　優先序：core　誰填：pipeline　一列代表：一個聲音事件一列　主鍵：`event_id`　來源設備：B;C;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | id | 必填 |  |  | SE 加五位數，依 start_t_sec 排序 | `SE00118` |
| `event` | enum | 必填 |  | `applause` / `laughter` / `silence` / `chatter` | applause 掌聲；laughter 笑聲；silence 全場安靜：段落進行中講台與台下都沒有語音、掌聲與笑聲，且音量低於 silence_level_db 連續 silence_min_sec 以上；chatter 台下討論聲：台下多人同時說話、不是講台的語音 | `laughter` |
| `mic` | id | 必填 |  | `B` / `C` / `A1` / `X5` | 判定這個事件的收音設備代號；同一事件多支收到時填訊號最強的一支 | `B` |
| `start_t_sec` | number | 必填 | s |  | 第一個分數超過 event_score_threshold 的分析窗起點 | `1544.0` |
| `end_t_sec` | number | 必填 | s |  | 最後一個超過門檻的分析窗終點；間隔小於 event_merge_gap_sec 的同類事件合併 | `1547.8` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:44+08:00` |
| `duration_sec` | number | 必填 | s |  | end_t_sec 減 start_t_sec；短於 event_min_sec 的事件不收錄 | `3.8` |
| `score_mean` | number | 必填 | 0–1 |  | 事件期間各分析窗該類別分數的平均 | `0.72` |
| `score_max` | number | 必填 | 0–1 |  | 事件期間各分析窗該類別分數的最大值 | `0.94` |
| `level_db_max` | number | 可留空 | dBFS |  | 事件期間的音量峰值，反映強度；收音設備增益不同，只能在同一支 mic 內比較 | `-12.5` |
| `is_polite` | boolean | 必填 |  | `true` / `false` | 禮貌性掌聲：event 為 applause 且 start_t_sec 落在任一段落開始或結束前後 polite_window_sec 秒內；laughter、silence 與 chatter 一律 false | `false` |
| `segment_id` | id | 必填 |  |  | start_t_sec 所屬的段落 | `S03` |
| `sentence_id` | id | 可留空 |  |  | start_t_sec 當下正在說或最近一句已說完的句子 | `T00043` |
| `slide_id` | id | 可留空 |  |  | start_t_sec 當下投影幕上的頁 | `S03-P011` |

## `reactions/peaks.csv`：反應高峰與高峰前三秒

照固定規則算出的反應高峰排名與高峰前三秒講的話；不替人挑重點。

版本：v1　優先序：core　誰填：pipeline　一列代表：一個高峰一列　主鍵：`peak_id`　來源設備：B;C;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `peak_id` | id | 必填 |  |  | PK 加三位數，依 start_t_sec 排序 | `PK021` |
| `rank` | integer | 必填 |  |  | 依 score 由高到低排名，1 最高；同分以 start_t_sec 早者在前 | `3` |
| `start_t_sec` | number | 必填 | s |  | 高峰窗起點：把非禮貌掌聲、笑聲事件與舉手機事件中，重疊或間隔小於 peak_merge_gap_sec 者合併成一窗 | `1544.0` |
| `end_t_sec` | number | 必填 | s |  | 高峰窗終點 | `1552.0` |
| `peak_t_sec` | number | 必填 | s |  | 窗內各訊號正規化後加總最大的一秒 | `1546.0` |
| `peak_clock` | datetime | 必填 |  |  | peak_t_sec 換算的台北時間 | `2026-11-12T12:25:46+08:00` |
| `segment_id` | id | 必填 |  |  | peak_t_sec 所屬的段落 | `S03` |
| `speaker_id` | string | 必填 |  |  | peak_t_sec 當下的說話者 | `garry-tan` |
| `slide_id` | id | 可留空 |  |  | peak_t_sec 當下投影幕上的頁 | `S03-P011` |
| `sentence_id` | id | 可留空 |  |  | peak_t_sec 當下正在說或最近一句已說完的句子 | `T00043` |
| `pre3s_sentence_ids` | id_list | 可留空 |  |  | 與 [start_t_sec−3; start_t_sec) 有重疊的句子代號，以 ; 分隔 | `T00042;T00043` |
| `pre3s_text` | string | 可留空 |  |  | 上述句子的 text 依序以空格接起來 | `The best founders I know talk to users every week.` |
| `pre3s_action` | string | 可留空 |  |  | 高峰前三秒講者做了什麼動作（換頁、停頓、手勢、走位、請台下回應），由設備 A 的影片或現場筆記人工記下；看不到留空 | `換到下一頁並停頓兩秒` |
| `signals` | id_list | 必填 |  | `applause` / `laughter` / `phone` | 窗內出現的訊號，以 ; 分隔 | `laughter;phone` |
| `applause_sec` | number | 必填 | s |  | 窗內非禮貌掌聲的秒數 | `0` |
| `laughter_sec` | number | 必填 | s |  | 窗內笑聲的秒數 | `3.8` |
| `phone_count_max` | integer | 可留空 | people |  | 窗內 reactions/phone_raise.csv 事件 phone_count_peak 的最大值；沒有舉手機事件填 0；沒有影像時留空 | `18` |
| `score` | number | 必填 |  |  | w_applause×applause_sec + w_laughter×laughter_sec + w_phone×phone_count_max；權重見 schema/parameters.csv；窗內任一句 is_sensitive 為 true 的高峰不收錄 | `12.2` |

## `reactions/phone_raise.csv`：舉手機

同時舉手機（拍照、錄影）的人數達到門檻的時段，以及最多幾人、占可見人數多少。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一次舉手機事件一列　主鍵：`raise_id`　來源設備：X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `raise_id` | id | 必填 |  |  | PH 加五位數，依 start_t_sec 排序 | `PH00012` |
| `start_t_sec` | number | 必填 | s |  | 事件起點：同一秒舉手機的人數第一次達到 raise_event_min_people 的秒。舉手機：畫面中偵測到手機、手機高於持有者的肩膀、且持續 phone_up_min_sec 秒以上；拍照、錄影與舉起手機看都算 | `1544` |
| `end_t_sec` | number | 必填 | s |  | 事件終點：舉手機人數回到 raise_event_min_people 以下的秒；間隔小於 raise_merge_gap_sec 的事件合併，短於 raise_event_min_sec 的不收錄 | `1551` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:44+08:00` |
| `duration_sec` | number | 必填 | s |  | end_t_sec 減 start_t_sec | `7` |
| `peak_t_sec` | number | 必填 | s |  | 事件內同一秒舉手機人數最多的秒；同數取最早 | `1546` |
| `segment_id` | id | 必填 |  |  | peak_t_sec 所屬的段落 | `S03` |
| `slide_id` | id | 可留空 |  |  | peak_t_sec 當下投影幕上的頁 | `S03-P011` |
| `sentence_id` | id | 可留空 |  |  | peak_t_sec 當下正在說或最近一句已說完的句子 | `T00043` |
| `phone_count_peak` | integer | 必填 | people |  | 估計人數：peak_t_sec 那一秒舉手機的人數；被擋住的人數不到，是下限 | `18` |
| `visible_count` | integer | 必填 | people |  | peak_t_sec 那一秒 coverage_zones 內偵測到的人數 | `212` |
| `phone_share_peak` | number | 必填 | 0–1 |  | 占可見人數比例：phone_count_peak 除以 visible_count | `0.085` |
| `camera` | id | 必填 |  | `X5` | 偵測用的設備代號 | `X5` |
| `coverage_zones` | id_list | 必填 |  |  | peak_t_sec 當下畫面可用、有算進來的座位區代號，以 ; 分隔；代號見 docs/venue_map.md | `Z1;Z2;Z3` |

## `reactions/hand_raise.csv`：舉手

同時舉手的人數達到門檻的時段，以及最多幾人、占可見人數多少；舉著手機的不算。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一次舉手事件一列　主鍵：`raise_id`　來源設備：X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `raise_id` | id | 必填 |  |  | HR 加五位數，依 start_t_sec 排序 | `HR00004` |
| `start_t_sec` | number | 必填 | s |  | 事件起點：同一秒舉手的人數第一次達到 raise_event_min_people 的秒。舉手：手腕高於頭頂、持續 hand_raise_min_sec 秒以上；手上拿著手機的算舉手機，不算舉手 | `1544` |
| `end_t_sec` | number | 必填 | s |  | 事件終點：舉手人數回到 raise_event_min_people 以下的秒；間隔小於 raise_merge_gap_sec 的事件合併，短於 raise_event_min_sec 的不收錄 | `1551` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:44+08:00` |
| `duration_sec` | number | 必填 | s |  | end_t_sec 減 start_t_sec | `7` |
| `peak_t_sec` | number | 必填 | s |  | 事件內同一秒舉手人數最多的秒；同數取最早 | `1546` |
| `segment_id` | id | 必填 |  |  | peak_t_sec 所屬的段落 | `S03` |
| `slide_id` | id | 可留空 |  |  | peak_t_sec 當下投影幕上的頁 | `S03-P011` |
| `sentence_id` | id | 可留空 |  |  | peak_t_sec 當下正在說或最近一句已說完的句子 | `T00043` |
| `hand_count_peak` | integer | 必填 | people |  | 估計人數：peak_t_sec 那一秒舉手的人數；被擋住的人數不到，是下限 | `64` |
| `visible_count` | integer | 必填 | people |  | peak_t_sec 那一秒 coverage_zones 內偵測到的人數 | `205` |
| `hand_share_peak` | number | 必填 | 0–1 |  | 占可見人數比例：hand_count_peak 除以 visible_count | `0.312` |
| `camera` | id | 必填 |  | `X5` | 偵測用的設備代號 | `X5` |
| `coverage_zones` | id_list | 必填 |  |  | peak_t_sec 當下畫面可用、有算進來的座位區代號，以 ; 分隔；代號見 docs/venue_map.md | `Z1;Z2;Z3` |

## `reactions/stage_polls.csv`：講者在台上做的現場調查

講者請台下舉手或回應的時刻，以及當下舉手的人數。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一次調查一列　主鍵：`poll_id`　來源設備：B;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `poll_id` | id | 必填 |  |  | PL 加三位數，依 t_sec 排序 | `PL004` |
| `segment_id` | id | 必填 |  |  | 所屬段落 | `S03` |
| `speaker_id` | string | 必填 |  |  | 提問的講者 | `garry-tan` |
| `sentence_id` | id | 必填 |  |  | 講者提出調查的那一句，對應 content/transcript.csv | `T00120` |
| `question_text` | string | 必填 |  |  | 該句的 text 原文 | `How many of you have already quit your job?` |
| `t_sec` | number | 必填 | s |  | 該句的 end_t_sec，回應窗由此開始 | `2210.5` |
| `clock` | datetime | 必填 |  |  | t_sec 換算的台北時間 | `2026-11-12T12:36:50+08:00` |
| `response_type` | enum | 必填 |  | `raise_hand` / `applause` / `shout` / `other` | 講者要求的回應方式 | `raise_hand` |
| `window_sec` | number | 必填 | s |  | 計算回應的時間窗長度，等於 stage_poll_window_sec | `8` |
| `hand_count_peak` | integer | 條件必填（條件寫在定義中） | people |  | 回應窗內同一秒舉手人數的最大值（舉手定義同 reactions/hand_raise.csv）；response_type 不是 raise_hand 時留空 | `64` |
| `visible_count` | integer | 條件必填（條件寫在定義中） | people |  | hand_count_peak 那一秒 coverage_zones 內偵測到的人數 | `205` |
| `hand_share_peak` | number | 條件必填（條件寫在定義中） | 0–1 |  | hand_count_peak 除以 visible_count；只代表看得到的座位區 | `0.312` |
| `camera` | id | 必填 |  | `X5` | 偵測用的設備代號 | `X5` |
| `coverage_zones` | id_list | 必填 |  |  | 畫面可用、有算進來的座位區代號，以 ; 分隔 | `Z1;Z2;Z3` |
| `note` | string | 可留空 |  |  | 其他說明 |  |

## `reactions/timeline_minute.csv`：每分鐘總表

每分鐘彙整講者、簡報、聲音、舉手機與在座人數，給 AI 一次讀完。

版本：v1　優先序：core　誰填：pipeline　一列代表：一分鐘一列　主鍵：`minute_idx`　來源設備：B;C;A;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `minute_idx` | integer | 必填 |  |  | 從 T0 起第幾分鐘，T0 以前為負數 | `25` |
| `start_t_sec` | number | 必填 | s |  | 這一分鐘的起點，等於 minute_idx×60 | `1500` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:00+08:00` |
| `segment_id` | id | 可留空 |  |  | 這一分鐘內佔最多秒數的段落；不在任何段落時留空 | `S03` |
| `speaker_id` | string | 可留空 |  |  | 這一分鐘內說最多秒數的說話者 | `garry-tan` |
| `slide_ids` | id_list | 可留空 |  |  | 這一分鐘內出現過的簡報頁，以 ; 分隔，依出現順序 | `S03-P011;S03-P012` |
| `page_title` | string | 可留空 |  |  | 這一分鐘內顯示最久那一頁的 page_title | `Talk to users` |
| `transcript_text` | string | 可留空 |  |  | start_t_sec 落在這一分鐘的句子 text 依序以空格接起來；is_sensitive 的句子以「[不公開]」代替；這一分鐘沒有句子時留空 | `The best founders I know talk to users every week. ...` |
| `sentence_count` | integer | 必填 |  |  | start_t_sec 落在這一分鐘的句子數 | `14` |
| `char_count` | integer | 必填 | chars |  | 上述句子的字數總和，計法同 content/segment_function.csv | `212` |
| `applause_sec` | number | 必填 | s |  | 與這一分鐘重疊的非禮貌掌聲秒數 | `0` |
| `polite_applause_sec` | number | 必填 | s |  | 與這一分鐘重疊的禮貌掌聲秒數 | `0` |
| `laughter_sec` | number | 必填 | s |  | 與這一分鐘重疊的笑聲秒數 | `3.8` |
| `silence_sec` | number | 必填 | s |  | 與這一分鐘重疊的全場安靜秒數 | `0` |
| `phone_count_max` | integer | 可留空 | people |  | 與這一分鐘重疊的 reactions/phone_raise.csv 事件 phone_count_peak 最大值；沒有事件填 0；沒有影像時留空 | `18` |
| `hand_count_max` | integer | 可留空 | people |  | 與這一分鐘重疊的 reactions/hand_raise.csv 事件 hand_count_peak 最大值；沒有事件填 0；沒有影像時留空 | `0` |
| `visible_count` | integer | 可留空 | people |  | 可見人數：presence/presence_minute.csv 這一分鐘各區 visible_count 加總 | `212` |
| `standing_count` | integer | 可留空 | people |  | 站立人數：presence/presence_minute.csv 這一分鐘各區 standing_count 加總 | `4` |
| `left_count` | integer | 可留空 | people |  | 離席：presence/presence_minute.csv 這一分鐘各區 left_count 加總 | `3` |
| `returned_count` | integer | 可留空 | people |  | 回座：presence/presence_minute.csv 這一分鐘各區 returned_count 加總 | `1` |
| `peak_ids` | id_list | 可留空 |  |  | peak_t_sec 落在這一分鐘的高峰，以 ; 分隔 | `PK021` |

## `presence/presence_minute.csv`：在座、離席與站著聽

每區每分鐘的可見人數、坐著與站著的人數、離席與回座。

版本：v1.1　優先序：core　誰填：pipeline　一列代表：一台鏡頭一區一分鐘一列　主鍵：`minute_idx+camera+zone`　來源設備：X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `minute_idx` | integer | 必填 |  |  | 從 T0 起第幾分鐘，T0 以前為負數 | `25` |
| `start_t_sec` | number | 必填 | s |  | 這一分鐘的起點 | `1500` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:25:00+08:00` |
| `camera` | id | 必填 |  | `X5` | 拍攝座位區的設備代號 | `X5` |
| `zone` | id | 必填 |  |  | 座位區代號，範圍畫在 docs/venue_map.md | `Z2` |
| `visible_count` | integer | 條件必填（條件寫在定義中） | people |  | 可見人數：這一分鐘每秒在這一區偵測到的人數，取 valid 秒數的中位數；valid_sec 為 0 時留空 | `71` |
| `seated_count` | integer | 條件必填（條件寫在定義中） | people |  | 坐著的人數：visible_count 中判定為坐姿的人數，取中位數 | `68` |
| `standing_count` | integer | 條件必填（條件寫在定義中） | people |  | 站立人數：在這一區站著、且同一位置持續站立 stand_min_sec 秒以上的人數，取中位數；走動中的人不算 | `3` |
| `left_count` | integer | 條件必填（條件寫在定義中） | people |  | 離席：這一分鐘內從這一區座位起身、走出這一區的人數 | `2` |
| `returned_count` | integer | 條件必填（條件寫在定義中） | people |  | 回座：這一分鐘內從區外走進這一區並坐下的人數 | `1` |
| `valid_sec` | integer | 必填 | s |  | 這一分鐘內這一區畫面可用的秒數（0–60）；被遮住、鏡頭移動或過暗的秒不算 | `60` |

## `presence/fill_order.csv`：各區坐滿順序

前、中、後三區分別在什麼時候坐到五成與八成。

版本：v1.1　優先序：reduced　誰填：pipeline　一列代表：一個區域群組一列　主鍵：`zone_group`　來源設備：X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `zone_group` | enum | 必填 |  | `front` / `middle` / `back` | 座位區群組；各 zone 屬於哪一群寫在 docs/venue_map.md | `front` |
| `camera` | id | 必填 |  | `X5` | 計算用的設備代號 | `X5` |
| `max_seated_count` | integer | 必填 | people |  | 這一群各區 seated_count 加總後（分鐘值）的全場最大值 | `96` |
| `fill_50_t_sec` | number | 可留空 | s |  | 這一群 seated_count 加總第一次達到 max_seated_count 50% 的分鐘起點；入場前畫面拍不到時留空 | `-1200` |
| `fill_80_t_sec` | number | 可留空 | s |  | 這一群 seated_count 加總第一次達到 max_seated_count 80% 的分鐘起點 | `-600` |
| `fill_50_clock` | datetime | 可留空 |  |  | fill_50_t_sec 換算的台北時間 | `2026-11-12T11:40:00+08:00` |
| `fill_80_clock` | datetime | 可留空 |  |  | fill_80_t_sec 換算的台北時間 | `2026-11-12T11:50:00+08:00` |
| `fill_rank` | integer | 必填 |  | `1` / `2` / `3` | 依 fill_80_t_sec 先後排名；未達八成的排在最後 | `1` |

## `presence/csi.csv`：Wifi 人流

由 Wifi 接收器的 CSI 推估各區的移動強度、相對密度與主要移動方向；不代表人數。

版本：v1.1　優先序：extension　誰填：pipeline　一列代表：一區一個時間窗一列　主鍵：`window_start_t_sec+zone`　來源設備：W

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `window_start_t_sec` | number | 必填 | s |  | 時間窗起點；窗長為 csi_window_sec | `1500` |
| `start_clock` | datetime | 必填 |  |  | window_start_t_sec 換算的台北時間 | `2026-11-12T12:25:00+08:00` |
| `window_sec` | number | 必填 | s |  | 時間窗長度，等於 csi_window_sec | `10` |
| `zone` | id | 必填 |  |  | 區域代號，同 docs/venue_map.md | `Z3` |
| `device` | id | 必填 |  | `W` | Wifi 接收器設備代號 | `W` |
| `motion_level` | number | 必填 | 0–1 |  | 該區移動強度：CSI 變化量依全場最大值正規化，0 為靜止、1 為全場最強 | `0.42` |
| `density_level` | enum | 可留空 |  | `low` / `mid` / `high` | 該區和其他區相比的相對密度，依 csi_density_cutoffs 分級；不代表人數；做不到時留空 | `mid` |
| `direction` | enum | 可留空 |  | `toward_stage` / `toward_exit` / `lateral` / `none` | 該區主要移動方向：toward_stage 往舞台；toward_exit 往出口；lateral 橫向；none 沒有明顯方向；做不到時留空 | `toward_exit` |
| `valid` | boolean | 必填 |  | `true` / `false` | 這個時間窗的訊號是否可用；false 時 motion_level 仍照算但不建議引用 | `true` |

## `after_talk/crowd_after_talk.csv`：講完被圍住

講者下台後被圍住多久、最多幾人、說到話與等了又走的人數；人工計數。

版本：v1.1　優先序：core　誰填：manual_annotation　一列代表：一位講者一列　主鍵：`segment_id+speaker_id`　來源設備：E

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `segment_id` | id | 必填 |  |  | 講者所在的段落 | `S03` |
| `speaker_id` | string | 必填 |  |  | 被圍住的講者 | `garry-tan` |
| `stage_exit_t_sec` | number | 必填 | s |  | 講者離開講台的時間 | `3330.0` |
| `start_t_sec` | number | 必填 | s |  | 圍住開始：講者下台後，圈內人數第一次達到 crowd_min_people 的時間 | `3342.0` |
| `end_t_sec` | number | 必填 | s |  | 講者離開該區，或圈內人數少於 crowd_min_people 持續 30 秒的時間 | `4110.0` |
| `start_clock` | datetime | 必填 |  |  | start_t_sec 換算的台北時間 | `2026-11-12T12:55:30+08:00` |
| `duration_sec` | number | 必填 | s |  | end_t_sec 減 start_t_sec | `780` |
| `peak_crowd` | integer | 必填 | people |  | 期間同一時刻在講者 crowd_radius_m 公尺內、面向講者的最多人數 | `23` |
| `talked_count` | integer | 必填 | people |  | 和講者有一來一往對話的不同人數 | `6` |
| `left_without_talking` | integer | 必填 | people |  | 在圈內停留 30 秒以上、沒有和講者對話就離開的人數 | `9` |
| `mean_talk_sec` | number | 條件必填（條件寫在定義中） | s |  | 每位對話者從開口到結束的平均秒數；talked_count 為 0 時留空 | `64` |
| `median_talk_sec` | number | 條件必填（條件寫在定義中） | s |  | 同上的中位數 | `48` |
| `coverage` | enum | 必填 |  | `full` / `partial` | full 從講者下台拍到 end_t_sec；partial 中途沒拍到，數字只算有拍到的部分 | `full` |
| `annotator_count` | integer | 必填 | people |  | 獨立計數的人數；兩人以上時填平均並在 note 寫差距 | `2` |
| `note` | string | 可留空 |  |  | 其他說明 |  |

## `questions/onsite_qa.csv`：台上 Q&A

現場台上被問到的問題與回答的起訖時間。

版本：v1　優先序：core　誰填：pipeline_reviewed　一列代表：一個問題一列　主鍵：`qa_id`　來源設備：B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `qa_id` | id | 必填 |  |  | QA 加三位數，依 question_start_t_sec 排序 | `QA007` |
| `segment_id` | id | 必填 |  |  | 所屬段落 | `S03` |
| `answerer_speaker_id` | string | 必填 |  |  | 回答的講者 | `garry-tan` |
| `asker_type` | enum | 必填 |  | `audience` / `host` / `online_submitted` | 提問者類型：台下觀眾、主持人代問、線上或事先送來的問題 | `audience` |
| `question_start_t_sec` | number | 必填 | s |  | 提問第一句的 start_t_sec | `3120.4` |
| `answer_start_t_sec` | number | 必填 | s |  | 回答第一句的 start_t_sec | `3141.0` |
| `answer_end_t_sec` | number | 必填 | s |  | 回答最後一句的 end_t_sec | `3230.2` |
| `question_sentence_ids` | id_list | 必填 |  |  | 提問的句子代號，以 ; 分隔 | `T00610;T00611` |
| `answer_sentence_ids` | id_list | 必填 |  |  | 回答的句子代號，以 ; 分隔 | `T00612;T00613;T00614` |
| `question_text` | string | 必填 |  |  | 把提問改寫成一句問題，移除提問者的姓名、公司與其他身分線索 | `在台灣做硬體新創，要怎麼找第一個海外客戶？` |
| `category` | enum | 必填 |  | `fundraising` / `product` / `team` / `market` / `yc_application` / `ai` / `hardware` / `career` / `taiwan` / `personal_advice` / `other` | 問題主題 | `hardware` |
| `is_sensitive` | boolean | 必填 |  | `true` / `false` | 問題或回答任一句 is_sensitive 為 true 時為 true；true 時 question_text 改為「[不公開]」 | `false` |

## `questions/pre_event.csv`：活動前收到的問題

活動前從報名表收到的問題，以及當天有沒有被回答。

版本：v1　優先序：core　誰填：office　一列代表：一個問題一列　主鍵：`pre_q_id`　來源設備：form

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `pre_q_id` | id | 必填 |  |  | PQ 加四位數，依收到時間排序 | `PQ0015` |
| `target` | string | 必填 |  | `speaker_id` / `organizer` / `any` | 想問的對象：講者填 speaker_id；問主辦方填 organizer；不限對象填 any | `garry-tan` |
| `question_text` | string | 條件必填（條件寫在定義中） |  |  | 把問題改寫成一句，移除提問者的姓名、公司與其他身分線索；consent_public 為 false 時留空，只保留對象與類別供統計 | `YC 怎麼看台灣團隊的申請？` |
| `category` | enum | 必填 |  | `fundraising` / `product` / `team` / `market` / `yc_application` / `ai` / `hardware` / `career` / `taiwan` / `personal_advice` / `other` | 問題主題 | `yc_application` |
| `source` | enum | 必填 |  | `coffee_morning_form` / `luma_form` / `hf_access_form` / `qr_card` | 收到的管道 | `coffee_morning_form` |
| `consent_public` | boolean | 必填 |  | `true` / `false` | 提問者是否勾選同意問題內容公開 | `true` |
| `submitted_date` | date | 必填 |  |  | 收到的日期，只到日 | `2026-11-08` |
| `answered_status` | enum | 必填 |  | `answered` / `partially_answered` / `not_answered` / `not_checked` | 當天是否被回答：answered 台上有句子直接回應問題核心；partially_answered 只回應一部分；not_answered 逐字稿全部比對後沒有；not_checked 尚未比對 | `not_checked` |
| `matched_qa_id` | id | 可留空 |  |  | 被回答時對應的 questions/onsite_qa.csv 的 qa_id；不是在 Q&A 回答時留空 |  |
| `matched_sentence_ids` | id_list | 可留空 |  |  | 回應這個問題的句子代號，以 ; 分隔 |  |

## `questions/unasked.csv`：想問但沒問到的問題

報名表、QR 與採訪收到、但沒有在台上問出口的問題。

版本：v1.1　優先序：core　誰填：field_staff　一列代表：一個問題一列　主鍵：`unasked_id`　來源設備：form;E

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `unasked_id` | id | 必填 |  |  | UQ 加四位數 | `UQ0032` |
| `target` | string | 必填 |  | `speaker_id` / `organizer` / `any` | 想問的對象，同 questions/pre_event.csv | `diana-hu` |
| `question_text` | string | 條件必填（條件寫在定義中） |  |  | 把問題改寫成一句，移除提問者的姓名、公司與其他身分線索；consent_public 為 false 時留空，只保留對象與類別供統計 | `怎麼判斷一個 AI 產品是功能還是公司？` |
| `category` | enum | 必填 |  | `fundraising` / `product` / `team` / `market` / `yc_application` / `ai` / `hardware` / `career` / `taiwan` / `personal_advice` / `other` | 問題主題 | `ai` |
| `source` | enum | 必填 |  | `coffee_morning_form` / `qr_card` / `interview` / `hf_access_form` | 收到的管道 | `qr_card` |
| `consent_public` | boolean | 必填 |  | `true` / `false` | 提問者是否勾選同意問題內容公開 | `true` |
| `collected_phase` | enum | 必填 |  | `before` / `during` / `after` | 在活動前、活動中或活動後收到 | `during` |
| `collected_date` | date | 必填 |  |  | 收到的日期，只到日 | `2026-11-12` |
| `answered_status` | enum | 必填 |  | `answered` / `partially_answered` / `not_answered` / `not_checked` | 是否其實在台上被回答了，定義同 questions/pre_event.csv | `not_answered` |
| `matched_sentence_ids` | id_list | 可留空 |  |  | 回應這個問題的句子代號，以 ; 分隔 |  |

## `questions/remembered_moments.csv`：你記得哪一刻

活動後一週問參加者記得哪一刻，對回現場高峰與句子。

版本：v2　優先序：core　誰填：office　一列代表：一則回覆一列　主鍵：`response_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `response_id` | id | 必填 |  |  | RM 加四位數 | `RM0009` |
| `moment_text` | string | 必填 |  |  | 把回覆改寫成一句，移除回覆者的身分線索 | `Garry 問誰已經離職創業，全場一半的人舉手` |
| `matched_peak_id` | id | 可留空 |  |  | 對到的 reactions/peaks.csv 高峰；對不到留空 | `PK021` |
| `matched_sentence_ids` | id_list | 可留空 |  |  | 對到的句子代號，以 ; 分隔 | `T00120` |
| `matched_segment_id` | id | 可留空 |  |  | 對到的段落 | `S03` |
| `match_method` | enum | 條件必填（條件寫在定義中） |  | `manual` / `ai_assisted` | 有對到時必填：人工或 AI 輔助加人工確認 | `manual` |
| `match_confidence` | enum | 條件必填（條件寫在定義中） |  | `high` / `medium` / `low` | 有對到時必填：high 回覆引用的話或細節與逐字稿相符；medium 主題相符；low 只有大概時段相符 | `high` |
| `response_date` | date | 必填 |  |  | 收到回覆的日期 | `2026-11-19` |

## `startups/topics.csv`：創業題目分布

報名表收到的創業題目與階段；去識別後才收錄。

版本：v1.1　優先序：core　誰填：office　一列代表：一個題目一列　主鍵：`topic_id`　來源設備：form

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `topic_id` | id | 必填 |  |  | ST 加四位數 | `ST0044` |
| `category` | enum | 必填 |  | `ai_infra` / `ai_application` / `devtools` / `b2b_saas` / `fintech` / `health` / `climate` / `consumer` / `education` / `hardware` / `robotics` / `other` | 題目類別 | `hardware` |
| `stage` | enum | 必填 |  | `idea` / `prototype` / `paying_customers` / `funded` / `other` | 目前階段：還在想、做出原型、有付費客戶、已募資 | `prototype` |
| `one_liner` | string | 條件必填（條件寫在定義中） |  |  | 改寫成一句的題目描述，不含公司名、產品名與人名；consent_public 為 true 時必填，false 時留空 | `用感測器幫小型工廠預測設備故障` |
| `is_hardware` | boolean | 必填 |  | `true` / `false` | 產品是否包含自行設計或製造的硬體 | `true` |
| `source` | enum | 必填 |  | `coffee_morning_form` / `hf_access_form` / `interview` | 收到的管道 | `coffee_morning_form` |
| `consent_public` | boolean | 必填 |  | `true` / `false` | 報名者是否勾選同意題目描述公開 | `true` |
| `collected_date` | date | 必填 |  |  | 收到的日期 | `2026-11-07` |

## `speakers/profiles.csv`：講者公開資料

學經歷、現職、YC 關係與跟台灣的連結；只用本人或其公司公開的來源。

版本：v0.5　優先序：core　誰填：office　一列代表：一位講者一列　主鍵：`speaker_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `speaker_id` | id | 必填 |  |  | 講者代號：英文名與姓的小寫，以 - 連接 | `garry-tan` |
| `display_name` | string | 必填 |  |  | 講者公開使用的姓名 | `Garry Tan` |
| `role_title` | string | 必填 |  |  | 現職職稱，照本人公開寫法 | `President & CEO` |
| `organization` | string | 必填 |  |  | 現職單位 | `Y Combinator` |
| `yc_relation` | enum | 必填 |  | `partner` / `staff` / `alumni_founder` / `guest` / `other` | 與 YC 的關係：partner 現任合夥人；staff 其他 YC 員工；alumni_founder YC 校友創辦人；guest 外部講者 | `partner` |
| `yc_batch` | string | 可留空 |  |  | YC 梯次，例如 W12；不是校友留空 |  |
| `notable_investments` | string | 可留空 |  |  | 投資或輔導過的公司，以 ; 分隔；只列本人或 YC 公開的資料；沒有留空 | `Coinbase;Instacart` |
| `bio_summary` | string | 必填 |  |  | 我們寫的兩句以內簡介，只根據 source_urls 的內容 | `【範例】YC 總裁暨執行長，曾共同創辦 Posterous` |
| `taiwan_connection` | string | 可留空 |  |  | 我們寫的一句：和台灣的公開連結；沒有就留空 |  |
| `source_urls` | url_list | 必填 |  |  | 資料來源網址，以 ; 分隔；只用本人、本人公司或 YC 官網 | `https://www.ycombinator.com/people/garry-tan` |
| `source_types` | id_list | 必填 |  | `self` / `company` / `yc` | 與 source_urls 一一對應的來源類型，以 ; 分隔 | `yc` |
| `retrieved_date` | date | 必填 |  |  | 查詢日期 | `2026-11-06` |

## `speakers/news.csv`：講者近期新聞

活動前一兩天的講者相關新聞；只放連結、發布者、日期與一句摘要。

版本：v0.5　優先序：core　誰填：office　一列代表：一則新聞一列　主鍵：`news_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `news_id` | id | 必填 |  |  | NW 加四位數，依 published_date 排序 | `NW0007` |
| `speaker_id` | id | 必填 |  |  | 相關講者 | `garry-tan` |
| `title` | string | 必填 |  |  | 原文標題 | `【範例】Example headline` |
| `publisher` | string | 必填 |  |  | 發布者名稱 | `【範例】Example News` |
| `publisher_type` | enum | 必填 |  | `self` / `company` / `third_party` | self 講者本人發布；company 講者的公司發布；third_party 第三方報導，只當參考 | `third_party` |
| `published_date` | date | 必填 |  |  | 發布日期 | `2026-11-03` |
| `url` | url | 必填 |  |  | 原文網址 | `https://example.com/news/123` |
| `summary_zh` | string | 必填 |  |  | 我們寫的一句摘要，不引用原文段落 | `【範例】講者宣布在台北舉辦 Startup School` |
| `retrieved_date` | date | 必填 |  |  | 查詢日期 | `2026-11-10` |

## `speakers/new_vs_old.csv`：過去講法與這場對照

講者過去公開講過的觀點，活動後對逐字稿標出這場重複、更新或新增。

版本：v0.5　優先序：bonus　誰填：office　一列代表：一個觀點一列　主鍵：`claim_id`　來源設備：online;B

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `claim_id` | id | 必填 |  |  | CL 加四位數 | `CL0012` |
| `speaker_id` | id | 必填 |  |  | 講者 | `garry-tan` |
| `claim_summary` | string | 必填 |  |  | 我們寫的一句：這個觀點是什麼 | `【範例】創辦人應該每週和使用者談話` |
| `past_source_url` | url | 條件必填（條件寫在定義中） |  |  | 過去講過時的出處；只用本人或其公司發布；this_talk_status 為 new_in_talk 時留空 |  |
| `past_source_type` | enum | 條件必填（條件寫在定義中） |  | `self` / `company` | 出處類型；同上條件 | `self` |
| `past_date` | date | 條件必填（條件寫在定義中） |  |  | 過去講的日期；同上條件 | `2025-04-12` |
| `this_talk_status` | enum | 必填 |  | `pending` / `repeated` / `updated` / `new_in_talk` / `contradicted` / `not_mentioned` | 這場的對照結果：pending 活動前尚未對照；repeated 重複講；updated 同一觀點有新內容；new_in_talk 過去沒講過；contradicted 與過去相反；not_mentioned 這場沒提 | `pending` |
| `new_in_talk_summary` | string | 條件必填（條件寫在定義中） |  |  | 我們寫的一句：這場比過去多講了什麼；this_talk_status 為 updated 或 new_in_talk 時必填 | `【範例】新增了在台灣找硬體共同創辦人的建議` |
| `matched_sentence_ids` | id_list | 可留空 |  |  | 這場對應的句子代號，以 ; 分隔 |  |
| `note` | string | 可留空 |  |  | 其他說明 |  |

## `social/speakers_yc_posts.csv`：講者與 YC 的公開貼文

講者與 YC 人員本人帳號在活動前後的公開貼文；只放連結、日期與一句摘要。

版本：v0.5　優先序：core　誰填：office　一列代表：一則貼文一列　主鍵：`post_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `post_id` | id | 必填 |  |  | YP 加五位數，依 posted_at 排序 | `YP00031` |
| `account_type` | enum | 必填 |  | `speaker` / `yc_staff` / `yc_official` | 發文帳號類型 | `speaker` |
| `speaker_id` | id | 條件必填（條件寫在定義中） |  |  | account_type 為 speaker 時必填 | `garry-tan` |
| `account_handle` | string | 必填 |  |  | 公開帳號名稱，不含 @ | `garrytan` |
| `platform` | enum | 必填 |  | `x` / `linkedin` / `facebook` / `instagram` / `threads` | 平台 | `x` |
| `url` | url | 必填 |  |  | 貼文網址 | `https://x.com/example/status/123` |
| `posted_at` | datetime | 必填 |  |  | 發文時間，換算為台北時間 | `2026-11-11T21:04:00+08:00` |
| `phase` | enum | 必填 |  | `before` / `during` / `after` | 相對活動開門與散場時間：開門前、開門到散場、散場後 | `before` |
| `summary_zh` | string | 必填 |  |  | 我們寫的一句摘要，不引用原文 | `【範例】預告明天在台北的演講` |
| `retrieved_at` | datetime | 必填 |  |  | 抓取時間 | `2026-11-12T08:00:00+08:00` |

## `social/post_to_moment.csv`：公開貼文對到現場時刻

用貼文的照片與引用句推回是現場哪一刻；屬於推論。

版本：v2　優先序：core　誰填：pipeline_reviewed　一列代表：一則對應一列　主鍵：`match_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `match_id` | id | 必填 |  |  | PM 加五位數 | `PM00008` |
| `post_ref` | id | 必填 |  |  | 對應 online/posts.csv 或 social/speakers_yc_posts.csv 的 post_id | `OP00102` |
| `evidence_type` | enum | 必填 |  | `quote` / `photo` / `quote_and_photo` | 推回現場時刻的依據：貼文引用的句子、照片內容，或兩者 | `quote_and_photo` |
| `matched_sentence_id` | id | 可留空 |  |  | 推得的句子 | `T00043` |
| `matched_slide_id` | id | 可留空 |  |  | 推得的簡報頁 | `S03-P011` |
| `matched_peak_id` | id | 可留空 |  |  | 推得的高峰 | `PK021` |
| `match_method` | enum | 必填 |  | `manual` / `ai_assisted` | 人工或 AI 輔助加人工確認 | `ai_assisted` |
| `match_confidence` | enum | 必填 |  | `high` / `medium` / `low` | high 引用句與逐字稿一致或照片中的簡報頁可辨識；medium 主題與時段相符；low 只能推到段落 | `high` |
| `note` | string | 可留空 |  |  | 推論理由；本表全部屬於推論 |  |

## `online/posts.csv`：活動後公開貼文

活動後的公開貼文與互動數；只放連結、日期與一句摘要。

版本：v2　優先序：core　誰填：office　一列代表：一則貼文一列　主鍵：`post_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `post_id` | id | 必填 |  |  | OP 加五位數，依 posted_at 排序 | `OP00102` |
| `platform` | enum | 必填 |  | `x` / `linkedin` / `facebook` / `instagram` / `threads` | 平台 | `threads` |
| `account_type` | enum | 必填 |  | `speaker` / `yc` / `attendee` / `media` / `company` / `other` | 發文帳號類型 | `attendee` |
| `account_handle` | string | 必填 |  |  | 公開帳號名稱，不含 @；私人帳號的貼文不收錄 | `example_handle` |
| `url` | url | 必填 |  |  | 貼文網址 | `https://www.threads.net/@example/post/123` |
| `posted_at` | datetime | 必填 |  |  | 發文時間，換算為台北時間 | `2026-11-12T19:22:00+08:00` |
| `hours_after_end` | number | 必填 | h |  | posted_at 距散場時間的小時數；散場前為負數 | `1.37` |
| `summary_zh` | string | 必填 |  |  | 我們寫的一句摘要，不引用原文 | `【範例】分享 Garry 講使用者訪談的那一頁` |
| `quoted_sentence_ids` | id_list | 可留空 |  |  | 貼文引用到的句子代號，以 ; 分隔 | `T00043` |
| `quoted_slide_ids` | id_list | 可留空 |  |  | 貼文引用或拍到的簡報頁，以 ; 分隔 | `S03-P011` |
| `likes` | integer | 可留空 |  |  | 抓取當下的按讚數 |  |
| `reposts` | integer | 可留空 |  |  | 抓取當下的轉發或分享數 |  |
| `comments` | integer | 可留空 |  |  | 抓取當下的留言數 |  |
| `retrieved_at` | datetime | 必填 |  |  | 抓取時間 | `2026-11-14T10:00:00+08:00` |

## `online/search_lift.csv`：提到後的搜尋量

講者提到工具或公司後，Google Trends 台灣搜尋量的變化。

版本：v2　優先序：extension　誰填：office　一列代表：一個詞一列　主鍵：`mention_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `mention_id` | id | 必填 |  |  | 第一次提到的 content/tool_mentions.csv mention_id | `TM0012` |
| `normalized_name` | string | 必填 |  |  | 查詢的詞，同 content/tool_mentions.csv | `Cursor` |
| `mention_t_sec` | number | 必填 | s |  | 第一次提到的時間，同該 mention 的 t_sec | `5133.0` |
| `geo` | string | 必填 |  |  | Google Trends 地區代碼 | `TW` |
| `granularity` | enum | 必填 |  | `hourly` / `daily` | Google Trends 資料粒度；比較前後一小時時必須是 hourly | `hourly` |
| `index_1h_before` | number | 必填 |  |  | 提到前一小時的 Google Trends 指數 | `8` |
| `index_1h_after` | number | 必填 |  |  | 提到後一小時的 Google Trends 指數 | `19` |
| `baseline_index` | number | 可留空 |  |  | 活動前 7 天同一時段的平均指數 | `12` |
| `window_peak_index` | number | 可留空 |  |  | 第一次提到後 48 小時內的最大指數 | `31` |
| `lift_ratio` | number | 條件必填（條件寫在定義中） |  |  | index_1h_after 除以 index_1h_before；index_1h_before 為 0 時留空 | `2.38` |
| `retrieved_at` | datetime | 必填 |  |  | 抓取時間 | `2026-11-15T10:00:00+08:00` |
| `source_url` | url | 必填 |  |  | Google Trends 查詢網址 | `https://trends.google.com/trends/explore?geo=TW&q=Cursor` |

## `side_events/luma.csv`：周邊活動報名人數

台北場周邊活動 Luma 公開頁上的人數；不收名單。

版本：v2　優先序：bonus　誰填：office　一列代表：一個周邊活動一列　主鍵：`event_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | id | 必填 |  |  | LE 加三位數 | `LE004` |
| `title` | string | 必填 |  |  | 活動名稱 | `【範例】YC Coffee Morning` |
| `host` | string | 必填 |  |  | 主辦單位 | `【範例】Sensible Intelligence Lab` |
| `start_clock` | datetime | 必填 |  |  | 開始時間 | `2026-11-12T09:00:00+08:00` |
| `end_clock` | datetime | 可留空 |  |  | 結束時間 | `2026-11-12T11:30:00+08:00` |
| `area` | string | 必填 |  |  | 行政區或地標 | `信義區` |
| `luma_url` | url | 必填 |  |  | Luma 公開頁網址 | `https://lu.ma/example` |
| `count_public` | integer | 必填 | people |  | 公開頁上顯示的人數 | `210` |
| `count_type` | enum | 必填 |  | `going` / `registered` / `approved` / `unknown` | 公開頁上這個數字的意思 | `going` |
| `is_ours` | boolean | 必填 |  | `true` / `false` | 是否為我們辦的活動 | `true` |
| `retrieved_at` | datetime | 必填 |  |  | 抓取時間 | `2026-11-12T23:00:00+08:00` |

## `outside/entry_minute.csv`：進場與出場人流

每分鐘走進與走出會場的人數。

版本：v1.1　優先序：bonus　誰填：pipeline　一列代表：一分鐘一列　主鍵：`minute_idx+camera`　來源設備：H;X5

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `minute_idx` | integer | 必填 |  |  | 從 T0 起第幾分鐘，T0 以前為負數 | `-30` |
| `start_clock` | datetime | 必填 |  |  | 這一分鐘的起點 | `2026-11-12T11:30:00+08:00` |
| `camera` | id | 必填 |  | `H` / `X5` | 計數用的設備代號 | `H` |
| `entering` | integer | 必填 | people |  | 這一分鐘越過門口線往內的人數 | `18` |
| `exiting` | integer | 必填 | people |  | 這一分鐘越過門口線往外的人數 | `0` |
| `method` | enum | 必填 |  | `manual_tally` / `auto_count` | 人工計數或自動計數 | `manual_tally` |
| `coverage` | enum | 必填 |  | `full` / `partial` | 這一分鐘是否全程有畫面 | `full` |

## `outside/passersby_10min.csv`：看了看板卻沒進場

場外看板前經過、停下、拍照的人數與同時段 QR 掃碼數。

版本：v1.1　優先序：bonus　誰填：pipeline_reviewed　一列代表：十分鐘一列　主鍵：`window_start_clock+camera`　來源設備：H;H2

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `window_start_clock` | datetime | 必填 |  |  | 十分鐘窗的起點 | `2026-11-12T13:10:00+08:00` |
| `window_end_clock` | datetime | 必填 |  |  | 十分鐘窗的終點 | `2026-11-12T13:20:00+08:00` |
| `camera` | id | 必填 |  | `H` / `H2` | 拍攝看板的設備代號 | `H` |
| `passersby` | integer | 必填 | people |  | 經過看板前方判定區的人數 | `140` |
| `stopped` | integer | 必填 | people |  | 在判定區停留 stop_min_sec 秒以上的人數 | `22` |
| `photographed` | integer | 必填 | people |  | 舉起手機對看板拍照的人數 | `7` |
| `qr_scans` | integer | 可留空 |  |  | 同一時段 QR 後台的掃碼數；沒有 QR 時留空 | `3` |
| `method` | enum | 必填 |  | `manual_tally` / `auto_count` | 人工計數或自動計數 | `manual_tally` |
| `includes_other_event` | boolean | 必填 |  | `true` / `false` | 同時段有其他展覽人流、無法區分時為 true | `true` |

## `rankings/trivia.csv`：冷知識排行榜

由其他表照公開規則算出的冷知識；不碰任何個人。

版本：v1.1　優先序：bonus　誰填：office　一列代表：一則冷知識一列　主鍵：`trivia_id`

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `trivia_id` | id | 必填 |  |  | TR 加三位數 | `TR003` |
| `title_zh` | string | 必填 |  |  | 好讀的冷知識標題 | `全場第一個大笑點出現在開場第 4 分鐘` |
| `value` | number | 必填 |  |  | 冷知識的數值 | `4` |
| `unit` | string | 必填 |  |  | 數值單位 | `分鐘` |
| `rule` | string | 必填 |  |  | 一句話寫出計算規則，引用欄位名稱 | `reactions/sound_events.csv 中第一個 laughter 事件的 start_t_sec 換算為分鐘` |
| `source_files` | id_list | 必填 |  |  | 用到的檔案路徑，以 ; 分隔 | `reactions/sound_events.csv` |
| `t_sec` | number | 可留空 | s |  | 有對應時刻時填 | `240` |
| `clock` | datetime | 可留空 |  |  | t_sec 換算的台北時間 | `2026-11-12T12:04:00+08:00` |

## `derivatives/works.csv`：二創回灌

二創者回報的作品；和現場紀錄分開。

版本：v2　優先序：core　誰填：office　一列代表：一件作品一列　主鍵：`work_id`　來源設備：online

| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |
| --- | --- | --- | --- | --- | --- | --- |
| `work_id` | id | 必填 |  |  | WK 加四位數，依 submitted_date 排序 | `WK0003` |
| `title` | string | 必填 |  |  | 作品名稱 | `【範例】Startup School 記憶島` |
| `creator_handle` | string | 必填 |  |  | 創作者同意公開的名稱 | `example_creator` |
| `work_type` | enum | 必填 |  | `video` / `article` / `app` / `3d_scene` / `visualization` / `game` / `other` | 作品類型 | `3d_scene` |
| `url` | url | 必填 |  |  | 作品網址 | `https://example.com/work/1` |
| `ai_tools` | string | 可留空 |  |  | 使用的 AI 工具，以 ; 分隔 | `Claude;Cursor` |
| `time_spent_hours` | number | 可留空 | h |  | 創作者自報的製作時數 | `3` |
| `datapack_version` | enum | 必填 |  | `v0.5` / `v1` / `v1.1` / `v2` | 使用的資料包版本 | `v1` |
| `files_used` | id_list | 可留空 |  |  | 用到的資料包檔案路徑，以 ; 分隔 | `reactions/peaks.csv;content/transcript.csv` |
| `submitted_via` | enum | 必填 |  | `hf_pull_request` / `email` / `upload` | 回報管道 | `hf_pull_request` |
| `submitted_date` | date | 必填 |  |  | 回報日期 | `2026-11-14` |
| `license` | string | 可留空 |  |  | 作品授權，例如 CC BY 4.0 |  |

## 參數

狀態：`fixed` 已定；`to_test` 目前是建議起始值，試錄後依結果調整；`to_decide` 還沒決定。值有改時改 `schema/parameters.csv` 並寫進 CHANGELOG。

| 參數 | 值 | 單位 | 用在 | 定義 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| `t0` | opening_applause_onset |  | `all` | T0（t_sec = 0）：開場第一段掌聲在主收音設備上的起點；所有裝置以這個聲音事件對時 | fixed |
| `slide_change_diff_threshold` | 0.3 | 0–1 | `content/slide_changes.csv` | 投影畫面前後差異達到這個值才算換頁（detect_method 為 visual_diff 時） | to_test |
| `event_score_threshold` | 0.5 | 0–1 | `reactions/sound_events.csv` | 分析窗的類別分數達到這個值才算該類別 | to_test |
| `event_merge_gap_sec` | 1 | s | `reactions/sound_events.csv` | 同類事件間隔小於這個秒數就合併 | to_test |
| `event_min_sec` | 1 | s | `reactions/sound_events.csv` | 事件長度短於這個秒數不收錄 | to_test |
| `silence_level_db` | -50 | dBFS | `reactions/sound_events.csv` | 全場安靜的音量上限 | to_test |
| `silence_min_sec` | 3 | s | `reactions/sound_events.csv` | 全場安靜至少持續的秒數 | to_test |
| `polite_window_sec` | 10 | s | `reactions/sound_events.csv` | 段落開始或結束前後這個秒數內的掌聲視為禮貌性掌聲 | to_test |
| `analysis_fps` | 2 | fps | `reactions/phone_raise.csv;reactions/hand_raise.csv;presence/presence_minute.csv` | Insta360 影片拿來偵測的每秒張數 | fixed |
| `person_conf_min` | 0.5 | 0–1 | `reactions/phone_raise.csv;reactions/hand_raise.csv;presence/presence_minute.csv` | 人的偵測信心達到這個值才算一個人 | to_test |
| `phone_conf_min` | 0.4 | 0–1 | `reactions/phone_raise.csv` | 手機的偵測信心達到這個值才算有手機 | to_test |
| `phone_up_min_sec` | 1 | s | `reactions/phone_raise.csv` | 手機高於肩膀持續達到這個秒數才算「舉手機」 | to_test |
| `hand_raise_min_sec` | 1 | s | `reactions/hand_raise.csv;reactions/stage_polls.csv` | 手腕高於頭頂持續達到這個秒數才算「舉手」 | to_test |
| `stand_min_sec` | 30 | s | `presence/presence_minute.csv` | 同一位置持續站立達到這個秒數才算「站著聽」；短於這個秒數視為起身走動 | to_test |
| `raise_event_min_people` | 3 | people | `reactions/phone_raise.csv;reactions/hand_raise.csv` | 同一秒舉手機或舉手的人數達到這個值才算進入事件 | to_test |
| `raise_event_min_sec` | 1 | s | `reactions/phone_raise.csv;reactions/hand_raise.csv` | 舉手機或舉手事件短於這個秒數不收錄 | to_test |
| `raise_merge_gap_sec` | 2 | s | `reactions/phone_raise.csv;reactions/hand_raise.csv` | 舉手機或舉手事件間隔小於這個秒數就合併 | to_test |
| `peak_merge_gap_sec` | 3 | s | `reactions/peaks.csv` | 高峰候選間隔小於這個秒數就合併成同一窗 | to_test |
| `pre_peak_window_sec` | 3 | s | `reactions/peaks.csv` | 高峰前要看的秒數（Franck 定為三秒） | fixed |
| `w_applause` | 1 |  | `reactions/peaks.csv` | score 中掌聲秒數的權重 | fixed |
| `w_laughter` | 2 |  | `reactions/peaks.csv` | score 中笑聲秒數的權重 | fixed |
| `w_phone` | 1 |  | `reactions/peaks.csv` | score 中舉手機人數的權重 | fixed |
| `stage_poll_window_sec` | 8 | s | `reactions/stage_polls.csv` | 講者提出調查後計算回應的秒數 | to_test |
| `fill_thresholds` | 0.5;0.8 | ratio | `presence/fill_order.csv` | 坐滿順序的兩個門檻（最大值的五成與八成） | fixed |
| `crowd_radius_m` | 1.5 | m | `after_talk/crowd_after_talk.csv` | 講者周圍幾公尺內算「圍住」 | fixed |
| `crowd_min_people` | 3 | people | `after_talk/crowd_after_talk.csv` | 圈內少於這個人數持續 30 秒就算結束 | fixed |
| `stop_min_sec` | 3 | s | `outside/passersby_10min.csv` | 在看板前停留至少這個秒數才算「停下」 | fixed |
| `bathroom_min_minutes` | 5 | min | `rankings/trivia.csv` | 廁所時段：同一區離席後出現回座的最短分鐘數；以區為單位看 left_count 與 returned_count，不追個人 | fixed |
| `bathroom_max_minutes` | 15 | min | `rankings/trivia.csv` | 廁所時段：同一區離席後出現回座的最長分鐘數；以區為單位看 left_count 與 returned_count，不追個人 | fixed |
| `csi_window_sec` | 10 | s | `presence/csi.csv` | CSI 每個時間窗的長度 | to_test |
| `csi_density_cutoffs` | 0.33;0.67 | 0–1 | `presence/csi.csv` | density_level 分級：同一時間窗各區 motion_level 的分位數，低於第一個為 low、高於第二個為 high | to_test |
