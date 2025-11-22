# Ninja Sage Panel

This repository hosts the Ninja Sage Panel GUI and core helpers that talk to Ninja Sage game services via AMF. The project is structured as a package (`ninja_sage`) with the GUI under `ninja_sage/gui` and supporting logic under `ninja_sage/core`.

## Requirements

- Python 3.13+
- Install dependencies (use the same requirements that power the PyInstaller build):

  ```powershell
  python -m pip install -r requirements.txt
  ```

  or rely on `pyproject.toml` if you prefer `pip install .` before packaging.

### Using `uv`

`uv` is a lightweight Python package manager that can read `pyproject.toml` and manage virtual environments automatically. To use it in this project:

1. Install `uv` globally if you haven't already:

   ```powershell
   python -m pip install uv
   ```

2. Install dependencies and create the environment (runs `uv install` once):

   ```powershell
   uv sync
   ```

3. Run the GUI or build script inside the `uv` environment:

   ```powershell
   uv run main.py
   uv run build.py
   ```

`uv sync` reads `pyproject.toml`, so keeping the dependency list there ensures `uv` stays in sync with `requirements.txt`.

## Build

You can build a single-file executable via PyInstaller by reusing the existing helper:

```powershell
python build.py
```

`build.py` delegates to `PyInstaller.__main__` and points at the root `main.py` stub (which now forwards to `ninja_sage.gui.main.main`). That keeps build scripts targeting `main.py` while the real GUI lives in the package.

If you prefer to run PyInstaller manually, target `main.py` and include the `ninja_sage` package:

```powershell
pyinstaller --name NinjaSageBot --onefile --console --add-data "data;data" main.py
```

Adjust any other flags (icons, hidden imports) as needed for your platform.

## Usage

1. Ensure `quick_login.json` exists (the GUI will save it automatically after the first successful manual login).
2. Run the GUI with:

   ```powershell
   uv run main.py
   ```

   or execute the bundled binary produced by PyInstaller.

3. The welcome screen checks the game version, takes you through login/character selection, and then opens the main menu.
4. Start any action (leveling, eudemon boss, events, etc.) via the buttons—every action runs on a background thread and writes to the detachable log window.
5. Use the **Stop Current Action** button if you need to cancel a running task; the UI centralizes that logic so every action respects the shared `stop_event`.

See `docs/gui.md` for a breakdown of how the GUI, logging window, and action helpers are wired together.
