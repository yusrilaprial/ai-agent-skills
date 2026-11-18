# AI Agent Skills Setup

Installer otomatis untuk memasang koleksi Agent Skills (`SKILL.md`) ke berbagai AI coding agent (OpenCode, OpenAI Codex, Claude Code, Gemini CLI, Cursor, dan GitHub Copilot).

## Cara Menggunakan

1. Ekstrak arsip ini dan buka terminal di direktori proyek:
   ```bash
   unzip ai-agent-skills.zip
   cd ai-agent-skills
   ```

2. Jalankan installer interaktif. Di Windows, gunakan:
   ```powershell
   py setup.py
   ```
   Jika perintah `py` tidak tersedia, gunakan `python setup.py`. Di macOS/Linux, gunakan `python3 setup.py`.

3. Pilih skill yang ingin dipasang terlebih dahulu. Lalu pilih agent AI tujuan, cakupan pemasangan (global atau project), dan metode pemasangan. Gunakan **Panah Atas/Bawah** untuk berpindah pilihan, **Spasi** untuk memilih, **A** untuk memilih semua, lalu tekan **Enter**.

## Mode CLI Langsung (Non-Interaktif)

- Pasang skill ke OpenCode dan Codex secara global menggunakan symlink (Windows):
  ```bash
  py setup.py --skills nama-skill --agents opencode,codex --scope global --mode symlink
  ```
- Pasang skill ke direktori proyek tertentu:
  ```bash
  py setup.py --skills nama-skill --agents opencode,codex --scope project --project-dir C:\path\ke\proyek
  ```
- Cek status pemasangan skill di semua agent:
  ```bash
  py setup.py --list
  ```
- Hapus skill dari agent tertentu:
  ```bash
  py setup.py --skills nama-skill --uninstall --agents opencode,codex --scope global
  ```

## Menambah Skill Baru di Masa Depan

Cukup buat folder baru di dalam `skills/<nama-skill>/SKILL.md`. Installer akan otomatis mendeteksi skill tersebut saat dijalankan kembali.
