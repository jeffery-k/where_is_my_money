from tkinter import *
import tkinter.scrolledtext as tkst
from threading import Thread, Lock, Event


HORIZONTAL_PADDING = 10
VERTICAL_PADDING = 10
WINDOW_GEOMETRY = '500x600'
FOREGROUND_COLOR = 'white'
BACKGROUND_COLOR = 'grey'
FONT = ('Courier', 15)

BUTTON_ENTER = "Continue"
THIN_DIVIDER = "\n------------------------------\n"



class Display(Thread):
    def __init__(self, string='', title='', finalizer=None):
        if title == '':
            title = 'Display'

        self.string = string
        self.title = title
        self.finalizer = finalizer
        self.buttons_active = False
        self.event = Event()
        self.lock = Lock()
        self.logs = []

        super().__init__(daemon=True)
        self.start()
        self.event.wait()
        self.event.clear()

    def run(self):
        self.window = Tk()
        self.window.title(self.title)
        self.window.configure(bg=BACKGROUND_COLOR)
        self.window.geometry(WINDOW_GEOMETRY)

        self.text_frame = tkst.Frame(master=self.window, bg=BACKGROUND_COLOR)
        self.text_box = tkst.ScrolledText(master=self.text_frame, font=FONT,
                                          bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                                          width=60, height=30, wrap=WORD)
        self.inputs = ButtonSet(self.window, event=self.event)

        self.text_frame.pack(fill=BOTH, expand=YES)
        self.text_box.pack(padx=HORIZONTAL_PADDING, pady=VERTICAL_PADDING,
                           fill=BOTH, expand=True)
        self.event.set()

        self.window.mainloop()

        if self.finalizer is not None:
            self.finalizer.finalize()

    def print(self, string=''):
        with self.lock:
            self.string = string
        self.redraw()

    def input(self, string='', options=None):
        with self.lock:
            self.inputs.clear_buttons()
            self.string = '\n' + string

            if options:
                for option in options:
                    self.inputs.add_button(option)
                self.buttons_active = True
                self.redraw()
                value = self.inputs.harvest()
            else:
                self.inputs.add_text_field()
                self.buttons_active = True
                self.redraw()
                value = self.inputs.harvest()
        return value

    def redraw(self):
        if self.buttons_active:
            self.inputs.pack()
        else:
            self.inputs.unpack()

        self.text_box.configure(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.insert(END, self.string)
        self.text_box.configure(state=DISABLED)


class ButtonSet:
    def __init__(self, window, event):
        self.window = window

        self.buttons = []
        self.result = None
        self.event = event

    def clear_buttons(self):
        for button in self.buttons:
            button.pack_forget()
        self.buttons = []

    def add_button(self, string=''):
        text = string if string is not '' else BUTTON_ENTER
        button = Button(self.window, text=text, font=FONT,
                        bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                        command=(lambda: self.plant(string)))
        self.buttons.append(button)

    def add_text_field(self):
        entry = Entry(self.window)
        button = Button(self.window, text=BUTTON_ENTER, font=FONT,
                        bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR,
                        command=(lambda: self.plant(entry.get())))
        self.buttons.append(entry)
        self.buttons.append(button)

    def pack(self):
        for button in self.buttons:
            button.pack()

    def unpack(self):
        for button in self.buttons:
            button.pack_forget()

    def plant(self, seed):
        self.result = seed
        self.event.set()

    def harvest(self):
        self.event.wait()
        result = self.result
        self.result = None
        self.event.clear()
        return result
