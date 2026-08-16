# How to Share This Project (READ THIS FIRST)

## Step 1 — Make the ZIP (this is what YOU do)

1. Copy this whole project folder to your friend.
2. **IMPORTANT:** Before zipping, delete the `venv` folder from the copy.
   - It is large (~300+ MB) and is NOT portable.
   - Your friend will recreate it automatically with `setup.bat`.
3. **IMPORTANT:** KEEP the file `python-3.14.7-amd64.exe` in the project.
   - `setup.bat` uses it to install Python automatically if your friend doesn't have it.
4. Right-click the project folder -> Send to -> Compressed (zipped) folder.
5. Send the `.zip` file to your friend.

## Step 2 — What your friend does

1. Unzip the project to any folder, e.g. `C:\StopSignProject`.
2. Open the `PROJECT SHAREING INFO` folder and **double-click `setup.bat`**.
   - If Python 3.11+ is already installed, it is used automatically.
   - If not, `setup.bat` silently installs the bundled **Python 3.14** for you.
   - Then it creates a venv and installs PyTorch (CPU), ultralytics, OpenCV, etc.
   - Takes a few minutes. Needs internet the first time.
3. Done. Now double-click **`test_photo.bat`** to test the model on any photo.

## What your friend must have installed

| Software | Required |
|---|---|
| Python 3.11+ | NO — installed automatically by setup.bat (Python 3.14 is bundled) |
| Packages (torch, ultralytics, opencv...) | Installed automatically by setup.bat |
| Internet connection | Only needed once, during setup.bat |

## Troubleshooting

- **setup.bat says "python-3.14.7-amd64.exe was not found"** -> the installer file is missing
  from the project folder. Put it back, or download Python 3.14 from
  https://www.python.org/downloads/ and run setup again.
- **setup.bat fails mid-install** -> check internet, then run it again (it resumes safely).
- **Model still works even if packages differ slightly** -> versions are pinned in `requirements.txt`.

## Note on the files

- `venv` must NOT be in the ZIP (not portable).
- `python-3.14.7-amd64.exe` MUST be in the ZIP (setup.bat needs it to install Python).
- Everything else travels fine: `scripts\`, `models\`, `dataset\`, `dataset.yaml`, `test_photo.bat`.
- All scripts use relative paths, so the project works from any location.