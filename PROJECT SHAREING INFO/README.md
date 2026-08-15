# How to Share This Project (READ THIS FIRST)

## Step 1 — Make the ZIP (this is what YOU do)

1. Copy this whole project folder to your friend.
2. **IMPORTANT:** Before zipping, delete the `venv` folder from the copy.
   - It is large (~300+ MB) and is NOT portable.
   - Your friend will recreate it automatically with `setup.bat`.
3. Right-click the project folder -> Send to -> Compressed (zipped) folder.
4. Send the `.zip` file to your friend.

## Step 2 — What your friend does

1. Install **Python 3.10 or newer** from https://www.python.org/downloads/
   - Tick **"Add Python to PATH"** during installation.
2. Unzip the project to any folder, e.g. `C:\StopSignProject`.
3. Open the `PROJECT SHAREING INFO` folder and **double-click `setup.bat`**.
   - It creates a venv and installs PyTorch (CPU), ultralytics, OpenCV, etc.
   - Takes a few minutes. Needs internet.
4. Done. Now double-click **`test_photo.bat`** to test the model on any photo.

## What your friend must have installed

| Software | Required |
|---|---|
| Python 3.10+ | YES (with "Add to PATH") |
| Packages (torch, ultralytics, opencv...) | Installed automatically by setup.bat |
| Internet connection | Only needed once, during setup.bat |

## Troubleshooting

- **"python is not recognized"** -> Python not added to PATH. Reinstall Python and tick the box.
- **setup.bat fails mid-install** -> check internet, then run it again (it resumes safely).
- **Model still works even if packages differ slightly** -> versions are pinned in `requirements.txt`.

## Note on the files

- `venv` must NOT be in the ZIP (not portable).
- Everything else travels fine: `scripts\`, `models\`, `dataset\`, `dataset.yaml`, `test_photo.bat`.
- All scripts use relative paths, so the project works from any location.
