#main gui for our project, tuneCoach. Made by the group , Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

import tkinter as tk
import tkinter.ttk as ttk
import PIL.Image
import PIL.ImageTk
from datetime import date
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pitchDisplay import *
from FeedbackSystem import *

#background color constant, used by pretty much all of these classes.
background_color = "#575759"

#stand-in variable for noise-filter level, when we come up with some sort of filter, then can initialize real variable like the threshold variable in main of master.py 
noise_filter_level = 20



#class to create practice session objects. Will hold all the data for each practice session
class practice_session:
    def __init__(self, name):
        #note history can hold numbers corresponding to the appropriate notes. 1 = C, 2 = C#... I think it would be cool to add in a break point to signify a stop in the practice sesion, like a 13 or something.
        self._noteHistory = []
        #pitches can hold a int value of how off the cents are for the note in noteHistory of the same index.
        self._notePitches = []
        self._scoreList = []
        self._scoreIndex = []
        self._name = name
        self._date = date.today()
        self._pitch_count = [0,0,0,0,0,0,0,0,0,0,0,0]
        self._pitch_class = [0,0,0,0,0,0,0,0,0,0,0,0]
        self._overall = 0
        self._total_count = 0
        self._cents = 0
        #see about adding raw data

#dfferent classes for pop-up windows.
class session_history:
    def create_circle(self, x, y, r, canvasName, fillColor): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, fill = fillColor)
    
    def __init__(self, workingFrame, width, height):
        self.canvas = tk.Canvas(workingFrame,width = width/2, height = height/4, relief = tk.RIDGE, bd = 5, bg = "#bdd0df")
        self.canvas.pack(side = tk.LEFT, padx = width/4)
        largeImage = PIL.Image.open("piano.jpeg")
        largeImage = largeImage.resize((int(width/10),int(height/3.9)), PIL.Image.ANTIALIAS)
        pianoImage = PIL.ImageTk.PhotoImage(largeImage)
        self.width = width
        self.height = height

        self.canvas.create_image(0, 0, anchor = tk.NW, image = pianoImage)
        
        self.noteDict = {
            "C" : height/3.9/15,
            "C#" : height/3.9/15*2.1,
            "D" : height/3.9/15*3.2,
            "D#" : height/3.9/15*4.3,
            "E" : height/3.9/15*5.6,
            "F" : height/3.9/15*7.1,
            "F#" : height/3.9/15*8.4,
            "G" : height/3.9/15*9.5,
            "G#" : height/3.9/15*10.6,
            "A" : height/3.9/15*11.7,
            "A#" : height/3.9/15*12.7,
            "B" : height/3.9/15*14

        }

        for note in self.noteDict:
            self.canvas.create_line(width/10, self.noteDict[note], width/2, self.noteDict[note], width = 3)

        self.circle_list = [None] * 64 # TODO: don't hardcode size and coordinate with Feedback buffer
        self.canvas.image = pianoImage
        

    def update(self, data):
        recent = list(data.display_buffer)
        thresh1 = 10
        thresh2 = 25
        for i, (note, cents) in enumerate(recent):
            color = "red"
            if abs(cents) <= thresh1:
                color = "green"
            elif abs(cents) <= thresh2:
                color = "yellow"

            circle = self.circle_list[i]
            x = self.width/10 + (i+1)*20
            y = self.noteDict[note]
            if circle == None:
                print("Create")
                c = self.create_circle(x, y, 10, self.canvas, color)
                self.circle_list[i] = c
            else:
                self.canvas.coords(circle, x - 10, y - 10, x + 10, y + 10)


class more_info_window(tk.Toplevel):
    def refresh(self, window, master, obj):
        window.destroy()
        more_info_window(master, obj)
    def __init__(self, master, obj):
        self.master = master
        myWindow = tk.Toplevel(master)
        finalString = ""
        if obj._practice_session is None:
            finalString += "\n No Input Yet"
        elif obj._practice_session._total_count > 0:
            avg_cents= obj._practice_session._cents / obj._practice_session._total_count
            for i in range(12):
                if obj._practice_session._pitch_count[i] == 0:
                    finalString += ("\n" + obj._notes[i] + " was not played/sung in the session.")
                else:
                    pitch_error = (100.0*obj._practice_session._pitch_class[i]) / obj._practice_session._pitch_count[i]
                    finalString += ("\n%s was in tune for %.2f %% of the time." % (obj._notes[i], pitch_error))
            finalString += "\n"
            finalString += "\nOverall"
            finalString += "\nYou were in tune for %.2f %% of the time." % obj.get_overall()
            finalString += "\nYou were off by an average of %.2f cents." % avg_cents
        else:
            finalString += "\nno input yet"
        myLabel = Label(myWindow, text = finalString, bg = background_color, fg = "white")
        myLabel.pack()
        exitButton = Button(myWindow, text = "Exit", command = lambda : myWindow.destroy())
        exitButton.pack()
        refreshButton = Button(myWindow, text = "Refresh", command = lambda : self.refresh(myWindow, master, obj))
        refreshButton.pack()
        myWindow.lift(master)

class session_diagnostics:
    def more_info_window_caller(self,master, obj):
        myMoreInfoWindow = more_info_window(master, obj)
    def update_plot(self, new_score, master):
        if master.practiceSession is not None:
            master.practiceSession._scoreList.append(new_score)
            if len(master.practiceSession._scoreList) > 10:
                master.practiceSession._scoreList.pop(0)
            else:
                master.practiceSession._scoreIndex.append(len(master.practiceSession._scoreIndex))
            self.a.clear()
            self.a.set_xlim([0,10])
            self.a.set_ylim([0,100])
            self.a.set_autoscale_on(FALSE)
            self.a.set_title("Score Over Time")
            self.a.set_ylabel("Score")
            self.a.plot( master.practiceSession._scoreIndex, master.practiceSession._scoreList, color = "blue")
            self.canvas.draw()
    def __init__(self, workingFrame, obj, master):
        #testLabel = tk.Label(workingFrame, text = "testing", bg = background_color, fg = "white")
        #testLabel.pack()
        topestFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        topFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        rightFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        middleFrame = tk.Frame(workingFrame, bd = 5, bg= background_color)
        bottomFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)

        topestFrame.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")
        topFrame.grid(row = 1, column = 0, sticky = "nsew")
        rightFrame.grid(row = 1, column = 1, rowspan = 3, sticky = "nsew")
        middleFrame.grid(row = 2, column = 0, sticky = "nsew")
        bottomFrame.grid(row = 3, column = 0, sticky = "nsew")

        workingFrame.grid_rowconfigure(0, weight = 1)
        workingFrame.grid_rowconfigure(1, weight = 1)
        workingFrame.grid_rowconfigure(2, weight = 1)
        workingFrame.grid_rowconfigure(3, weight = 1)
        workingFrame.grid_columnconfigure(0, weight = 1)
        workingFrame.grid_columnconfigure(1, weight = 2)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.
        titleLabel = tk.Label(topestFrame, text = "Session Diagnostics", bg = background_color, fg = "white", font = ("calibri", 20))
        titleLabel.pack(side = tk.TOP)
        self.sessionName = tk.Label(topestFrame, text = "No Practice Session Selected",bg = background_color, fg = "white" )
        self.sessionName.pack(side  = tk.BOTTOM)
        #v = tk.StringVar()
        v = "Overall Score: %.2f" % obj.get_overall()
        self.overallScoreLabel = tk.Label(topFrame, text = v, bg = background_color, fg = "white")
        self.overallScoreLabel.pack()
        moreInfoButton = Button(middleFrame,text = "More info", command = lambda : self.more_info_window_caller(master, obj))
        moreInfoButton.pack()
        defaultX = [0]
        defaultY = [0]
        self.fig = Figure(figsize=(3,3))
        self.a = self.fig.add_subplot(111)
        self.a.plot(defaultX,defaultY,color='blue')
        #not sure whether or not we want it to have the same axis the whole time
        self.a.set_ylim([0,100])
        self.a.set_xlim([0,10])
        self.a.set_title ("Score Over Time", fontsize=16)
        self.a.set_ylabel("Score", fontsize=14)
        self.a.set_autoscale_on(FALSE)

        self.canvas = FigureCanvasTkAgg(self.fig, master=rightFrame)
        self.canvas.get_tk_widget().configure(relief = tk.RIDGE, bd = 5)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()


#settings window to create a new session
class new_session_window(tk.Toplevel):
    def creating_a_new_session(self, mainWindow,oldWindow, newName, obj):
        oldWindow.destroy()
        mySession = practice_session(newName)
        mainWindow.practiceSessionList.append(mySession)
        mainWindow.practiceSessionNameList.append(mySession._name)
        mainWindow.practiceSession = mySession
        obj._practice_session = mySession
        mainWindow.myDiagnosticObject.sessionName.configure(text = newName)
    def __init__(self, master, mainWindow, obj):
        self.master = master
        new_sesh_window = tk.Toplevel(master)
        new_sesh_window.geometry("500x100")
        topFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)
        leftFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(new_sesh_window, bd = 5, bg= background_color)
        rightFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)

        topFrame.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")
        leftFrame.grid(row = 1, column = 0, sticky = "nsew")
        middleFrame.grid(row = 1, column = 1, sticky = "nsew")
        rightFrame.grid(row = 1, column = 2, sticky = "nsew")
        
        new_sesh_window.grid_rowconfigure(0, weight = 1)
        new_sesh_window.grid_rowconfigure(1, weight = 3)
        new_sesh_window.grid_columnconfigure(0, weight = 1)
        new_sesh_window.grid_columnconfigure(1, weight = 1)
        new_sesh_window.grid_columnconfigure(2, weight = 1)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame,text = "Create New Session", bg = background_color, fg = "white")
        createSessionLabel.pack()
        new_sesh_window.lift(master)
        textEntryLabel = tk.Label(leftFrame, text = "Enter name of new Session", fg = "white", bg = background_color)
        textEntryLabel.pack()
        textEntry = tk.Entry(middleFrame)
        textEntry.insert(tk.END, "new-session-1")
        textEntry.pack()
        enterEntry = tk.Button(rightFrame, text = "Enter", command = lambda: self.creating_a_new_session(mainWindow,new_sesh_window,textEntry.get(), obj))
        enterEntry.pack()

        new_sesh_window.lift(master)

#settings window to load new session
class load_session_window(tk.Toplevel):
    def call_function(self, value):
        self.reset_practice_session(self.mainWindow, value, self.obj)
    def reset_practice_session(self, mainWindow, newPracticeSession, obj):
        for practiceSession in mainWindow.practiceSessionList:
            if practiceSession._name == newPracticeSession:
                mainWindow.practiceSession = practiceSession
                obj._practice_session = practiceSession
                mainWindow.myDiagnosticObject.sessionName.configure(text = newPracticeSession) 
    def __init__(self, master, mainWindow, obj):
        self.obj = obj
        self.mainWindow = mainWindow
        self.master = master

        load_window = tk.Toplevel(master)
        topFrame = tk.Frame(load_window, bd = 5, bg = background_color)
        leftFrame = tk.Frame(load_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(load_window, bd = 5, bg= background_color)
        rightFrame = tk.Frame(load_window, bd = 5, bg = background_color)

        topFrame.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")
        leftFrame.grid(row = 1, column = 0, sticky = "nsew")
        middleFrame.grid(row = 1, column = 1, sticky = "nsew")
        rightFrame.grid(row = 1, column = 2, sticky = "nsew")
        
        load_window.grid_rowconfigure(0, weight = 1)
        load_window.grid_rowconfigure(1, weight = 3)
        load_window.grid_columnconfigure(0, weight = 1)
        load_window.grid_columnconfigure(1, weight = 1)
        load_window.grid_columnconfigure(2, weight = 1)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame,text = "Load Previous Session", bg = background_color, fg = "white")
        createSessionLabel.pack()
        if len(mainWindow.practiceSessionList) > 0:
            selectSessionLabel = tk.Label(leftFrame, text = "Select a session to load", bg = background_color, fg = "white")
            selectSessionLabel.pack()
            firstSession = StringVar(master)
            firstSession.set(mainWindow.practiceSessionNameList[0])
            print("hello")
            loadSessionDropDown = tk.OptionMenu(middleFrame, firstSession, *mainWindow.practiceSessionNameList, command = self.call_function)
            loadSessionDropDown.pack()
            #acceptButton = tk.Button(middleFrame, text = "Select", command = lambda: reset_practice_session(loadSessionDropDown.get(), mainWindow))
            #acceptButton.pack()
        else:
            standInLabel = tk.Label(middleFrame, text = "No sessions to choose from.", fg = "white", bg = background_color)
            standInLabel.pack()

        load_window.lift(master)

#settings window to end current session
class end_session_window(tk.Toplevel):
    def __init__(self, master, mainWindow, obj):
        self.master = master
        mainWindow.practiceSession = None
        obj._practice_session = None
        mainWindow.myDiagnosticObject.a.clear()
        mainWindow.myDiagnosticObject.a.set_title("Score Over Time")
        mainWindow.myDiagnosticObject.a.set_ylabel("Score")
        mainWindow.myDiagnosticObject.canvas.draw()
        self.end_sesh_window = tk.Toplevel(master)
        self.end_sesh_window.configure(bg = background_color)
        self.end_sesh_window.geometry("200x100")
        topFrame = tk.Frame(self.end_sesh_window, bg = background_color, bd = 5)
        bottomFrame = tk.Frame(self.end_sesh_window, bg = background_color, bd = 5)
        topFrame.grid(row =0, sticky = "nsew")
        bottomFrame.grid(row =1, sticky = "nsew")
        self.end_sesh_window.grid_rowconfigure(0, weight = 1)
        self.end_sesh_window.grid_rowconfigure(1,weight = 1)
        successLabel = tk.Label(topFrame, text = "Session ended successfully.", fg = "white", bg= background_color)
        successLabel.pack()
        endButton = tk.Button(bottomFrame, text = "Ok", command = lambda : self.end_sesh_window.destroy())
        endButton.pack()

#tuner settings window
class tuner_settings_window(tk.Toplevel):
    def update_pitch_settings(self, newPitch, newFilterLevel, oldSettingsView, obj):
        obj.update_threshold(newPitch)
        noise_filter_level = newFilterLevel
        oldSettingsView.destroy()
    def __init__(self, master, obj):
        self.master = master
        tuner_settings_window = tk.Toplevel(master)
        tuner_settings_window.geometry("500x300")

        topFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(tuner_settings_window, bd = 5,bg =  background_color)
        middleFrame1 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        middleFrame2 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame1 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame2 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomestFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)

        #putting the frames into a grid layout

        topFrame.grid(row = 0, column = 0, columnspan = 3, sticky = "nsew")
        middleFrame.grid(row = 1, column = 0, columnspan = 1,sticky = "nsew")
        middleFrame1.grid(row = 1, column = 1, sticky = "nsew")
        middleFrame2.grid(row = 1, column = 2, sticky = "snew")
        bottomFrame.grid(row = 2, column = 0,sticky = "nsew")
        bottomFrame1.grid(row = 2, column = 1, sticky = "nsew")
        bottomFrame2.grid(row = 2, column = 2, sticky = "nsew")
        bottomestFrame.grid(row = 3, column = 0, columnspan = 3, sticky = "nsew")

        #setting up grid weights.

        tuner_settings_window.grid_rowconfigure(0, weight = 1)
        tuner_settings_window.grid_rowconfigure(1, weight = 5)
        tuner_settings_window.grid_rowconfigure(2, weight = 5)
        tuner_settings_window.grid_rowconfigure(3, weight = 1)
        tuner_settings_window.grid_columnconfigure(0, weight = 1)
        tuner_settings_window.grid_columnconfigure(1, weight = 1)
        tuner_settings_window.grid_columnconfigure(2, weight = 1)

        tuner_label = tk.Label(topFrame, text = "Tuner Settings", font=("Calibri", 20))
        tuner_label.config(bg = background_color, fg = "white")
        tuner_label.pack()


        centsitivity = tk.Label(middleFrame, text = "Margin of Acceptable Pitch Error +- ")
        centsitivity.config(bg = background_color, fg= "white")
        centsitivity.pack()

        pitch_sensitivity_scale = tk.Scale(middleFrame1, from_= 0, to_ = 50, orient = tk.HORIZONTAL)
        pitch_sensitivity_scale.config(bg = background_color, fg = "white")
        pitch_sensitivity_scale.pack()

        inCents = tk.Label(middleFrame2, text = "cents")
        inCents.config(bg = background_color, fg = "white")
        inCents.pack()

        outside_noise_filter_level = tk.Label(bottomFrame, text = "Pitch Detection Threshold")
        outside_noise_filter_level.config(bg = background_color, fg = "white")
        outside_noise_filter_level.pack()

        outside_noise_scale = tk.Scale(bottomFrame1, from_= 0, to_ = 40, orient = tk.HORIZONTAL)
        outside_noise_scale.config(bg = background_color, fg = "white")
        outside_noise_scale.pack()        

        inCents = tk.Label(bottomFrame2, text = "decibals")
        inCents.config(bg = background_color, fg = "white")
        inCents.pack()
        
        doneButton = ttk.Button(bottomestFrame, text = "Apply", command = lambda: update_pitch_settings(self, pitch_sensitivity_scale.get(), outside_noise_scale.get(),tuner_settings_window, obj))
        doneButton.pack()

        tuner_settings_window.lift(master)

class save_window(tk.Toplevel):
    def __init__(self, mainWindow, root, obj):
        print("will create the save window")

class remove_window(tk.Toplevel):
    def __init__(self, mainWindow, root, obj):
        print("will create the remove window")

#main gui
class main_window(tk.Frame):

    def __init__(self, master, manager, obj):
        self.practiceSessionList = []
        self.practiceSessionNameList = []
        self.practiceSession = None
        self.isPaused = False
        tk.Frame.__init__(self, master)
        self.master = master

        self.audio_manager = manager
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar(self.master, obj)
        self.layout_frames(self.master, screen_width, screen_height, obj)

    #adding menu options to the top of the screen.
    def save_practice_session(self, obj):
        save_window(self, self.master, obj)
    def remove_practice_session(self, obj):
        remove_window(self, self.master,obj)
    def tuner_settings(self, obj):
        settingsWindow = tuner_settings_window(self.master, obj)
    def change_layout(self):
        print("this will change the layout")
    def user_settings(self):
        print("function to display menu to change user settings")
    def load_faq(self):
        print("function to load app faq")
    def load_tutorial(self):
        print("function to load a tutorial for how to use the app")   
    def new_practice_session(self, obj):
        newPracticeSessionWindow = new_session_window(self.master, self, obj)
    def load_practice_session(self, obj):
        loadPracticeSessionWindow = load_session_window(self.master, self, obj)
    def end_practice_session(self, obj):
        end_session_window(self.master, self, obj)   
    
    def create_menubar(self, master, obj):
        menubar = tk.Menu(master)    

        master.config(menu=menubar)

        file_menu = tk.Menu(menubar)

        #file menubar
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Practice Session", command = lambda: self.new_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label="End Practice Session", command = lambda: self.end_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label="Load Practice Session", command = lambda: self.load_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label = "Save Practice Session", command = lambda: self.save_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label = "Remove Practice Session", command = lambda : self.remove_practice_session(obj))

        #settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Tuner Settings", command = lambda: self.tuner_settings( master, obj))
        settings_menu.add_separator
        settings_menu.add_command(label="User Settings", command =self.user_settings)
        settings_menu.add_separator

        #view menubar
        view_menu = tk.Menu(menubar)
        menubar.add_cascade(label="View", menu = view_menu)
        view_menu.add_command(label="Change layout", command = self.change_layout)
        view_menu.add_separator

        #help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="FAQ", command = self.load_faq)
        help_menu.add_separator
        help_menu.add_command(label="Tutorial", command = self.load_tutorial)
        help_menu.add_separator
        #creating frames to organize the screen.
    
    def layout_frames(self, master, screen_width, screen_height, obj):
        bottomFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)
        leftFrame = tk.Frame(master, bd = 5, relief = tk.RAISED ,bg =  background_color)
        rightFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)

        #putting the frames into a grid layout

        bottomFrame.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew")
        leftFrame.grid(row = 0, column = 0, sticky = "nsew")
        rightFrame.grid(row = 0, column = 1, sticky = "nsew")

        #setting up grid weights.

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=3)
        master.grid_columnconfigure(1, weight=4)

        #i think that here we can work on creating the funcitonality for each individual frame, ex: tuner, pitch history, information.

        #adding temporary label to the Pitch Detector Section
        tuner_header = tk.Label(rightFrame, text = "Pitch Detector", font=("Calibri", 20))
        tuner_header.config(bg = background_color, fg = "white")
        tuner_header.pack()

        self.myHistoryObject = session_history(bottomFrame, screen_width, screen_height)
        self.myDiagnosticObject = session_diagnostics(leftFrame, obj, master)

        pitch = PitchDisplay(master, rightFrame, self.audio_manager)
        master.after(10, pitch.update_data)
