# 版本紀錄

每一版寫：新增、修改、移除了哪些檔案與欄位，以及下一版預計加入什麼。不寫「仍在處理中」，寫「第一版收錄某某；第二版某時加入某某」。

## 架構調整（發布前）

- 對照 Franck v0 架構版補上欄位：`manifest.csv` 的 `description`、`filled_by`、`priority`；`content/transcript.csv` 的 `text_raw`（轉寫原文）；`reactions/sound_events.csv` 的 `chatter`（台下討論聲）與 `level_db_max`；`reactions/peaks.csv` 的 `pre3s_action`；`reactions/timeline_minute.csv` 的 `transcript_text`；`questions/pre_event.csv`、`questions/unasked.csv`、`startups/topics.csv` 的 `consent_public`；`online/search_lift.csv` 的前後一小時指數；`derivatives/works.csv` 的 `files_used` 等
- 修改：`reactions/phone_raise.csv` 改為一次舉起來事件一列

## v0.5（【發布日期】）

- 新增：`content/agenda.csv`（只有公開的講者名單與開門時間）、`speakers/`、`social/speakers_yc_posts.csv`、`docs/venue_map.md`
- 下一版（v1，散場 2 小時內）：逐字稿、換頁、聲音事件、反應高峰、每分鐘總表、台上 Q&A、舞台照片
