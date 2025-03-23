import yfinance as yf
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import math
import unicodedata

# ---------------------------
# Google Sheets API認証
# ---------------------------
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your_service_account.json', scope)
client = gspread.authorize(creds)

# ---------------------------
# 株価を取得する関数（安定版）
# ---------------------------
def get_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.fast_info['last_price']
    except Exception as e:
        print(f"{ticker}の価格取得失敗: {e}")
        return None

# ---------------------------
# 銘柄コードを全角→半角、空白除去、大文字化
# ---------------------------
def normalize_code(code):
    return unicodedata.normalize('NFKC', code).strip().upper()

# ---------------------------
# ティッカー変換関数（日本株のみ .T を付与）
# ---------------------------
def convert_ticker(code, is_japanese=False):
    return code if (is_japanese and code.endswith(".T")) else (f"{code}.T" if is_japanese else code)

# ---------------------------
# シート処理関数
# ---------------------------
def process_sheet(sheet_name, start_row, end_row, is_japanese=False):
    ws = client.open("your_google sheets_name").worksheet("worksheetname")
    data = ws.get_all_values()
    df = pd.DataFrame(data[start_row-1:end_row], columns=data[start_row-2])
    df.columns = df.columns.str.strip()

    # 銘柄コード整形（全角→半角、空白除去、大文字化）
    df["銘柄コード"] = df["銘柄コード"].fillna("").astype(str)
    df["銘柄コード"] = df["銘柄コード"].apply(normalize_code)
    df = df[df["銘柄コード"] != ""]

    # ティッカー列作成
    df["Ticker"] = df["銘柄コード"].apply(lambda x: convert_ticker(x, is_japanese))

    # デバッグ：ティッカー一覧
    print(f"\n▶ 処理中のティッカー一覧（{sheet_name}）:")
    print(df["Ticker"].tolist())

    # 数値列を変換
    df["保有数量"] = df["保有数量"].astype(float)
    df["平均取得額"] = df["平均取得額"].astype(float)

    # 現在値取得
    df["現在値"] = df["Ticker"].apply(get_price)

    # デバッグ：現在値確認
    print("▶ 取得した現在値:")
    print(df[["Ticker", "現在値"]])

    # 損益計算
    df["損益"] = (df["現在値"] - df["平均取得額"]) * df["保有数量"]

    # スプレッドシートに反映（NaN除外）
    for i, row in df.iterrows():
        row_num = start_row + i
        if row["現在値"] is not None and not math.isnan(row["現在値"]):
            ws.update_cell(row_num, 6, round(row["現在値"], 2))  # F列：現在値
            ws.update_cell(row_num, 7, round(row["損益"], 2))    # G列：損益

# ---------------------------
# 実行：米国株 & 日本株
# ---------------------------
process_sheet("worksheetname", start_row=3, end_row=13, is_japanese=False)  # 米国株
process_sheet("worksheetname", start_row=19, end_row=23, is_japanese=True)   # 日本株