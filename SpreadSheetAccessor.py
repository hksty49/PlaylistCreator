import gspread
from google.oauth2.service_account import Credentials

# ワークシートのグローバル変数
worksheet = None

def get_event_details():
    """
    スプレッドシートからイベントの詳細情報を取得する関数。

    Args:
        worksheet: gspreadのワークシートオブジェクト

    Returns:
        dict: イベントの詳細情報を格納した辞書
    """
    # データを一括取得
    cell_ranges = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']
    global worksheet  # グローバル変数を使用
    cells = worksheet.batch_get(cell_ranges)

    # 空のセルにデフォルト値を設定
    values = [cell[0][0] if cell else "" for cell in cells]

    # データを辞書に割り当て
    event_details = {
        "year": values[0],
        "month": values[1],
        "day_from": values[2],
        "day_to": values[3],
        "event": values[4],
        "artist": values[5],
        "with_artist": values[6],
        "place": values[7],
    }

    return event_details

# 曲順、曲名、アーティスト名を取得し辞書型に変換
def get_setlist():
    global worksheet  # グローバル変数を使用
    all_data = worksheet.get_all_values()

    # 12行目以降を取得（0インデックスなので11から）
    playlist_data = []
    for row in all_data[11:]:
        if len(row) < 3:  # A, B, C列が不足している場合は終了
            break
        track_number = row[0].strip() if row[0] else None
        track_name = row[1].strip() if row[1] else None
        artist_name = row[2].strip() if row[2] else None

        # 曲名またはアーティスト名が空の場合、終了
        if not track_name or not artist_name:
            break

        # 辞書型データとして追加
        playlist_data.append({
            "track_number": track_number,
            "track_name": track_name,
            "artist_name": artist_name
        })

    return playlist_data

def access_spreadsheet():
    """
    スプレッドシートにアクセスし、イベントの詳細とプレイリストデータを取得する関数。
    
    Returns:
        tuple: イベントの詳細情報とプレイリストデータを格納した辞書
    """

    # 認証のスコープを設定
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # 認証情報をサービスアカウントのJSONファイルから作成
    json_path = 'key_spreadsheet.json'
    creds = Credentials.from_service_account_file(json_path, scopes=SCOPES)

    # gspread を使って認証
    gc = gspread.authorize(creds)

    # スプレッドシートにアクセス
    spreadsheet_name = 'Setlist'
    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet('Setlist')
