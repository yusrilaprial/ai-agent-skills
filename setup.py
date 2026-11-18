#!/usr/bin/env python3
"""Interactive & CLI installer for AI Agent Skills."""

import argparse
import os
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_SOURCE_DIR = SCRIPT_DIR / "skills"

AGENTS = [
    {
        "id": "opencode",
        "name": "OpenCode (CLI & VS Code)",
        "global_dir": Path.home() / ".config" / "opencode" / "skills",
        "project_dir": Path(".opencode") / "skills",
    },
    {
        "id": "codex",
        "name": "OpenAI Codex (CLI & VS Code)",
        "global_dir": Path.home() / ".codex" / "skills",
        "project_dir": Path(".agents") / "skills",
    },
    {
        "id": "claude",
        "name": "Claude Code",
        "global_dir": Path.home() / ".claude" / "skills",
        "project_dir": Path(".claude") / "skills",
    },
    {
        "id": "gemini",
        "name": "Gemini CLI",
        "global_dir": Path.home() / ".gemini" / "skills",
        "project_dir": Path(".gemini") / "skills",
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "global_dir": Path.home() / ".cursor" / "skills",
        "project_dir": Path(".cursor") / "skills",
    },
    {
        "id": "copilot",
        "name": "GitHub Copilot (VS Code)",
        "global_dir": Path.home() / ".copilot" / "skills",
        "project_dir": Path(".github") / "skills",
    },
]


def discover_skills() -> list[Path]:
    if not SKILLS_SOURCE_DIR.exists():
        return []
    return [
        entry
        for entry in sorted(SKILLS_SOURCE_DIR.iterdir())
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    ]


def _read_key() -> str:
    if os.name == "nt":
        import msvcrt

        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ext = msvcrt.getch()
            if ext == b"H":
                return "UP"
            if ext == b"P":
                return "DOWN"
            return ""
        if ch == b" ":
            return "SPACE"
        if ch in (b"\r", b"\n"):
            return "ENTER"
        if ch in (b"\x03", b"q", b"Q"):
            return "QUIT"
        if ch in (b"a", b"A"):
            return "ALL"
        return ""

    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            if seq == "[A":
                return "UP"
            if seq == "[B":
                return "DOWN"
            return ""
        if ch == " ":
            return "SPACE"
        if ch in ("\r", "\n"):
            return "ENTER"
        if ch in ("\x03", "q", "Q"):
            return "QUIT"
        if ch in ("a", "A"):
            return "ALL"
        if ch == "k":
            return "UP"
        if ch == "j":
            return "DOWN"
        return ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def interactive_multiselect(
    title: str, options: list[dict], default_selected: bool = False
) -> list[int]:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return fallback_multiselect(title, options)

    selected = [default_selected] * len(options)
    cursor = 0
    rendered_lines = 0

    def render() -> None:
        nonlocal rendered_lines
        if rendered_lines > 0:
            sys.stdout.write(f"\033[{rendered_lines}A\033[J")

        lines = [
            f"\033[1m{title}\033[0m",
            "\033[2m(Panah Atas/Bawah: navigasi | Spasi: pilih | A: semua | Enter: lanjut | Q: batal)\033[0m",
        ]
        for idx, opt in enumerate(options):
            pointer = "\033[36m>\033[0m" if idx == cursor else " "
            checkbox = "\033[32m[x]\033[0m" if selected[idx] else "[ ]"
            desc = f" \033[2m- {opt['desc']}\033[0m" if opt.get("desc") else ""
            lines.append(f" {pointer} {checkbox} {opt['label']}{desc}")

        output = "\n".join(lines) + "\n"
        sys.stdout.write(output)
        sys.stdout.flush()
        rendered_lines = len(lines)

    try:
        render()
        while True:
            key = _read_key()
            if key == "UP":
                cursor = (cursor - 1) % len(options)
                render()
            elif key == "DOWN":
                cursor = (cursor + 1) % len(options)
                render()
            elif key == "SPACE":
                selected[cursor] = not selected[cursor]
                render()
            elif key == "ALL":
                target_state = not all(selected)
                selected = [target_state] * len(options)
                render()
            elif key == "ENTER":
                print()
                return [i for i, flag in enumerate(selected) if flag]
            elif key == "QUIT":
                print("\nSetup dibatalkan.")
                sys.exit(0)
    except Exception:
        return fallback_multiselect(title, options)


def fallback_multiselect(title: str, options: list[dict]) -> list[int]:
    print(f"\n{title}")
    for idx, opt in enumerate(options, start=1):
        desc = f" - {opt['desc']}" if opt.get("desc") else ""
        print(f"  {idx}. {opt['label']}{desc}")
    raw = input("Masukkan nomor pilihan (pisahkan dengan koma, misal 1,2 atau 'all'): ").strip()
    if raw.lower() == "all":
        return list(range(len(options)))
    indices = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            num = int(part) - 1
            if 0 <= num < len(options) and num not in indices:
                indices.append(num)
    return indices


def interactive_single_choice(title: str, choices: list[tuple[str, str]]) -> str:
    print(f"\033[1m{title}\033[0m")
    for idx, (_, label) in enumerate(choices, start=1):
        print(f"  {idx}. {label}")
    while True:
        raw = input(f"Pilih [1-{len(choices)}] (default 1): ").strip()
        if raw == "":
            return choices[0][0]
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1][0]
        print("Pilihan tidak valid, silakan coba lagi.")


def remove_existing_target(target_path: Path) -> None:
    if target_path.is_symlink() or target_path.is_file():
        target_path.unlink()
    elif target_path.is_dir():
        shutil.rmtree(target_path)


def install_skill(
    skill_dir: Path,
    agent: dict,
    scope: str,
    mode: str,
    project_root: Path,
) -> tuple[bool, str]:
    base_dir = (
        agent["global_dir"]
        if scope == "global"
        else project_root / agent["project_dir"]
    )
    target_path = base_dir / skill_dir.name

    try:
        base_dir.mkdir(parents=True, exist_ok=True)
        if target_path.exists() or target_path.is_symlink():
            remove_existing_target(target_path)

        if mode == "symlink":
            try:
                target_path.symlink_to(skill_dir, target_is_directory=True)
                return True, f"Symlink -> {target_path}"
            except OSError:
                shutil.copytree(skill_dir, target_path)
                return True, f"Copied (fallback symlink) -> {target_path}"
        else:
            shutil.copytree(skill_dir, target_path)
            return True, f"Copied -> {target_path}"
    except Exception as exc:
        return False, f"Gagal ({target_path}): {exc}"


def uninstall_skill(
    skill_name: str,
    agent: dict,
    scope: str,
    project_root: Path,
) -> tuple[bool, str]:
    base_dir = (
        agent["global_dir"]
        if scope == "global"
        else project_root / agent["project_dir"]
    )
    target_path = base_dir / skill_name
    if not (target_path.exists() or target_path.is_symlink()):
        return False, f"Tidak ditemukan di {target_path}"
    remove_existing_target(target_path)
    return True, f"Dihapus dari {target_path}"


def list_status(skills: list[Path], project_root: Path) -> None:
    print("\033[1mDaftar Skill Tersedia:\033[0m")
    for s in skills:
        print(f"  - {s.name}")

    print("\n\033[1mStatus Pemasangan per Agent:\033[0m")
    for agent in AGENTS:
        print(f"\n  {agent['name']} ({agent['id']})")
        for s in skills:
            g_path = agent["global_dir"] / s.name
            p_path = project_root / agent["project_dir"] / s.name
            g_status = "Terpasang (Global)" if (g_path.exists() or g_path.is_symlink()) else "-"
            p_status = "Terpasang (Project)" if (p_path.exists() or p_path.is_symlink()) else "-"
            print(f"    • {s.name}: Global=[{g_status}] | Project=[{p_status}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup AI Agent Skills")
    parser.add_argument(
        "--agents",
        help="Daftar ID agent dipisah koma (contoh: opencode,codex,claude)",
    )
    parser.add_argument(
        "--skills",
        help="Daftar nama skill dipisah koma (default: semua skill di folder skills/)",
    )
    parser.add_argument(
        "--scope",
        choices=["global", "project"],
        help="Lokasi instalasi: global (~/) atau project (./)",
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Path root proyek tujuan jika scope=project (default: direktori saat ini)",
    )
    parser.add_argument(
        "--mode",
        choices=["symlink", "copy"],
        default=None,
        help="Metode instalasi: symlink atau copy",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Hapus skill dari agent yang dipilih",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Tampilkan daftar skill dan status instalasi",
    )
    args = parser.parse_args()

    available_skills = discover_skills()
    if not available_skills:
        print("Error: Tidak ada folder skill valid (dengan SKILL.md) di direktori 'skills/'.")
        sys.exit(1)

    project_root = Path(args.project_dir).expanduser().resolve()

    if args.list:
        list_status(available_skills, project_root)
        return

    # 1. Pilih Skill
    if args.skills:
        requested = {name.strip() for name in args.skills.split(",") if name.strip()}
        selected_skills = [s for s in available_skills if s.name in requested]
    elif len(available_skills) == 1:
        selected_skills = available_skills
        print(f"Skill terdeteksi: \033[32m{selected_skills[0].name}\033[0m\n")
    else:
        skill_opts = [{"label": s.name, "desc": str(s)} for s in available_skills]
        picked_skill_idx = interactive_multiselect(
            "1. Pilih skill yang ingin dipasang:", skill_opts, default_selected=False
        )
        selected_skills = [available_skills[i] for i in picked_skill_idx]

    if not selected_skills:
        print("Tidak ada skill yang dipilih. Setup selesai.")
        return

    # 2. Pilih Agent AI
    if args.agents:
        requested_agents = {a.strip().lower() for a in args.agents.split(",") if a.strip()}
        selected_agents = [a for a in AGENTS if a["id"] in requested_agents]
    else:
        agent_opts = [
            {
                "label": a["name"],
                "desc": f"global: {a['global_dir']}",
            }
            for a in AGENTS
        ]
        picked_agent_idx = interactive_multiselect(
            "Pilih agent AI tujuan:", agent_opts, default_selected=False
        )
        selected_agents = [AGENTS[i] for i in picked_agent_idx]

    if not selected_agents:
        print("Tidak ada agent AI yang dipilih. Setup selesai.")
        return

    # 3. Pilih Scope (Global vs Project)
    scope = args.scope or interactive_single_choice(
        "Pilih cakupan pemasangan:",
        [
            ("global", "Global (berlaku untuk semua proyek di user ini)"),
            ("project", "Project (hanya di dalam folder proyek tertentu)"),
        ],
    )

    if scope == "project" and not args.scope:
        custom_dir = input(
            f"\nMasukkan path root proyek tujuan (Enter untuk '{project_root}'): "
        ).strip()
        if custom_dir:
            project_root = Path(custom_dir).expanduser().resolve()

    # 4. Eksekusi Uninstall atau Install
    if args.uninstall:
        print("\n\033[1mMenghapus skill...\033[0m")
        for skill in selected_skills:
            for agent in selected_agents:
                ok, msg = uninstall_skill(skill.name, agent, scope, project_root)
                icon = "\033[32m✔\033[0m" if ok else "\033[33m!\033[0m"
                print(f"  {icon} [{agent['name']}] {skill.name}: {msg}")
        return

    mode = args.mode or interactive_single_choice(
        "\nPilih metode pemasangan:",
        [
            ("symlink", "Symlink (direkomendasikan - update di repo otomatis sinkron)"),
            ("copy", "Copy (salinan file mandiri ke folder masing-masing agent)"),
        ],
    )

    print("\n\033[1mMemasang skill...\033[0m")
    for skill in selected_skills:
        for agent in selected_agents:
            ok, msg = install_skill(skill, agent, scope, mode, project_root)
            icon = "\033[32m✔\033[0m" if ok else "\033[31m✖\033[0m"
            print(f"  {icon} [{agent['name']}] {skill.name}: {msg}")

    print("\n\033[32mSelesai!\033[0m Muat ulang (Reload Window) VS Code / sesi CLI agent Anda agar skill langsung aktif.")


if __name__ == "__main__":
    main()
