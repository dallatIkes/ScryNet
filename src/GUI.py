import string
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

class GUI:
    """GUI for the application.
    """
    
    def __init__(self) -> None:
        """Constructor.
        """
        
        # Window configuration
        self.window = ttk.Window(themename='darkly')
        self.window.geometry('1422x900')
        self.window.title('Pilotage')
        
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
        
        ttk.Button(master=self.configFrame, text='Apply', takefocus=False, command=lambda: self.fmp.setParam(
            float(self.startFreq.get()),
            float(self.stopFreq.get()),
            float(self.amplRef.get()),
            float(self.amplCase.get()),
            float(self.rbw.get()))).grid(row=1, column=5)
        
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
        self.plotFrame.rowconfigure(0, weight=1)
        self.plotFrame.rowconfigure(1, weight=1)
        for col in range(2):
            self.plotFrame.columnconfigure(col, weight=1)
        
        # ttk.Button(master=self.plotFrame, text='Show Plot', takefocus=False, command=self.plotGraph).grid(row=0, column=0, sticky='news')
        # ttk.Button(master=self.plotFrame, text='Enregister', takefocus=False, command=self.saveGraph).grid(row=0, column=1, sticky='news')
        
        # Adding tabs to the tab manager
        self.tabs.add(self.configFrame, text='Paramètres')
        self.tabs.add(self.traceFrame, text='Traces')
        self.tabs.add(self.plotFrame, text='Visualisation')
        
        def on_tab_change(event):
            if event.widget.tab(event.widget.select(), 'text') == 'Visualisation':
                self.plotGraph()
                self.window.state('zoomed')
        
        self.tabs.bind('<<NotebookTabChanged>>', on_tab_change)
        
        self.tabs.pack(expand=1, fill='both')
        
        # Application loop
        self.window.mainloop()
      
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
        inputFrame.grid(row=1, column=col)
        
      
    def drawTraceFrame(self, num: int) -> None:
        """Draws a custom frame to manage one of the instrument's traces.

        Args:
            num (int): Trace number.
        """
        
        traceName = ttk.Label(master=self.traceFrame, text=f'Trace {num}', font=self.font)
        
        def setType(type: string):
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
        
        def setMode(mode: string):
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
        
        
    def set_dropdown_font(self, event):
        """Sets the font for the dropdown menu items."""
        widget = event.widget
        widget.update()
        dropdown = widget.tk.call('ttk::combobox::PopdownWindow', widget._w)
        dropdown_listbox = dropdown + '.f.l'
        font_to_use = font.Font(family='Arial', size=20)
        widget.tk.call(dropdown_listbox, 'configure', '-font', font_to_use)
        
    def plotGraph(self):
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
        
        ttk.Button(master=self.plotFrame, text='Show Plot', takefocus=False, command=self.plotGraph).grid(row=0, column=0, sticky='news')
        ttk.Button(master=self.plotFrame, text='Enregister', takefocus=False, command=self.saveGraph).grid(row=0, column=1, sticky='news')

        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotFrame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='news')
        else:
            self.canvas.draw()
            
    def saveGraph(self):
        self.saveWindow = ttk.Toplevel(self.window)
        self.saveWindow.geometry('460x180+500+500')
        self.saveWindow.resizable(False, False)
        self.saveWindow.overrideredirect(True)
        
        def confirm_save():
            name = graphName.get()
            print(name)  
            if name:  
                self.fig.savefig('../saves/'+name+'.png')  
                self.saveWindow.destroy()
        
        graphName = ttk.StringVar()
        graphName.set(datetime.datetime.now())
        ttk.Label(master=self.saveWindow, text='Sauvegarder le graphe', font=self.font).pack(pady=5)
        saveName = ttk.Entry(master=self.saveWindow, textvariable=graphName, font=self.font)
        saveName.bind('<FocusIn>', lambda _: graphName.set(''))
        saveName.pack(expand=1, fill='x')
        btnFrame = ttk.Frame(master=self.saveWindow)
        ttk.Button(master=btnFrame, text='Confirmer', takefocus=False, command=confirm_save).pack(side='left', padx=5,expand=1, fill='x')
        ttk.Button(master=btnFrame, text='Annuler', takefocus=False, command=self.saveWindow.destroy).pack(side='left', padx=5, expand=1, fill='x')
        btnFrame.pack(expand=1, fill='x', pady=10)
        