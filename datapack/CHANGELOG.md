# 版本紀錄

每一版寫：新增、修改、移除了哪些檔案與欄位，以及下一版預計加入什麼。不寫「仍在處理中」，寫「第一版收錄某某；第二版某時加入某某」。

## 架構調整（發布前）

- 對照 Franck v0 架構版補上欄位：`manifest.csv` 的 `description`、`filled_by`、`priority`；`content/transcript.csv` 的 `text_raw`（轉寫原文）；`reactions/sound_events.csv` 的 `chatter`（台下討論聲）與 `level_db_max`；`reactions/peaks.csv` 的 `pre3s_action`；`reactions/timeline_minute.csv` 的 `transcript_text`；`questions/pre_event.csv`、`questions/unasked.csv`、`startups/topics.csv` 的 `consent_public`；`online/search_lift.csv` 的前後一小時指數；`derivatives/works.csv` 的 `files_used` 等
- 修改：台下影像改由 Insta360（X5）偵測，移除座位區面積法；`reactions/phone_raise.csv`、`reactions/stage_polls.csv`、`reactions/timeline_minute.csv`、`presence/` 改為人數欄位；X5 加入 `reactions/sound_events.csv` 的收音設備
- 新增：`reactions/hand_raise.csv`（舉手）
- 移除：`scene/photos/`、`scene/stage_splat.ply`；`scene/scene_notes.md` 改為 `scene/scene_description.md`，資料包只放文字

## 架構調整：負責人與參數（發布前）

- CSV 改為 UTF-8 含 BOM
- 新增：`file_owners.csv`（內部用，打包時排除）、`presence/csi.csv`（Wifi 人流，v1.1 延伸）
- 參數定案：每秒取 2 張、高峰權重 1/2/1、圍住 1.5 公尺與 3 人、停下 3 秒；其餘測試門檻填入建議起始值

## v0.5（【發布日期】）

- 新增：`content/agenda.csv`（只有公開的講者名單與開門時間）、`speakers/`、`social/speakers_yc_posts.csv`、`docs/venue_map.md`
- 下一版（v1，散場 2 小時內）：逐字稿、換頁、聲音事件、反應高峰、每分鐘總表、台上 Q&A、場景描述
