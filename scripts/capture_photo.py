#!/usr/bin/env python3
"""
Capture a photo from the default webcam and save it.

Usage:
  python3 scripts/capture_photo.py [output_filename]
  python3 scripts/capture_photo.py --no-preview -d 1 captured.jpg

Options:
  output_filename      Optional. If omitted a timestamped filename is used.
  -d, --device         Camera device index (default 0).
  --no-preview         Capture a single frame without opening a preview window.
  --width WIDTH        Optional capture width (pixels).
  --height HEIGHT      Optional capture height (pixels).
  --frames N           Warm-up frames to discard before capture (default 5).

Controls (preview mode):
  - Press SPACE to capture and save the current frame.
  - Press 'q' or ESC to quit without saving.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime

import cv2


def parse_args():
    p = argparse.ArgumentParser(description="Capture a photo from a webcam using OpenCV.")
    p.add_argument("output", nargs="?", help="Output filename (jpg/png). If omitted a timestamped name is used.")
    p.add_argument("-d", "--device", type=int, default=0, help="Camera device index (default 0).")
    p.add_argument("--no-preview", action="store_true", help="Do not show preview; capture a single frame.")
    p.add_argument("--width", type=int, help="Optional capture width in pixels.")
    p.add_argument("--height", type=int, help="Optional capture height in pixels.")
    p.add_argument("--frames", type=int, default=5, help="Warm-up frames to discard before capture.")
    return p.parse_args()


def timestamp_filename(ext: str = "jpg") -> str:
    return datetime.now().strftime(f"photo_%Y%m%d_%H%M%S.{ext}")


def open_camera(device: int):
    cap = cv2.VideoCapture(device, cv2.CAP_ANY)
    if not cap.isOpened():
        return None
    return cap


def set_resolution(cap, width: int | None, height: int | None):
    if width:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def warmup(cap, frames: int):
    for _ in range(max(0, frames)):
        cap.read()


def capture_headless(cap, outname: str, warmup_frames: int):
    warmup(cap, warmup_frames)
    ret, frame = cap.read()
    if not ret:
        print("Error: failed to read frame from camera", file=sys.stderr)
        return False
    cv2.imwrite(outname, frame)
    print(f"Saved photo to {outname}")
    return True


def capture_with_preview(cap, outname: str, warmup_frames: int):
    window_name = "Press SPACE to capture, q to quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    warmup(cap, warmup_frames)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame", file=sys.stderr)
            return False

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)

        # SPACE pressed
        if key % 256 == 32:
            cv2.imwrite(outname, frame)
            print(f"Saved photo to {outname}")
            return True
        # 'q' or ESC pressed
        elif key & 0xFF in (ord("q"), 27):
            print("Exiting without saving")
            return False


def main():
    args = parse_args()
    out = args.output or timestamp_filename("jpg")

    cap = open_camera(args.device)
    if cap is None:
        print(f"Error: cannot open webcam device {args.device}", file=sys.stderr)
        sys.exit(1)

    if args.width or args.height:
        set_resolution(cap, args.width, args.height)

    try:
        if args.no_preview:
            ok = capture_headless(cap, out, args.frames)
        else:
            ok = capture_with_preview(cap, out, args.frames)
    finally:
        cap.release()
        cv2.destroyAllWindows()

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()