from __future__ import annotations

import compileall
import os
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
PYPROJECT = ROOT / "pyproject.toml"


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def check_pyproject() -> None:
    text = _read(PYPROJECT)
    try:
        import tomllib
    except ModuleNotFoundError:
        if not re.search(r'(?m)^name = "adpages-tools"$', text):
            raise AssertionError("pyproject.toml is missing the project name")
        if not re.search(r'(?m)^version = "[^"]+"$', text):
            raise AssertionError("pyproject.toml is missing the project version")
        print("tomllib unavailable; pyproject.toml passed structural fallback check")
        return

    data = tomllib.loads(text)
    if data["project"]["name"] != "adpages-tools":
        raise AssertionError("Unexpected project name")
    if not data["project"]["dependencies"] == []:
        raise AssertionError("Package should remain dependency-free")


def check_compiles() -> None:
    for path in (SRC, TESTS, ROOT / "scripts"):
        if not compileall.compile_dir(path, quiet=1):
            raise AssertionError(f"Python compile failed for {path}")


def check_tests() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(TESTS)],
        cwd=ROOT,
        env=env,
        check=True,
    )


def check_privacy_notes() -> None:
    readme = _read(ROOT / "README.md").lower()
    privacy = _read(ROOT / "PRIVACY.md").lower()
    required = [
        "no external api calls",
        "no hidden tracking",
        "no hosted backend",
    ]
    for phrase in required:
        if phrase not in readme:
            raise AssertionError(f"README.md missing privacy phrase: {phrase}")
        if phrase not in privacy:
            raise AssertionError(f"PRIVACY.md missing privacy phrase: {phrase}")


def check_no_network_or_secret_patterns() -> None:
    scanned_paths = list((ROOT / "src").rglob("*.py")) + list((ROOT / "tests").rglob("*.py"))
    blocked_patterns = [
        "requests.",
        "urllib.request",
        "http.client",
        "socket.",
        "subprocess.run([\"curl\"",
        "api_key =",
        "secret =",
        "password =",
        "token =",
    ]
    for path in scanned_paths:
        text = _read(path).lower()
        for pattern in blocked_patterns:
            if pattern in text:
                raise AssertionError(f"Blocked pattern {pattern!r} found in {path.relative_to(ROOT)}")


def main() -> int:
    check_pyproject()
    check_compiles()
    check_tests()
    check_privacy_notes()
    check_no_network_or_secret_patterns()
    print("adpages-tools checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

