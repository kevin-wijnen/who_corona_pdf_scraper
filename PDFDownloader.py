import requests
from pathlib import Path

def download_PDF(link, downloadmap, filename):
    response = requests.get(link, stream = True)
    Path(downloadmap).mkdir(parents=True, exist_ok=True)
    if response.status_code == 404:
        return False
    with open(str(Path(downloadmap,"{}.pdf".format(filename))), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return True