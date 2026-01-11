#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video cutting tool using ffmpeg
Drag a video file onto this script to cut it
"""

import os
import sys
import subprocess
from pathlib import Path


def get_base_path():
    """Get the base path of the script or executable.
    Works correctly with PyInstaller bundles."""
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        return Path(sys.executable).parent.absolute()
    else:
        # Running as a normal Python script
        return Path(__file__).parent.absolute()


def parse_time(time_str):
    """Parse time string in format HHMMSS (e.g. 013245 -> 1h 32m 45s)"""
    clean = time_str.strip()
    if not clean.isdigit():
        raise ValueError("Invalid time format: Only digits expected in HHMMSS form.")
    length = len(clean)
    if length > 6 or length < 1:
        raise ValueError("Invalid time format: String length should be from 1 to 6 digits (HHMMSS, MMSS, SS).")
    # Pad the string to always be 6 digits
    clean_padded = clean.zfill(6)  # '45' => '000045'
    hours = int(clean_padded[:-4]) if length > 4 else 0
    minutes = int(clean_padded[-4:-2]) if length > 2 else 0
    seconds = int(clean_padded[-2:])
    return hours * 3600 + minutes * 60 + seconds


def format_time(seconds):
    """Format seconds to HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{int(minutes):02d}:{secs:06.3f}"


def cut_video(input_path, start_time, end_time, output_path):
    """Cut video using ffmpeg with fast copy mode (no re-encoding)"""
    duration = end_time - start_time
    
    # Build ffmpeg command for fast copy mode
    # -ss before -i enables input seeking (much faster)
    # -c copy copies streams without re-encoding (fast copy mode)
    # Use ffmpeg.exe from the same directory if exists, else use system ffmpeg
    base_path = get_base_path()
    local_ffmpeg = base_path / 'ffmpeg.exe'
    if local_ffmpeg.exists():
        ffmpeg_exe = str(local_ffmpeg)
    else:
        ffmpeg_exe = 'ffmpeg'  # Use system ffmpeg

    cmd = [
        ffmpeg_exe,
        '-ss', format_time(start_time),  # Input seeking (faster)
        '-i', str(input_path),
        '-t', format_time(duration),
        '-c', 'copy',  # Copy all codecs (fast, no re-encoding)
        '-map', '0',  # Copy all streams
        '-avoid_negative_ts', 'make_zero',
        str(output_path),
        '-y'  # Overwrite output file if exists
    ]
    
    print(f"\nExecuting ffmpeg command (fast copy mode, no re-encoding)...")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print("Video cutting completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg execution failed")
        print(f"Error message: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure ffmpeg is installed and added to system PATH.")
        return False


def main():
    # Get input file from command line argument (drag-and-drop)
    if len(sys.argv) < 2:
        print("Please drag a video file onto this script, or provide the video file path via command line.")
        print("Usage: python python.py <video_file>")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    # Validate input file
    if not input_path.exists():
        print(f"Error: File does not exist: {input_path}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"Error: Not a valid file: {input_path}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"Input file: {input_path}")
    print(f"File size: {input_path.stat().st_size / (1024*1024):.2f} MB")
    
    # Get start time
    start_input = ""
    while True:
        start_input = input("Please enter start time (format: HHMMSS): ").strip()
        try:
            start_time = parse_time(start_input)
            if start_time < 0:
                print("Error: Start time cannot be negative")
                continue
            break
        except ValueError as e:
            print(f"Error: Invalid time format - {e}")
    
    # Get end time
    end_input = ""
    while True:
        end_input = input("Please enter end time (format: HHMMSS): ").strip()
        try:
            end_time = parse_time(end_input)
            if end_time <= start_time:
                print("Error: End time must be greater than start time")
                continue
            break
        except ValueError as e:
            print(f"Error: Invalid time format - {e}")
    
    print(f"\nStart time: {format_time(start_time)}")
    print(f"End time: {format_time(end_time)}")
    print(f"Duration: {format_time(end_time - start_time)}")
    

    # Get script directory for output
    script_dir = get_base_path()
    
    # Generate output filename
    input_stem = input_path.stem
    input_suffix = input_path.suffix
    output_path = script_dir / f"{input_stem}_{start_input}_{end_input}{input_suffix}"
    
    # Counter for output filename if file exists
    counter = 1
    while output_path.exists():
        output_path = script_dir / f"{input_stem}_{start_input}_{end_input}_{counter}{input_suffix}"
        counter += 1
    
    print(f"Output file: {output_path}\n")
    
    # Confirm before processing
    confirm = input("\nConfirm cutting? (Y/n): ").strip().lower()
    if confirm not in ('', 'y'):
        print("Operation cancelled.")
        sys.exit(0)
    
    # Cut video
    success = cut_video(input_path, start_time, end_time, output_path)
    
    if success:
        print(f"\nOutput file saved to: {output_path}")
        file_size = output_path.stat().st_size / (1024*1024)
        print(f"Output file size: {file_size:.2f} MB")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

