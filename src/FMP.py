import string
import telnetlib
import time
import numpy as np
import matplotlib.pyplot as plt

traces = range(1, 7)

class FMP:
    """Field Master Pro class used to control the instrument.
    """
    def __init__(self, ipAddr: string, port: int = 9001) -> None:
        """Constructor.

        Args:
            ipAddr (string): IP Address of the analyzer (check system information).
            port (int): port of the analyzer (9001 for Anritsu)
        """

        # Define IP address and port
        self.ip = ipAddr
        self.port = port

        # Establish connection to the device
        self.tn = telnetlib.Telnet(self.ip, self.port)
        
        # self.setStartFreq(2.0e9)
        # self.setStopFreq(4.5e9)
        
        # self.continuousOff()
        # self.abort()
        
        self.reset()
            
        # self.setTraceTypeClearWrite(1)
        # self.setTraceModeActive(1)
        
        # self.sweepLaunch()
        # self.continuousOn()   
        
        # currentSweepNumber = self.getSweepCount(1)
        # while(currentSweepNumber == 0):
        #     print(self.getSweepCount(1))
        #     time.sleep(1)
        
        # self.drawData()

        # End connection with the device
        # self.tn.close()

    def send_command(self, command: string) -> string:
        """Send a command to the instrument and read the response.

        Args:
            command (string): Telnet command.

        Returns:
            string: Telnet response given by the instrument.
        """
        self.tn.write(command.encode('ascii') + b"\n")
        time.sleep(1)  # Allow some time for the command to be processed
        response = self.tn.read_very_eager().decode('ascii').strip()
        return response

    def getId(self) -> string:
        """Identifies the instrument.

        Returns:
            string: Instrument ID.
        """
        self.send_command('*IDN?')

    def getStartFreq(self) -> float:
        """Gets the start frequency.

        Returns:
            float: Start frequency (GHz).
        """
        return float(float(self.send_command('FREQ:STAR?'))/1.0e9)
    
    def setStartFreq(self, freq:float) -> None:
        """Sets the start frequency.

        Args:
            freq (float): Start frequency (GHz).
        """
        self.send_command(f'FREQ:STAR {freq*1e9}')

    def getStopFreq(self) -> float:
        """Gets the stop frequency.

        Returns:
            float: Stop frequency (GHz).
        """
        return float(float(self.send_command('FREQ:STOP?'))/1e9)
    
    def setStopFreq(self, freq: float) -> None:
        """Sets the stop frequency.

        Args:
            freq (float): Stop frequency (GHz).
        """
        self.send_command(f'FREQ:STOP {freq*1e9}')
        
    def getRBW(self) -> float:
        """Gets the Resolution Bandwidth.

        Returns:
            float: Resolution Bandwidth (Hz)
        """
        return self.send_command('BAND:RES?')
        
    def setRBW(self, freq: float) -> None:
        """Sets the Resolution Bandwidth.

        Args:
            freq (float): Resolution Bandwidth (Hz).
        """
        self.send_command(f'BAND:RES {freq} Hz')
        
    def getRefLvl(self) -> float:
        """Gets the Reference level.

        Returns:
            float: Amplitude reference (top limit in dB).
        """
        return self.send_command('DISP:WIND:TRAC:Y:SCAL:RLEV?')
        
    def setRefLvl(self, ampl: float) -> None:
        """Sets the Reference level to the corresponding amplitude.

        Args:
            ampl (float): Amplitude reference (top limit in dB).
        """
        self.send_command(f'DISP:WIND:TRAC:Y:SCAL:RLEV {ampl}')
        
    def getTraceScale(self) -> float:
        """Gets the trace vertical scale

        Returns:
            float: Scale (dB/division)
        """
        return self.send_command('DISP:WINDow:TRACe:Y:PDIVision?')
        
    def setTraceScale(self, scale: float) -> None:
        """Sets the trace vertical scale.

        Args:
            scale (float): Scale (dB/division).
        """
        self.send_command(f'DISP:WINDow:TRACe:Y:PDIVision {scale}')
    
    def setParam(self, startFreq: float, stopFreq: float, gainRef: float, gainScale: float, rbw: float):
        """Sets the instrument main parameters.

        Args:
            startFreq (float): Start frequency (GHz).
            stopFreq (float): Stop frequency (GHz).
            gainRef (float): Top gain limit (dB)
            gainScale (float): Cell scale (dB/division)
            rbw (float): Rsolution bandwidth (kHz)
        """
        self.setStartFreq(startFreq)
        self.setStopFreq(stopFreq)
        self.setRefLvl(gainRef)
        self.setTraceScale(gainScale)
        self.setRBW(rbw)

    def setTraceMode(self, nb: int, mode: string) -> None:
        """Sets the selected trace mode.

        Args:
            nb (int): Trace number.
            mode (string): Trace mode <Active | Hold/View | Blank>
        """
        self.send_command(f'TRACe{nb}:UPDate {mode}')
    
    def setTraceModeActive(self, nb: int) -> None:
        """Sets the selected trace to Active mode.

        Args:
            nb (int): Trace number.
        """
        self.setTraceMode(nb, '1')

    def setTraceModeHold(self, nb: int) -> None:
        """Sets the selected trace to Hold/View mode.

        Args:
            nb (int): Trace number.
        """
        self.setTraceMode(nb, '0')

    # This method acts like blank but doesn't really change the trace mode on the instrument
    def setTraceModeBlank(self, nb: int) -> None:
        """Sets the selected trace to Blank mode.

        Args:
            nb (int): Trace number.
        """
        self.setTraceMode(nb, '0')
        self.send_command(f'TRACe:CLEar {nb}')

    def setTraceType(self, nb: int, type:string) -> None:
        """Sets the selected trace type.

        Args:
            nb (int): Trace number.
            type (string): Trace type : <NORM | MIN | MAX | AVER>
        """
        self.send_command(f'TRACe{nb}:TYPE {type}')

    def setTraceTypeClearWrite(self, nb: int) -> None:
        """Sets the selected trace to Clear/Write type.

        Args:
            nb (int): Trace number.
        """
        self.setTraceType(nb, 'NORMal')
    
    def setTraceTypeMin(self, nb: int) -> None:
        """Sets the selected trace to Min Hold type.

        Args:
            nb (int): Trace number.
        """
        self.setTraceType(nb, 'MINimum')
    
    def setTraceTypeMax(self, nb: int) -> None:
        """Sets the selected trace to Max Hold type.

        Args:
            nb (int): Trace number.
        """
        self.setTraceType(nb, 'MAXimum')
    
    def setTraceTypeAverage(self, nb: int) -> None:
        """Sets the selected trace to Average type.

        Args:
            nb (int): Trace number.
        """
        self.setTraceType(nb, 'AVERage')
        
    def reset(self) -> None:
        """Blanks every trace.
        """
        for traceNumber in traces:
            self.setTraceTypeClearWrite(traceNumber)
            self.setTraceModeBlank(traceNumber)

    def getSweepCount(self, nb: int) -> int:
        """Gets the current sweep number.

        Args:
            nb (int): Trace number.

        Returns:
            int: Current sweep number.
        """
        return int(self.send_command(f'TRACe{nb}:SWEep:COUNt?'))
    
    def abort(self) -> None:
        """Aborts any sweep in progress.
        """
        self.send_command('ABORT')
        
    def continuousOn(self) -> None:
        """Turns on continuous sweep mode.
        """
        self.send_command('INIT:CONT ON')
        
    def continuousOff(self) -> None:
        """Turns off continuous sweep mode.
        """
        self.send_command('INIT:CONT OFF')
        
    def sweepLaunch(self) -> None:
        """Starts a measurement sweep.
        """
        self.send_command('INIT')
    
    def getTrace(self, nb: int) -> list[float]:
        """Gets a specific trace data.

        Args:
            nb (int): The trace number.

        Returns:
            list[float]: The trace data parsed as a float list.
        """
        trace_data = self.send_command(f'TRACE:DATA? {nb}')
        try:
            # We parse the data in a float list while removing the first six characters (irrelevent measure code)
            return list(map(float, trace_data.split(',', 1)[1].strip().split(',')))
        except:
            print(f'\033[93mWarning : Trace number {nb} is not active.\033[0m')
            return []
    
    def getTraces(self) -> list[list[float]]:
        """Gets all the instrument traces.

        Returns:
            list[list[float]]: The traces data parsde as a float matrix.
        """
        return [self.getTrace(i) for i in traces]
    
    def getPointNumber(self) -> int :
        """Gets the number of points in the traces.

        Returns:
            int: Point number.
        """
        return int(self.send_command('DISP:POIN?'))
    
    def drawData(self) -> None:
        """Plots the traces.
        """
        self.figure = plt.figure(figsize=(5,5))
        
        frequencies = np.linspace(self.getStartFreq(), self.getStopFreq(), self.getPointNumber())
        amplitudes = self.getTraces()

        for amplitude in amplitudes:
            if amplitude != []:
                plt.plot(frequencies, amplitude, marker='x')

        plt.xlabel('Fréqence (Hz)')
        plt.ylabel('Gain (dB)')
        plt.title('Graphe')
        plt.grid(True)
        plt.show()
