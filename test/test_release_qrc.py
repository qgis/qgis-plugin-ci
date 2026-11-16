#! /usr/bin/env python

# standard
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# Project
from qgispluginci.parameters import Parameters
from qgispluginci.release import compile_qrc


class TestCompileQrc(unittest.TestCase):
    def setUp(self):
        self.parameters = Parameters({"plugin_path": "qgis_plugin_CI_testing"})
        self.qrc_file = Path("qgis_plugin_CI_testing/resources.qrc")

    def test_compile_qrc(self):
        """The .qrc file is compiled, with an import of qgis.PyQt instead of PySide."""
        with TemporaryDirectory() as tmp_dir:
            output_file = Path(tmp_dir) / "resources_rc.py"
            compile_qrc(self.qrc_file, output_file, self.parameters)

            content = output_file.read_text()
            self.assertIn("from qgis.PyQt import QtCore", content)
            self.assertNotIn("PySide", content)
            self.assertIn("qt_resource_data", content)
            self.assertIn("def qInitResources():", content)
            # the generated module must be valid Python
            compile(content, str(output_file), "exec")

    def test_compile_qrc_missing_rcc(self):
        """A missing rcc executable stops the process."""
        self.parameters.rcc_path = "rcc-does-not-exist"
        with TemporaryDirectory() as tmp_dir:
            with self.assertRaises(SystemExit) as cm:
                compile_qrc(
                    self.qrc_file, Path(tmp_dir) / "resources_rc.py", self.parameters
                )
        self.assertEqual(1, cm.exception.code)

    def test_compile_qrc_invalid_file(self):
        """A .qrc file referencing a missing resource stops the process."""
        with TemporaryDirectory() as tmp_dir:
            qrc_file = Path(tmp_dir) / "invalid.qrc"
            qrc_file.write_text(
                "<RCC><qresource><file>does-not-exist.png</file></qresource></RCC>"
            )
            with self.assertRaises(SystemExit) as cm:
                compile_qrc(qrc_file, Path(tmp_dir) / "invalid_rc.py", self.parameters)
        self.assertEqual(1, cm.exception.code)


if __name__ == "__main__":
    unittest.main()
