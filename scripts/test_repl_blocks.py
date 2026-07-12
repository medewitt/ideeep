#!/usr/bin/env python3
"""Unit tests for repl_blocks.py.

Run with plain Python (stdlib only — the tests exec trivial statements and mock
the REPL launchers, so neither the scientific dependencies nor IPython are
needed):

    python3 scripts/test_repl_blocks.py

These lock in the block selection semantics (--block / --through / --none), the
--none flag added for the editor "send block to REPL" integration (open a REPL
in the page's environment without running any blocks), and the REPL launcher's
IPython-with-code.interact-fallback behavior.
"""
import io
import os
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repl_blocks as rb


def doc(*lines: str) -> str:
    return "\n".join(lines) + "\n"


PAGE = doc(
    "# Page",
    "",
    "```python",
    "a = 1",
    "```",
    "",
    "prose between blocks",
    "",
    "```python",
    "# no-run",
    "b = 2",
    "```",
    "",
    "```r",
    "x <- 1",
    "```",
)


class CollectBlocksTests(unittest.TestCase):
    def test_collects_python_blocks_in_order(self):
        blocks = rb.collect_blocks(PAGE, "python", respect_directives=False)
        self.assertEqual(len(blocks), 2)
        self.assertIn("a = 1", blocks[0])
        self.assertIn("b = 2", blocks[1])

    def test_respect_directives_drops_no_run(self):
        blocks = rb.collect_blocks(PAGE, "python", respect_directives=True)
        self.assertEqual(len(blocks), 1)
        self.assertIn("a = 1", blocks[0])

    def test_other_language(self):
        blocks = rb.collect_blocks(PAGE, "r", respect_directives=False)
        self.assertEqual(len(blocks), 1)
        self.assertIn("x <- 1", blocks[0])


class SelectTests(unittest.TestCase):
    BLOCKS = ["one", "two", "three"]

    def test_default_selects_all_numbered_from_one(self):
        self.assertEqual(rb.select(self.BLOCKS, None, None),
                         [(1, "one"), (2, "two"), (3, "three")])

    def test_only(self):
        self.assertEqual(rb.select(self.BLOCKS, 2, None), [(2, "two")])

    def test_through(self):
        self.assertEqual(rb.select(self.BLOCKS, None, 2),
                         [(1, "one"), (2, "two")])

    def test_empty_input(self):
        self.assertEqual(rb.select([], None, None), [])


class LaunchReplTests(unittest.TestCase):
    def test_prefers_ipython_when_importable(self):
        fake = types.ModuleType("IPython")
        fake.start_ipython = mock.MagicMock()
        ns = {"a": 1}
        with mock.patch.dict(sys.modules, {"IPython": fake}):
            with mock.patch("code.interact") as interact:
                rb.launch_repl(ns, total=1)
        fake.start_ipython.assert_called_once()
        self.assertIs(fake.start_ipython.call_args.kwargs["user_ns"], ns)
        interact.assert_not_called()

    def test_falls_back_to_code_interact(self):
        ns = {"a": 1}
        # sys.modules[name] = None makes `import IPython` raise ImportError.
        with mock.patch.dict(sys.modules, {"IPython": None}):
            with mock.patch("code.interact") as interact:
                rb.launch_repl(ns, total=1)
        interact.assert_called_once()
        self.assertIs(interact.call_args.kwargs["local"], ns)

    def test_banner_lists_scope(self):
        err = io.StringIO()
        with mock.patch.dict(sys.modules, {"IPython": None}):
            with mock.patch("code.interact"):
                with mock.patch.object(sys, "stderr", err):
                    rb.launch_repl({"alpha": 1, "__hidden": 2}, total=3)
        self.assertIn("3 block(s) loaded", err.getvalue())
        self.assertIn("alpha", err.getvalue())
        self.assertNotIn("__hidden", err.getvalue())


class RunPythonTests(unittest.TestCase):
    def test_blocks_share_a_namespace_and_repl_gets_it(self):
        with mock.patch.object(rb, "launch_repl") as launch:
            with mock.patch.object(sys, "stderr", io.StringIO()):
                rc = rb.run_python([(1, "a = 1"), (2, "b = a + 1")],
                                   total=2, open_repl=True)
        self.assertEqual(rc, 0)
        ns = launch.call_args.args[0]
        self.assertEqual(ns["b"], 2)
        # the banner reflects the blocks actually run, not the page total
        self.assertEqual(launch.call_args.args[1], 2)

    def test_repl_banner_counts_loaded_not_page_total(self):
        with mock.patch.object(rb, "launch_repl") as launch:
            with mock.patch.object(sys, "stderr", io.StringIO()):
                rb.run_python([], total=2, open_repl=True)
        self.assertEqual(launch.call_args.args[1], 0)

    def test_no_repl_skips_launch(self):
        with mock.patch.object(rb, "launch_repl") as launch:
            with mock.patch.object(sys, "stderr", io.StringIO()):
                rb.run_python([(1, "a = 1")], total=1, open_repl=False)
        launch.assert_not_called()


class RunExternalTests(unittest.TestCase):
    def test_banner_counts_loaded_not_page_total(self):
        err = io.StringIO()
        with mock.patch.object(rb.inj, "toolchain_available", lambda lang: True):
            with mock.patch.object(rb.subprocess, "run") as run:
                run.return_value.returncode = 0
                with mock.patch.object(sys, "stderr", err):
                    rc = rb.run_external("r", [], total=3, open_repl=True)
        self.assertEqual(rc, 0)
        self.assertIn("0 R block(s) preloaded", err.getvalue())


class MainNoneFlagTests(unittest.TestCase):
    def run_main(self, *argv):
        with mock.patch.object(sys, "argv", ["repl_blocks.py", *argv]):
            return rb.main()

    def page(self, text):
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8")
        self.addCleanup(os.unlink, tmp.name)
        tmp.write(text)
        tmp.close()
        return tmp.name

    def test_none_runs_no_blocks_and_opens_repl(self):
        path = self.page(PAGE)
        with mock.patch.object(rb, "run_python", return_value=0) as run:
            rc = self.run_main(path, "--none")
        self.assertEqual(rc, 0)
        selected, total = run.call_args.args[0], run.call_args.args[1]
        self.assertEqual(selected, [])
        self.assertEqual(total, 2)          # numbering still reflects the page
        self.assertTrue(run.call_args.args[2])   # open_repl

    def test_none_accepts_page_with_zero_blocks(self):
        path = self.page(doc("# prose only", "", "no code here"))
        with mock.patch.object(rb, "run_python", return_value=0) as run:
            rc = self.run_main(path, "--none")
        self.assertEqual(rc, 0)
        self.assertEqual(run.call_args.args[0], [])

    def test_without_none_zero_blocks_is_still_an_error(self):
        path = self.page(doc("# prose only"))
        with mock.patch.object(sys, "stderr", io.StringIO()):
            rc = self.run_main(path)
        self.assertEqual(rc, 1)

    def test_none_is_exclusive_with_block_and_through(self):
        path = self.page(PAGE)
        for extra in (["--block", "1"], ["--through", "1"]):
            with mock.patch.object(sys, "stderr", io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    self.run_main(path, "--none", *extra)
            self.assertEqual(ctx.exception.code, 2)

    def test_block_and_through_still_exclusive(self):
        path = self.page(PAGE)
        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_main(path, "--block", "1", "--through", "2")

    def test_block_zero_still_rejected(self):
        path = self.page(PAGE)
        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                self.run_main(path, "--block", "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
