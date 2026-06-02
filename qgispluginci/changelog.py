#! python3  # noqa E265

"""
Changelog parser. Following <https://keepachangelog.com/en/1.0.0/>.
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import re
import sys
from pathlib import Path
from typing import Any

# 3rd party
import keepachangelog

# package
from qgispluginci.version_note import VersionNote


# ############################################################################
# ########## Globals #############
# ################################

logger = logging.getLogger(__name__)

# ############################################################################
# ########## Classes #############
# ################################


class ChangelogParser:
    CHANGELOG_FILEPATH: Path | None = None

    @classmethod
    def has_changelog(
        cls,
        parent_folder: Path | str = Path(),
        changelog_path: Path | str = "CHANGELOG.md",
    ) -> bool:
        """Check if a changelog file exists within the parent folder. If it does, \
        it returns True and the file path is stored as class attribute. If not, it \
        returns False and the class attribute is reset to None.

        Args:
            parent_folder (Union[Path, str], optional): parent folder where to look \
                for a `CHANGELOG.md` file. Defaults to Path(".").

            changelog_path str: Path relative to parent_folder. Defaults to CHANGELOG.md.

        Raises:
            FileExistsError: if the parent_folder path doesn't exist
            TypeError: if the path is not a folder but a path

        Returns:
            bool: True if a CHANGELOG.md exists within the parent_folder
        """
        # reset stored path as class attribute
        cls.CHANGELOG_FILEPATH = None

        # ensure using pathlib.Path
        if isinstance(parent_folder, str):
            parent_folder = Path(parent_folder)

        # check if the folder exists
        if not parent_folder.exists():
            logger.error(
                f"Parent folder doesn't exist: {parent_folder.resolve()}",
                exc_info=FileExistsError(),
            )
            sys.exit(1)
        # check if path is a folder
        if not parent_folder.is_dir():
            logger.error(
                f"Path is not a folder: {parent_folder.resolve()}", exc_info=TypeError()
            )
            sys.exit(1)

        # build, check and store the changelog path
        cls.CHANGELOG_FILEPATH = parent_folder / changelog_path
        if cls.CHANGELOG_FILEPATH.is_file():
            logger.info(f"Changelog file used: {cls.CHANGELOG_FILEPATH.resolve()}")
            return True
        else:
            logger.warning(
                f"Changelog file doesn't exist: {cls.CHANGELOG_FILEPATH.resolve()}"
            )
            cls.CHANGELOG_FILEPATH = None
            return False

    def __init__(
        self,
        parent_folder: Path | str = Path(),
        changelog_path: str = "CHANGELOG.md",
    ):
        self.has_changelog(parent_folder=parent_folder, changelog_path=changelog_path)

    def _version_note_from_version_number(
        self, version_key: str, data: dict[str, Any]
    ) -> VersionNote | None:
        """Build a :class:`VersionNote` from a keepachangelog version entry.

        Args:
            version_key (str): version string as returned by keepachangelog.
            data (dict[str, Any]): the version dict produced by ``keepachangelog.to_dict()``.

        Returns:
            VersionNote or None if the version string cannot be decomposed.
        """
        metadata = data.get("metadata", {})

        # Prefer the already-parsed semantic_version when available
        # (keepachangelog cannot always produce it, e.g. for "v0.1.1")
        sem_ver = metadata.get("semantic_version")
        if sem_ver:
            major = str(sem_ver["major"])
            minor = str(sem_ver["minor"])
            patch = str(sem_ver["patch"])
            prerelease: str = sem_ver.get("prerelease") or ""
        else:
            # Fallback: parse the version string ourselves
            raw_version = version_key.lstrip("v")
            if "-" in raw_version:
                main_version, prerelease = raw_version.split("-", 1)
            else:
                main_version, prerelease = raw_version, ""

            parts = main_version.split(".")
            if len(parts) < 3:
                logger.warning(
                    f"Skipping version with unexpected format: {version_key!r}"
                )
                return None
            major, minor, patch = parts[0], parts[1], parts[2]

        # release_date is kept as a string by keepachangelog (non-ISO dates included)
        release_date = metadata.get("release_date")
        date_str = str(release_date) if release_date is not None else ""

        raw_text = self._raw_section_text(version_key)

        return VersionNote(
            major=major,
            minor=minor,
            patch=patch,
            url="",
            prerelease=prerelease,
            separator="",
            date=date_str,
            text_raw=f"\n{raw_text}\n" if raw_text else "\n",
        )

    def _parse(self) -> list[VersionNote] | None:
        """Parse the changelog and return one :class:`VersionNote` per released version.

        Returns:
            list[VersionNote]: entries ordered newest-first, matching the file order.
        """
        if not self.CHANGELOG_FILEPATH:
            return None

        changelog_parsed: dict | None = None

        try:
            changelog_parsed = keepachangelog.to_dict(
                str(self.CHANGELOG_FILEPATH), show_unreleased=False
            )
            print(changelog_parsed.keys())
        except Exception as exc:
            logger.error(
                f"Failed to parse changelog '{self.CHANGELOG_FILEPATH}'. Trace: {exc}",
                exc_info=exc,
            )
            return None

        result: list[VersionNote] = []
        for version_key, data in changelog_parsed.items():
            vn = self._version_note_from_version_number(version_key, data)
            if vn is not None:
                result.append(vn)
        return result

    def last_items(self, count: int) -> str:
        """Content to add in the metadata.txt.

        Args:
            count (int): Maximum number of tags to include in the file.

        Returns:
            str: changelog extraction ready to be added to metadata.txt
        """
        changelog_content = self._parse()
        if not changelog_content:
            return ""

        count = int(count)
        output = "\n"

        for version in changelog_content[0:count]:
            version_note = VersionNote(*version)
            output += f" Version {version_note.version}:\n"
            for item in version_note.text.split("\n"):
                if item:
                    output += f" {item}\n"
            output += "\n"
        return output

    def _version_note(self, tag: str) -> VersionNote | None:
        """Get the tuple for a given version."""
        changelog_content = self._parse()
        if not len(changelog_content):
            logger.error(
                f"Parsing the changelog ({self.CHANGELOG_FILEPATH.resolve()}) "
                "returned an empty content."
            )
            return None

        if tag == "latest":
            return VersionNote(*changelog_content[0])

        for version in changelog_content:
            version_note = VersionNote(*version)
            if version_note.version == tag:
                return version_note

    def latest_version(self) -> str:
        """Return the latest tag described in the changelog file."""
        latest = self._version_note("latest")
        logger.debug(
            "Latest version retrieved from changelog "
            f"({self.CHANGELOG_FILEPATH.resolve()}): {latest.version}"
        )
        return latest.version

    def content(self, tag: str) -> str | None:
        """Get a version content to add in a release according to the version name."""
        version_note = self._version_note(tag)
        if not version_note:
            return None

        return version_note.text


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    pass
