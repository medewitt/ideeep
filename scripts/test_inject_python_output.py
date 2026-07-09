#!/usr/bin/env python3
"""Unit tests for inject_python_output.py.

Run with plain Python (stdlib only — the tests exec trivial print statements,
so none of the heavy scientific dependencies the injector declares for *content*
blocks are needed):

    python3 scripts/test_inject_python_output.py

These lock in both the injection behavior and the content-hash caching added for
issue #68: the fingerprint must depend only on the ordered python code blocks
(not prose, not the injected output), and a warm cache must let a page be
skipped while a genuine code change still forces re-execution.
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inject_python_output as inj

START, END = inj.START, inj.END


def doc(*blocks: str) -> str:
    """Assemble a Markdown doc from raw block strings."""
    return "\n".join(blocks)


class ProcessTests(unittest.TestCase):
    def test_injects_stdout_between_markers(self):
        src = doc("# Page", "", "```python", "print('hello')", "```", "")
        out = inj.process(src)
        self.assertIn(START, out)
        self.assertIn(END, out)
        self.assertIn("hello", out)
        # injected output sits after the closing fence, wrapped in a text block
        self.assertRegex(out, r"```\n\n" + inj_esc(START) + r"\n```text\nhello\n```\n" + inj_esc(END))

    def test_idempotent(self):
        src = doc("```python", "print(2 + 2)", "```")
        once = inj.process(src)
        twice = inj.process(once)
        self.assertEqual(once, twice)
        self.assertEqual(once.count(START), 1)

    def test_no_run_skips_execution(self):
        src = doc("```python", "# no-run", "print('should not appear')", "```")
        out = inj.process(src)
        self.assertNotIn(START, out)
        self.assertNotIn("should not appear\n```text", out)

    def test_erroring_block_injects_nothing(self):
        src = doc("```python", "raise ValueError('boom')", "```")
        out = inj.process(src)
        self.assertNotIn(START, out)

    def test_silent_block_injects_nothing(self):
        src = doc("```python", "x = 1 + 1  # no print", "```")
        self.assertNotIn(START, inj.process(src))

    def test_shared_namespace_across_blocks(self):
        src = doc("```python", "shared = 7", "```", "",
                  "```python", "print(shared * 6)", "```")
        out = inj.process(src)
        self.assertIn("42", out)

    def test_output_is_truncated(self):
        body = "\n".join(f"print({i})" for i in range(inj.MAX_LINES + 5))
        src = doc("```python", body, "```")
        out = inj.process(src)
        self.assertIn("... (output truncated)", out)
        # exactly MAX_LINES numeric lines are kept before the truncation notice
        shown = out.split("```text\n", 1)[1].split("\n```", 1)[0].splitlines()
        self.assertEqual(len(shown), inj.MAX_LINES + 1)  # +1 for the notice

    def test_non_python_fence_untouched(self):
        src = doc("```r", "print('r is never executed')", "```")
        self.assertEqual(inj.process(src), src)

    def test_strip_injected_round_trip(self):
        src = doc("```python", "print('x')", "```")
        injected = inj.process(src)
        stripped = "\n".join(inj.strip_injected(injected.split("\n")))
        self.assertEqual(stripped, src)


class FingerprintTests(unittest.TestCase):
    def test_extract_block_sources_orders_and_excludes_output(self):
        src = inj.process(doc("```python", "print('a')", "```", "",
                              "```python", "print('b')", "```"))
        self.assertEqual(inj.extract_block_sources(src), ["print('a')", "print('b')"])

    def test_fingerprint_ignores_prose(self):
        a = doc("Some prose.", "```python", "print(1)", "```")
        b = doc("Totally different prose here.", "```python", "print(1)", "```")
        self.assertEqual(inj.page_fingerprint(a), inj.page_fingerprint(b))

    def test_fingerprint_ignores_injected_output(self):
        src = doc("```python", "print(1)", "```")
        self.assertEqual(inj.page_fingerprint(src),
                         inj.page_fingerprint(inj.process(src)))

    def test_fingerprint_changes_with_code(self):
        a = doc("```python", "print(1)", "```")
        b = doc("```python", "print(2)", "```")
        self.assertNotEqual(inj.page_fingerprint(a), inj.page_fingerprint(b))

    def test_fingerprint_tracks_no_run_marker(self):
        a = doc("```python", "print(1)", "```")
        b = doc("```python", "# no-run", "print(1)", "```")
        self.assertNotEqual(inj.page_fingerprint(a), inj.page_fingerprint(b))

    def test_fingerprint_tracks_block_order(self):
        a = doc("```python", "print(1)", "```", "", "```python", "print(2)", "```")
        b = doc("```python", "print(2)", "```", "", "```python", "print(1)", "```")
        self.assertNotEqual(inj.page_fingerprint(a), inj.page_fingerprint(b))


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._orig_cache_path = inj.CACHE_PATH
        inj.CACHE_PATH = os.path.join(self.tmp.name, "cache.json")
        self.addCleanup(lambda: setattr(inj, "CACHE_PATH", self._orig_cache_path))

    def test_cache_roundtrip(self):
        files = {"content/math/a.md": "deadbeef", "content/math/b.md": "cafef00d"}
        inj.save_cache(files)
        self.assertEqual(inj.load_cache(), files)

    def test_load_missing_cache_returns_empty(self):
        self.assertEqual(inj.load_cache(), {})

    def test_load_rejects_wrong_version(self):
        with open(inj.CACHE_PATH, "w") as f:
            f.write('{"version": 999, "files": {"x": "y"}}')
        self.assertEqual(inj.load_cache(), {})

    def test_load_rejects_corrupt_json(self):
        with open(inj.CACHE_PATH, "w") as f:
            f.write("{not json")
        self.assertEqual(inj.load_cache(), {})

    def _write_page(self, name, code):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w") as f:
            f.write(doc("# Page", "", "```python", code, "```", ""))
        return path

    def _run(self, *argv):
        old = sys.argv
        sys.argv = ["inject", *argv]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                return inj.main()
        finally:
            sys.argv = old

    def test_write_then_check_is_cached_and_passes(self):
        page = self._write_page("p.md", "print('cached output')")
        self.assertEqual(self._run("--write", page), 0)
        with open(page) as f:
            self.assertIn("cached output", f.read())
        # warm --check: fingerprint matches cache, page skipped, gate green
        self.assertEqual(self._run("--check", page), 0)

    def test_prose_edit_does_not_invalidate_cache(self):
        page = self._write_page("p.md", "print('x')")
        self._run("--write", page)
        with open(page) as f:
            body = f.read()
        with open(page, "w") as f:
            f.write("A new prose line.\n" + body)
        # code unchanged -> still cached -> check passes without re-running
        self.assertEqual(self._run("--check", page), 0)

    def test_code_edit_forces_recheck_and_fails_when_stale(self):
        page = self._write_page("p.md", "print('one')")
        self._run("--write", page)
        with open(page) as f:
            body = f.read()
        # change the code but leave the now-stale injected output in place
        with open(page, "w") as f:
            f.write(body.replace("print('one')", "print('two')"))
        # fingerprint changes -> cache miss -> re-run -> detects stale output
        self.assertEqual(self._run("--check", page), 1)

    def test_writing_subset_preserves_other_entries(self):
        p1 = self._write_page("p1.md", "print('one')")
        p2 = self._write_page("p2.md", "print('two')")
        self._run("--write", p1, p2)
        self.assertEqual(len(inj.load_cache()), 2)
        # rewriting only p1 must not drop p2's fingerprint
        self._run("--write", p1)
        self.assertEqual(len(inj.load_cache()), 2)


def inj_esc(s: str) -> str:
    import re
    return re.escape(s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
