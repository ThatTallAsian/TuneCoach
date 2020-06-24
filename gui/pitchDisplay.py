from tkinter import *
from math import sin, cos, radians
import sys
sys.path.insert(1, '../python_bridge')
from ctypes import *
import threading
from pitch_utilities import *

class PitchDisplay:
    def __init__(self, master, pitch=None, hertz=None, cents=None):
        self.NEEDLE = None
        if not pitch:
            self._pitchValue = 'C' # default display
            self.current_pitch_display = 'C'
        else:
            self._pitchValue = pitch
            self.current_pitch_display = 'C'

        if not hertz:
            self._hertzValue = 261.625565 # middle C - hardcodedstr(event.char)
        else:
            self._hertzValue = hertz

        if not cents:
            self._centsValue = 0
        else:
            self._centsValue = cents

        self._default_cents_bound = 100 # 50 cents below and above is allowed
        super().__init__()
        self.frame = Frame(master)
        self.frame.pack()

        self.title = 'Pitch Information'
        self.label = Label(master, text="Hello World")
        self.label.pack()

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        master.geometry(f'{self.screen_width}x{self.screen_height}')

        self.canvas = Canvas(master, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        print(master.winfo_screenheight(), master.winfo_screenwidth())

        self.display_default_gui()
        self.current_needle_display = self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=self._pitchValue)
        self.display_current_gui()

    def display_current_gui(self):
        self.canvas.delete(self.NEEDLE)
        self.canvas.delete(self.current_needle_display)
        temp = (self._default_cents_bound/2) - self._centsValue
        offset = (temp / self._default_cents_bound) * 90 #90 degrees, 45 offset from start +x
        startValue = offset + 45
        extentValue = 90 - offset

        self.canvas.delete(self.current_pitch_display)
        self.current_pitch_display = self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=self._pitchValue)

        # if startValue > 120:
        #     self.current_needle_display = self.canvas.create_arc(self.screen_width/4,self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        #     self.canvas.itemconfig(self.current_needle_display, fill='red', start=startValue, outline='',extent = extentValue)
        # else if startValue >

        #THIS
        self.current_needle_display = self.canvas.create_arc(self.screen_width / 4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        #THIS
        self.canvas.itemconfig(self.current_needle_display, fill="black", style=PIESLICE, start = startValue, outline = '', extent = extentValue)

        # startAngle = offset + 45
        #
        # center_x = self.screen_width / 2
        # center_y = self.screen_height / 2
        #
        # other_x = center_x + (center_x / 2) * cos(startAngle)
        # other_y = center_y - (center_y / 2) * sin(startAngle)
        #
        # if startAngle < 135 and startAngle > 45:
        #     self.NEEDLE = self.canvas.create_line(center_x, center_y, other_x, other_y)
        # else:
        #     print("Not in cents range")
        # self.canvas.itemconfig(self.NEEDLE, )
        # self.current_needle_display = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        # self.canvas.itemconfig(self.current_needle_display, fill="black", style=PIESLICE, start=startValue, outline='', extent=extentValue)
    def display_default_gui(self):
        pitch_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(pitch_arc, fill="lightgrey", style=PIESLICE, stipple="gray25", start=45, outline='')

        left_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_red_arc, start=120, width=5, fill="#ffbfbf", extent=15, outline='')

        left_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_yellow_arc,  start=95, width=5, fill="#fffeb0", extent=25, outline='')

        green_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(green_arc, start=85, width=5, fill="#ccffbf", extent=10, outline='')

        right_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(right_yellow_arc, start=60, width=5, fill="#fffeb0", extent=25, outline='')

        right_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.itemconfig(right_red_arc, start=45, width=5, fill="#ffbfbf", extent=15, outline='')

    def update_pitch(self, value): # event as parameter
        self._pitchValue = value

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self, value):
        self._centsValue = value # perfectly in tune hardcoded - str(event.char)

    def update_data(self, handle, lib): #event
        # print("updating data based on realtime changes")
        response = c_double()
        success = lib.read_stream(handle, byref(response))
        if success and response:
            hz = response.value
            midi = hz_to_midi(hz)
            pitch_class = midi_to_pitch_class(midi)
            desired_hz = closest_in_tune_frequency(hz)
            cent = cents(desired_hz, hz)
            name = pitch_class_to_name(pitch_class, Accidental.SHARP)
            self.update_cents(cent)
            self.update_hertz()
            self.update_pitch(name)
            self.display_current_gui()

        root.after(10, self.update_data, handle, lib)

def load_library():
    lib = cdll.LoadLibrary("../python_bridge/libPitchDetection.so")
    lib.create_stream.argtypes = [c_int]
    lib.create_stream.restype = c_void_p
    lib.pause_stream.argtypes = [c_void_p]
    lib.resume_stream.argtypes = [c_void_p]
    lib.kill_stream.argtypes = [c_void_p]
    lib.is_alive.argtypes = [c_void_p]
    lib.is_alive.restype = c_bool
    lib.read_stream.restype = c_bool
    lib.read_stream.argtypes = [c_void_p, POINTER(c_double)]
    lib.peek_stream.argtypes = [c_void_p]
    lib.peek_stream.restype = c_double
    return lib

class AudioThread(threading.Thread):
    def __init__(self, handle, lib):
        super().__init__()
        self.handle = handle
        self.lib = lib

    def run(self):
        print("Starting")
        self.lib.start_stream(self.handle)

if __name__ == "__main__":
    root = Tk()
    root.title("TuneCoach")
    pitch = PitchDisplay(root)

    lib = load_library()
    handle = lib.create_stream(44100)
    audio = AudioThread(handle, lib)
    audio.start()
    root.after(10, pitch.update_data, handle, lib)
    root.mainloop()
