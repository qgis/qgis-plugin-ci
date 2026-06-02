from dataclasses import dataclass


@dataclass
class VersionNote:
    """Object describing a version note in a changelog."""

    date: str | None = None
    major: str | None = None
    minor: str | None = None
    patch: str | None = None
    prerelease: str | None = None
    separator: str | None = None
    text_raw: str | None = None
    url: str | None = None

    # @classmethod
    # def from_dict(version_as_dict: dict) -> "VersionNote":
    #     return VersionNote(

    #     )

    @property
    def text(self) -> str:
        """Remove many \n at the start and end of the string."""
        return self.text_raw.strip()

    @property
    def is_prerelease(self) -> bool:
        if self.prerelease and len(self.prerelease):
            return True
        else:
            return False

    @property
    def version(self) -> str:
        """Version name.

        Returns:
            str: _description_
        """
        if self.prerelease:
            return f"{self.major}.{self.minor}.{self.patch}-{self.prerelease}"
        else:
            return f"{self.major}.{self.minor}.{self.patch}"
