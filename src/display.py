from tkinter import *
import tkinter.scrolledtext as tkst
from threading import Thread, Lock, Event


HORIZONTAL_PADDING = 10
VERTICAL_PADDING = 10
WINDOW_GEOMETRY = '600x800'
FOREGROUND_COLOR = 'white'
BACKGROUND_COLOR = 'black'
FONT = ('Courier', 15)

BUTTON_ENTER = "Press to Continue"

INVALID = "INPUT INVALID!"
PROCESSING = "PROCESSING ;)"

THICK_DIVIDER = "\n==============================\n"
THIN_DIVIDER = "\n------------------------------\n"
MICRO_DIVIDER = "\n---------------\n"
TEENY_DIVIDER = "\n-----\n"
THICK_SEPARATOR = "||"
THIN_SEPARATOR = "|"


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
        self.buttons = ButtonSet(self.window, event=self.event)

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

    def input(self, string='', prompt='', options=None):
        with self.lock:
            self.buttons.clear_buttons()
            self.string = THICK_DIVIDER + '\n' + string
            if '' != prompt:
                self.string += '\n' + THICK_SEPARATOR
                self.string += '  ' + prompt + '\n'
            if options:
                for option in options:
                    self.buttons.add_button(option)
                self.buttons_active = True
                self.redraw()
                value = self.buttons.harvest()
            else:
                pass
                #TODO text input

        self.processing()
        return value

    def processing(self):
        self.string += '\n\n' + THICK_DIVIDER + '\n' + PROCESSING
        self.buttons_active = False
        self.redraw()

    def log(self, string):
        self.logs.append('LOG:\n' + string)

    def redraw(self):
        if self.buttons_active:
            self.buttons.pack()
        else:
            self.buttons.unpack()

        self.text_box.configure(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.insert(END, self.string)
        self.text_box.configure(state=DISABLED)


class ButtonSet:
    def __init__(self, window, event=None):
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

    def pack(self):
        for button in self.buttons:
            button.pack()

    def unpack(self):
        for button in self.buttons:
            button.pack_forget()

    def plant(self, seed):
        self.result = seed
        if self.event is not None:
            self.event.set()

    def harvest(self):
        if self.event is not None:
            self.event.wait()
            self.event.clear()

        result = self.result
        self.result = None
        return result
