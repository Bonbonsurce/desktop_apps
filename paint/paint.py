import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint")

        self.current_shape = "Freehand"
        self.brush_size = 5
        self.brush_color = "black"
        self.drawing = False
        self.current_shape_id = None  # ID текущей фигуры
        self.start_x, self.start_y = None, None
        self.last_x, self.last_y = None, None

        self.canvas = tk.Canvas(root, bg="white")

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side=tk.TOP)

        self.button_line = ttk.Button(self.button_frame, text="Line")
        self.button_rectangle = ttk.Button(self.button_frame, text="Rectangle")
        self.button_square = ttk.Button(self.button_frame, text="Square")
        self.button_oval = ttk.Button(self.button_frame, text="Oval")
        self.button_freehand = ttk.Button(self.button_frame, text="Freehand")
        self.button_color = ttk.Button(self.button_frame, text="Change color")
        self.combobox = ttk.Combobox(self.button_frame, values=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        self.combobox.set(self.brush_size)
        self.button_eraser = ttk.Button(self.button_frame, text="Eraser")
        self.button_clear_all = ttk.Button(self.button_frame, text="Clear all")

        self.button_line.pack(side=tk.LEFT)
        self.button_rectangle.pack(side=tk.LEFT)
        self.button_square.pack(side=tk.LEFT)
        self.button_oval.pack(side=tk.LEFT)
        self.button_freehand.pack(side=tk.LEFT)
        self.button_color.pack(side=tk.LEFT)
        self.combobox.pack(side=tk.LEFT)
        self.button_eraser.pack(side=tk.LEFT)
        self.button_clear_all.pack(side=tk.LEFT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_line.bind("<Button-1>", self.set_shape_line)
        self.button_rectangle.bind("<Button-1>", self.set_shape_rectangle)
        self.button_square.bind("<Button-1>", self.set_shape_square)
        self.button_oval.bind("<Button-1>", self.set_shape_oval)
        self.button_freehand.bind("<Button-1>", self.set_shape_freehand)
        self.button_color.bind("<Button-1>", self.change_brush_color)
        self.combobox.bind("<<ComboboxSelected>>", self.combobox_select)
        self.button_eraser.bind("<Button-1>", self.eraser)
        self.button_clear_all.bind("<Button-1>", self.clear_all)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def set_shape_line(self, event):
        self.current_shape = "Line"

    def set_shape_rectangle(self, event):
        self.current_shape = "Rectangle"

    def set_shape_oval(self, event):
        self.current_shape = "Oval"

    def set_shape_square(self, event):
        self.current_shape = "Square"

    def set_shape_freehand(self, event):
        self.current_shape = "Freehand"

    def start_drawing(self, event):
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y
        self.last_x, self.last_y = event.x, event.y

    def stop_drawing(self, event):
        self.drawing = False
        self.current_shape_id = None

    def draw(self, event):
        if self.drawing:
            end_x, end_y = event.x, event.y

            if self.current_shape_id:
                self.canvas.delete(self.current_shape_id)

            if self.current_shape == "Freehand":
                self.canvas.create_line(self.last_x, self.last_y, end_x, end_y, fill=self.brush_color, width=self.brush_size)
                self.last_x, self.last_y = end_x, end_y
            else:
                if self.current_shape == "Line":
                    self.current_shape_id = self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill=self.brush_color, width=self.brush_size)
                elif self.current_shape == "Oval":
                    self.current_shape_id = self.canvas.create_oval(self.start_x, self.start_y, end_x, end_y, fill=self.brush_color, outline=self.brush_color)
                elif self.current_shape == "Rectangle":
                    self.current_shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, fill=self.brush_color, outline=self.brush_color)
                elif self.current_shape == "Square":
                    side_length = min(abs(end_x - self.start_x), abs(end_y - self.start_y))
                    if end_x < self.start_x:
                        end_x = self.start_x - side_length
                    else:
                        end_x = self.start_x + side_length
                    if end_y < self.start_y:
                        end_y = self.start_y - side_length
                    else:
                        end_y = self.start_y + side_length
                    self.current_shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, fill=self.brush_color, outline=self.brush_color)

    def combobox_select(self, event):
        self.brush_size = int(self.combobox.get())

    def change_brush_color(self, event):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def eraser(self, event):
        self.current_shape = "Freehand"
        self.brush_color = "white"

    def clear_all(self, event):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
