import requests
import json
import re
from datetime import datetime

INPUT_FILE = "Jchannels_cleaned.json"
OUTPUT_FILE = "Jchannels_final.json"
COOKIE_API = "https://globalplay.live/jiotvww/api.php"

def fetch_hdnea_token():
    try:
        r = requests.get(COOKIE_API, timeout=10)
        r.raise_for_status()
        match = re.search(r"(st=\d+~exp=\d+~acl=/\*~hmac=[a-f0-9]+)", r.text)
        if match:
            return f"__hdnea__={match.group(1)}"
        else:
            raise ValueError("Token not found in response")
    except Exception as e:
        print(" Error fetching token:", e)
        return None

def update_channels(token):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    for cid, data in channels.items():
        if "playbackURL" in data:
            if "?" in data["playbackURL"]:
                data["playbackURL"] += "&" + token
            else:
                data["playbackURL"] += "?" + token

   
    channels["_last_update"] = datetime.utcnow().isoformat()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, indent=4)

    print(f" Updated JSON saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    token = fetch_hdnea_token()
    if token:
        update_channels(token)
