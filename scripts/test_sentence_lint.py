#!/usr/bin/env python3
"""Unit tests for sentence_lint.py.

Run with plain Python (stdlib only):

    python3 scripts/test_sentence_lint.py

Beyond the basic one-sentence-per-line reflow, these lock in that the linter is
*spoiler-aware*: the `:::spoiler`/`:::details` opener, the bare `:::` closer, and
`:::{include}:::` shortcodes must stay on their own line. A reflow that merged a
summary onto the first body sentence, or detached the closing `:::`, would
corrupt the block for the site's `expand_spoilers` parser (an unterminated block
renders as raw text), so it is guarded here.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sentence_lint as sl


def reflow(text: str) -> str:
    return sl.reflow(text)


class ReflowBasics(unittest.TestCase):
    def test_splits_two_sentences_onto_two_lines(self):
        self.assertEqual(reflow("One two. Three four."), "One two.\nThree four.")

    def test_is_idempotent(self):
        once = reflow("A first sentence. A second sentence.")
        self.assertEqual(once, reflow(once))

    def test_leaves_fenced_code_untouched(self):
        src = "```python\nx = 1; y = 2  # not prose. do not split.\n```"
        self.assertEqual(reflow(src), src)

    def test_leaves_display_math_untouched(self):
        src = "\\[\na = b. c = d.\n\\]"
        self.assertEqual(reflow(src), src)

    def test_image_caption_with_math_bracket_not_split(self):
        # A figure caption whose alt text contains a `]` (a math interval like
        # $[0,1]$) must still be masked as one image and never reflowed at the
        # sentence boundary inside the alt text. Regression for the image-mask
        # regex under-matching on `]`.
        src = ("![Left: it keeps a probability in $[0,1]$. "
               "Right: the offset flips the ranking.](../assets/figures/x.svg \"fig:x\")")
        self.assertEqual(reflow(src), src)


class SpoilerAwareness(unittest.TestCase):
    def test_opener_not_merged_with_first_sentence(self):
        # No blank line between the opener and the body — the linter must NOT
        # glue the summary onto the first sentence.
        src = ":::spoiler Show the derivation\nFirst sentence. Second sentence.\n:::"
        out = reflow(src)
        lines = out.split("\n")
        self.assertEqual(lines[0], ":::spoiler Show the derivation")
        self.assertIn("First sentence.", lines)
        self.assertIn("Second sentence.", lines)
        # body sentences are still split one-per-line
        self.assertEqual(lines[1], "First sentence.")
        self.assertEqual(lines[2], "Second sentence.")

    def test_closer_stays_on_its_own_line(self):
        src = ":::spoiler S\nOnly sentence here.\n:::"
        out = reflow(src)
        self.assertTrue(out.endswith("\n:::"), out)
        self.assertIn("\nOnly sentence here.\n", "\n" + out + "\n")

    def test_details_alias_and_bare_marker_preserved(self):
        src = ":::details More\nBody one. Body two.\n:::"
        out = reflow(src).split("\n")
        self.assertEqual(out[0], ":::details More")
        self.assertEqual(out[-1], ":::")

    def test_summary_with_inline_math_preserved(self):
        src = ":::spoiler Show why the sum is $a/(1-r)$\nWrite the sum. Simplify.\n:::"
        out = reflow(src).split("\n")
        self.assertEqual(out[0], ":::spoiler Show why the sum is $a/(1-r)$")

    def test_idempotent_on_spoiler_block(self):
        src = ":::spoiler S\nOne. Two. Three.\n:::"
        once = reflow(src)
        self.assertEqual(once, reflow(once))
        # exactly one opener and one closer survive
        self.assertEqual(once.count(":::spoiler"), 1)
        self.assertEqual([l for l in once.split("\n")].count(":::"), 1)

    def test_include_shortcode_not_reflowed(self):
        src = "Some prose sentence.\n:::{course-policies.md}:::\nMore prose here."
        out = reflow(src)
        self.assertIn(":::{course-policies.md}:::", out.split("\n"))


if __name__ == "__main__":
    unittest.main()
