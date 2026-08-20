

to set up the project on your device

1. Unzip the project to any folder or pull it from git hub, e.g. `C:\StopSignProject`.
2. Open the `PROJECT SHAREING INFO` folder and **double-click `setup.bat`**.
   - If Python 3.11+ is already installed, it is used automatically.
   - If not, `setup.bat` silently installs the bundled **Python 3.14** for you.
   - Then it creates a venv and installs PyTorch (CPU), ultralytics, OpenCV, etc.
   - Takes a few minutes. Needs internet the first time.
3. Done. Now double-click **`test_photo.bat`** to test the model on any photo.

## What you must have installed

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

## now run the project
   1. run test_photo.bat
   2. select a photo
   3. results will automatically appears
   4. You can also see the results from the folder runs\detections
