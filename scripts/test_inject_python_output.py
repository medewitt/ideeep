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
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inject_python_output as inj

START, END = inj.START, inj.END
R_START, R_END = inj.R_START, inj.R_END
JULIA_START, JULIA_END = inj.JULIA_START, inj.JULIA_END


def force_available(*langs):
    """Patch so the named opt-in languages report their toolchain present."""
    return mock.patch.object(
        inj, "toolchain_available", lambda lang: lang in langs or lang == "python")


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

    def test_illustrative_r_block_untouched(self):
        # An R block with no `# run` directive is illustrative -> never runs,
        # even with the toolchain forced present.
        src = doc("```r", "print('r is illustrative by default')", "```")
        with force_available("r"):
            self.assertEqual(str(inj.process(src)), src)

    def test_incidental_run_substring_does_not_trigger(self):
        # `# runs n times` contains "# run" but is not the directive line.
        src = doc("```r", "total <- 0  # runs n times", "```")
        with force_available("r"), \
                mock.patch.object(inj, "run_language_blocks") as runner:
            out = str(inj.process(src))
        runner.assert_not_called()
        self.assertEqual(out, src)

    def test_strip_injected_round_trip(self):
        src = doc("```python", "print('x')", "```")
        injected = inj.process(src)
        stripped = "\n".join(inj.strip_injected(injected.split("\n")))
        self.assertEqual(stripped, str(src))


class RunDirectiveTests(unittest.TestCase):
    """Opt-in R/Julia execution, with the interpreter process mocked so the
    core orchestration is exercised on every machine (no R/Julia needed)."""

    def test_r_run_directive_injects_between_r_markers(self):
        src = doc("```r", "# run", "cat('hi from R\\n')", "```")
        with force_available("r"), \
                mock.patch.object(inj, "run_language_blocks",
                                  return_value=["hi from R\n"]):
            out = str(inj.process(src))
        self.assertIn(R_START, out)
        self.assertIn(R_END, out)
        self.assertIn("hi from R", out)
        self.assertNotIn(START, out)                 # not the python markers

    def test_julia_run_directive_injects_between_julia_markers(self):
        src = doc("```julia", "# run", 'println("hi from Julia")', "```")
        with force_available("julia"), \
                mock.patch.object(inj, "run_language_blocks",
                                  return_value=["hi from Julia\n"]):
            out = str(inj.process(src))
        self.assertIn(JULIA_START, out)
        self.assertIn(JULIA_END, out)
        self.assertIn("hi from Julia", out)

    def test_shared_state_blocks_passed_to_runner_in_order(self):
        src = doc("```r", "# run", "x <- 7", "```", "",
                  "```r", "# run", "cat(x * 6)", "```")
        with force_available("r"), \
                mock.patch.object(inj, "run_language_blocks",
                                  return_value=[None, "42"]) as runner:
            out = str(inj.process(src))
        # both runnable blocks handed to a single process, in document order
        (lang, codes), _ = runner.call_args
        self.assertEqual(lang, "r")
        self.assertEqual(codes, ["# run\nx <- 7", "# run\ncat(x * 6)"])
        self.assertIn("42", out)

    def test_error_block_injects_nothing_but_later_block_runs(self):
        src = doc("```r", "# run", "stop('boom')", "```", "",
                  "```r", "# run", "cat('after')", "```")
        with force_available("r"), \
                mock.patch.object(inj, "run_language_blocks",
                                  return_value=[None, "after"]):
            out = str(inj.process(src))
        self.assertEqual(out.count(R_START), 1)      # only the second injects
        self.assertIn("after", out)

    def test_run_directive_in_python_is_noop(self):
        # `# run` is meaningless in python (which runs by default); it must not
        # suppress or alter execution.
        src = doc("```python", "# run", "print('still runs')", "```")
        out = str(inj.process(src))
        self.assertIn(START, out)
        self.assertIn("still runs", out)


class ToolchainMissingTests(unittest.TestCase):
    def setUp(self):
        inj._warned_missing.clear()                  # isolate the per-run warning dedup

    def test_missing_toolchain_leaves_page_unchanged_and_flags_incomplete(self):
        src = doc("```r", "# run", "cat('hi')", "```")
        with mock.patch.object(inj, "toolchain_available", return_value=False), \
                mock.patch.object(inj, "run_language_blocks") as runner, \
                contextlib.redirect_stderr(io.StringIO()) as err:
            page = inj.process(src)
        runner.assert_not_called()                   # never even attempted
        self.assertEqual(str(page), src)             # committed output intact
        self.assertTrue(page.incomplete)
        self.assertIn("Rscript", err.getvalue())     # warned on stderr

    def test_missing_toolchain_preserves_committed_output(self):
        # A page already carrying injected R output keeps it byte-for-byte when
        # the toolchain is absent (markers of an inactive language aren't stripped).
        injected = doc("```r", "# run", "cat('hi')", "```", "",
                       R_START, "```text", "hi", "```", R_END)
        with mock.patch.object(inj, "toolchain_available", return_value=False), \
                contextlib.redirect_stderr(io.StringIO()):
            page = inj.process(injected)
        self.assertEqual(str(page), injected)
        self.assertTrue(page.incomplete)

    def test_runner_failure_flags_incomplete(self):
        # Interpreter present but the process fails/times out -> None wholesale.
        src = doc("```julia", "# run", 'println("x")', "```")
        with force_available("julia"), \
                mock.patch.object(inj, "run_language_blocks", return_value=None), \
                contextlib.redirect_stderr(io.StringIO()):
            page = inj.process(src)
        self.assertEqual(str(page), src)
        self.assertTrue(page.incomplete)


class RunnerParsingTests(unittest.TestCase):
    """run_language_blocks' stdout parsing, with subprocess.run mocked."""

    def _fake_proc(self, stdout, returncode=0):
        return mock.Mock(stdout=stdout, stderr="", returncode=returncode)

    def test_splits_output_per_block_on_sentinel(self):
        b, e = inj.BLOCK_SENTINEL, inj.ERROR_SENTINEL
        stdout = f"prelude\n{b}\nfirst\n{b}\nsecond\n"
        with mock.patch.object(inj.subprocess, "run",
                               return_value=self._fake_proc(stdout)):
            out = inj.run_language_blocks("r", ["a", "b"])
        self.assertEqual(out, ["first\n", "second\n"])

    def test_error_sentinel_marks_block_none(self):
        b, e = inj.BLOCK_SENTINEL, inj.ERROR_SENTINEL
        stdout = f"{b}\n{e}\n{b}\nok\n"
        with mock.patch.object(inj.subprocess, "run",
                               return_value=self._fake_proc(stdout)):
            out = inj.run_language_blocks("r", ["bad", "good"])
        self.assertEqual(out, [None, "ok\n"])

    def test_nonzero_returncode_returns_none(self):
        with mock.patch.object(inj.subprocess, "run",
                               return_value=self._fake_proc("", returncode=1)):
            self.assertIsNone(inj.run_language_blocks("r", ["a"]))

    def test_timeout_returns_none(self):
        import subprocess as sp
        with mock.patch.object(inj.subprocess, "run",
                               side_effect=sp.TimeoutExpired("Rscript", 1)):
            self.assertIsNone(inj.run_language_blocks("r", ["a"]))

    def test_segment_count_mismatch_returns_none(self):
        # Fewer sentinels than blocks (e.g. interpreter died mid-run) -> None.
        stdout = f"{inj.BLOCK_SENTINEL}\nonly one\n"
        with mock.patch.object(inj.subprocess, "run",
                               return_value=self._fake_proc(stdout)):
            self.assertIsNone(inj.run_language_blocks("r", ["a", "b"]))


class MixedLanguageTests(unittest.TestCase):
    def test_idempotent_across_languages(self):
        src = doc("```python", "print('py')", "```", "",
                  "```r", "# run", "cat('r')", "```", "",
                  "```julia", "# run", 'println("jl")', "```")

        def fake_runner(lang, codes):
            return [f"{lang} out\n" for _ in codes]

        with force_available("r", "julia"), \
                mock.patch.object(inj, "run_language_blocks", side_effect=fake_runner):
            once = str(inj.process(src))
            twice = str(inj.process(once))
        self.assertEqual(once, twice)
        for start in (START, R_START, JULIA_START):
            self.assertEqual(once.count(start), 1)

    def test_strip_injected_handles_all_marker_families(self):
        bare = doc("```python", "print('py')", "```", "",
                   "```r", "# run", "cat('r')", "```", "",
                   "```julia", "# run", 'println("jl")', "```")

        def fake_runner(lang, codes):
            return [f"{lang} out\n" for _ in codes]

        with force_available("r", "julia"), \
                mock.patch.object(inj, "run_language_blocks", side_effect=fake_runner):
            injected = str(inj.process(bare))
        stripped = "\n".join(inj.strip_injected(injected.split("\n")))
        self.assertEqual(stripped, bare)


class RealInterpreterSmokeTests(unittest.TestCase):
    """End-to-end against a real interpreter when present (skipped in CI and
    this container, which have neither)."""

    @unittest.skipUnless(shutil.which("Rscript"), "Rscript not installed")
    def test_real_r_shared_state(self):
        src = doc("```r", "# run", "x <- 6", "```", "",
                  "```r", "# run", "cat(x * 7)", "```")
        out = str(inj.process(src))
        self.assertIn("42", out)
        self.assertIn(R_START, out)

    @unittest.skipUnless(shutil.which("julia"), "julia not installed")
    def test_real_julia_output(self):
        src = doc("```julia", "# run", 'println(6 * 7)', "```")
        out = str(inj.process(src))
        self.assertIn("42", out)
        self.assertIn(JULIA_START, out)


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

    def test_fingerprint_tracks_run_toggle(self):
        off = doc("```r", "cat('x')", "```")
        on = doc("```r", "# run", "cat('x')", "```")
        self.assertNotEqual(inj.page_fingerprint(off), inj.page_fingerprint(on))

    def test_fingerprint_ignores_illustrative_r_edits(self):
        # Editing an R block that never opted in must not invalidate the cache.
        a = doc("Prose.", "```r", "cat('one')", "```")
        b = doc("Prose.", "```r", "cat('a totally different body')", "```")
        self.assertEqual(inj.page_fingerprint(a), inj.page_fingerprint(b))

    def test_fingerprint_distinguishes_r_from_julia(self):
        r = doc("```r", "# run", "cat('x')", "```")
        jl = doc("```julia", "# run", "cat('x')", "```")
        self.assertNotEqual(inj.page_fingerprint(r), inj.page_fingerprint(jl))

    def test_python_only_fingerprint_is_toolchain_independent(self):
        # The value must not depend on whether R/Julia are installed, so a warm
        # cache built on one machine is trusted on another.
        src = doc("```python", "print(1)", "```")
        with mock.patch.object(inj, "toolchain_available", return_value=False):
            missing = inj.page_fingerprint(src)
        with force_available("r", "julia"):
            present = inj.page_fingerprint(src)
        self.assertEqual(missing, present)


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

    def _write_raw(self, name, text):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w") as f:
            f.write(text)
        return path

    def test_missing_toolchain_page_not_cached(self):
        page = self._write_raw(
            "r.md", doc("# Page", "", "```r", "# run", "cat('hi')", "```", ""))
        with mock.patch.object(inj, "toolchain_available", return_value=False), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self._run("--write", page), 0)
        # incomplete page must not be recorded fresh -> re-runs elsewhere
        self.assertNotIn(os.path.normpath(page), inj.load_cache())

    def test_check_passes_when_toolchain_absent(self):
        # A page with committed R output and no toolchain is not "out of date":
        # its markers aren't stripped, so nothing changes.
        page = self._write_raw("r.md", doc(
            "# Page", "", "```r", "# run", "cat('hi')", "```", "",
            R_START, "```text", "hi", "```", R_END, ""))
        with mock.patch.object(inj, "toolchain_available", return_value=False), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self._run("--check", page), 0)


def inj_esc(s: str) -> str:
    import re
    return re.escape(s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
