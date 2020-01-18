from pathlib import Path
from datetime import datetime

NOW = datetime.now()
TIMESTAMP = f"{NOW.hour}-{NOW.minute}-{NOW.second}"


def debug_html_request(filename, html_data, html_requests_folder='./log'):
    html_requests_folder = Path(html_requests_folder)

    if not html_requests_folder.exists():
        html_requests_folder.mkdir()

    html_file = html_requests_folder / Path(f"{filename}_{TIMESTAMP}.html")
    with html_file.open('wb') as fh:
        fh.write(html_data)
