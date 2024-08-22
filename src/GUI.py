import string
import threading
from typing import Callable
import time
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from FMP import FMP

def center_window(window) -> None:
    """Function to center a window on the screen.

    Args:
        window : window to center.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()  
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y-50}")

class GUI:
    """GUI for the application.
    """
    
    def __init__(self) -> None:
        """Constructor.
        """
        
        # Window configuration
        self.window = ttk.Window(themename='darkly')
        self.window.withdraw()
        self.window.geometry('1650x900')
        center_window(self.window)
        self.window.title('ScryNet')
        self.window.iconbitmap('../assets/icon.ico')

        # Draws the splash screen while the main application is loading
        self.drawSplashScreen()
        threading.Thread(target=self.loadApp).start()
        self.splash.mainloop()

        # Application loop
        self.window.mainloop()

    def drawSplashScreen(self) -> None:
        """Displays the splash screen.
        """
        self.splash = ttk.Toplevel(self.window)
        self.splash.geometry('400x500')
        center_window(self.splash)
        self.splash.overrideredirect(True)

        ttk.Label(master=self.splash, text='ScryNet', font='Arial 20').pack(expand=1)
        self.logo = ttk.PhotoImage(file='../assets/logo.png')
        ttk.Label(master=self.splash, image=self.logo).pack(expand=1)
        ttk.Label(master=self.splash, text='Lancement de l\'application...').pack(expand=1)
        self.splashProgress = ttk.Progressbar(master=self.splash, mode='indeterminate')
        self.splashProgress.start()
        self.splashProgress.pack(expand=1, fill='x', padx=20)
        ttk.Label(master=self.splash, text='by Samy CHAABI - stagiaire ENSSAT - 2024', font='Arial 6').pack(expand=1)
        self.splash.update()


    def loadApp(self) -> None:
        """Creates and loads the main application.
        """
        
        # Style config
        self.font = 'Arial 20'
        
        # Connecting to the Field Master Pro
        self.fmp = FMP('192.168.1.17')
    
        # Tab manager
        self.tabs = ttk.Notebook(master=self.window)
        
        # Config frame
        self.configFrame = ttk.Frame(master=self.tabs)
        for col in range(6):
            self.configFrame.columnconfigure(col, weight=1)
        self.configFrame.rowconfigure(0, weight=2)
        for row in range(3):
            self.configFrame.rowconfigure(row+1, weight=1)
        
        ttk.Label(master=self.configFrame, text='Paramètres', font=self.font).grid(row=0, column=0, columnspan=6)
        
        self.startFreq = ttk.StringVar()
        self.stopFreq = ttk.StringVar()
        self.amplRef = ttk.StringVar()
        self.amplCase = ttk.StringVar()
        self.rbw  = ttk.StringVar()
        
        self.drawConfigFrame('Fréquence limite à gauche\n(en GHz)', self.startFreq, self.fmp.getStartFreq, 0)
        self.drawConfigFrame('Fréquence limite à droite\n(en GHz)', self.stopFreq, self.fmp.getStopFreq, 1)
        self.drawConfigFrame('Amplitude limite en haut\n(en dB)', self.amplRef, self.fmp.getRefLvl, 2)
        self.drawConfigFrame('Échelle d\'amplitude\n(en dB/div)', self.amplCase, self.fmp.getTraceScale, 3)
        self.drawConfigFrame('Largeur de bande\n(en Hz)', self.rbw, self.fmp.getRBW, 4)
        
        ttk.Button(master=self.configFrame, text='Appliquer', takefocus=False, command=self.applyParam).grid(row=1, column=5, sticky='s')
        
        self.presetBtnFrame = ttk.Frame(master=self.configFrame)

        self.drawPresetBtn('WiFi 2', '2.4', '2.5')
        self.drawPresetBtn('WiFi 5', '5.170', '5.730')
        self.drawPresetBtn('WiFi 6E', '5.925', '6.425')
        self.drawPresetBtn('Preset 4', '0', '9')
        self.drawPresetBtn('Preset 5', '0', '9')

        self.presetBtnFrame.grid(row=2, column=0, columnspan=2, sticky='ew')
        
        
        # Trace frame
        self.traceFrame = ttk.Frame(master=self.tabs)
        for col in range(3):
            self.traceFrame.columnconfigure(col, weight=1)
        self.traceFrame.rowconfigure(0, weight=1)
        for row in range(6):
            self.traceFrame.rowconfigure(row+1, weight=2)
        self.traceFrame.pack(expand=1, fill='both')
        
        ttk.Label(master=self.traceFrame, text='Type', font=self.font).grid(row=0, column=1)
        ttk.Label(master=self.traceFrame, text='Mode', font=self.font).grid(row=0, column=2)
        
        for traceNumber in range(1, 7):
            self.drawTraceFrame(traceNumber) 
            
        
        # Plot frame
        self.canvas = None
        
        self.plotFrame = ttk.Frame(master=self.tabs)
        for row in range(2):
            self.plotFrame.rowconfigure(row, weight=1)
        for col in range(2):
            self.plotFrame.columnconfigure(col, weight=1)
        
        self.progress = ttk.Progressbar(master=self.plotFrame, mode='indeterminate')
        self.progressTitle = ttk.Label(master=self.plotFrame, text='Chargement du graphe...', font=self.font)
        
        # Adding tabs to the tab manager
        self.tabs.add(self.configFrame, text='Paramètres')
        self.tabs.add(self.traceFrame, text='Traces')
        self.tabs.add(self.plotFrame, text='Visualisation')
        
        # Binding shortcuts according to the current tab
        def on_tab_change(event) -> None:
            currentTab = event.widget.tab(event.widget.select(), 'text')
            match currentTab:
                case 'Paramètres':
                    self.window.unbind_all('<Key>')
                    self.window.bind('<Return>', lambda _: self.applyParam())
                case 'Traces':
                    self.window.unbind_all('<Key>')
                    pass
                case 'Visualisation':
                    self.window.unbind_all('<Key>')
                    self.window.bind('<Control-s>', lambda _: self.saveGraph())
                    self.window.bind('<Control-r>', lambda _: self.loadGraph())
                    self.loadGraph()
                    # self.window.state('zoomed')
        
        self.tabs.bind('<<NotebookTabChanged>>', on_tab_change)
        
        self.tabs.pack(expand=1, fill='both')

        self.window.bind('<Return>', lambda _: self.applyParam())
        
        # App finished loading
        self.splash.destroy()
        self.window.deiconify()

        # # Application loop
        # self.window.mainloop()

    def applyParam(self) -> None:
        """Applies the selected parameters.
        """
        self.fmp.setParam(
        float(self.startFreq.get()),
        float(self.stopFreq.get()),
        float(self.amplRef.get()),
        float(self.amplCase.get()),
        float(self.rbw.get()))
      
    def drawConfigFrame(self, title: string, var: ttk.StringVar,setDefaultValueFunc: Callable[[None], float], col: int) -> None:
        """Draws a custom frame to configure the instrument's parameters.

        Args:
            title (string): Parameter name.
            var (ttk.StringVar): StringVar linked to the entry.
            setDefaultValueFunc (Callable[[None], str]): Function to get the current value of the parameter.
            col (int): Column where to draw the frame.
        """
        inputFrame = ttk.Frame(master=self.configFrame)
        ttk.Label(master=inputFrame, text=title, font='Arial 14', justify='center').pack(expand=1, fill='both')
        var.set(str(setDefaultValueFunc()))
        paramInput = ttk.Entry(master=inputFrame, textvariable=var, takefocus=False)
        paramInput.bind('<FocusIn>', lambda _: var.set(''))
        
        paramInput.pack(expand=1, fill='both')
        inputFrame.grid(row=1, column=col, sticky='s')

    def applyPreset(self, startFreq: string, stopFreq: string) -> None:
        """Applies a preset

        Args:
            startFreq (float): Preset start frequency.
            stopFreq (float): Preset stop fequency.
        """
        self.startFreq.set(startFreq)
        self.stopFreq.set(stopFreq)
        self.applyParam()

    def drawPresetBtn(self, text: string, startFreq: string, stopFreq: string) -> None:
        """Draws a button that applies a specific preset.

        Args:
            text (string): Preset name.
            startFreq (float): Preset start frequency.
            stopFreq (float): Preset stop frequency.
        """
        ttk.Button(master=self.presetBtnFrame, text=text, takefocus=False, command=lambda: self.applyPreset(startFreq, stopFreq)).pack(side='left', expand=1)
        
      
    def drawTraceFrame(self, num: int) -> None:
        """Draws a custom frame to manage one of the instrument's traces.

        Args:
            num (int): Trace number.
        """
        
        traceName = ttk.Label(master=self.traceFrame, text=f'Trace {num}', font=self.font)
        
        def setType(type: string) -> None:
            if type=='Clear/Write':
                self.fmp.setTraceTypeClearWrite(num)
            elif type=='Maximum':
                self.fmp.setTraceTypeMax(num)
            elif type=='Minimum':
                self.fmp.setTraceTypeMin(num)
            else:
                self.fmp.setTraceTypeAverage(num)
        
        selectedTraceType = ttk.StringVar()
        typeValues = ['Clear/Write', 'Maximum', 'Minimum', 'Average']
        traceType = ttk.Combobox(master=self.traceFrame, state='readonly', values=typeValues, font=self.font, textvariable=selectedTraceType)
        traceType.current(0)
        traceType.bind('<<ComboboxSelected>>', lambda _: setType(selectedTraceType.get()))
        
        def setMode(mode: string) -> None:
            if mode=='Active':
                self.fmp.setTraceModeActive(num)
            elif mode=='Hold/View':
                self.fmp.setTraceModeHold(num)
            else:
                self.fmp.setTraceModeBlank(num)
        
        selectedTraceMode = ttk.StringVar()
        modeValues = ['Active', 'Hold/View', 'Blank']
        traceMode = ttk.Combobox(master=self.traceFrame, state='readonly', values=modeValues, font=self.font, textvariable=selectedTraceMode)
        traceMode.current(2)
        traceMode.bind('<<ComboboxSelected>>', lambda _: setMode(selectedTraceMode.get()))
        
        traceName.grid(row=num, column=0)
        traceType.grid(row=num, column=1)
        traceMode.grid(row=num, column=2)
        
        # Bind to dropdown open event
        traceType.bind('<Button-1>', self.set_dropdown_font)
        traceMode.bind('<Button-1>', self.set_dropdown_font)
        
        
    def set_dropdown_font(self, event) -> None:
        """Sets the font for the dropdown menu items."""
        widget = event.widget
        widget.update()
        dropdown = widget.tk.call('ttk::combobox::PopdownWindow', widget._w)
        dropdown_listbox = dropdown + '.f.l'
        font_to_use = font.Font(family='Arial', size=20)
        widget.tk.call(dropdown_listbox, 'configure', '-font', font_to_use)
        
    def plotGraph(self) -> None:
        """Generates and displays the plot in the Tkinter window."""
        frequencies = np.linspace(self.fmp.getStartFreq(), self.fmp.getStopFreq(), self.fmp.getPointNumber()-1)
        amplitudes = self.fmp.getTraces()

        if not hasattr(self, 'fig'):
            self.fig = Figure()
            self.ax = self.fig.add_subplot()

        self.ax.clear()

        for amplitude in amplitudes:
            if len(amplitude) > 0:
                self.ax.plot(frequencies, amplitude, marker='x')

        self.ax.set_xlabel('Fréquence (Hz)')
        self.ax.set_ylabel('Gain (dB)')
        self.ax.set_title('Graphe')
        self.ax.grid(True)

        self.progress.stop()
        self.progress.grid_forget()
        self.progressTitle.grid_forget()
        
        # ttk.Button(master=self.plotFrame, text='Show Plot', takefocus=False, command=self.plotGraph).grid(row=0, column=0, sticky='news')
        # ttk.Button(master=self.plotFrame, text='Enregister', takefocus=False, command=self.saveGraph).grid(row=0, column=1, sticky='news')

        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='news')

    def loadGraph(self) -> None:
        if self.canvas:
            self.canvas.get_tk_widget().grid_forget()
        
        self.progressTitle.grid(row=0, column=0, columnspan=2, sticky='s')
        self.progress.grid(row=1, column=0, columnspan=2, sticky='new', padx=200, pady=50)
        self.progress.start()
        threading.Thread(target=self.plotGraph).start()

    def saveGraph(self) -> None:
        """Saves the current plot into the 'saves' directory.
        """
        self.saveWindow = ttk.Toplevel(self.window)
        self.saveWindow.withdraw()
        self.saveWindow.geometry('460x180')
        center_window(self.saveWindow)
        self.saveWindow.deiconify()
        self.saveWindow.resizable(False, False)
        self.saveWindow.overrideredirect(True)
        
        def confirm_save() -> None:
            name = graphName.get()
            if name:  
                self.fig.savefig('../saves/'+name+'.png') # change to '../saves/'+name='.png' when compiled
                self.saveWindow.destroy()
        
        graphName = ttk.StringVar()
        graphName.set(str(datetime.datetime.now()).replace(':', '_')) # ':' is a prohibited character in windows filenames
        ttk.Label(master=self.saveWindow, text='Sauvegarder le graphe', font=self.font).pack(pady=5)
        saveName = ttk.Entry(master=self.saveWindow, textvariable=graphName, font=self.font)
        saveName.bind('<FocusIn>', lambda _: graphName.set(''))
        saveName.pack(expand=1, fill='x')
        btnFrame = ttk.Frame(master=self.saveWindow)
        ttk.Button(master=btnFrame, text='Confirmer', takefocus=False, command=confirm_save).pack(side='left', padx=5,expand=1, fill='x')
        ttk.Button(master=btnFrame, text='Annuler', takefocus=False, command=self.saveWindow.destroy).pack(side='left', padx=5, expand=1, fill='x')
        btnFrame.pack(expand=1, fill='x', pady=10)
        