"""Run the host-only skill installer offline, stopping before global writes."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "skills/public/find-skills/scripts/install-skill.sh"
)
BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(
    BASH is None, reason="bash is required to run install-skill.sh"
)


def _run_installer(tmp_path, cwd, *args):
    capture = tmp_path / "installer-calls.txt"
    env = os.environ.copy()
    env.pop("BASH_ENV", None)
    env.pop("ENV", None)
    env["FIND_SKILLS_INSTALL_CALLS"] = str(capture)
    result = subprocess.run(
        [
            BASH,
            "-c",
            'npx() { printf "%s\\n" "$@" >> "$FIND_SKILLS_INSTALL_CALLS"; return 77; }; '
            'export -f npx; "$@"',
            "find-skills-test",
            BASH,
            str(SCRIPT),
            *args,
        ],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    calls = capture.read_text(encoding="utf-8").splitlines() if capture.exists() else []
    return result, calls


def test_markerless_working_directory_explains_host_only_install(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    result, calls = _run_installer(tmp_path, workspace, "owner/repo@skill-name")

    assert result.returncode != 0
    assert "deer-flow.code-workspace" in result.stderr
    assert "host" in result.stderr.lower()
    assert "Capability Center" in result.stderr
    assert calls == []


@pytest.mark.parametrize(
    "nested", [False, True], ids=["repository-root", "nested-directory"]
)
def test_host_checkout_reaches_global_installer_before_any_writes(tmp_path, nested):
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / "deer-flow.code-workspace").touch()
    cwd = checkout / "nested" if nested else checkout
    cwd.mkdir(exist_ok=True)

    result, calls = _run_installer(tmp_path, cwd, "owner/repo@skill-name")

    assert result.returncode == 77
    assert calls == ["skills", "add", "owner/repo@skill-name", "-g", "-y"]
    assert not (checkout / "skills").exists()


@pytest.mark.parametrize(
    "args",
    [
        (),
        ("",),
        ("owner/repo",),
        ("owner/repo@",),
        ("@skill",),
        ("repo@skill",),
        ("owner/repo@../skill",),
        ("owner/repo@one@two",),
    ],
)
def test_invalid_identifier_reports_usage_without_installing(tmp_path, args):
    (tmp_path / "deer-flow.code-workspace").touch()

    result, calls = _run_installer(tmp_path, tmp_path, *args)

    assert result.returncode != 0
    assert "owner/repo@skill-name" in result.stderr
    assert calls == []
