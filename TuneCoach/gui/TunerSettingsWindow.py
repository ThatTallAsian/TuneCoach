import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.python_bridge.pitch_utilities import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def input_check(self, new_cents, f_note, f_oct, t_note, t_oct, window):
        keytype = KeySignatureType[self.ktype.get().upper()]
        low = string_to_pitch_class(f_note)
        high = string_to_pitch_class(t_note)
        from_midi = pitch_with_octave(low, int(f_oct))
        to_midi = pitch_with_octave(high, int(t_oct))

        if from_midi >= to_midi:
            error_frame_style = ttk.Style()
            error_frame_style.configure('ErrorFrame.TFrame', background=Colors.background, border=5)

            error_frame = ttk.Frame(window, style='ErrorFrame.TFrame')
            error_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")

            error_label_style = ttk.Style()
            error_label_style.configure('ErrorLabel.TLabel', background=Colors.background, font=(None, 12), foreground='red')
            error_label = ttk.Label(error_frame, text="Invalid Note Range!", style='ErrorLabel.TLabel')
            error_label.pack()
        else:
            self.update_tuner_settings(new_cents, self.current_key_signature, from_midi, to_midi, window)

    def update_tuner_settings(self, cent_threshold, key_signature, from_midi, to_midi, oldSettingsView):
        self.mainWindow.controller.update_tuner_settings(cent_threshold, key_signature, from_midi, to_midi)
        oldSettingsView.destroy()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        data = mainWindow.controller.session.data
        tuner_settings_window = tk.Toplevel(self.mainWindow.master)
        tuner_settings_window.geometry("500x300")

        tuner_settings_window.grid()

        top_frame = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        middle_frame1 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        middle_frame2 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        middle_frame3 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        # bottom_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        # bottom_frame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        # bottom_frame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomest_frame = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        # top_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        # middle_frame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        # middle_frame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        #middle_frame3 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        bottom_frame1 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        bottom_frame2 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        bottom_frame3 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        range_frame1 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        range_frame2 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        range_frame3 = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)
        done_frame = ttk.Frame(tuner_settings_window)#, bd=5, bg=background_color)

        # putting the frames into a grid layout
        top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        middle_frame1.grid(row=1, column=0, columnspan=1, sticky="nsew")
        middle_frame2.grid(row=1, column=1, sticky="nsew")
        middle_frame3.grid(row=1, column=2, sticky="nsew")
        bottom_frame1.grid(row=2, column=0, sticky="nsew")
        bottom_frame2.grid(row=2, column=1, sticky="nsew")
        bottom_frame3.grid(row=2, column=2, sticky="nsew")
        range_frame1.grid(row=3, column=0, sticky="nsew")
        range_frame2.grid(row=3, column=1, sticky="nsew")
        range_frame3.grid(row=3, column=2, sticky="nsew")
        done_frame.grid(row=5, column=0, columnspan=3, sticky="nsew")

        # setting up grid weights.

        tuner_settings_window.grid_rowconfigure(0, weight=1)
        tuner_settings_window.grid_rowconfigure(1, weight=5)
        tuner_settings_window.grid_rowconfigure(1, weight=5)
        tuner_settings_window.grid_rowconfigure(3, weight=1)
        tuner_settings_window.grid_columnconfigure(0, weight=1)
        tuner_settings_window.grid_columnconfigure(1, weight=1)
        tuner_settings_window.grid_columnconfigure(2, weight=1)

        tuner_label = ttk.Label(top_frame, text="Tuner Settings")#, font=("Calibri", 20))
        # tuner_label.config(bg=background_color, fg="white")
        tuner_label.pack()


        centsitivity = ttk.Label(middle_frame1, text="Margin of Acceptable Pitch Error +- ")
        # centsitivity.config(bg=background_color, fg="white")

        # centsitivity = tk.Label(middle_frame1, text="Margin of Acceptable Pitch Error +- ")
        # centsitivity.config(bg=background_color, fg="white")

        centsitivity.pack()

        v = tk.DoubleVar()
        v.set(data.green_thresh)

        cent_scale = tk.Scale(middle_frame2, from_=1, to=25, orient=tk.HORIZONTAL, variable=v)
        cent_scale.config(bg=Colors.background, fg="white")
        cent_scale.pack()

        in_cents = tk.Label(middle_frame3, text="cents")
        in_cents.config(bg=Colors.background, fg="white")
        in_cents.pack()

        sig_label = tk.Label(bottom_frame1, text="Key Signature")
        sig_label.config(bg=Colors.background, fg="white")
        sig_label.pack()

        range_label = tk.Label(range_frame1, text="Note Range")
        range_label.config(bg=Colors.background, fg="white")
        range_label.pack()

        # TODO: extract into keysignature and allow for better initialization, create circle-of-fifths-based data structure
        self.major_key_names = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
        self.major_accidentals = [Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.SHARP,
                                        Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]
        self.major_numbers = [0, 5, 2, 3, 4, 1, 6, 1, 4, 3, 2, 5] # number of sharps/flats in each key
        self.minor_key_names = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
        self.minor_accidentals = [Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                        Accidental.SHARP, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]
        self.minor_numbers = [3, 4, 1, 6, 1, 4, 3, 2, 5, 0, 5, 2]


        self.current_key_signature = data.key_signature
        current_type = data.key_signature.ktype
        self.root = tk.IntVar(value=self.current_key_signature.raw_value)
        self.ktype = tk.StringVar(value=current_type.value)
        self.radio_buttons = []

        # Grid of key signature buttons
        for i in range(0, 12):
            name = ""
            if current_type == KeySignatureType.MINOR:
                name = self.minor_key_names[i]
            else:
                name = self.major_key_names[i]
            button = tk.Radiobutton(bottom_frame2, text=name, indicatoron=0, width=3, variable=self.root, value=i, command=self.selection_changed)
            button.grid(row=i//4 + 1, column=i%4)
            self.radio_buttons.append(button)

        major_button = tk.Radiobutton(bottom_frame3, text="Major", indicatoron=0, width=6, variable=self.ktype, value="Major", command=self.selection_changed)
        major_button.grid(row=1, column=0)
        minor_button = tk.Radiobutton(bottom_frame3, text="Minor", indicatoron=0, width=6, variable=self.ktype, value="Minor", command=self.selection_changed)
        minor_button.grid(row=2, column=0)


        # MIDI RANGE SELECTION
        self.from_note = tk.StringVar(value=data.lowest_note)
        from_octave = tk.IntVar(value=data.lowest_octave)
        self.to_note = tk.StringVar(value=data.highest_note)
        to_octave = tk.IntVar(value=data.highest_octave)

        self.from_note_menu = tk.OptionMenu(range_frame2, self.from_note, *self.major_key_names)
        self.from_note_menu.grid(row=1, column=0)
        from_octave_menu = tk.OptionMenu(range_frame2, from_octave, 2, 3, 4, 5, 6, 7)
        from_octave_menu.grid(row=1, column=1)

        to_text = tk.Label(range_frame2, text="to")
        to_text.config(bg=Colors.background, fg="white")
        to_text.grid(row=1, column=3)

        self.to_note_menu = tk.OptionMenu(range_frame3, self.to_note, *self.major_key_names)
        self.to_note_menu.grid(row=1, column=0)
        to_octave_menu = tk.OptionMenu(range_frame3, to_octave, 2, 3, 4, 5, 6, 7)
        to_octave_menu.grid(row=1, column=1)

        self.refresh_om(self.from_note, self.to_note)

        #def input_check(self, new_cents, f_note, f_oct, t_note, t_oct, window):
        #done_button = ttk.Button(done_frame, text="Apply", command=lambda: self.update_tuner_settings(cent_scale.get(), self.current_key_signature, self.from_note.get(), from_octave.get(), self.to_note.get(), to_octave.get(), tuner_settings_window))
        done_button = ttk.Button(done_frame, text="Apply", command=lambda: self.input_check(cent_scale.get(), self.from_note.get(), from_octave.get(), self.to_note.get(), to_octave.get(), tuner_settings_window))

        done_button.pack()
        tuner_settings_window.lift(self.mainWindow.master)

    def selection_changed(self, redraw=True):
        index = self.root.get()
        keytype = KeySignatureType[self.ktype.get().upper()]
        num_accidentals = 0
        if keytype == KeySignatureType.MINOR:
            accidental = self.minor_accidentals[index]
            name = self.minor_key_names[index]
            num_accidentals = self.minor_numbers[index]
        else:
            accidental = self.major_accidentals[index]
            name = self.major_key_names[index]
            num_accidentals = self.major_numbers[index]
            
        self.current_key_signature = KeySignature(name, index, accidental, num_accidentals, keytype)

        if redraw:
            self.refresh_om(self.from_note, self.to_note)
            if self.ktype.get() == "Minor":
                names = self.minor_key_names
            else:
                names = self.major_key_names
            for i in range(0, 12):
                self.radio_buttons[i].config(text=names[i])

    def refresh_om(self, from_def, to_def):
        self.from_note_menu['menu'].delete(0, 'end')
        self.to_note_menu['menu'].delete(0, 'end')
        notes = [self.current_key_signature.get_display_for(n) for n in range(0,12)]
        start = self.current_key_signature.raw_value
        notes = notes[start:] + notes[:start] # rotate so current root is first
        for note in notes:
            self.from_note_menu['menu'].add_command(label=note, command=tk._setit(from_def, note))
            self.to_note_menu['menu'].add_command(label=note, command=tk._setit(to_def, note))