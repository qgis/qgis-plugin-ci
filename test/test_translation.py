#! /usr/bin/env python

# standard library
import logging
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# project
from qgispluginci.parameters import Parameters
from qgispluginci.translation import Translation


# Logging
logger = logging.getLogger(__name__)


class TestLocalTranslation(unittest.TestCase):
    """Translation with only local TS files."""

    def setUp(self):
        self.parameters = Parameters.make_from(
            path_to_config_file=Path("test/fixtures/.qgis-plugin-ci")
        )

    def make_translation(self, i18n_folder: Path) -> Translation:
        translation = Translation(self.parameters)
        self.assertIsNone(translation.tx_client)
        translation.ts_file = str(i18n_folder / Path(translation.ts_file).name)
        translation.language_ts_files = lambda: [
            str(i18n_folder / Path(f).name)
            for f in Translation.language_ts_files(translation)
        ]
        return translation

    def test_update_strings_empty_ts_file(self):
        """An existing empty TS file, or a missing i18n folder, must not fail."""
        with TemporaryDirectory() as tmp_dir:
            for create_empty_file in (True, False):
                i18n_folder = Path(tmp_dir) / f"i18n_{create_empty_file}"
                translation = self.make_translation(i18n_folder)
                ts_file = Path(translation.ts_file)
                if create_empty_file:
                    ts_file.parent.mkdir()
                    ts_file.touch()

                translation.update_strings()

                content = ts_file.read_text()
                self.assertIn("<TS", content)
                self.assertIn("some UTF-8 translation", content)

    def test_update_strings_all_languages(self):
        """The TS file of each language is created, the source one included."""
        with TemporaryDirectory() as tmp_dir:
            i18n_folder = Path(tmp_dir) / "i18n"
            translation = self.make_translation(i18n_folder)

            translation.update_strings(all_languages=True)

            resource = self.parameters.i18n_resource_name
            expected = {
                f"{resource}_{lang}.ts"
                for lang in [
                    self.parameters.translation_source_language,
                    *self.parameters.translation_languages,
                ]
            }
            self.assertEqual(expected, {f.name for f in i18n_folder.glob("*.ts")})
            for ts_file in i18n_folder.glob("*.ts"):
                self.assertIn("some UTF-8 translation", ts_file.read_text())

            # language attributes, from the file name, except for the source file
            source = self.parameters.translation_source_language
            for ts_file in i18n_folder.glob("*.ts"):
                lang = ts_file.stem.rsplit("_", 1)[1]
                content = ts_file.read_text()
                if lang == source:
                    self.assertNotIn("language=", content)
                else:
                    self.assertIn(
                        f'language="{lang}" sourcelanguage="{source}"', content
                    )

    def test_set_ts_language(self):
        """The language is read from the file name, existing attributes are kept."""
        translation = Translation(self.parameters)
        resource = self.parameters.i18n_resource_name
        cases = {
            # file name, <TS> tag before -> <TS> tag after
            f"{resource}_fr.ts": (
                '<TS version="2.1">',
                '<TS version="2.1" language="fr" sourcelanguage="en">',
            ),
            f"{resource}_pt_BR.ts": (
                '<TS version="2.1" language="">',
                '<TS version="2.1" language="pt_BR" sourcelanguage="en">',
            ),
            f"{resource}_de.ts": (
                '<TS version="2.1" language="de_CH" sourcelanguage="fr">',
                '<TS version="2.1" language="de_CH" sourcelanguage="fr">',
            ),
            "other_file_it.ts": (
                '<TS version="2.1">',
                '<TS version="2.1">',
            ),
        }
        with TemporaryDirectory() as tmp_dir:
            for name, (before, after) in cases.items():
                with self.subTest(name=name):
                    ts_file = Path(tmp_dir) / name
                    ts_file.write_text(
                        f'<?xml version="1.0" encoding="utf-8"?>\n{before}\n</TS>\n'
                    )
                    translation.set_ts_language(ts_file)
                    self.assertIn(after, ts_file.read_text())


if __name__ == "__main__":
    unittest.main()
