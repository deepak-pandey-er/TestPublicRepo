# Webcam photo capture (Python)

This repository includes a small Python script to capture a photo from a webcam using OpenCV.

Prerequisites
- Python 3.7+
- A connected webcam

Install dependencies

```bash
pip install -r requirements.txt
```

Usage

Preview mode (default):
```bash
python3 scripts/capture_photo.py [output_filename]
```

Headless / immediate capture (no preview):
```bash
python3 scripts/capture_photo.py --no-preview [output_filename]
```

Examples:
- `python3 scripts/capture_photo.py` — shows preview, press SPACE to capture and save as `photo_YYYYMMDD_HHMMSS.jpg`.
- `python3 scripts/capture_photo.py my_photo.jpg` — preview mode, saves to `my_photo.jpg` when you press SPACE.
- `python3 scripts/capture_photo.py --no-preview my_photo.jpg` — immediately captures one frame and saves to `my_photo.jpg`.

Options:
- `-d, --device` — camera index (default 0).
- `--width` and `--height` — optional resolution to set.
- `--frames` — warm-up frames to discard before capture (default 5).

Notes
- On Linux you might need additional system packages (e.g., v4l-utils) or to grant permission to the device.
- If the repository is empty you can create the files locally and push them to your repo (instructions below).

How to add these files to your repository (command-line)
1. Clone (or create) your repo locally:
```bash
git clone git@github.com:deepak-pandey-er/TestPublicRepo.git
cd TestPublicRepo
```
2. Create the scripts directory and add files (or copy the files above into the repo):
```bash
mkdir -p scripts
# add scripts/capture_photo.py and requirements.txt and README.md (paste contents)
```
3. Commit and push:
```bash
git add .
git commit -m "Add webcam photo capture script"
git push -u origin main
```

Alternative: use GitHub web UI to create new files and paste the file contents.

If you'd like, I can:
- Provide a minimal GitHub Actions workflow to test that the script runs in headless mode (CI environment), or
- Convert the script to a small package/CLI entrypoint,
- Or generate a one-line curl/wget command to upload captured images to a server.

Tell me which next step you want.