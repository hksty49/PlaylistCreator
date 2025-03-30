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


def generate_playlist_name(event_details):
    """
    プレイリスト名を生成する関数。

    Args:
        event_details (dict): イベントの詳細情報を格納した辞書。
    
    Returns:
        str: 生成されたプレイリスト名。
    """
    # 日付の取得
    day_from = event_details.get("day_from", "").zfill(2)
    day_to = event_details.get("day_to", "").zfill(2)

    if day_to != "00":
        day = f"{day_from} - {day_to}"
    else:
        day = day_from
    
    year = event_details.get("year", "")
    month = event_details.get("month", "")
    event = event_details.get("event", "")

    return f"{year}.{month}.{day} {event}"

def generate_playlist_description(event_details):
    """
    プレイリストの説明を生成する関数。

    Args:
        event_details (dict): イベントの詳細情報を格納した辞書。
    
    Returns:
        str: 生成されたプレイリストの説明。
    """
    artist = event_details.get("artist", "")
    with_artist = event_details.get("with_artist", "")
    if with_artist != "":
        artist = f"{artist} × {with_artist}"  # 全角の「×」を使用

    place = event_details.get("place", "")

    return f"{artist} @ {place}"

def create_playlist(setlist, event_details):
    """
    プレイリストを作成し、Dictionary型の曲情報に基づいて曲を追加する。

    Args:
        songs_dict (dict): 曲順をキー、曲名とアーティスト名を値とする辞書。
        playlist_name (str): プレイリスト名。
        description (str): プレイリストの説明。
    """
    # Spotify API認証
    authenticate_spotify()

    playlist_name = generate_playlist_name(event_details)
    playlist_description = generate_playlist_description(event_details)

    # プレイリストを作成
    playlist = spotify.user_playlist_create(USER_NAME, playlist_name, description=playlist_description)

    # 曲を検索してプレイリストに追加
    uris = []
    for order, (track, artist) in setlist.items():
        search_key = f"{track} {artist}"
        results = search_songs(search_key, 1)
        if results['tracks']['items']:
            uris.append(results['tracks']['items'][0]['uri'])
        else:
            print(f"曲が見つかりませんでした: {track} by {artist}")

    # プレイリストに曲を追加
    if uris:
        add_songs_to_playlist(playlist['id'], uris)
        print(f"プレイリスト '{playlist_name}' に曲を追加しました。")
    else:
        print("追加する曲がありませんでした。")
