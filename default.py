import xbmc
import xbmcgui
import json
import os
import xbmcvfs

LOG_FILE = xbmcvfs.translatePath('special://temp/remove_empty_shows.log')

def log(msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def get_tvshows():
    request = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.GetTVShows",
        "params": {"properties": ["title", "episode"]},
        "id": 1
    }
    response = json.loads(xbmc.executeJSONRPC(json.dumps(request)))
    tvshows = response['result'].get('tvshows', [])
    log(f"Found {len(tvshows)} TV shows")
    return tvshows

def remove_tvshow(tvshow):
    tvshow_id = tvshow['tvshowid']
    title = tvshow['title']
    request = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.RemoveTVShow",
        "params": {"tvshowid": tvshow_id},  # only tvshowid
        "id": 1
    }
    result = json.loads(xbmc.executeJSONRPC(json.dumps(request)))
    log(f"Removed '{title}' (ID {tvshow_id}): {result}")

def main():
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Remove Empty Shows', 'Searching...')
    tvshows = get_tvshows()
    if (pDialog.iscanceled()): return
    pDialog.update(80, 'Processing shows')
    empty_shows = [show for show in tvshows if show.get('episode', 0) == 0]
    pDialog.update(100)
    if (pDialog.iscanceled()): return
    pDialog.close()

    if not empty_shows:
        xbmcgui.Dialog().ok("Remove Empty TV Shows", "No empty TV shows found.")
        return

    num = len(empty_shows)
    confirm = xbmcgui.Dialog().yesno(
        "Remove Empty TV Shows",
        f"Found {num} empty TV shows. Delete them?",
        yeslabel="Delete",
        nolabel="Cancel"
    )

    if confirm:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Remove Empty Shows', 'Removing')
        for index, show in enumerate(empty_shows):
            pDialog.update((index*100) // num, f"Removing ({index + 1}/{num}): {show['title']}")
            remove_tvshow(show)
        pDialog.close()

        xbmcgui.Dialog().notification(
            "Kodi",
            f"Removed {len(empty_shows)} empty TV shows",
            xbmcgui.NOTIFICATION_INFO,
            4000
        )
    else:
        xbmcgui.Dialog().notification(
            "Kodi",
            "No TV shows were removed",
            xbmcgui.NOTIFICATION_INFO,
            3000
        )

if __name__ == "__main__":
    main()
