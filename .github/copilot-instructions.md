# Copilot / AI Agent Instructions for Image Editor (HIT137 Assignment 3)

## Quick start ✅
- Install deps: `python -m pip install -r requirements.txt` (Windows: tkinter is usually included).
- Run app (canonical entrypoint): `python main.py` — this opens the Tk GUI.
- Lightweight tests:
  - `python img_processor.py` → will generate `test_image.png`, `test_grayscale.png`, `test_blur.png`.
  - `python img_display.py` → opens a short visual test of the display class.

---

## Big picture / architecture 🔧
- **Entrypoint:** `main.py` (creates a `tk.Tk()` window and instantiates `ImageEditor`).
- **Three main components:**
  1. `ImageEditor` (`img_editor.py`) — GUI and app coordination (menus, controls, status bar).
  2. `ImageProcessor` (`img_processor.py`) — image editing logic and history (undo/redo).
  3. `ImageDisplay` (`img_display.py`) — converts OpenCV (BGR numpy arrays) to `PIL.ImageTk.PhotoImage` and displays on a `Canvas`.
- **Data flow:** `ImageEditor` calls `ImageProcessor` to modify images → displays results via `ImageDisplay.display_image(processor.get_current_image())`.
- **Why this split:** Separation of concerns: processing logic is pure CV/numpy (testable and reusable), GUI logic keeps state and user interaction, display handles GUI-specific conversions and scaling.

---

## Important project-specific conventions & patterns 📐
- Use underscore (`_`) prefix for internal/private instance variables (e.g., `_current_image`, `_history`).
- `ImageProcessor.get_current_image()` returns a COPY (safe from outside mutation). Prefer it over accessing internals.
- `ImageDisplay` MUST keep a reference to the `PhotoImage` object (the implementation stores it as `self._photo_image`) to avoid garbage collection and disappearing images.
- Ranges & invariants enforced inside processor methods (follow these exact rules when calling or adding features):
  - `apply_blur(intensity)` → intensity forced odd, clamped to >=1 (UI uses 1–25 range).
  - `adjust_brightness(value)` → clamps to [-100, 100].
  - `adjust_contrast(value)` → clamps to [0.5, 3.0].
  - `scale_image(percent)` → clamps to [25, 200] (uses `resize_image` internally).
  - `rotate_image(angle)` → only 90, 180, 270 accepted.
  - `flip_image(direction)` → accepts `'horizontal'` or `'vertical'`.
- History: `ImageProcessor` keeps up to the last 20 states (undo/redo).

---

## How to add features (concise recipe) 🧩
1. Add a pure function/method to `ImageProcessor` that manipulates `self._current_image` and calls `_add_to_history(self._current_image)`.
2. Add a UI control in `ImageEditor._create_controls()` (button/slider etc.).
3. Implement a small wrapper method in `ImageEditor` to call the processor method, then run:
   - `self._refresh_display()`
   - `self._is_modified = True`
   - `self._update_status()`
   - Reset any UI controls (sliders) if intended UX.
4. Verify display behavior (no GC of PhotoImage), and add small unit or manual test (many classes have a `if __name__ == "__main__"` test block).

Example (pattern):
- `self.processor.apply_blur(intensity)` → `self._refresh_display(); self._is_modified=True; self._update_status()`

---

## Integration points & gotchas ⚠️
- Images are OpenCV BGR numpy arrays. `ImageDisplay` converts BGR→RGB then to `PIL.Image` → `ImageTk.PhotoImage`. Any new image-processing code should preserve this format contract.
- Saving uses `cv2.imwrite()` from the processor. Ensure correct file extension and that `self._current_image` is not None.
- GUI uses `tkinter` mainloop; tests that instantiate classes directly (bypass `main.py`) can be used for quick feedback.
- Note: `img_editor.py` test block contains a small bug — it references `ImageEditorApp` instead of `ImageEditor`. Prefer `main.py` as the canonical startup.

---

## Debugging & workflows 🔍
- Manual run for quick iteration: `python main.py` while you modify code. Close window or press Ctrl+C in terminal to stop.
- Use the module-level tests in `img_processor.py` and `img_display.py` to validate core functionality without the full GUI.
- For changes to UI layout, check `ImageEditor._create_layout()` and `_create_controls()` for the scrollable control pattern (canvas + scrollbar + frame).

---

## Files to inspect first (for any task) 📁
- `main.py` — launch flow and user instructions
- `img_editor.py` — GUI wiring and UX patterns
- `img_processor.py` — all image operations and history logic
- `img_display.py` — conversion & display rules
- `requirements.txt` — dependencies (opencv-python, Pillow, numpy)

---

If anything above is unclear or you want examples added (e.g., a suggested unit-test scaffold or a behavior diagram), tell me which section to expand and I will iterate. ✅
