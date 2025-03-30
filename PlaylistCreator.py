from SpotifyAccessor import create_playlist

# プレイリストを作成する関数
def generate_playlist():
    # プレイリストのデータを定義
    playlist_data = {
        "songs": [
            {"title": "Song A", "artist": "Artist 1", "order": 1},
            {"title": "Song B", "artist": "Artist 2", "order": 2},
            {"title": "Song C", "artist": "Artist 3", "order": 3},
        ],
        "name": "My Custom Playlist",
        "description": "A playlist created programmatically."
    }

    # create_playlist関数を呼び出す
    create_playlist(playlist_data)

# メインスクリプトとして実行された場合に関数を呼び出す
if __name__ == "__main__":
    generate_playlist()