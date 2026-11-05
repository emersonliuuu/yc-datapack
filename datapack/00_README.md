# YC Startup School Taipei 2026 現場資料包

【版本 vX】・【發布日期】・Sensible Intelligence Lab

這包資料記錄 2026-11-12 YC Startup School Taipei 現場「全場一起經歷了什麼」：每一句話、每一頁簡報，以及台下當下的掌聲、笑聲、舉手與舉手機的時刻。只看全場，不看任何一個人。

## 先讀哪幾個

| 想做什麼 | 先讀 |
| --- | --- |
| 交給 AI 問當天狀況 | `01_transcript_segmented.md`，再加 `reactions/timeline_minute.csv` |
| 找全場反應最大的時刻 | `reactions/peaks.csv` |
| 看每一頁簡報有多少人舉手機拍 | `content/slide_changes.csv` 對 `reactions/phone_raise.csv` |
| 看有哪些檔案、從哪來 | `manifest.csv` |
| 查欄位意思 | `docs/field_reference.md` |

## 讀數字前要知道的

- **時間**：所有表的 `t_sec` 從開場第一段掌聲起算（T0 = 0）。用 `t_sec` 就能跨表對齊。
- **只有文字**：這包只有 CSV 與 Markdown，沒有影片、音檔與照片；場景寫在 `scene/scene_description.md`。
- **台下人數**：舉手、舉手機、在座與站著都由一台 Insta360 的 360 影片數出來，只數人、不認人。
- **人數是下限**：被擋住的人數不到，所有人數都是「至少」。
- **有範圍**：鏡頭只拍到部分座位區，範圍見 `docs/venue_map.md`；量不到的東西見 `docs/limitations.md`。
- **留空不是零**：留空代表沒測到；`0` 代表有測、結果是零。

## 三條規則

1. **標註來源與版本**：使用或改作時寫明「資料來源：YC Startup School Taipei 現場資料包 vX，Sensible Intelligence Lab」。
2. **不拿來認人**：不與其他資料結合去找出特定個人。
3. **作品請寫回**：做好的二創請回報，會收進下一版的 `derivatives/works.csv`。

## 這版改了什麼

【從 CHANGELOG.md 複製本版的段落】
