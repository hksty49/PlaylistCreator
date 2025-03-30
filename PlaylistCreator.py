from SpotifyAccessor import create_playlist, authenticate_spotify 
from SpreadSheetAccessor import access_spreadsheet, get_event_details, get_setlist

# メインスクリプトとして実行された場合に関数を呼び出す
if __name__ == "__main__":
    
    # 初期化・認証
    access_spreadsheet()  # スプレッドシートにアクセス
    authenticate_spotify()  # Spotify API認証

    # スプレッドシートからデータを取得
    event_details = get_event_details();
    setlist = get_setlist()

    print("イベント詳細:", event_details)
    print("セットリスト:", setlist)

    #　プレイリスト作成