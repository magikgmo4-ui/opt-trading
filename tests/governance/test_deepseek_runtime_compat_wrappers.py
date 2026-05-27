from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_legacy_student_cmd_is_not_recursive():
    content = _read("scripts/student/student_cmd.sh")
    assert 'exec /opt/trading/scripts/student/student_cmd.sh' not in content
    assert 'exec bash "/opt/trading/student/scripts/student_cmd.sh" "$@"' in content


def test_legacy_student_entrypoints_delegate_to_canonical_student_tree():
    expected = {
        "scripts/student/student_menu.sh": 'exec bash "/opt/trading/student/scripts/student_menu.sh" "$@"',
        "scripts/student/student_sanity_check.sh": 'exec bash "/opt/trading/student/scripts/student_sanity_check.sh" "$@"',
        "scripts/student/deepseek_student_cmd.sh": 'exec bash "/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh" "$@"',
        "scripts/student/deepseek_student_menu.sh": 'exec bash "/opt/trading/student/scripts/wrappers/deepseek_student_menu.sh" "$@"',
        "scripts/student/deepseek_student_sanity_check.sh": 'exec bash "/opt/trading/student/scripts/wrappers/deepseek_student_sanity_check.sh" "$@"',
        "scripts/student/deepseek_student_install.sh": 'exec bash "/opt/trading/student/scripts/wrappers/deepseek_student_install.sh" "$@"',
    }

    for rel_path, target in expected.items():
        content = _read(rel_path)
        assert target in content, rel_path


def test_root_shortcut_installer_points_to_canonical_student_entrypoints():
    content = _read("scripts/install_student_shortcuts.sh")
    assert 'sudo ln -sf "$BASE/student/scripts/student_menu.sh" /usr/local/bin/menu-student' in content
    assert 'sudo ln -sf "$BASE/student/scripts/student_cmd.sh" /usr/local/bin/cmd-student' in content
    assert 'sudo ln -sf "$BASE/student/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student' in content
