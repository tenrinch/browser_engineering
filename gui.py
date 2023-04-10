import tkinter
import sys


# Define Window size
WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self):
        self.window = tkinter.Tk() #create a window
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        ) # create a canvas on top of the window where things can be drown
        self.canvas.pack()
    

    def load(self, url):
        # create objects and shapes on the canvas
        self.canvas.create_rectangle(10,20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text='Hi!')

        

if __name__ == '__main__':
    Browser().load(sys.argv[1])
    """
     mainloop() starts the process of redrawing the screen.
     it enters a loop that looks similar to this:
     while True:
        for evt in pendingEvents():
        handleEvent(evt)
        drawScreen()
    
    The example event loop above may look like an infinite loop that locks up the computer, but it’s not, because of preemptive multitasking among threads and processes and/or a variant of the event loop that sleeps unless it has inputs that wake it up from another thread or process.
    """
    tkinter.mainloop() 
    

   

