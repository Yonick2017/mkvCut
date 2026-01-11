# mkvCut

A simple video cutting tool using ffmpeg that allows you to quickly cut video files without re-encoding (fast copy mode).

## Features

- **Fast Copy Mode**: Uses ffmpeg's stream copy feature to cut videos without re-encoding, making the process extremely fast
- **Drag-and-Drop Support**: Simply drag a video file onto the script to start
- **Simple Time Format**: Enter start and end times in HHMMSS format (e.g., `013245` for 1 hour, 32 minutes, 45 seconds)
- **Automatic Output Naming**: Output files are automatically named based on input filename and time range
- **No Re-encoding**: Preserves original video quality and avoids time-consuming re-encoding

## Requirements

- Python 3.x
- ffmpeg.exe (included in the project directory)

## Usage

### Setting Up a Virtual Environment

Before running the script, it's recommended to use a Python virtual environment.

1. **Create a virtual environment** in the project folder:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install requirements from `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```


### Basic Usage

1. **Drag and drop** a video file onto `mkvCut.py`, or run from command line:
   ```bash
   python mkvCut.py <video_file>
   ```

2. **Enter start time** in HHMMSS format (e.g., `013245` for 1h 32m 45s)
   - You can use shorter formats: `3245` (32m 45s) or `45` (45s)
   - Hours and minutes are optional if not needed

3. **Enter end time** in the same format
   - End time must be greater than start time

4. **Confirm** the operation when prompted

5. The cut video will be saved in the same directory as the script with the format:
   `{original_filename}_{start_time}_{end_time}.{extension}`

## Notes

- The output file will be saved in the same directory as `mkvCut.py`
- If an output file with the same name already exists, a counter will be appended (e.g., `_1`, `_2`)
- The script uses `ffmpeg.exe` from the same directory as the script
- Fast copy mode only works when cutting at keyframe boundaries; ffmpeg will handle this automatically

