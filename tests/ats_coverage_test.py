# -*- coding: UTF-8 -*-

'''
Module
    ats_coverage_test.py
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
    Defines test cases for ats_coverage.py.
Execute
    python3 -m unittest discover -s tests -p '*_test.py'
'''

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Ensure parent directory is in sys.path to import ats_coverage
sys.path.append(str(Path(__file__).parent.parent))


class ATSCoverageTestCase(unittest.TestCase):
    '''
        Defines class ATSCoverageTestCase with test cases.
        Tests the functions in ats_coverage.py.
    '''

    def setUp(self) -> None:
        '''Set up temporary project structure before each test case.'''
        self.old_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

        # Clear any cached imports from previous runs
        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or name.startswith("dummy_test") or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)

        # Create dummy package with a subdirectory to cover _build_tree directories traversal
        self.pkg_dir = Path("dummy_package")
        self.pkg_dir.mkdir()
        (self.pkg_dir / "__init__.py").write_text("def hello() -> str:\n    return 'world'\n", encoding="utf-8")
        (self.pkg_dir / "submodule.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")
        
        self.pkg_subdir = self.pkg_dir / "subdir"
        self.pkg_subdir.mkdir()
        (self.pkg_subdir / "file.py").write_text("def sub() -> None:\n    pass\n", encoding="utf-8")

        # Create dummy test directory and test
        self.test_dir = Path("tests")
        self.test_dir.mkdir()
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

        # Create dummy README.md with required tags and some inside content to trigger replace_mode continue blocks
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
        '''Clean up temporary project structure after each test case.'''
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

        # Clean up any loaded dummy modules to prevent leaking to other tests
        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or name.startswith("dummy_test") or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)

    def test_find_root_package(self) -> None:
        '''Test that find_root_package resolves the root package folder.'''
        from ats_coverage import find_root_package

        submodule_path = str((self.pkg_dir / "submodule.py").resolve())
        root_package = find_root_package(submodule_path)
        self.assertIsNotNone(root_package)
        self.assertEqual(root_package.name, "dummy_package")

    def test_run_and_load_coverage(self) -> None:
        '''Test running coverage and loading the generated report.'''
        from ats_coverage import run_coverage, load_report

        report_file = run_coverage("dummy_package")
        self.assertTrue(Path(report_file).exists())
        self.assertEqual(report_file, "dummy_package_coverage.json")

        report_data = load_report(report_file)
        self.assertIn("files", report_data)
        self.assertIn("totals", report_data)

    def test_update_readme_and_structure(self) -> None:
        '''Test that README.md is updated correctly with coverage and structure.'''
        from ats_coverage import run_coverage, load_report, update_readme, update_structure

        report_file = run_coverage("dummy_package")
        report_data = load_report(report_file)

        # Mock a file outside of the root package to trigger fallback path module name resolution
        report_data["files"]["/some/other/file.py"] = {
            "summary": {
                "num_statements": 10,
                "missing_lines": 0,
                "percent_covered_display": "100"
            }
        }

        update_readme(report_data)
        update_structure("dummy_package")

        updated_readme = self.readme_path.read_text(encoding="utf-8")
        
        # Verify coverage table is inserted
        self.assertIn("| Name | Stmts | Miss | Cover |", updated_readme)
        self.assertIn("dummy_package/__init__.py", updated_readme)
        self.assertIn("file.py", updated_readme) # fallback module name
        
        # Verify structure tree is inserted
        self.assertIn("dummy_package/", updated_readme)
        self.assertIn("submodule.py", updated_readme)
        self.assertIn("subdir/", updated_readme) # subdirectory traverse check

    def test_generate_tree_lines_single_file(self) -> None:
        '''Test that generate_tree_lines handles single file scripts correctly.'''
        from ats_coverage import generate_tree_lines

        # Test with a single file (like dummy_package/__init__.py)
        file_path = "dummy_package/__init__"
        lines, num_dirs, num_files = generate_tree_lines(file_path)
        self.assertEqual(num_dirs, 0)
        self.assertEqual(num_files, 1)
        self.assertIn("__init__.py", lines[0])

    def test_generate_tree_lines_missing(self) -> None:
        '''Test that generate_tree_lines raises ATSFileError on missing file/folder.'''
        from ats_coverage import generate_tree_lines
        from ats_utilities.exceptions.ats_file_error import ATSFileError

        with self.assertRaises(ATSFileError):
            generate_tree_lines("nonexistent_path")

    def test_missing_readme_markers(self) -> None:
        '''Test that update functions skip gently if markers are missing.'''
        from ats_coverage import run_coverage, load_report, update_readme, update_structure

        # Write README without markers
        self.readme_path.write_text("# Just a Title\n", encoding="utf-8")

        report_file = run_coverage("dummy_package")
        report_data = load_report(report_file)

        # Should not raise exception, just log and exit
        update_readme(report_data)
        update_structure("dummy_package")

        updated_readme = self.readme_path.read_text(encoding="utf-8")
        self.assertEqual(updated_readme, "# Just a Title\n")

    def test_run_coverage_invalid_type(self) -> None:
        '''Test that run_coverage raises ATSTypeError on invalid type.'''
        from ats_coverage import run_coverage
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            run_coverage(123)

    def test_run_coverage_missing_package(self) -> None:
        '''Test that run_coverage raises ATSFileError on missing package.'''
        from ats_coverage import run_coverage
        from ats_utilities.exceptions.ats_file_error import ATSFileError
        with self.assertRaises(ATSFileError):
            run_coverage("nonexistent_package")

    def test_load_report_invalid_type(self) -> None:
        '''Test that load_report raises ATSTypeError on invalid type.'''
        from ats_coverage import load_report
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            load_report(123)

    def test_load_report_missing_file(self) -> None:
        '''Test that load_report raises ATSFileError on missing file.'''
        from ats_coverage import load_report
        from ats_utilities.exceptions.ats_file_error import ATSFileError
        with self.assertRaises(ATSFileError):
            load_report("nonexistent_file.json")

    def test_find_root_package_invalid_type(self) -> None:
        '''Test that find_root_package raises ATSTypeError on invalid type.'''
        from ats_coverage import find_root_package
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            find_root_package(123)

    def test_update_readme_invalid_type(self) -> None:
        '''Test that update_readme raises ATSTypeError on invalid type.'''
        from ats_coverage import update_readme
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            update_readme(123)

    def test_update_structure_invalid_type(self) -> None:
        '''Test that update_structure raises ATSTypeError on invalid type.'''
        from ats_coverage import update_structure
        from ats_utilities.exceptions.ats_type_error import ATSTypeError
        with self.assertRaises(ATSTypeError):
            update_structure(123)

    def test_update_readme_missing_file(self) -> None:
        '''Test that update_readme skips when README.md is missing.'''
        from ats_coverage import update_readme
        self.readme_path.unlink()
        update_readme({"files": {}})  # Should skip without error

    def test_update_structure_missing_file(self) -> None:
        '''Test that update_structure skips when README.md is missing.'''
        from ats_coverage import update_structure
        self.readme_path.unlink()
        update_structure("dummy_package")  # Should skip without error

    def test_update_readme_missing_tags(self) -> None:
        '''Test that update_readme skips when summary/details tags are missing.'''
        from ats_coverage import update_readme
        # Marker is present but tags are missing
        self.readme_path.write_text("### Code coverage\n", encoding="utf-8")
        update_readme({"files": {}})  # Should skip without error

    def test_update_structure_missing_tags(self) -> None:
        '''Test that update_structure skips when summary/details tags are missing.'''
        from ats_coverage import update_structure
        # Marker is present but tags are missing
        self.readme_path.write_text("### Tool structure\n", encoding="utf-8")
        update_structure("dummy_package")  # Should skip without error


if __name__ == '__main__':
    unittest.main()
