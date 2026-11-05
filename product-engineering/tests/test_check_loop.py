"""Stdlib tests for check_loop.py test-token mapping and plan cleanup. Run: python3 -m unittest discover -s tests"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("check_loop", Path(__file__).resolve().parent.parent / "scripts" / "check_loop.py")
check_loop = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_loop)


class Case(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        check_loop.REPO = self.root

    def tearDown(self):
        self._tmp.cleanup()

    def missing(self, ids, test_text):
        (self.root / "tests").mkdir(exist_ok=True)
        (self.root / "tests" / "a.test.ts").write_text(test_text)
        return check_loop.test_mapping("01", ids, ["tests/a.test.ts"])["missing"]


class TokenMapping(Case):
    def test_sub_token_does_not_match_t32(self):
        self.assertEqual(self.missing(["T3.2"], "it('T32 other', ...)"), ["T3.2"])

    def test_sub_token_matches_dot_or_underscore(self):
        self.assertEqual(self.missing(["T3.2"], "it('T3.2 nav', ...)"), [])
        self.assertEqual(self.missing(["T3.2"], "def test_t3_2_nav(): ..."), [])

    def test_parent_not_satisfied_by_its_sub_token(self):
        self.assertEqual(self.missing(["T3", "T3.1"], "it('T3.1 x', ...)"), ["T3"])

    def test_plain_token_with_numeric_suffix(self):
        self.assertEqual(self.missing(["T3"], "def test_t3_404_page(): ..."), [])
        self.assertEqual(self.missing(["T3"], "def test_t32(): ..."), ["T3"])


class PlanCleanup(Case):
    def plan_errors(self, status):
        d = self.root / "active" / "01-x"
        d.mkdir(parents=True)
        (d / "plan.md").write_text(f"| # | Unit | Type | Serves | Tier | Status |\n| :-- | :-- | :-- | :-- | :-- | :-- |\n| 01 | Skeleton | infra | all | P0 | {status} |\n")
        return check_loop.check_plan(d / "plan.md")["errors"]

    def test_finished_plan_must_move_to_history(self):
        self.assertTrue(any("move this milestone" in e for e in self.plan_errors("done")))

    def test_unfinished_plan_stays(self):
        self.assertFalse(any("move this milestone" in e for e in self.plan_errors("todo")))


if __name__ == "__main__":
    unittest.main()
