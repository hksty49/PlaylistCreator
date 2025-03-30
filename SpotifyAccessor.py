import spotipy

# 定数としてユーザー名を定義
USER_NAME = '31c4kg7waubwzd5wzgfsyrvifdpa'

# グローバル変数としてSpotifyオブジェクトを定義
spotify = None

def authenticate_spotify():
    """Spotify APIの認証を行い、グローバル変数に設定する"""
    global spotify  # グローバル変数を使用
    client_id = '306828be1b044a5592215915dcdeb6f0'
    client_secret = '6523f5c5214c4241be3081128c6ca5c8'

    authentication_dict = {
        "client_id": client_id,
        "client_secret": client_secret,
        "username": USER_NAME,
        "redirect_uri": 'http://127.0.0.1:8080/',
        "scope": "playlist-modify-public,playlist-modify-private,ugc-image-upload"
    }
    token = spotipy.util.prompt_for_user_token(**authentication_dict)
    spotify = spotipy.Spotify(auth=token)

def search_songs(search_key, num_songs):
    """指定したキーワードで曲を検索する"""
    results = spotify.search(q=search_key, limit=num_songs, offset=0, type='track', market=None)
    return results

def extract_unique_songs(results, num_songs):
    """検索結果からユニークな曲を抽出する"""
    songs_unique = []
    songs_unique_index = []
    for i in range(num_songs):
        song_name = results['tracks']['items'][i]['name']
        artists_info = results['tracks']['items'][i]['artists']
        artists = [artists_info[j]['name'] for j in range(len(artists_info))]
        if (song_name, artists[0]) not in songs_unique:
            songs_unique.append((song_name, artists[0]))
        songs_unique_index.append(i)
    return songs_unique, songs_unique_index

def add_songs_to_playlist(playlist_id, uris):
    """プレイリストに曲を追加する"""
    spotify.playlist_add_items(playlist_id, uris)

def create_playlist(songs_dict, playlist_name, description):
    """
    プレイリストを作成し、Dictionary型の曲情報に基づいて曲を追加する。

    Args:
        songs_dict (dict): 曲順をキー、曲名とアーティスト名を値とする辞書。
        playlist_name (str): プレイリスト名。
        description (str): プレイリストの説明。
    """
    # Spotify API認証
    authenticate_spotify()

    # プレイリストを作成
    playlist = spotify.user_playlist_create(USER_NAME, playlist_name, description=description)

    # 曲を検索してプレイリストに追加
    uris = []
    for order, (track_name, artist_name) in songs_dict.items():
        search_key = f"{track_name} {artist_name}"
        results = search_songs(search_key, 1)
        if results['tracks']['items']:
            uris.append(results['tracks']['items'][0]['uri'])
        else:
            print(f"曲が見つかりませんでした: {track_name} by {artist_name}")

    # プレイリストに曲を追加
    if uris:
        add_songs_to_playlist(playlist['id'], uris)
        print(f"プレイリスト '{playlist_name}' に曲を追加しました。")
    else:
        print("追加する曲がありませんでした。")

if __name__ == "__main__":
    # サンプルの曲情報
    sample_songs = {
        1: ("Revolution", "coldrain"),
        2: ("Gone", "coldrain"),
        3: ("The Side Effects", "coldrain")
    }
    sample_playlist_name = "My Favorite Songs"
    sample_description = "This playlist was created using Spotify API."

    create_playlist(sample_songs, sample_playlist_name, sample_description)
