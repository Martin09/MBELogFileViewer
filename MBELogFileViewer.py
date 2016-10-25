# -*- coding: utf-8 -*-
"""
Created on Thu Jun 09 10:03:10 2016

@author: Martin Friedl
"""

#TODO: Add the AsCracker opening percentage to the power graph
#TODO: Make the shutters graph more readable

from MBE_Tools import LogFile
#import os
from pandas import DataFrame as df

# for command-line arguments
import sys
import datetime
# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui,uic
# Numpy functions for image creation
import numpy as np
# Matplotlib Figure object
import matplotlib.gridspec as gridspec

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('MBELogFileViewer.ui', self)
        
#        #Set default values
#        self.startVoltage = 0
#        self.endVoltage = 50
#        self.NPoints = 26
#        self.duty = 8
#        self.saved = False
#        self.filename = None
#        
#        # Connect up the buttons.
#        self.pbOpen.clicked.connect(self.openDoc)
        self.pbLoad.clicked.connect(self.loadFile)
        self.actionLoad.triggered.connect(self.loadFile)

        # Connect up the checkboxes
        # Scale checkboxes
        self.cbTemperature.stateChanged.connect(self.updateTempScale)        
        self.cbPower.stateChanged.connect(self.updatePowerScale)        
        self.cbPressure.stateChanged.connect(self.updatePressureScale)
        self.cbTime.stateChanged.connect(self.updateTimeScale)
        # Temperature checkboxes
        self.cbAsCrackTemp.stateChanged.connect(self.updatePlots)
        self.cbSbConTemp.stateChanged.connect(self.updatePlots)
        self.cbSbCrackTemp.stateChanged.connect(self.updatePlots)
        self.cbAlTemp.stateChanged.connect(self.updatePlots)
        self.cbGaTemp.stateChanged.connect(self.updatePlots)
        self.cbInTemp.stateChanged.connect(self.updatePlots)
        self.cbAsTemp.stateChanged.connect(self.updatePlots)
        self.cbSbTemp.stateChanged.connect(self.updatePlots)
        self.cbManipTemp.stateChanged.connect(self.updatePlots)
        self.cbPyroTemp.stateChanged.connect(self.updatePlots)
        self.cbSUKOTemp.stateChanged.connect(self.updatePlots)
        self.cbSUSITemp.stateChanged.connect(self.updatePlots)
        # Power checkboxes
        self.cbAsCrackPower.stateChanged.connect(self.updatePlots)
        self.cbSbConPower.stateChanged.connect(self.updatePlots)
        self.cbSbCrackPower.stateChanged.connect(self.updatePlots)
        self.cbAlPower.stateChanged.connect(self.updatePlots)
        self.cbGaPower.stateChanged.connect(self.updatePlots)
        self.cbInPower.stateChanged.connect(self.updatePlots)
        self.cbAsPower.stateChanged.connect(self.updatePlots)
        self.cbSbPower.stateChanged.connect(self.updatePlots)        
        self.cbManipPower.stateChanged.connect(self.updatePlots)
        self.cbSUKOPower.stateChanged.connect(self.updatePlots)
        self.cbSUSIPower.stateChanged.connect(self.updatePlots)  
        # Pressure checkboxes
        self.cbBFMPressure.stateChanged.connect(self.updatePlots)
        self.cbMBEPressure.stateChanged.connect(self.updatePlots)                      
        # Shutter checkboxes
        self.cbSbConShutter.stateChanged.connect(self.updatePlots)
        self.cbSbCrackShutter.stateChanged.connect(self.updatePlots)
        self.cbAlShutter.stateChanged.connect(self.updatePlots)
        self.cbGaShutter.stateChanged.connect(self.updatePlots)
        self.cbInShutter.stateChanged.connect(self.updatePlots)
        self.cbAsShutter.stateChanged.connect(self.updatePlots)
        self.cbSbShutter.stateChanged.connect(self.updatePlots)
        self.cbManipShutter.stateChanged.connect(self.updatePlots)
        self.cbPyroShutter.stateChanged.connect(self.updatePlots)
        self.cbSUKOShutter.stateChanged.connect(self.updatePlots)
        self.cbSUSIShutter.stateChanged.connect(self.updatePlots)
        
        # Connect up input lines
        self.lePowerFrom.editingFinished.connect(self.updatePowerScale)        
        self.lePowerTo.editingFinished.connect(self.updatePowerScale)
        self.lePressFrom.editingFinished.connect(self.updatePressureScale)
        self.lePressTo.editingFinished.connect(self.updatePressureScale)         
        self.leTempFrom.editingFinished.connect(self.updateTempScale)         
        self.leTempTo.editingFinished.connect(self.updateTempScale)         
        self.leTimeFrom.editingFinished.connect(self.updateTimeScale)         
        self.leTimeTo.editingFinished.connect(self.updateTimeScale)         
#        
#        # Create validators to validate the inputs (ints or doubles)
#        self.leStartV.setValidator(QtGui.QDoubleValidator())
#        self.leEndV.setValidator(QtGui.QDoubleValidator())
#        self.leNPoints.setValidator(QtGui.QIntValidator())    
#        self.leDuty.setValidator(QtGui.QIntValidator())        
#        
#        #Apply defaults to line edit fields in GUI
#        self.leStartV.setText(str(self.startVoltage))
#        self.leEndV.setText(str(self.endVoltage))
#        self.leNPoints.setText(str(self.NPoints))        
#        self.leDuty.setText(str(self.duty))
#        
        #Add NavigationToolbar
        self.mplwidget.figure.set_dpi(100)
        self.mplwidget.mpl_toolbar = NavigationToolbar(self.mplwidget.figure.canvas, self.mplwidget)
        self.verticalLayout1.setDirection(QtGui.QBoxLayout.BottomToTop)
        self.verticalLayout1.addWidget(self.mplwidget.mpl_toolbar,1)

        self.mplwidget.figure.clear()
        
        grid = gridspec.GridSpec(4, 1)
        grid.update(wspace=0.025, hspace=0.10) # set the spacing between axes. 

        self.mplwidget.plotTemp = self.mplwidget.figure.add_subplot(grid[0])
        self.mplwidget.plotPower = self.mplwidget.figure.add_subplot(grid[1],sharex=self.mplwidget.plotTemp)
        self.mplwidget.plotPressure = self.mplwidget.figure.add_subplot(grid[2],sharex=self.mplwidget.plotTemp)
        self.mplwidget.plotShutter = self.mplwidget.figure.add_subplot(grid[3],sharex=self.mplwidget.plotTemp)
                       
        self.mplwidget.mpl_connect('draw_event', self.updateScales)
        #TODO: hide xaxis tick labels properly, not the bottom axis though
#        self.mplwidget.figure.subplots_adjust(left=0.05, right=0.99, top=0.98, bottom=0.01)
        self.show()
          
    def updateScales(self,event):
        lower,upper=self.mplwidget.plotTemp.set_ylim(auto=True)
        self.leTempFrom.setText(str(lower))
        self.leTempTo.setText(str(upper))
        lower,upper=self.mplwidget.plotPower.set_ylim(auto=True)
        self.lePowerFrom.setText(str(lower))
        self.lePowerTo.setText(str(upper))     
        lower,upper=self.mplwidget.plotPressure.set_ylim(auto=True)
        self.lePressFrom.setText(str(lower))
        self.lePressTo.setText(str(upper))        
        lower,upper=self.mplwidget.plotTemp.set_xlim(auto=True)
        self.leTimeFrom.setText(str(lower))
        self.leTimeTo.setText(str(upper))            
     
    #TODO: Connect function to update lineEdits of scales whenever the scales change in the mplwidget
    def updateTempScale(self):
        autoscale = self.cbTemperature.isChecked()        
        if autoscale:
            lower,upper=self.mplwidget.plotTemp.set_ylim(auto=True)
            self.leTempFrom.setText(str(lower))
            self.leTempTo.setText(str(upper))
        else:
            lower = self.leTempFrom.text()
            if lower:
                lower = float(lower)
            else:
                lower = None
            upper = self.leTempTo.text()
            if upper:
                upper = float(upper)
            else:
                upper = None
            self.mplwidget.plotTemp.set_ylim(bottom=lower,top=upper)  
            self.mplwidget.figure.canvas.draw()
    def updatePowerScale(self):
        autoscale = self.cbPower.isChecked()        
        if autoscale:
            lower,upper=self.mplwidget.plotPower.set_ylim(auto=True)
            self.lePowerFrom.setText(str(lower))
            self.lePowerTo.setText(str(upper))
        else:
            lower = self.lePowerFrom.text()
            if lower:
                lower = float(lower)
            else:
                lower = None
            upper = self.lePowerTo.text()
            if upper:
                upper = float(upper)
            else:
                upper = None
            self.mplwidget.plotPower.set_ylim(bottom=lower,top=upper)      
            self.mplwidget.figure.canvas.draw()
    def updatePressureScale(self):
        autoscale = self.cbPressure.isChecked()        
        if autoscale:
            lower,upper=self.mplwidget.plotPressure.set_ylim(auto=True)
            self.lePressFrom.setText(str(lower))
            self.lePressTo.setText(str(upper))
        else:        
            lower = self.lePressFrom.text()
            if lower:
                lower = float(lower)
            else:
                lower = None
            upper = self.lePressTo.text()
            if upper:
                upper = float(upper)
            else:
                upper = None
            self.mplwidget.plotPressure.set_ylim(bottom=lower,top=upper)    
            self.mplwidget.figure.canvas.draw()
    def updateTimeScale(self):
        autoscale = self.cbTime.isChecked()        
        if autoscale:
            lower,upper=self.mplwidget.plotTemp.set_xlim(auto=True)
            self.leTimeFrom.setText(str(lower))
            self.leTimeTo.setText(str(upper))
        else:           
            lower = self.leTimeFrom.text()
            if lower:
                lower = float(lower)
            else:
                lower = None
            upper = self.leTimeTo.text()
            if upper:
                upper = float(upper)
            else:
                upper = None
            self.mplwidget.plotTemp.set_xlim(left=lower,right=upper)
            self.mplwidget.figure.canvas.draw()
            
    def updatePlots(self):
        sending_button = self.sender()
        variable = self.dictCBLink[str(sending_button.objectName())]  
        print('{:s} Clicked! Variable {:s}'.format(str(sending_button.objectName()),variable))        
        line = [line for line in self.mplwidget.lines if line.get_label()==variable][0]
        line.set_visible(sending_button.isChecked())
        self.mplwidget.figure.canvas.draw()

           
    def loadFile(self, fileName = None):
        print('Load a file!')     
        if not(fileName): #If no fileName given to function, then ask for it from user
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Choose a log file to plot', '.', filter='*.log')
        if fileName:
            self.filename = fileName
            print self.filename
        try:
            log = LogFile(str(self.filename))
            self.data = df(log.data)
            self.data = self.data[self.data.Time > 0]
        except IOError: 
            print('Error - Could not load log file "{:s}"'.format(fileName))      
        self.initPlots()
        self.parseData()
        self.initDicts()
#        self.clearPlot()
        self.plotData()
      
    def initPlots(self):
        self.mplwidget.plotTemp.cla()
        self.mplwidget.plotPower.cla()
        self.mplwidget.plotPressure.cla()
        self.mplwidget.plotShutter.cla()
        
        self.mplwidget.plotTemp.title.set_visible(False)   
        self.mplwidget.plotTemp.grid()
        self.mplwidget.plotTemp.set_title("Log File Plots")
        self.mplwidget.plotTemp.set_ylabel("Temperature ($^\circ$C)")  
        
        self.mplwidget.plotPower.title.set_visible(False)
        self.mplwidget.plotPower.grid()
        self.mplwidget.plotPower.set_ylabel("Output Power (%)")  
        
        self.mplwidget.plotPressure.title.set_visible(False) 
        self.mplwidget.plotPressure.grid()
        self.mplwidget.plotPressure.set_ylabel("Pressure (Torr)")  

        self.mplwidget.plotShutter.title.set_visible(False)
        self.mplwidget.plotShutter.grid()
        self.mplwidget.plotShutter.set_ylabel("Shutter")     

#        self.mplwidget.plotShutter.fmt_xdata = DateFormatter('%Y-%m-%d')
        self.mplwidget.figure.autofmt_xdate()    
        
#        self.mplwidget.figure.subplots_adjust(left=0.1, right=0.99, top=0.98, bottom=0.08)                
        
#        xax.set_major_locator(dates.HourLocator(byhour=range(0,24,2)))
#        xax.set_major_formatter(dates.DateFormatter('%H:%M'))  
#        xax.set_minor_locator(dates.MinuteLocator(byminute=range(0,60,10)))
        
#        import matplotlib.dates as mdates
#        myFmt = mdates.DateFormatter('%d')
#        ax.xaxis.set_major_formatter(myFmt)        
        
    def parseData(self):
        #Parse the data into smaller dataframes, one for each plot
        self.dfTemp = self.data.filter(regex=".PV$")
        self.dfTemp['Pyrometer.T'] = self.data.loc[:,'Pyrometer.T']
        self.dfTemp['Time'] = self.data['Time'].apply(lambda d: datetime.datetime.fromtimestamp(d))    
#        self.dfTemp['Time'] = to_datetime(self.data.loc[:,'Time'],unit='s')
        self.dfPower = self.data.filter(regex=".OP$")
        self.dfPower['Time'] = self.dfTemp['Time']
        self.dfPressure= df()
        self.dfPressure['Time'] = self.dfTemp['Time']
        self.dfPressure['MBE.P'] = self.data.loc[:,'MBE.P']
        self.dfPressure['BFM.P'] = self.data.loc[:,'BFM.P']        
        self.dfShutter = self.data.filter(regex="^Shutter.")
        self.dfShutter['Time'] = self.dfTemp['Time']    
        
        self.dfTemp=self.dfTemp.set_index('Time')
        self.dfPower=self.dfPower.set_index('Time')
        self.dfPressure=self.dfPressure.set_index('Time')
        self.dfShutter=self.dfShutter.set_index('Time')

    def initDicts(self):
        #TODO: convert the values from integers to booleans
        self.dictPlot = dict(zip(self.dfPower.columns,np.ones_like(self.dfPower.columns)))
        self.dictPlot.update(dict(zip(self.dfPressure.columns,np.ones_like(self.dfPressure.columns))))
        self.dictPlot.update(dict(zip(self.dfTemp.columns,np.ones_like(self.dfTemp.columns))))
        self.dictPlot.update(dict(zip(self.dfShutter.columns,np.ones_like(self.dfShutter.columns))))
        
        #TODO: populate from dfTemp.columns and other DFs
        # Temperature checkboxes
        self.dictCBLink = {'cbAsCrackTemp':'AsCracker.PV',
                      'cbSbConTemp':'SbCond.PV',
                      'cbSbCrackTemp':'SbCracker.PV',
                      'cbAlTemp':'Al.PV',
                      'cbGaTemp':'Ga.PV',
                      'cbInTemp':'In.PV',
                      'cbAsTemp':'As.PV',
                      'cbSbTemp':'Sb.PV',
                      'cbManipTemp':'Manip.PV',
                      'cbPyroTemp':'Pyrometer.T',
                      'cbSUKOTemp':'SUKO.PV',
                      'cbSUSITemp':'SUSI.PV',
                      'cbAsCrackPower':'AsCracker.OP',
                      'cbSbConPower':'SbCond.OP',
                      'cbSbCrackPower':'SbCracker.OP',
                      'cbAlPower':'Al.OP',
                      'cbGaPower':'Ga.OP',
                      'cbInPower':'In.OP',
                      'cbAsPower':'As.OP',
                      'cbSbPower':'Sb.OP',
                      'cbManipPower':'Manip.OP',
                      'cbSUKOPower':'SUKO.OP',
                      'cbSUSIPower':'SUSI.OP',
                      'cbBFMPressure':'BFM.P',
                      'cbMBEPressure':'MBE.P',
                      'cbSbConShutter':'Shutter.SbCond',        #REMOVE THIS SHUTTER!
                      'cbSbCrackShutter':'Shutter.SbCracker',   #REMOVE THIS SHUTTER!
                      'cbAlShutter':'Shutter.Al',
                      'cbGaShutter':'Shutter.Ga',
                      'cbInShutter':'Shutter.In',
                      'cbAsShutter':'Shutter.As',
                      'cbSbShutter':'Shutter.Sb',
                      'cbManipShutter':'Shutter.Manip',
                      'cbPyroShutter':'Shutter.Pyrometer',
                      'cbSUKOShutter':'Shutter.SUKO',
                      'cbSUSIShutter':'Shutter.SUSI'} 

    #TODO:Have a problem, initialize the dicts above from the dataframes below, but 
    #then need to check the dicts in the loops below, therefore should separate
    #the dataframe initialization from the plotting loops to avaoid this!
    def plotData(self):
        print('Plot Data!')
        #Not working when exporting to exe
#        #TODO: Set the formatting of the xlabels when zooming in
#        self.dfTemp.plot(ax=self.mplwidget.plotTemp,legend=False,grid=True)
#        self.dfPower.plot(ax=self.mplwidget.plotPower,legend=False,grid=True)
#        self.dfPressure.plot(ax=self.mplwidget.plotPressure,legend=False,grid=True,logy=True)
#        self.dfShutter.plot(ax=self.mplwidget.plotShutter,legend=False,grid=True)
#        print('Plot Data!1')        
        
        for col in self.dfTemp.columns:
            if col == 'Time': continue
            self.mplwidget.plotTemp.plot(self.dfTemp.index,self.dfTemp[col])        
#            self.dfTemp.plot(ax=self.mplwidget.plotTemp)
        for col in self.dfPower.columns:
            if col == 'Time': continue
            self.mplwidget.plotPower.plot(self.dfPower.index,self.dfPower[col])
        for col in self.dfPressure.columns:
            if col == 'Time': continue
            self.mplwidget.plotPressure.semilogy(self.dfPressure.index,self.dfPressure[col])
        for col in self.dfShutter.columns:
            if col == 'Time': continue
#            TDOO: plot these as shaded boxes
#            TODO: Make the open values not exacty 1 to make overlapping shutters easier to see
#            df2.plot.area(x='TimeInMin',ax=ax2,grid=True,ylim=[-0.1,1.1],stacked=False,sharex=True)
#            self.dfShutter.plot.area(x='Time',ax=self.mplwidget.plotShutter,grid=True,ylim=[-0.1,1.1],stacked=False)            
            self.mplwidget.plotShutter.plot(self.dfShutter.index,self.dfShutter[col])
            
        self.mplwidget.figure.subplots_adjust(left=0.1, right=0.99, top=0.98, bottom=0.1)        
        print('Plot Data!2')            
        self.mplwidget.figure.canvas.draw()
        print('Plot Data!3')                
        self.mplwidget.lines = self.mplwidget.plotTemp.lines
        self.mplwidget.lines.extend(self.mplwidget.plotPower.lines)
        self.mplwidget.lines.extend(self.mplwidget.plotPressure.lines)
        self.mplwidget.lines.extend(self.mplwidget.plotShutter.lines)
        print('Plot Data!4')
        #Set the scaling of the x-axes
        self.xax = self.mplwidget.plotTemp.get_xaxis() # get the x-axis
        self.adf = self.xax.get_major_formatter()

        self.adf.scaled[1./24] = '%H:%M'  # set the < 1d scale to H:M
        self.adf.scaled[1.0] = '%Y-%m-%d' # set the > 1d < 1m scale to Y-m-d
        self.adf.scaled[30.] = '%Y-%m' # set the > 1m < 1Y scale to Y-m
        self.adf.scaled[365.] = '%Y' # set the > 1y scale to Y                
    
    def getData(self):
        return self.data

    def cleanUp(self):
        # Clean up everything
        for i in self.__dict__:
            item = self.__dict__[i]
            clean(item)
     # end cleanUp

def clean(item):
    """Clean up the memory by closing and deleting the item if possible."""
    if isinstance(item, list) or isinstance(item, dict):
        for _ in range(len(item)):
            clean(list(item).pop())
    else:
        try:
            item.close()
        except (RuntimeError, AttributeError): # deleted or no close method
            pass
        try:
            item.deleteLater()
        except (RuntimeError, AttributeError): # deleted or no deleteLater method
            pass
# end clean


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        
    def __getattr__(self, attr): 
        return getattr(self.terminal, attr)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
        
if __name__ == '__main__':
    # Create the GUI application
    sys.stdout = Logger("Log.txt")
    qApp = QtGui.QApplication(sys.argv)
    window = MyWindow()
#    qApp.setActiveWindow(window) #<---- This is what's probably missing
    qApp.aboutToQuit.connect(window.cleanUp)          
    
    window.show() 
#    window.loadFile(fileName='Log_160802_err.log')
#    data = window.getData()
#    
#    dfTemp = data.filter(regex=".PV$")
#    dfTemp['Time'] = data.loc[:,'Time']
#    #Add pyrometer temperature
#    dfPower = data.filter(regex=".OP$")
#    dfPower['Time'] = data.loc[:,'Time']    
#    #Add MBE and BFM pressures
#    dfShutter = data.filter(regex="^Shutter.")
#    dfShutter['Time'] = data.loc[:,'Time']    
#    
#    dfPressure= df()
#    dfPressure['Time'] = data.loc[:,'Time']
#    dfPressure['MBE.P'] = data.loc[:,'MBE.P']
#    dfPressure['BFM.P'] = data.loc[:,'BFM.P']
    
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(qApp.exec_())
    
    