# 與 Franck v0 架構版的欄位對照

對照來源：`datapack_yc_taipei_1112_v0.zip`（11/2 v0 架構版，中文欄位、只有標題列）。左邊是 Franck 的欄位，右邊是本 repo 的欄位。

- 「—」：這版沒有對應欄位，原因寫在備註。
- 「新增」：v0 沒有、本 repo 依收集項目 database 或 DOC-791 加上的欄位，不逐一列出，見 `datapack/docs/field_reference.md`。

## 檔案層級

| Franck v0 | 本 repo | 備註 |
| --- | --- | --- |
| `fnb/consumption.csv` | — | 收集項目 database 已移除 |
| `networking/groups_10min.csv` | — | 收集項目 database 已移除 |
| `reactions/laugh_spread.csv` | — | 收集項目 database 已移除；笑聲在 `reactions/sound_events.csv` |
| `online/hashtag_minute.csv` | — | 收集項目 database 已移除 |
| `online/youbike_parking.csv` | — | 收集項目 database 已移除 |
| — | `reactions/hand_raise.csv`、`content/segment_function.csv`、`reactions/stage_polls.csv`、`notes/`、`scene/`、`social/`、`side_events/luma.csv`、`speakers/news.csv`、`speakers/public_projects.md`、`questions/remembered_moments.csv` | v0 之後收集項目 database 新增 |
| 中文檔名（`00_先看這個.md` 等） | 英文檔名 | 對照見 `README.md` |
| `scene/photos/`、3D 模型 | `scene/scene_description.md` | 資料包只放文字，場景改用文字描述 |
| `docs/場地平面圖`（圖） | `docs/venue_map.md`（文字） | 同上 |
| UTF-8 含 BOM | UTF-8 不含 BOM | 待確認：Excel 直接開中文會亂碼時再改回 BOM |

## 欄位層級

| 檔案 | Franck v0 | 本 repo | 備註 |
| --- | --- | --- | --- |
| `manifest.csv` | 檔案、在說什麼、從哪來、誰填、優先序 | `path`、`description`、`source_devices`、`filled_by`、`priority` | 優先序：核心 `core`、加分 `bonus`、降級 `reduced`、延伸 `extension` |
| `content/transcript.csv` | 開始、結束、段落、講者 | `start_t_sec`、`end_t_sec`、`segment_id`、`speaker_id` | |
| | 原文、校對版 | `text_raw`、`text` | |
| | 信心 | `asr_confidence` | |
| `content/agenda.csv` | 段落、開始、結束、講者、主題、類型 | `segment_id`、`start_t_sec`、`end_t_sec`、`speaker_ids`、`title`、`segment_type` | |
| `content/slides_notes.csv` | 頁次、講者、頁標題、我們的筆記 | `slide_id`、`speaker_id`、`page_title`、`notes` | |
| | 開始、結束 | `first_shown_t_sec`、`total_dwell_sec` | 同一頁可能出現多次；每次的起訖在 `content/slide_changes.csv` |
| `content/slide_changes.csv` | 時間、從第幾頁、到第幾頁、講者 | `start_t_sec`、`from_slide_id`、`slide_id`、`speaker_id` | |
| `content/taiwan_mentions.csv` | 時間、講者、原話 | `t_sec`、`speaker_id`、`sentence_text` | |
| | 提到什麼 | `term`、`category` | |
| `content/tool_mentions.csv` | 時間、講者、工具或公司、原話 | `t_sec`、`speaker_id`、`term`、`sentence_text` | |
| `reactions/sound_events.csv` | 開始、結束 | `start_t_sec`、`end_t_sec` | |
| | 類型（掌聲、笑聲、安靜、討論聲） | `event`：`applause`、`laughter`、`silence`、`chatter` | |
| | 強度 | `score_max`、`level_db_max` | 分成模型分數與音量峰值 |
| | 收音點 | `mic` | |
| | 對到頁次、對到哪一句 | `slide_id`、`sentence_id` | |
| `reactions/phone_raise.csv` | 開始、結束、對到頁次 | `start_t_sec`、`end_t_sec`、`slide_id` | 一次舉手機事件一列 |
| | 估計人數 | `phone_count_peak` | |
| | 占可見人數比例 | `phone_share_peak`、`visible_count` | |
| `reactions/peaks.csv` | 名次、時間、頁次、講者 | `rank`、`peak_t_sec`、`slide_id`、`speaker_id` | |
| | 反應類型、強度 | `signals`、`score` | |
| | 高峰前三秒講者做了什麼 | `pre3s_text`、`pre3s_action` | 分成說的話與動作 |
| `reactions/timeline_minute.csv` | 分鐘、段落、講者、頁次 | `minute_idx`、`segment_id`、`speaker_id`、`slide_ids` | |
| | 逐字稿摘要 | `transcript_text` | 不摘要，放這一分鐘的原句 |
| | 掌聲秒數、笑聲秒數 | `applause_sec`、`laughter_sec` | |
| | 舉手機估計 | `phone_count_max` | 另加舉手 `hand_count_max` |
| | 可見人數、站立人數 | `visible_count`、`standing_count` | |
| | 離席、回座 | `left_count`、`returned_count` | |
| `presence/presence_minute.csv` | 分鐘、區 | `minute_idx`、`zone` | |
| | 可見人數、站立人數 | `visible_count`、`standing_count` | 另加坐著的人數 `seated_count` |
| | 離席、回座 | `left_count`、`returned_count` | |
| `presence/fill_order.csv` | 時間、區、大約坐滿幾成 | `fill_50_t_sec`、`fill_80_t_sec`、`zone_group`、`max_seated_count` | 改為一區一列，記坐到最多人數五成與八成的時間 |
| `after_talk/crowd_after_talk.csv` | 講者、下台時間 | `speaker_id`、`stage_exit_t_sec` | |
| | 圍住開始、圍住結束、最多幾人 | `start_t_sec`、`end_t_sec`、`peak_crowd` | |
| | 說到話的人數、等了又走的人數 | `talked_count`、`left_without_talking` | |
| `questions/onsite_qa.csv` | 時間、講者、問題 | `question_start_t_sec`、`answerer_speaker_id`、`question_text` | |
| | 回答開始、回答結束 | `answer_start_t_sec`、`answer_end_t_sec` | |
| `questions/pre_event.csv` | 想問的講者、問題、來源、時間、同意公開 | `target`、`question_text`、`source`、`submitted_date`、`consent_public` | 不同意公開時 `question_text` 留空 |
| `questions/unasked.csv` | 想問的講者、問題、來源、時間、同意公開 | `target`、`question_text`、`source`、`collected_date`、`consent_public` | 同上 |
| `startups/topics.csv` | 題目、類別、階段、來源 | `one_liner`、`category`、`stage`、`source` | |
| | 同意被聯絡 | `consent_public` | 改為同意題目公開；聯絡資訊另存，不進資料包 |
| `speakers/profiles.csv` | 講者、職稱、公司 | `display_name`、`role_title`、`organization` | |
| | YC 梯次或投資過的公司 | `yc_batch`、`notable_investments` | |
| | 跟台灣的連結、來源網址、查詢日期 | `taiwan_connection`、`source_urls`、`retrieved_date` | |
| `speakers/new_vs_old.csv` | 講者、這場的說法 | `speaker_id`、`claim_summary` | |
| | 過去講過嗎、過去出處 | `this_talk_status`、`past_source_url` | |
| | 這場新增了什麼 | `new_in_talk_summary` | |
| `online/posts.csv` | 發文時間、平台、公開網址 | `posted_at`、`platform`、`url` | |
| | 引用到的時刻或頁次 | `quoted_sentence_ids`、`quoted_slide_ids` | |
| | 抓取日期 | `retrieved_at` | |
| `online/search_lift.csv` | 提到的時間、工具或公司 | `mention_t_sec`、`normalized_name` | |
| | 提到前一小時、提到後一小時搜尋指數 | `index_1h_before`、`index_1h_after` | 沿用 Franck 的前後一小時；七天基準改為選填 |
| | 來源 | `source_url` | |
| `outside/entry_minute.csv` | 分鐘、進場人數、出場人數 | `minute_idx`、`entering`、`exiting` | |
| `outside/passersby_10min.csv` | 時段、路過、停下、停下並拍照、掃 QR | `window_start_clock`、`passersby`、`stopped`、`photographed`、`qr_scans` | |
| `rankings/trivia.csv` | 排行、結果、怎麼算的、用到哪幾張表 | `title_zh`、`value`、`rule`、`source_files` | |
| `derivatives/works.csv` | 收到時間、作者、作品網址 | `submitted_date`、`creator_handle`、`url` | |
| | 用了哪些檔案、用哪個 AI、花多久 | `files_used`、`ai_tools`、`time_spent_hours` | |

## 刻意不同的地方

1. **台下影像只用 X5**：v0 的 R、D 改由一台 Insta360 X5 的 360 影片偵測舉手、舉手機、坐著、站著、離席與回座；X5 的收音也加進 `reactions/sound_events.csv` 的 `mic`。
2. **舉手與舉手機分開**：v0 只有 `phone_raise`；X5 偵測得出手與手機，另加 `reactions/hand_raise.csv`，舉著手機的只算舉手機。
3. **舉手機改為事件**：v0 的 `phone_raise` 沒寫一列代表什麼，這版定為「一次舉手機事件一列」，起訖由 `raise_event_min_people` 等參數決定。
4. **只有文字**：舞台照片、3D 模型與平面圖檔不進資料包，改成 `scene/scene_description.md` 與 `docs/venue_map.md` 的文字描述。
5. **逐字稿摘要改放原句**：`timeline_minute.transcript_text` 放這一分鐘的原句，不摘要，符合「不放判斷」。
