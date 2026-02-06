import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import cv2


class ImageDisplay:
   
    
    def __init__(self, parent, width=800, height=600):
        
        # Saves dimensions 
        self._width = width
        self._height = height
        
        self._photo_image = None
        self._canvas = Canvas(
            parent,
            width=width,
            height=height,
            bg='#fef9f3',  
            highlightthickness=2,
            highlightbackground='#b4a5d3', 
            highlightcolor='#d4c5f9'  
        )
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._show_placeholder()
        
        self._image_id = None
    
    
    def _show_placeholder(self):
       
        # Background rectangle for placeholder
        self._placeholder_bg = self._canvas.create_rectangle(
            self._width // 2 - 200,
            self._height // 2 - 100,
            self._width // 2 + 200,
            self._height // 2 + 100,
            fill='#ffeef2',  
            outline='#b4a5d3',  
            width=2
        )
        
        self._placeholder_icon = self._canvas.create_text(
            self._width // 2,
            self._height // 2 - 40,
            text="Photo",
            fill='#b4a5d3',  
            font=('Arial', 48)
        )
        
     
        self._placeholder_text = self._canvas.create_text(
            self._width // 2,
            self._height // 2 + 20,
            text="No Image Loaded",
            fill='#8b7fa8',  
            font=('Arial', 16, 'bold'),
            justify=tk.CENTER
        )
        
       
        self._placeholder_subtitle = self._canvas.create_text(
            self._width // 2,
            self._height // 2 + 50,
            text="Click 'File → Open' to load an image",
            fill='#a899c7',  # Light purple-gray
            font=('Arial', 11),
            justify=tk.CENTER
        )
    
    
    def display_image(self, cv_image):
        if cv_image is None:
            return
        
        if hasattr(self, '_placeholder_bg'):
            self._canvas.delete(self._placeholder_bg)
            self._canvas.delete(self._placeholder_icon)
            self._canvas.delete(self._placeholder_text)
            self._canvas.delete(self._placeholder_subtitle)
        
        # Step 1- Converts BGR to RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Step 2- Gets image size
        height, width = rgb_image.shape[:2]
        
   
        scale_width = self._width / width
        scale_height = self._height / height
        scale = min(scale_width, scale_height)
        
        if scale > 1.0:
            scale = 1.0
        
        # Calculates new size
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resizes if needed
        if scale < 1.0:
            rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Step 3- Converts to PIL Image
        pil_image = Image.fromarray(rgb_image)
        
        # Step 4- Converts to PhotoImage
        self._photo_image = ImageTk.PhotoImage(pil_image)
        
        # Step 5- Calculates position to center image
        x = (self._width - new_width) // 2
        y = (self._height - new_height) // 2
        
        # Step 6- Display on canvas
        if self._image_id:
            self._canvas.delete(self._image_id) 
        
        self._image_id = self._canvas.create_image(
            x, y,
            anchor=tk.NW,
            image=self._photo_image
        )
    
    
    def clear(self):
        self._canvas.delete("all")
        self._image_id = None
        self._photo_image = None
        self._show_placeholder()