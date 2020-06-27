from main_window import *
from pitchDisplay import *
from tkinter import *
from FeedbackSystem import *
from AudioManager import *
import time

sys.path.insert(1, '../python_bridge')

def space_pressed(event, audio_manager, mainWindow):
    if audio_manager.is_paused():
        print("Resuming")
        mainWindow.isPaused = False
        audio_manager.resume()
    else:
        print("Pausing")
        mainWindow.isPaused = True
        audio_manager.pause()

def kill_pressed(event, audio_manager, data, start):
    print("Killing")
    print("")
    end = time.time()
    elapsed_time = end - start
    minutes = int(elapsed_time) // 60
    seconds = int(elapsed_time) % 60

    print("Here are the results of this session:")
    print("-------------------------------------")
    if minutes == 0:
        print("This session lasted", seconds, "seconds.")
    elif minutes == 1:
        print("This session lasted", minutes, "minute and", seconds, "seconds.")
    else:
        print("This session lasted", minutes, "minutes and", seconds, "seconds.")
    print("")
    data.display_all_data()
    audio_manager.destroy()

def cleanup(root, audio_manager):
    audio_manager.destroy()
    root.destroy()


def main():
    def score_update(mainWindow, data):
        if not mainWindow.isPaused:
            mainWindow.myDiagnosticObject.overallScoreLabel.config(text="Overall Score: %.2f" % data.get_overall())
            mainWindow.myDiagnosticObject.update_plot(int(data.get_overall()), mainWindow)
            print(data.get_overall())
        root.after(500, lambda: score_update(mainWindow, data))

    def piano_update(mainWindow, data):
        mainWindow.myHistoryObject.update(data)
        root.after(20, lambda: piano_update(mainWindow, data))

    threshold = 15
    data = FeedbackSystem(threshold)
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    manager = AudioManager(data)
    manager.start_capture()
    manager.start_reader()
    ourWindow = main_window(root, manager, data)
    root.bind('<space>', lambda event, arg=manager: space_pressed(event, arg, ourWindow))
    root.bind('q', lambda event, arg=manager: kill_pressed(event, arg, data, start))
    root.wm_protocol("WM_DELETE_WINDOW", lambda r=root, m=manager: cleanup(r, m))
    score_update(ourWindow, data)
    piano_update(ourWindow, data)
    root.mainloop()

if __name__ == "__main__":
    main()