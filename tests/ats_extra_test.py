# -*- coding: UTF-8 -*-

'''
Module
    ats_extra_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    ats_coverage is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    ats_coverage is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines extra test cases for ats_coverage.py and ats_updater.py.
Execute
    python3 -m unittest discover -s tests -p '*_test.py'
'''

import os
import sys
import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from runpy import run_path

sys.path.append(str(Path(__file__).parent.parent))

from ats_updater import generate_tree_lines
from ats_coverage import (
    run_coverage,
    load_report,
    update_readme,
    update_structure,
    update_index_coverage,
    _run_tests_and_collect,
)

SCRIPT_PATH = str(Path(__file__).parent.parent / "ats_coverage.py")


class ATSCoverageBaseTestCase(unittest.TestCase):
    '''
        Defines class ATSCoverageBaseTestCase with setUp and tearDown.
        Base test case class providing temporary package structure setup.

        It defines:

            :attributes: None.
            :methods:
                | setUp - Set up temporary project structure before each test case.
                | tearDown - Clean up temporary project structure after each test case.
    '''

    def setUp(self) -> None:
        '''
            Set up temporary project structure before each test case.

            :exceptions: None.
        '''
        self.old_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

        sys.path.insert(0, self.temp_dir.name)

        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        self.pkg_dir = Path("dummy_package")
        self.pkg_dir.mkdir(parents=True, exist_ok=True)
        (self.pkg_dir / "__init__.py").write_text("def hello() -> str:\n    return 'world'\n", encoding="utf-8")
        (self.pkg_dir / "submodule.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")
        
        self.pkg_subdir = self.pkg_dir / "subdir"
        self.pkg_subdir.mkdir(parents=True, exist_ok=True)
        (self.pkg_subdir / "file.py").write_text("def sub() -> None:\n    pass\n", encoding="utf-8")

        self.test_dir = Path("tests")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        (self.test_dir / "__init__.py").write_text("", encoding="utf-8")
        (self.test_dir / "dummy_test.py").write_text(
            "import unittest\n"
            "from dummy_package import hello\n"
            "from dummy_package.submodule import add\n\n"
            "class DummyTest(unittest.TestCase):\n"
            "    def test_hello(self):\n"
            "        self.assertEqual(hello(), 'world')\n"
            "    def test_add(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n",
            encoding="utf-8"
        )

        self.readme_content = (
            "# Dummy Project\n\n"
            "### Tool structure\n"
            "<details>\n"
            "<summary>Structure</summary>\n"
            "existing structure line 1\n"
            "existing structure line 2\n"
            "</details>\n\n"
            "### Code coverage\n"
            "<details>\n"
            "<summary>Coverage</summary>\n"
            "existing coverage line 1\n"
            "existing coverage line 2\n"
            "</details>\n\n"
            "### Docs\n"
        )
        self.readme_path = Path("README.md")
        self.readme_path.write_text(self.readme_content, encoding="utf-8")

    def tearDown(self) -> None:
        '''
            Clean up temporary project structure after each test case.

            :exceptions: None.
        '''
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        if self.temp_dir.name in sys.path:
            sys.path.remove(self.temp_dir.name)


class ATSCoverageExtraTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSCoverageExtraTestCase with extra test cases.
        Tests single file trees, RST updates, and index coverage CSV updates.

        It defines:

            :attributes: None.
            :methods:
                | test_generate_tree_lines_single_file_success - Test tree generation with single file.
                | test_generate_tree_lines_single_file_non_dir - Test tree generation with single file when not a directory.
                | test_update_structure_rst - Test update structure with RST file format.
                | test_update_structure_rst_framework - Test update structure with RST framework structure.
                | test_update_index_coverage - Test index coverage CSV updating.
                | test_update_index_coverage_os_error - Test index coverage handling of OSError.
                | test_load_report_os_error - Test load report handling of OSError.
                | test_update_readme_os_error - Test update readme handling of OSError.
                | test_update_structure_read_os_error - Test update structure read handling of OSError.
                | test_update_structure_write_os_error - Test update structure write handling of OSError.
                | test_main_script_success - Test executing ats_coverage.py as __main__ with success.
                | test_main_script_failure_load_report - Test executing ats_coverage.py as __main__ with load report failure.
                | test_main_script_failure_run_coverage - Test executing ats_coverage.py as __main__ with run coverage raising TypeError.
                | test_run_tests_and_collect - Test _run_tests_and_collect helper function.
                | test_run_coverage_mocked - Test run_coverage with mocked Coverage class.
                | test_main_script_success_run_path - Test executing ats_coverage.py as __main__ successfully via run_path.
    '''

    def test_generate_tree_lines_single_file_success(self) -> None:
        '''
            Test tree generation with single file.

            :exceptions: None.
        '''
        dummy_dir = Path("dummy_dir")
        dummy_dir.mkdir(parents=True, exist_ok=True)
        (dummy_dir / "dummy_file.py").write_text("# dummy", encoding="utf-8")
        lines, dirs, files = generate_tree_lines("dummy_dir")
        self.assertEqual(lines, ["    dummy_dir/\n", "         └── dummy_file.py\n"])
        self.assertEqual(dirs, 1)
        self.assertEqual(files, 1)

    def test_generate_tree_lines_single_file_non_dir(self) -> None:
        '''
            Test tree generation with single file when not a directory.

            :exceptions: None.
        '''
        file_path = Path("dummy_file.py")
        file_path.write_text("# dummy", encoding="utf-8")
        lines, dirs, files = generate_tree_lines("dummy_file")
        self.assertEqual(lines, ["    dummy_file.py\n"])
        self.assertEqual(dirs, 0)
        self.assertEqual(files, 1)

    def test_update_structure_rst(self) -> None:
        '''
            Test update structure with RST file format.

            :exceptions: None.
        '''
        rst_path = Path("index.rst")
        rst_content = (
            "Some header\n\n"
            "Tool structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n"
        )
        rst_path.write_text(rst_content, encoding="utf-8")
        update_structure("dummy_package", "index.rst")

        updated_rst = rst_path.read_text(encoding="utf-8")
        self.assertIn("dummy_package/", updated_rst)
        self.assertIn("Next Section", updated_rst)

    def test_update_structure_rst_framework(self) -> None:
        '''
            Test update structure with RST framework structure.

            :exceptions: None.
        '''
        rst_path = Path("index.rst")
        rst_content = (
            "Some header\n\n"
            "Framework structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n"
        )
        rst_path.write_text(rst_content, encoding="utf-8")
        update_structure("dummy_package", "index.rst")

        updated_rst = rst_path.read_text(encoding="utf-8")
        self.assertIn("dummy_package/", updated_rst)
        self.assertIn("Next Section", updated_rst)

    def test_update_index_coverage(self) -> None:
        '''
            Test index coverage CSV updating.

            :exceptions: None.
        '''
        run_coverage("dummy_package")
        report_file = "dummy_package.json"
        report_data = load_report(report_file)

        report_data["files"]["/some/other/file.py"] = {
            "summary": {
                "num_statements": 10,
                "missing_lines": 0,
                "percent_covered_display": "100"
            }
        }

        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        csv_path = "docs/source/coverage_table.csv"

        update_index_coverage(report_data, csv_path=csv_path)
        self.assertTrue(Path(csv_path).exists())

        csv_content = Path(csv_path).read_text(encoding="utf-8")
        self.assertIn('"Name", "Stmts", "Miss", "Cover"', csv_content)
        self.assertIn('"dummy_package/__init__.py"', csv_content)
        self.assertIn('""', csv_content)

    def test_update_index_coverage_os_error(self) -> None:
        '''
            Test index coverage handling of OSError.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        update_index_coverage(
            {"files": {}, "totals": {"num_statements": "0", "missing_lines": "0", "percent_covered_display": "0"}},
            csv_path=str(docs_dir)
        )

    def test_load_report_os_error(self) -> None:
        '''
            Test load report handling of OSError.

            :exceptions: None.
        '''
        dummy_file = Path("dummy_file.json")
        dummy_file.write_text("{}", encoding="utf-8")
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            result = load_report(str(dummy_file))
            self.assertEqual(result, {})

    def test_update_readme_os_error(self) -> None:
        '''
            Test update readme handling of OSError.

            :exceptions: None.
        '''
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            update_readme({"files": {}})

    def test_update_structure_read_os_error(self) -> None:
        '''
            Test update structure read handling of OSError.

            :exceptions: None.
        '''
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            update_structure("dummy_package")

    def test_update_structure_write_os_error(self) -> None:
        '''
            Test update structure write handling of OSError.

            :exceptions: None.
        '''
        original_open = open
        def mock_open_func(file, mode='r', *args, **kwargs):
            if 'w' in mode:
                raise OSError("Mocked write error")
            return original_open(file, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=mock_open_func):
            update_structure("dummy_package")

    def test_main_script_success(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with success.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            ".. Tool structure\n"
            ".. details:: Structure\n"
            "existing rst line\n"
            ".. end details\n",
            encoding="utf-8"
        )
        res = subprocess.run(["python3", SCRIPT_PATH, "dummy_package"])
        self.assertEqual(res.returncode, 0)

    def test_main_script_failure_load_report(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with load report failure.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            ".. Tool structure\n"
            ".. details:: Structure\n"
            "existing rst line\n"
            ".. end details\n",
            encoding="utf-8"
        )
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with patch("ats_updater.load_report", return_value={}):
                with self.assertRaises(SystemExit) as cm:
                    run_path(SCRIPT_PATH, run_name="__main__")
                self.assertEqual(cm.exception.code, 129)

    def test_main_script_failure_run_coverage(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with run coverage raising TypeError.

            :exceptions: None.
        '''
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with patch("ats_coverage.run_coverage", side_effect=TypeError("Mocked error")):
                with self.assertRaises(SystemExit) as cm:
                    run_path(SCRIPT_PATH, run_name="__main__")
                self.assertEqual(cm.exception.code, 128)

    def test_run_tests_and_collect(self) -> None:
        '''
            Test _run_tests_and_collect helper function.

            :exceptions: None.
        '''
        _run_tests_and_collect("dummy_package")

    def test_run_coverage_mocked(self) -> None:
        '''
            Test run_coverage with mocked Coverage class.

            :exceptions: None.
        '''
        import ats_coverage

        with patch("ats_coverage.check_exists") as mock_check, \
             patch("ats_coverage.Coverage") as mock_cov, \
             patch("ats_coverage._run_tests_and_collect") as mock_run:
            
            mock_instance = MagicMock()
            mock_cov.return_value = mock_instance

            ats_coverage.run_coverage("dummy_package")

            mock_check.assert_called_once()
            mock_cov.assert_called_once_with(
                source=["dummy_package"],
                config_file=".coveragerc",
                data_file=".coverage.dummy_package"
            )
            mock_instance.start.assert_called_once()
            mock_run.assert_called_once_with("dummy_package")
            mock_instance.stop.assert_called_once()
            mock_instance.save.assert_called_once()
            mock_instance.report.assert_called_once()
            mock_instance.json_report.assert_called_once_with(outfile="dummy_package.json")
            mock_instance.xml_report.assert_called_once_with(outfile="dummy_package.xml")
            mock_instance.html_report.assert_called_once_with(directory="htmlcov")

    def test_main_script_success_run_path(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ successfully.

            :exceptions: None.
        '''
        readme_path = Path("README.md")
        readme_path.write_text(self.readme_content, encoding="utf-8")

        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            "Some header\n\n"
            "Tool structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n",
            encoding="utf-8"
        )
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with self.assertRaises(SystemExit) as cm:
                run_path(SCRIPT_PATH, run_name="__main__")
            self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
