from pathlib import Path

import keepachangelog
import keepachangelog._changelog

from qgispluginci.version_note import VersionNote


changelog_parsed = keepachangelog.to_dict(
    f"{Path(__file__).parent.parent.parent.joinpath('CHANGELOG.md').resolve()}",
    show_unreleased=False,
)

print(changelog_parsed.keys())
version = changelog_parsed.get("v2.5.3")
print(type(version), version.keys(), version.get("metadata"))

version_meta = version.get("metadata")

vnote = VersionNote(
    date=version_meta.get("release_date"),
    major=version_meta.get("semantic_version").get("major"),
    minor=version_meta.get("semantic_version").get("minor"),
    patch=version_meta.get("semantic_version").get("patch"),
    prerelease=version_meta.get("semantic_version").get("prerelease"),
)

print(vnote.version)
