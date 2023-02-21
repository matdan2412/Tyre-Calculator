import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dat
import fastf1.plotting
import pandas as pd
import numpy as np
import datetime as dt
fastf1.plotting.setup_mpl()
import matplotlib.backends.backend_tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
import PySimpleGUI as sg

column1 = [[sg.Text('Lap quantity study')],
           [sg.Input(key='LapQty',tooltip='On how many laps would you like to study your tires?',size=(3))],
           [sg.Text('Reference times for Soft/Medium/Hard')],
           [sg.Input(key='SoftMin',size=('3')),sg.Text(':'),sg.Input(key='SoftSec',size=(3)),sg.Text('.'),sg.Input(key='SoftMs',size=(6))],
           [sg.Input(key='MedMin',size=('3')),sg.Text(':'),sg.Input(key='MedSec',size=(3)),sg.Text('.'),sg.Input(key='MedMs',size=(6))],
           [sg.Input(key='HardMin',size=('3')),sg.Text(':'),sg.Input(key='HardSec',size=(3)),sg.Text('.'),sg.Input(key='HardMs',size=(6))]]

column2 = [[sg.Text('Time loss for Soft/Medium/Hard (ms)')],
           [sg.Input(key='Soft loss', tooltip='Soft time loss (ms)',size=(10))],
           [sg.Input(key='Medium loss', tooltip='Medium time loss (ms)',size=(10))],
           [sg.Input(key='Hard loss', tooltip='Hard time loss (ms)',size=(10))],
           [sg.Text('Time loss of pitstop (s)')],
           [sg.Input(key='PSLoss',size=(5))],
           [sg.Button(button_text='Plot',enable_events=True,tooltip='Plot the graph')]]

layout = [[sg.Column(column1),sg.VerticalSeparator(),sg.Column(column2)]]

window = sg.Window('Tyre Calculator', layout, finalize=True, element_justification='center', font='Helvetica 18')

#Convertit les chronos donnés en dt.timedelta(minutes,secondes,ms) pour le graphique
def convert(x) :
    if ':' in x :
        if '.' in x :
            i = -1
            for k in x :
                i += 1
                if k == ':' :
                    break
            j = -1
            for k in x :
                j += 1
                if k == '.' :
                    break
            min = ''
            for k in range(0,i) :
                min = min + x[k]
            min = int(min)
            sec = ''
            for k in range(i+1,len(x)) :
                sec = sec + x[k]
            sec = float(sec)
            x = dt.timedelta(seconds=sec,minutes=min)
            return(x)
        else :
            print("problem")
    else :
        print("problem")

#La fenêtre
while True :
    event, values = window.read()
    if event == 'Plot' :
        SoftMin, SoftSec, SoftMs = int(values['SoftMin']), int(values['SoftSec']), int(values['SoftMs'])
        MedMin, MedSec, MedMs = int(values['MedMin']), int(values['MedSec']), int(values['MedMs'])
        HardMin, HardSec, HardMs = int(values['HardMin']), int(values['HardSec']), int(values['HardMs'])
        soft_loss, medium_loss, hard_loss = values['Soft loss'], values['Medium loss'], values['Hard loss']
        soft_time = dt.timedelta(seconds=SoftSec,milliseconds=SoftMs,minutes=SoftMin)
        medium_time = dt.timedelta(seconds=MedSec,milliseconds=MedMs,minutes=MedMin)
        hard_time = dt.timedelta(seconds=HardSec,milliseconds=HardMs,minutes=HardMin)
        soft_loss = dt.timedelta(milliseconds=int(soft_loss))
        medium_loss = dt.timedelta(milliseconds=int(medium_loss))
        hard_loss = dt.timedelta(milliseconds=int(hard_loss))
        break
    elif event == sg.WINDOW_CLOSED:
        break

window.close()

LapQty = int(values['LapQty'])
x = []
for i in range(1,LapQty+1) :
    x.append(i)
    
#ça peut être interessant de creer un dictionnaire genre tour 1 = chrono, deltaloss tour 2 = chrono, deltaloss
#crée la liste de chronos pour le graphique
soft_chronos = [soft_time+soft_loss*(i-1) for i in x]
medium_chronos = [medium_time+medium_loss*(i-1) for i in x]
hard_chronos = [hard_time+hard_loss*(i-1) for i in x]
#crée la liste des temps perdus pour le graphique
soft_cumulative = [k-soft_chronos[0] for k in soft_chronos]
medium_cumulative = [k-medium_chronos[0] for k in medium_chronos]
hard_cumulative = [k-hard_chronos[0] for k in hard_chronos]

fig, ax = plt.subplots(2)

ax[0].plot(x,soft_chronos,color='r')
ax[0].plot(x,medium_chronos,color='y')
ax[0].plot(x,hard_chronos,color='w')
ax[0].set_xlabel('Lap number')
ax[0].set_ylabel('Lap time')

ax[1].plot(x,soft_cumulative,color='r',label='Soft')
ax[1].plot(x,medium_cumulative,color='y',label='Medium')
ax[1].plot(x,hard_cumulative,color='w',label='Hard')
ax[1].set_xlabel('Lap number')
ax[1].set_ylabel('Delta loss')

plt.show()

#04/02/2023 138 Lignes avant opti/109 Lignes après opti 15/02/2023