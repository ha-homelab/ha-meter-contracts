"""Source distributions retain the inputs needed by the shipped release guide."""

import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SourceDistributionTests(unittest.TestCase):
    def test_release_guide_and_documentation_inputs_are_shipped(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-m", "build", "--sdist", "--no-isolation",
                 "--outdir", directory, str(ROOT)],
                capture_output=True, text=True, timeout=60, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            archives = list(Path(directory).glob("*.tar.gz"))
            self.assertEqual(len(archives), 1)
            with tarfile.open(archives[0], "r:gz") as archive:
                files = {
                    member.name.split("/", 1)[1]: member
                    for member in archive.getmembers()
                    if member.isfile() and "/" in member.name
                }
                for name in (
                    "RELEASING.md", ".github/workflows/check.yml",
                    "docs/languages.json", "docs/translations.json",
                    "requirements-ci.in", "requirements-ci.txt",
                ):
                    with self.subTest(name=name):
                        self.assertIn(name, files)
                        self.assertEqual(archive.extractfile(files[name]).read(),
                                         (ROOT / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
