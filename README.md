# StockPilot Free V1.1

免費 GitHub Pages 台美股每日歷史行情與量化分析網站。**非盤中即時報價，不提供下單。**

## 從舊版升級（iPhone Safari）

1. 解壓縮下載的 `stockpilot_v1_1.zip`。
2. 將 `index.html`、`symbols.json`、`requirements.txt`、`scripts/update.py`、`.github/workflows/update-prices.yml` 上傳到 GitHub 儲存庫相同的路徑。可使用 GitHub 網頁版 Upload files 上傳解壓後的資料夾內容；**要保留 `.github/workflows/` 目錄結構**。建議在電腦上上傳，iPhone 可以逐一建立檔案。
3. 確認 Settings → Actions → General → Workflow permissions 為 **Read and write permissions**（若無法選擇，需確認權限或組織政策）。
4. 開啟 Actions → **Update daily stock prices** → **Run workflow** → Run workflow。首次執行通常需要幾分鐘。
5. Actions 成功後，確認 `data/2330.TW.json` 等檔案已出現，再開啟 `https://areswise-sudo.github.io/stockpilot-free/` 並重新整理。
6. 排程在週一至週五 23:20 UTC（台灣時間次日上午 07:20），可能因 GitHub 排程延遲而稍晚執行。可手動執行更新。

## 新增股票並啟用自動行情

網頁的「＋ 新增股票」只增加**本機自選股**。若要自動抓取，必須在 `symbols.json` 新增，例如：

```json
{"code":"2317","name":"鴻海","market":"TW"}
```

`market` 只能是 `TW`（台股上市）、`TWO`（台股上櫃）或 `US`（美股），修改後再次執行 Actions。網站自選股存在瀏覽器 localStorage，無跨裝置同步。

## 資料品質與授權

使用 yfinance（非官方 Yahoo Finance 介面），不保證完整性、延遲程度、授權或可用性；請遵守資料提供者使用條款。GitHub Pages 公開儲存庫會公開所有產出的歷史行情檔案，不應加入個人資訊或金鑰。台股與美股交易日、時區不同，可能在同一日更新不同步。歷史 OHLC 使用 `auto_adjust=True`，可能與券商未還原報價不同。

若來源被限制或失效，Actions 會留下錯誤紀錄，既有資料不會被虛構價格取代。必要時改用合規授權的替代來源。

## 量化模型

MA20、MA60：最近 20/60 根收盤價平均。RSI14：Wilder 平滑。KD：9 日 RSV，K/D 初值 50，平滑 1/3。MACD：EMA12−EMA26，訊號 EMA9，柱狀體 DIF−訊號。ATR14：Wilder TR 平滑。評分為規則式，不是預測勝率。停損和目標是最後收盤價 ± 2/4 ATR 的**示範風險情境**，不代表合理估值。


## 一次部署後的日常使用

完成部署並首次執行 Actions 後，原本的九檔股票會自動按排程更新，不需每天重新上傳程式。網站上的「重新整理」只讀取最新已產生的資料，不會直接抓即時報價。

**限制：** 網站上直接新增的代碼只會儲存在你的瀏覽器；要讓新增代碼也每天自動更新，必須在 GitHub `symbols.json` 增加該代碼。免費 GitHub Pages 沒有安全的使用者後端，因此無法從公開網頁直接修改 GitHub 儲存庫。

**請勿把公開儲存庫放入 API 金鑰、密碼、帳戶資訊。** 若日後要求即時行情、個人化跨裝置同步、完整財報或保證資料可用，可能需要額外授權或付費服務。
