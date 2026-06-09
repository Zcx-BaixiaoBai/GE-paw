# gepaw Desktop 

 `scripts/wheel_build.sh`  **wheel**
?console  ** conda ** + **conda-pack**
 `pyproject.toml` ?

- **Windows**: wheel ?conda-pack ? ?NSIS ?(`.exe`)
- **macOS**: wheel ?conda-pack ??`.app` ? zip

## 

- **Windows**: Windows 10 ?
- **macOS**: macOS 14 (Sonoma)  Apple Silicon (M1/M2/M3/M4)

## 

- **conda**Miniconda/Anaconda PATH
- **Node.js / npm**?console ?
-  Windows?*NSIS**`makensis` ?PATH
- ****?`icon.ico` (Windows) ?`icon.icns` (macOS)  `scripts/pack/assets/` ?

## ?

?*?*?

**macOS**
```bash
bash ./scripts/pack/build_macos.sh
# : dist/gepaw.app

CREATE_ZIP=1 bash ./scripts/pack/build_macos.sh   #  .zip
```

**Windows (PowerShell)**
```powershell
./scripts/pack/build_win.ps1
# : dist/gepaw-Setup-<version>.exe
# 
#   - gepaw Desktop.vbs ()
#   - gepaw Desktop (Debug).bat (?
```

## macOS?

 .app 

```bash
#  conda / PYTHONPATH?
APP_ENV="$(pwd)/dist/gepaw.app/Contents/Resources/env"
PYTHONNOUSERSITE=1 PYTHONPATH= PYTHONHOME="$APP_ENV" "$APP_ENV/bin/python" -m gepaw desktop
```

`PYTHONNOUSERSITE=1` ?Python  `~/.local/lib/pythonX.Y/site-packages` ?Python traceback?`--log-level debug` ?

?*** .app  stderr/stdout  `~/.gepaw/desktop.log`?

macOS ****?

## macOS? Gatekeeper 

?Release  gepaw macOS zip  .app Apple Apple QwenPaw?Mac ?

- ****
  ?gepaw ?** Control + ?* ??**?* ??**?*Gatekeeper ?

- ****
   ** ??* gepaw **?* ?**?* ?

- ****
  `xattr -cr /Applications/gepaw.app`?.app ???

## CI

`.github/workflows/desktop-release.yml`?

- ****: Release  ? workflow_dispatch
- **Windows**:  console ? conda  + conda-pack ?NSIS ? artifact
- **macOS**:  console ? conda  + conda-pack ?.app ?zip ? artifact
- **Release**:  release ?Windows  macOS zip  Release ?

## 

|  |  |
|------|------|
| `build_common.py` |  conda  wheel  `gepaw[full]`conda-pack  |
| `build_macos.sh` |  wheel ?build_common ??gepaw.app zip |
| `build_win.ps1` |  wheel ?build_common ? ? VBS/BAT ??makensis ?|
| `desktop.nsi` | NSIS ?`dist/win-unpacked` |
| `assets/icon.ico` |  Windows  |
| `assets/icon.icns` |  macOS ?|
