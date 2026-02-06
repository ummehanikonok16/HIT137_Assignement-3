# Image Editor - HIT 147

## Overview
An image editing application Built with Python, Tkinter, OpenCV, and PIL for easy image manipulation.


**User Experience:**
- Intuitive layout with image display on left, controls on right
- Mouse wheel scrolling in control panel
- Real-time value displays on all sliders
- Professional spacing and typography
- Larger display area (900x650) for better viewing


### Step 1: Install Required Packages

```bash
pip install -r requirements.txt
```

**Required packages:**
- `opencv-python` - For image processing operations
- `Pillow` - For image format handling
- `numpy` - For numerical operations

### Step 2: Run the Application

```bash
python main.py
```

## Features & Tools

### Basic Filters
- **⚫ Grayscale** - Convert image to black and white
- **🔲 Edge Detection** - Detect edges using Canny algorithm

### Adjustments

** Blur Effect**
- Gaussian blur with adjustable intensity (1-25)
- Real-time preview of intensity value
- Smooth blur transitions

** Brightness**
- Adjust brightness from -100 to +100
- Precise control with slider
- Instant preview

**Contrast**
- Adjust contrast from 0.5x to 3.0x multiplier
- Fine-tune image contrast
- Real-time value display

### Transformations

** Rotation**
- Rotate 90° clockwise
- Rotate 180°
- Rotate 270° (90° counter-clockwise)
- Quick one-click rotation

**Flip**
- Horizontal flip (mirror left-right)
- Vertical flip (mirror top-bottom)

** Resize / Scale**
- Scale from 25% to 200%
- Maintains aspect ratio
- Smooth resizing algorithm

### History & Management
- **Undo**: Revert last action (up to 20 steps)
- **Redo**: Restore undone action
- ** Reset to Original**: Restore original image
- ** Save/Save As**: Export edited images


## File Structure

```
image-editor-pro/
├── main.py              # Application entry point
├── img_editor.py        # Main editor class with pastel UI
├── img_display.py       # Image display widget with soft styling
├── img_processor.py     # Image processing backend (OpenCV)
├── requirements.txt     # Python dependencies
└── README.md           # Documentation (this file)
```

## Supported Image Formats

### Input Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff, .tif)

### Output Formats
- PNG (default, lossless)
- JPEG (compressed)

## Usage Guide

### Getting Started

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Load an image**
   - Click the " Open" button in the header, OR

3. **Edit your image**
   - Use the control panel on the right side
   - Scroll down to see all available filters and adjustments
   - Real-time preview for all changes

4. **Save your work**
   - Click " Save" to save to the current file
  

**Technologies Used:**
- Python 3.x
- OpenCV (cv2)
- Pillow (PIL)
- NumPy
- Tkinter

