"""f-string moslik testi (HIGH-001).

PEP 701 (Python 3.12) dan oldin f-string ichida bir xil qo'shtirnoqli satr
ishlatish SyntaxError beradi:

    f"Bearer {os.getenv("API_KEY_REF")}"   # Python <=3.11: SyntaxError

Test bu naqshni topadi. Muammo tuzatilgunga qadar YIQILADI.
"""
import io
import os
import tokenize
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "tests"}


def find_nested_quote_fstrings(src):
    problems = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except Exception:
        return problems
    fs_start = getattr(tokenize, "FSTRING_START", -1)
    fs_end = getattr(tokenize, "FSTRING_END", -1)
    stack = []
    for tok in toks:
        if tok.type == fs_start:
            stack.append(tok.string[-1])
        elif tok.type == fs_end:
            if stack:
                stack.pop()
        elif tok.type == tokenize.STRING and stack:
            s = tok.string
            i = 0
            while i < len(s) and s[i] in "rRbBuUfF":
                i += 1
            if i < len(s) and s[i] == stack[-1]:
                problems.append((tok.start[0], tok.string))
    return problems


class FStringCompatTest(unittest.TestCase):
    def test_no_nested_quote_fstrings(self):
        findings = []
        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(root, name)
                try:
                    src = open(path, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                for line, s in find_nested_quote_fstrings(src):
                    rel = os.path.relpath(path, REPO_ROOT)
                    findings.append(f"{rel}:{line} -> {s}")
        self.assertEqual(
            findings,
            [],
            "Python <=3.11 da SyntaxError beruvchi f-string topildi "
            "(PEP 701). Ichki qo'shtirnoqni boshqasiga almashtiring:\n"
            + "\n".join(findings),
        )


if __name__ == "__main__":
    unittest.main()
