from importlib import metadata


_pkg_metadata = metadata.metadata("qgis-plugin-ci") or {}


__package_name__: str = _pkg_metadata.get("Name", "qgis-plugin-ci")
__version__ = _pkg_metadata.get("Version", "0.0.0-dev0")

__all__ = [
    "__package_name__",
    "__version__",
]
