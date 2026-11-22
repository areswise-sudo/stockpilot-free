import json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import yfinance as yf

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
DEFAULT=[('2330','台積電','TW'),('2301','光寶科','TW'),('2327','國巨','TW'),('2377','微星','TW'),('4542','科嶠','TWO'),('3498','陽程','TWO'),('NVDA','NVIDIA','US'),('CRWV','CoreWeave','US'),('TSLA','Tesla','US')]
watch=ROOT/'symbols.json'
if not watch.exists():
    watch.write_text(json.dumps([{'code':c,'name':n,'market':m} for c,n,m in DEFAULT],ensure_ascii=False,indent=2),encoding='utf8')
symbols=json.loads(watch.read_text(encoding='utf8'))
status=[]
for item in symbols:
    code=str(item['code']).upper().strip(); market=item['market'].upper(); ticker=code+('.TW' if market=='TW' else '.TWO' if market=='TWO' else '')
    safe=''.join(c for c in ticker if c.isalnum() or c in '.-_')
    try:
        df=yf.Ticker(ticker).history(period='2y',interval='1d',auto_adjust=True)
        if df is None or len(df)<65: raise ValueError('有效日線不足 65 筆')
        df=df.dropna(subset=['Close'])
        records=[]
        for dt,r in df.iterrows():
            if pd.isna(r['Close']):continue
            records.append({'date':dt.strftime('%Y-%m-%d'),'open':round(float(r['Open']),4),'high':round(float(r['High']),4),'low':round(float(r['Low']),4),'close':round(float(r['Close']),4),'volume':int(r['Volume']) if pd.notna(r['Volume']) else 0})
        if len(records)<65:raise ValueError('有效日線不足 65 筆')
        payload={'code':code,'name':item.get('name',code),'market':market,'symbol':ticker,'currency':'TWD' if market!='US' else 'USD','adjustment':'Yahoo Finance adjusted OHLC (auto_adjust=True)','provider':'Yahoo Finance via yfinance (unofficial)','fetched_at':datetime.now(timezone.utc).isoformat(),'bars':records}
        (DATA/(safe+'.json')).write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf8')
        status.append({'code':code,'symbol':ticker,'ok':True,'last_date':records[-1]['date'],'count':len(records)})
        print('OK',ticker,len(records),flush=True)
    except Exception as exc:
        status.append({'code':code,'symbol':ticker,'ok':False,'error':str(exc)[:220]})
        print('ERROR',ticker,str(exc),file=sys.stderr,flush=True)
    time.sleep(1)
(DATA/'status.json').write_text(json.dumps({'updated_at':datetime.now(timezone.utc).isoformat(),'results':status},ensure_ascii=False,indent=2),encoding='utf8')
if not any(x['ok'] for x in status):sys.exit('所有行情抓取失敗；保留既有資料，請檢查 Actions 紀錄')
