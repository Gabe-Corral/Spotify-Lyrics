import tkinter as tk

class About:

    def __init__(self, parent, child, info):
        self.parent = parent
        self.child = child
        self.info = info
        self.display_about_info()

    def display_about_info(self):
        """Displays info about the song or artist"""
        self.child.configure(bg='#586e75')
        self.child.wm_title("About")
        self.child.geometry("830x300")

        self.wrapper = tk.LabelFrame(self.child, width=780)
        self.canvas = tk.Canvas(self.wrapper, width=780)
        self.canvas.pack(side=tk.LEFT, fill="both")
        self.y_scroll = tk.Scrollbar(self.wrapper, orient="vertical",
        command=self.canvas.yview)

        self.x_scroll = tk.Scrollbar(self.wrapper, orient="horizontal",
        command=self.canvas.xview)

        self.y_scroll.pack(side=tk.RIGHT, fill="both")

        self.x_scroll.pack(side=tk.BOTTOM, fill="both")

        self.frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.y_scroll.set, bg='#586e75',
        xscrollcommand=self.x_scroll.set)

        self.canvas.bind("<Configure>",
        lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.wrapper.pack(fill="both", side="left")

        info_label = tk.Label(self.frame, text=self.info,
        bg="#586e75", fg="#073642")
        info_label.pack()
