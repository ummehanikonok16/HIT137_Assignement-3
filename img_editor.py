import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from img_processor import ImageProcessor
from img_display import ImageDisplay


class ImageEditor:
    
    def __init__(self, root):
       
        self.root = root
        self.root.title("Image Editor - HIT137 Assignment 3 (SYD_Group05)")
        self.root.geometry("1400x850")
        
        self.colors = {
            'bg_dark': '#faf8f3',         
            'bg_medium': '#fff9f0',       
            'bg_light': '#ffeef2',        
            'accent': '#b4a5d3',          
            'accent_bright': '#d4c5f9',   
            'text_light': '#4a4a4a',      
            'text_medium': '#8b7fa8',     
            'text_dark': '#5d5d5d',       
            'success': '#a8d5ba',         
            'warning': '#ffd4a3'          
        }
        
        # Configures root window
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Creates the image processor
        self.processor = ImageProcessor()
        
        # Tracks current file
        self._current_file = ""
        self._is_modified = False
        
        # Setups modern theme
        self._setup_theme()
        
        # Creates the GUI
        self._create_menu()
        self._create_header()
        self._create_layout()
        self._create_controls()
        self._create_status_bar()
        
    
    def _setup_theme(self):
        """Setup modern ttk theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_light'],
                       bordercolor=self.colors['accent'],
                       darkcolor=self.colors['bg_dark'],
                       lightcolor=self.colors['bg_light'],
                       troughcolor=self.colors['bg_dark'],
                       focuscolor=self.colors['accent_bright'],
                       selectbackground=self.colors['accent'],
                       selectforeground=self.colors['text_light'],
                       fieldbackground=self.colors['bg_light'],
                       font=('Segoe UI', 10))
        
        # Button styling
        style.configure('TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=10,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('TButton',
                 background=[('active', self.colors['accent_bright']),
                            ('pressed', '#0a5c5f')])
        
        # Label styling
        style.configure('TLabel',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10))
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['accent_bright'])
        
        style.configure('Section.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['accent_bright'])
        
        # Frame styling
        style.configure('TFrame',
                       background=self.colors['bg_medium'],
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_light'],
                       relief='flat')
        
        # Separator
        style.configure('TSeparator',
                       background=self.colors['accent'])
        
        # Scale/Slider
        style.configure('TScale',
                       background=self.colors['bg_medium'],
                       troughcolor=self.colors['bg_dark'],
                       borderwidth=0,
                       sliderrelief='flat')
    
    
    def _create_menu(self):
        """Creates modern menu bar"""
        menubar = tk.Menu(self.root,
                         bg=self.colors['bg_medium'],
                         fg=self.colors['text_light'],
                         activebackground=self.colors['accent'],
                         activeforeground=self.colors['text_light'],
                         borderwidth=0)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.colors['bg_medium'],
                           fg=self.colors['text_light'],
                           activebackground=self.colors['accent'],
                           activeforeground=self.colors['text_light'])
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self._open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_app, accelerator="Alt+F4")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.colors['bg_medium'],
                           fg=self.colors['text_light'],
                           activebackground=self.colors['accent'],
                           activeforeground=self.colors['text_light'])
        menubar.add_cascade(label="✏️ Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self._undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self._redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset to Original", command=self._reset, accelerator="Ctrl+R")
    
    
    def _create_header(self):
        """Create attractive header bar"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = ttk.Label(header_frame,
                               text="Image Editor",
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Quick action buttons
        button_frame = tk.Frame(header_frame, bg=self.colors['bg_medium'])
        button_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self._create_icon_button(button_frame, "📂 Open", self._open_image, 0)
        self._create_icon_button(button_frame, "💾 Save", self._save_image, 1)
        self._create_icon_button(button_frame, "↶ Undo", self._undo, 2)
        self._create_icon_button(button_frame, "↷ Redo", self._redo, 3)
    
    
    def _create_icon_button(self, parent, text, command, column):
        """Create modern icon button"""
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=self.colors['accent'],
                       fg=self.colors['text_light'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       padx=15,
                       pady=8,
                       cursor='hand2',
                       borderwidth=0)
        btn.grid(row=0, column=column, padx=5)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['accent_bright']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.colors['accent']))
        
        return btn
    
    
    def _create_layout(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Image display
        display_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Creates the image display
        self.display = ImageDisplay(display_frame, 900, 650)
    
    
    def _create_controls(self):
        # Right side: Control panel with card design
        control_frame = tk.Frame(self.main_frame,
                                bg=self.colors['bg_medium'],
                                width=350)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=0)
        control_frame.pack_propagate(False)
        
        # Title with icon
        title_frame = tk.Frame(control_frame, bg=self.colors['bg_medium'])
        title_frame.pack(pady=15)
        
        title = ttk.Label(title_frame,
                         text="🎛️ Controls",
                         style='Header.TLabel',
                         font=('Segoe UI', 18, 'bold'))
        title.pack()
        
        subtitle = ttk.Label(title_frame,
                            text="Adjust & Transform",
                            foreground=self.colors['text_medium'],
                            background=self.colors['bg_medium'],
                            font=('Segoe UI', 10))
        subtitle.pack()
        
        # Creates scrollable area
        canvas = tk.Canvas(control_frame,
                          bg=self.colors['bg_medium'],
                          highlightthickness=0,
                          width=330)
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        
        # Basic Filters Section
        self._add_section(scroll_frame, "🎨 Basic Filters")
        
        filter_frame = self._create_card(scroll_frame)
        
        self._create_styled_button(filter_frame, "Grayscale", self._apply_grayscale, "⚫")
        self._create_styled_button(filter_frame, "Edge Detection", self._apply_edges, "🔲")
        
        # Blur Section
        self._add_section(scroll_frame, "💫 Blur Effect")
        
        blur_card = self._create_card(scroll_frame)
        
        self.blur_var = tk.IntVar(value=5)
        
        blur_label_frame = tk.Frame(blur_card, bg=self.colors['bg_light'])
        blur_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(blur_label_frame, text="Intensity:",
                 background=self.colors['bg_light']).pack(side=tk.LEFT)
        
        self.blur_label = ttk.Label(blur_label_frame, text="5",
                                    foreground=self.colors['accent_bright'],
                                    background=self.colors['bg_light'],
                                    font=('Segoe UI', 10, 'bold'))
        self.blur_label.pack(side=tk.RIGHT)
        
        blur_slider = ttk.Scale(blur_card, from_=1, to=25,
                               orient=tk.HORIZONTAL, variable=self.blur_var)
        blur_slider.pack(pady=5, padx=10, fill=tk.X)
        blur_slider.config(command=lambda v: self.blur_label.config(text=f"{int(float(v))}"))
        
        self._create_styled_button(blur_card, "Apply Blur", self._apply_blur, "💫")
        
        # Brightness Section
        self._add_section(scroll_frame, "☀️ Brightness")
        
        bright_card = self._create_card(scroll_frame)
        
        self.brightness_var = tk.IntVar(value=0)
        
        bright_label_frame = tk.Frame(bright_card, bg=self.colors['bg_light'])
        bright_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(bright_label_frame, text="Adjustment:",
                 background=self.colors['bg_light']).pack(side=tk.LEFT)
        
        self.brightness_label = ttk.Label(bright_label_frame, text="0",
                                          foreground=self.colors['accent_bright'],
                                          background=self.colors['bg_light'],
                                          font=('Segoe UI', 10, 'bold'))
        self.brightness_label.pack(side=tk.RIGHT)
        
        brightness_slider = ttk.Scale(bright_card, from_=-100, to=100,
                                     orient=tk.HORIZONTAL, variable=self.brightness_var)
        brightness_slider.pack(pady=5, padx=10, fill=tk.X)
        brightness_slider.config(command=lambda v: self.brightness_label.config(text=f"{int(float(v))}"))
        
        self._create_styled_button(bright_card, "Apply Brightness", self._apply_brightness, "☀️")
        
        # Contrast Section
        self._add_section(scroll_frame, "◐ Contrast")
        
        contrast_card = self._create_card(scroll_frame)
        
        self.contrast_var = tk.DoubleVar(value=1.0)
        
        contrast_label_frame = tk.Frame(contrast_card, bg=self.colors['bg_light'])
        contrast_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(contrast_label_frame, text="Multiplier:",
                 background=self.colors['bg_light']).pack(side=tk.LEFT)
        
        self.contrast_label = ttk.Label(contrast_label_frame, text="1.0",
                                        foreground=self.colors['accent_bright'],
                                        background=self.colors['bg_light'],
                                        font=('Segoe UI', 10, 'bold'))
        self.contrast_label.pack(side=tk.RIGHT)
        
        contrast_slider = ttk.Scale(contrast_card, from_=0.5, to=3.0,
                                   orient=tk.HORIZONTAL, variable=self.contrast_var)
        contrast_slider.pack(pady=5, padx=10, fill=tk.X)
        contrast_slider.config(command=lambda v: self.contrast_label.config(text=f"{float(v):.1f}"))
        
        self._create_styled_button(contrast_card, "Apply Contrast", self._apply_contrast, "◐")
        
        # Rotation Section
        self._add_section(scroll_frame, "🔄 Rotation")
        
        rotation_card = self._create_card(scroll_frame)
        
        rotation_frame = tk.Frame(rotation_card, bg=self.colors['bg_light'])
        rotation_frame.pack(pady=5, fill=tk.X)
        
        self._create_compact_button(rotation_frame, "90°", lambda: self._rotate(90)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self._create_compact_button(rotation_frame, "180°", lambda: self._rotate(180)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self._create_compact_button(rotation_frame, "270°", lambda: self._rotate(270)).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Flip Section
        self._add_section(scroll_frame, "🔃 Flip")
        
        flip_card = self._create_card(scroll_frame)
        
        flip_frame = tk.Frame(flip_card, bg=self.colors['bg_light'])
        flip_frame.pack(pady=5, fill=tk.X)
        
        self._create_compact_button(flip_frame, "↔️ Horizontal", lambda: self._flip('horizontal')).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self._create_compact_button(flip_frame, "↕️ Vertical", lambda: self._flip('vertical')).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Scale Section
        self._add_section(scroll_frame, "📏 Resize / Scale")
        
        scale_card = self._create_card(scroll_frame)
        
        self.scale_var = tk.IntVar(value=100)
        
        scale_label_frame = tk.Frame(scale_card, bg=self.colors['bg_light'])
        scale_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(scale_label_frame, text="Scale:",
                 background=self.colors['bg_light']).pack(side=tk.LEFT)
        
        self.scale_label = ttk.Label(scale_label_frame, text="100%",
                                     foreground=self.colors['accent_bright'],
                                     background=self.colors['bg_light'],
                                     font=('Segoe UI', 10, 'bold'))
        self.scale_label.pack(side=tk.RIGHT)
        
        scale_slider = ttk.Scale(scale_card, from_=25, to=200,
                                orient=tk.HORIZONTAL, variable=self.scale_var)
        scale_slider.pack(pady=5, padx=10, fill=tk.X)
        scale_slider.config(command=lambda v: self.scale_label.config(text=f"{int(float(v))}%"))
        
        self._create_styled_button(scale_card, "Apply Scale", self._apply_scale, "📏")
    
    
    def _create_card(self, parent):
        """Create a card-style frame"""
        card = tk.Frame(parent,
                       bg=self.colors['bg_light'],
                       relief='flat',
                       borderwidth=0)
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # Add padding inside card
        inner_frame = tk.Frame(card, bg=self.colors['bg_light'])
        inner_frame.pack(fill=tk.BOTH, padx=15, pady=15)
        
        return inner_frame
    
    
    def _add_section(self, parent, title):
        """Add modern section header"""
        section_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        section_frame.pack(fill=tk.X, pady=(15, 5), padx=10)
        
        label = ttk.Label(section_frame,
                         text=title,
                         style='Section.TLabel')
        label.pack(side=tk.LEFT)
        
        # Decorative line
        line = tk.Frame(section_frame,
                       bg=self.colors['accent'],
                       height=2)
        line.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    
    def _create_styled_button(self, parent, text, command, icon=""):
        """Create modern styled button"""
        btn_text = f"{icon} {text}" if icon else text
        
        btn = tk.Button(parent,
                       text=btn_text,
                       command=command,
                       bg=self.colors['accent'],
                       fg=self.colors['text_light'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       padx=20,
                       pady=10,
                       cursor='hand2',
                       borderwidth=0)
        btn.pack(pady=5, fill=tk.X)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['accent_bright']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.colors['accent']))
        
        return btn
    
    
    def _create_compact_button(self, parent, text, command):
        """Create compact button for grouped controls"""
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=self.colors['accent'],
                       fg=self.colors['text_light'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       padx=10,
                       pady=8,
                       cursor='hand2',
                       borderwidth=0)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['accent_bright']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.colors['accent']))
        
        return btn
    
    
    def _create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = tk.Frame(self.root,
                                  bg=self.colors['bg_medium'],
                                  height=40)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        # Status icon
        self.status_icon = tk.Label(self.status_bar,
                                    text="●",
                                    fg=self.colors['success'],
                                    bg=self.colors['bg_medium'],
                                    font=('Arial', 16))
        self.status_icon.pack(side=tk.LEFT, padx=10)
        
        # Status text
        self.status_label = tk.Label(self.status_bar,
                                     text="Ready | No image loaded",
                                     fg=self.colors['text_light'],
                                     bg=self.colors['bg_medium'],
                                     font=('Segoe UI', 10),
                                     anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    
    def _update_status(self, message=None, status='ready'):
        """Update the status bar with current image info"""
        if message:
            text = message
        else:
            info = self.processor.get_image_info()
            
            if info['width'] > 0:
                filename = os.path.basename(self._current_file) if self._current_file else "Untitled"
                modified = " (Modified)" if self._is_modified else ""
                text = f"{filename}{modified} | {info['width']}x{info['height']} | {info['channels']} channels"
            else:
                text = "Ready | No image loaded"
        
        # Update icon color based on status
        if status == 'success':
            self.status_icon.config(fg=self.colors['success'])
        elif status == 'warning':
            self.status_icon.config(fg=self.colors['warning'])
        else:
            self.status_icon.config(fg=self.colors['accent'])
        
        self.status_label.config(text=text)
    
    
    def _open_image(self):
        """Open an image file"""
        filetypes = (
            ('All Images', '*.jpg *.jpeg *.png *.bmp *.gif'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        )
        
        filepath = filedialog.askopenfilename(
            title="Open Image",
            filetypes=filetypes
        )
        
        if filepath:
            if self.processor.load_image(filepath):
                self._current_file = filepath
                self._is_modified = False
                self._refresh_display()
                self._update_status(status='success')
                messagebox.showinfo("Success", "Image loaded successfully!")
            else:
                self._update_status("Failed to load image", status='warning')
                messagebox.showerror("Error", "Failed to load image")
    
    
    def _save_image(self):
        """Save the current image"""
        if not self._current_file:
            self._save_as()
            return
        
        if self.processor.save_image(self._current_file):
            self._is_modified = False
            self._update_status(status='success')
            messagebox.showinfo("Success", "Image saved successfully!")
        else:
            self._update_status("Failed to save image", status='warning')
            messagebox.showerror("Error", "Failed to save image")
    
    
    def _save_as(self):
        """Save with a new filename"""
        filetypes = (
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg'),
            ('All files', '*.*')
        )
        
        filepath = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=filetypes
        )
        
        if filepath:
            if self.processor.save_image(filepath):
                self._current_file = filepath
                self._is_modified = False
                self._update_status(status='success')
                messagebox.showinfo("Success", "Image saved successfully!")
            else:
                self._update_status("Failed to save image", status='warning')
                messagebox.showerror("Error", "Failed to save image")
    
    
    def _exit_app(self):
        """Exit the application"""
        if self._is_modified:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Save changes before exiting?"
            )
            if result is None:
                return
            elif result:
                self._save_image()
        
        self.root.destroy()
    
    
    def _undo(self):
        """Undo last action"""
        if self.processor.undo():
            self._refresh_display()
            self._is_modified = True
            self._update_status()
    
    
    def _redo(self):
        """Redo last undone action"""
        if self.processor.redo():
            self._refresh_display()
            self._is_modified = True
            self._update_status()
    
    
    def _reset(self):
        """Reset to original image"""
        if messagebox.askyesno("Reset", "Reset to original image?"):
            self.processor.reset_to_original()
            self._refresh_display()
            self._is_modified = False
            self._update_status()
    
    
    def _apply_grayscale(self):
        """Apply grayscale filter"""
        self.processor.convert_to_grayscale()
        self._refresh_display()
        self._is_modified = True
        self._update_status()
    
    
    def _apply_blur(self):
        intensity = self.blur_var.get()
        self.processor.apply_blur(intensity)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
    
    
    def _apply_edges(self):
        self.processor.detect_edges()
        self._refresh_display()
        self._is_modified = True
        self._update_status()
    
    
    def _apply_brightness(self):
        value = self.brightness_var.get()
        self.processor.adjust_brightness(value)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
        self.brightness_var.set(0)
        self.brightness_label.config(text="0")
    
    
    def _apply_contrast(self):
        value = self.contrast_var.get()
        self.processor.adjust_contrast(value)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
        self.contrast_var.set(1.0)
        self.contrast_label.config(text="1.0")
    
    
    def _rotate(self, angle):
        self.processor.rotate_image(angle)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
    
    
    def _flip(self, direction):
        self.processor.flip_image(direction)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
    
    
    def _apply_scale(self):
        percent = self.scale_var.get()
        self.processor.scale_image(percent)
        self._refresh_display()
        self._is_modified = True
        self._update_status()
        self.scale_var.set(100)
        self.scale_label.config(text="100%")
    
    
    def _refresh_display(self):
        """Refresh the display with current image"""
        current_image = self.processor.get_current_image()
        
        if current_image is not None:
            self.display.display_image(current_image)
    
    
    def run(self):
        """Start the application"""
        self.root.mainloop()