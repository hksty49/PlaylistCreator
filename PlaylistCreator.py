from SpotifyAccessor import create_playlist
from SpreadSheetAccessor import access_spreadsheet, get_event_details, get_setlist

# メインスクリプトとして実行された場合に関数を呼び出す
if __name__ == "__main__":
    
    # 初期化・認証
    access_spreadsheet()  # スプレッドシートにアクセス
 
    # スプレッドシートからデータを取得
    event_details = get_event_details()
    setlist = get_setlist()

    #　プレイリスト作成
    create_playlist(setlist, event_details)