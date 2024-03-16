import sys
import json
from pprint import pprint
from urllib import request


class DownloadCounter:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo


    def get_releases(self) -> list[dict]:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"

        with request.urlopen(url) as response:
            if (response.code == 200):
                return json.loads(response.read())

        return []


    def get_downloads(self, releases: list[dict]) -> dict[str, int]:
        tag_download_map = {}
        for release in releases:
            executable_assets = [asset for asset in release.get("assets", []) if asset.get("name").endswith(".exe")]
            for asset in executable_assets:
                tag_download_map[release.get("tag_name")] = asset.get("download_count", 0)

        return tag_download_map


    def accumulate_downloads(self, downloads: dict[str, int]) -> int:
        download_count = 0
        for count in downloads.values():
            download_count += count

        return download_count


    def dump_download_count(self):
        releases = self.get_releases()
        tag_download_map = self.get_downloads(releases)
        download_count = self.accumulate_downloads(tag_download_map)

        print(f"Release and Download Count for {self.owner}/{self.repo}")
        pprint(tag_download_map, indent=2, sort_dicts=False)
        print(f"Total downloads: {download_count}")


if (__name__ == "__main__"):
    if (len(sys.argv) != 3):
        raise ValueError("Usage: python download_counter.py <owner> <repo>")

    download_counter = DownloadCounter(sys.argv[1], sys.argv[2])
    download_counter.dump_download_count()
