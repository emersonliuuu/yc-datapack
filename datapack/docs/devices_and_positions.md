# 設備與機位

設備代號沿用 DOC-791 的 YC 設備與機位 database。原本拍座位區的 R、D1、D2 改由 X5 一台取代。每台設備放哪、誰顧，以當天實際為準，發布前把【】換成實際紀錄。各表的 `camera`、`mic`、`source_devices` 欄都用這裡的代號。

| 代號 | 設備 | 放哪 | 收什麼 | 用在 | 方案 |
| --- | --- | --- | --- | --- | --- |
| A | 手機，一般錄影 | 前排走道邊，對著投影幕 | 簡報畫面與換頁 | `content/slide_changes.csv`、`content/slides_notes.csv` | 兩人也要有 |
| A1 | 音控台音源 | 音控台 | 講台麥克風原音 | `content/transcript.csv` | 主辦方同意才加 |
| B | 錄音設備 | 前排座位 | 講者聲音、前排反應 | `content/transcript.csv`、`reactions/sound_events.csv` | 兩人也要有 |
| B2 | 電腦錄音 | 前排座位 | 講者聲音（逐字稿第二來源） | `content/transcript.csv` | 兩人也要有 |
| B3 | Wispr | 前排座位 | 即時逐字稿（第三來源） | `content/transcript.csv` | 人夠才加 |
| C | 手機錄音 | 前中段座位 | 台下反應 | `reactions/sound_events.csv` | 人夠才加 |
| E | 手機，手持 | 跟講者下台、走廊 | 講完被圍住、現場筆記 | `after_talk/crowd_after_talk.csv`、`notes/` | 兩人也要有 |
| H、H2 | 手機縮時 | 場外門口、YC 看板 | 路過、停下、拍照、進出場 | `outside/` | 兩人也要有 |
| X5 | Insta360 X5，360 影片含收音 | 【座位區中段走道，架高】，全程錄 | 座位區、舞台、投影幕；台下聲音 | `reactions/phone_raise.csv`、`reactions/hand_raise.csv`、`reactions/stage_polls.csv`、`presence/`、`reactions/sound_events.csv`、`content/slide_changes.csv`（備援）、`outside/entry_minute.csv`、`scene/scene_description.md` | 確定使用 |
| form | 報名表與 QR 表單 | 線上 | 問題、創業題目 | `questions/`、`startups/` | 兩人也要有 |
| online | 公開網路資料 | 線上 | 講者資料、貼文、搜尋量 | `speakers/`、`social/`、`online/`、`side_events/` | — |

## 當天實際配置

| 代號 | 實際位置 | 顧的人（角色代號） | 開始錄 | 結束錄 | 中斷時段 |
| --- | --- | --- | --- | --- | --- |
| 【】 | 【】 | 【】 | 【HH:MM:SS】 | 【HH:MM:SS】 | 【】 |
