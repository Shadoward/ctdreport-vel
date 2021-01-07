# -*- coding: utf-8 -*-
###############################################################
# Author:       patrice.ponchant@furgo.com  (Fugro Brasil)    #
# Created:      17/12/2020                                    #
# Python :      3.x                                           #
###############################################################

# The future package will provide support for running your code on Python 2.6, 2.7, and 3.3+ mostly unchanged.
# http://python-future.org/quickstart.html
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

##### For the basic function #####
import datetime
import sys
import glob
import os
import math
import pandas as pd
#import numpy as np

# gaph
from jinja2 import Template

#from bokeh.io import output_file, export_png
from bokeh.plotting import *
from bokeh.models import *
from bokeh.layouts import gridplot, column, layout, row
#from bokeh.models import Button
#from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.embed import components
from bokeh.resources import INLINE
#from bokeh.util.browser import view

##### CMD packages #####
from tqdm import tqdm
#from tabulate import tabulate

##### GUI packages #####
from gooey import Gooey, GooeyParser
from colored import stylize, attr, fg

##### Defined color palette #####
RelativityRed = '#C90119' #R201/G1/B25     
SignalGreen = '#237f52' #R253/G127/B82   
InfinityWhite = '#FFFFFF' #R255/G255/B255
QuantumBlue = '#011E41' #R1/G30/B65
QuantumBlue70 = "#0250AE" # R2/G80/B174
QuantumBlue50 = "#2385FC" # R35/G133/B252
QuantumBlue30 = "#91C1FD" # R145/G193/B253
GravityGrey = '#D9D8D6' #R217/G216/B214
GravityGrey70 = '#E4E4E2' #R228/G228/B226
GravityGrey50 = '#ECECEB' #R236/G236/B235
GravityGrey30 = '#F4F3F3' #R244/G243/B243
CosmicSand = '#D9BE89' #R217/G190/B137
CosmicSand70 = '#E4D2AC' #R228/G210/B172
CosmicSand50 = '#ECDFC4' #R236/G223/B196
CosmicSand30 = '#F4ECDC' #R244/G235/B220
PulseBlue = '#6788B1' #R103/G136/B177 
PulseBlue70 = '#95ACC8' #R149/G172/B200 
PulseBlue50 = '#B3C4D8' #R179/G196/B216 
PulseBlue30 = '#D1DBE8' #R209/G219/B232 
MotionGreen = '#8CB680' #R140/G182/B128 
MotionGreen70 = '#AFCCA6' #R175/G204/B166 
MotionGreen50 = '#C6DBC0' #R198/G219/B192 
MotionGreen30 = '#DDE9D9' #R221/G233/B217 
StrataTurquoise = '#479CAA' #R71/G156/B170   
StrataTurquoise70 = '#7EBAC4' #R126/G186/B196  
StrataTurquoise50 = '#A3CED5' #R163/G206/B213  
StrataTurquoise30 = '#C8E1E6' #R200/G225/B230
Orange = '#e18700'  #R225/G135/B0
GridGray = '#A9A9A9' #R169/G169/B169
Purple = '#800080' #R128/G0/B128
GreenViridis = '#79D151' #R121/G209/B81
YellowPlasma = '#FDE724' #R253/G231/B36
FugroColorList = [SignalGreen, PulseBlue, StrataTurquoise, CosmicSand, MotionGreen, QuantumBlue, 
                  Orange, Purple, QuantumBlue70, GreenViridis, YellowPlasma]

# 417574686f723a205061747269636520506f6e6368616e74
##########################################################
#                       Main code                        #
##########################################################
# this needs to be *before* the @Gooey decorator!
# (this code allows to only use Gooey when no arguments are passed to the script)
if len(sys.argv) >= 2:
    if not '--ignore-gooey' in sys.argv:
        sys.argv.append('--ignore-gooey')
        cmd = True 
    else:
        cmd = False  
        
# GUI Configuration
@Gooey(
    program_name='CTD Interactif Report for Starfix .vel files.',
    progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100",
    hide_progress_msg=True,
    richtext_controls=True,
    #richtext_controls=True,
    terminal_font_family = 'Courier New', # for tabulate table nice formatation
    #dump_build_config=True,
    #load_build_config="gooey_config.json",
    default_size=(930, 770),
    timing_options={        
        'show_time_remaining':True,
        'hide_time_remaining_on_complete':True
        },
    tabbed_groups=True,
    navigation='Tabbed',
    header_bg_color = '#95ACC8',
    #body_bg_color = '#95ACC8',
    menu=[{
        'name': 'File',
        'items': [{
                'type': 'AboutDialog',
                'menuTitle': 'About',
                'name': 'ctdreportvel',
                'description': 'CTD Interactif Report for Starfix .vel files',
                'version': '0.2.0',
                'copyright': '2020',
                'website': 'https://github.com/Shadoward/ctdreport-vel',
                'developer': 'patrice.ponchant@fugro.com',
                'license': 'MIT'
                }]
        },{
        'name': 'Help',
        'items': [{
            'type': 'Link',
            'menuTitle': 'Documentation',
            'url': ''
            }]
        }]
    )

def main():
    desc = "CTD Interactif Report for Starfix .vel files"    
    parser = GooeyParser(description=desc)
    
    mainopt = parser.add_argument_group('CTD Options', gooey_options={'columns': 1})
    metaopt = parser.add_argument_group('Metadata Options', gooey_options={'columns': 1})

    # Main Arguments
    mainopt.add_argument(
        '-i', '--velFolder', 
        dest='velFolder',       
        metavar='.vel Folder Path', 
        help='Option to be use to create unique report for each .vel in the folder',
        widget='DirChooser')
    
    mainopt.add_argument(
        '-n', '--numberfile', 
        dest='numberfile',       
        metavar='Number of files', 
        help='Number of files to be merge in one report.\n For more visibilty, please try to not pass 10 files per graph)',
        type=int,
        default=1)

    # mainopt.add_argument(
    #     '-f', '--velFilesSelect', 
    #     dest='velFilesSelect',       
    #     metavar='.vel Files', 
    #     help='Option to be use to select mutiples .vel files and create a unique report',
    #     widget='MultiFileChooser',
    #     gooey_options={'wildcard': "Starfix Velocity File (*.vel)|*.vel"})
    
    mainopt.add_argument(
        '-o', '--outputFolder',
        dest='outputFolder',
        metavar='Output Logs Folder',  
        help='Output folder to save all the report files.',
        widget='DirChooser')
    
    # Metadata Arguments
    metaopt.add_argument(
        '-t', '--instrument', 
        dest='instrument',
        metavar='Instrument Name', 
        widget='TextField',
        default='AML Oceanographic - Smart-X CTD',
        help='Instrument used to collect the sound velocity data.')
    
    metaopt.add_argument(
        '-c', '--velCalc', 
        dest='velCalc',
        metavar='Velocity Calculation', 
        choices=['Chen Millero', 'Del Grosso', 'Wilson'],
        help='Velocity Calculation used to calculate sound velocity.')
    
    metaopt.add_argument(
        '-g', '--geodetic', 
        dest='geodetic',
        metavar='Geodetic Parameters', 
        widget='TextField',
        default='NAD83(2011) / UTM zone 19N | EPSG Code: 6348',
        help='Geodetic parameters of the cooredinates.')    
    
        
    # Use to create help readme.md. TO BE COMMENT WHEN DONE
    # if len(sys.argv)==1:
    #    parser.print_help()
    #    sys.exit(1)   
        
    args = parser.parse_args()
    process(args, cmd)

def process(args, cmd):
    """
    Uses this if called as __main__.
    """
    velFolder = args.velFolder
    #velFilesSelect = args.velFilesSelect
    numberfile = int(args.numberfile)
    outputFolder = args.outputFolder
    instrument = args.instrument
    velCalc = args.velCalc
    geodetic = args.geodetic        

    ##########################################################
    #                 Listing the files                      #
    ##########################################################  
    print('', flush=True)
    print('##################################################', flush=True)
    print('CREATING REPORT FILES. PLEASE WAIT....', flush=True)
    print('##################################################', flush=True)
    #now = datetime.datetime.now() # record time of the subprocess
    
    if args.velFolder is not None:
        velListFile = []
        velListemtpy = []
        velListtmp = glob.glob(velFolder + "\\*.vel")
        if not velListtmp:
            print ('')
            sys.exit(stylize('No .vel files were found, quitting', fg('red')))
        for f in velListtmp:
            if os.stat(f).st_size == 0:
                velListemtpy.append(f)
            else:
                velListFile.append(f)
                
        velsplitlist = [velListFile[i:i + numberfile] for i in range(0, len(velListFile), numberfile)]
        pbar = tqdm(total=len(velsplitlist)) if cmd else print(f"Note: Output show file counting every {math.ceil(len(velsplitlist)/10)}", flush=True) # cmd vs GUI
        i = 0
        for el in velsplitlist:
            multiplegraph(el, outputFolder, velCalc, instrument, geodetic)
            progressBar(cmd, pbar, i, velsplitlist)
            i += 1
        
        if velListemtpy:
            print('', flush=True)
            print('The following file(s) was/were skip beacause there are empty.', flush=True)
            print(velListemtpy, flush=True)
        
        # for index, f in enumerate(velListFile):
        #     multiplegraph(velListFile, outputFolder, velCalc, instrument, geodetic)            
        #     #simplegraph(f, outputFolder, velCalc, instrument, geodetic)
        #     progressBar(cmd, pbar, index, velListFile)


##########################################################
#                       Functions                        #
########################################################## 
def lsinfo(f):  
    filename = os.path.splitext(os.path.basename(f))[0]        
    # Headers info
    dfinfo = pd.read_csv(f, nrows=4, sep="99aa99", header=None, engine='python')
    # Value from row 0
    row0 = dfinfo[0].iloc[0].split('Time: ')
    row0_1 = row0[0].split('Date: ')
    row0_2 = row0_1[0].split('Job Number: ')
    Job_Number = row0_2[-1]
    s = row0_1[-1]
    Date = datetime.datetime.strptime(row0_1[-1].rstrip(), '%B %d, %Y').strftime("%d %B %Y")
    Time = row0[-1]
    # Value from row 1
    Vessel = dfinfo[0].iloc[1].split('Vessel: ')[-1]
    # Value from row 2
    row1 = dfinfo[0].iloc[2].split('Area: ')
    Area = row1[-1]
    Client = row1[0].split('Client: ')[-1]
    # Value from row 3
    row0 = dfinfo[0].iloc[3].split('Time: ')
    row0_1 = row0[0].split('X:  ')
    row0_2 = row0_1[0].split('Y:  ')
    row0_3 = row0_2[0].split('Lon: ')
    Easting = row0_1[-1]
    Northing = row0_2[-1]
    Lon = row0_3[-1]
    Lat = row0_3[0].split('Lat: ')[-1]
        
    return filename, Job_Number, Date, Time, Vessel, Area, Client, Easting, Northing, Lat, Lon

def simplegraph(f, outputFolder, velCalc, instrument, geodetic):
    # get info from file      
    filename, Job_Number, Date, Time, Vessel, Area, Client, Easting, Northing, Lat, Lon = lsinfo(f)    
    # Parameters
    svp = "Sound Velocity [" + velCalc + ", m/s]"
    htmlfile = outputFolder + '\\' + filename + '_report.html'
    htmltitle = filename + " – " + Client + " – " + Area
    # get data
    dfvel = pd.read_csv(f, skiprows=5, sep=" ", header=None, usecols=[3,4,6]) #[3]=depth, [4]=velocity, [6]=temperature
    dfvel[3] = dfvel[3] * -1   
    temp = round(dfvel[6].mean(),2) # Temperature at Seabed [°C]
    avSV = round(dfvel[4].mean(),2) # Average SV [m/s] 
    seabedvel = round(dfvel[4].iloc[-1],2) # SV at Seabed [m/s]
    depth = round(dfvel[3].min(),2) # Max. Depth [m]

    ################ DATA PARAMETERS ################
    ###### -- Create Column Data Source that will be used by the plot -- ########

    datarawdata = dict( Depth=dfvel[3],
                        Temperature=dfvel[6],
                        SoundVelocity=dfvel[4]
                        )
    sourcerawdata = ColumnDataSource(datarawdata)
    ###### -- end -- ########

    ################ PLOTS PARAMETERS ################
    ###### -- Main-- ########
    TOOLTIPS = [
    ("Depth", "$y{0.1f}"),
    ("Measure", "$x{0.1f}"),
    ]

    plot_options = dict(y_axis_label='Depth [Hydrostatic, m]',
                        background_fill_color='#F4ECDC',
                        width=600,
                        height=600,
                        title="",
                        toolbar_location=None,
                        tooltips=TOOLTIPS,
                        #tools='crosshair,pan,wheel_zoom,box_zoom,reset,hover,save'
                        )
    ###### -- end -- ########

    ################ PLOTS ################
    ###### -- First one -- ########
    line0 = figure(**plot_options)
    #xaxis = LinearAxis(line0=line0, location="above")
    line0.line('SoundVelocity', 'Depth', source=sourcerawdata, color='#6788B1')
    line0.xaxis.axis_label = svp
    line0.x_range.bounds = 'auto'
    line0.y_range.bounds = 'auto'
    line0.axis.axis_label_text_font_size = "14pt"
    line0.axis.axis_label_text_font_style = "bold"
    
    ## -- Temperature [ºC] -- ##
    line1 = figure(y_range=line0.y_range, **plot_options)
    line1.line('Temperature', 'Depth', source=sourcerawdata, color='#6788B1')
    line1.xaxis.axis_label = "Temperature [°C]"
    line1.x_range.bounds = 'auto'
    line1.y_range.bounds = 'auto'
    line1.axis.axis_label_text_font_size = "14pt"
    line1.axis.axis_label_text_font_style = "bold"

    ###### -- end -- ########

    ################ TABLE ################
    ###### -- Set up table bottle columns-- ########
    columnstable = [
        TableColumn(field="Depth",          title="Depth [m]",          formatter=NumberFormatter(format="0.00")),
        TableColumn(field="SoundVelocity",  title=svp, 			        formatter=NumberFormatter(format="0.00")),
        TableColumn(field="Temperature",    title="Temperature [°C]",   formatter=NumberFormatter(format="0.00"))        
    ]
    ###### -- end -- ########

    ###### -- Create tables -- ########
    data_table = DataTable(source=sourcerawdata, columns=columnstable, editable=False, sortable=False, selectable=True)
    ###### -- end -- ########


    ########## PLOTS LAYOUT ################
    ###### -- Set up Plots layout -- ########
    p = gridplot([[line0, line1]])
    datatbl = layout([[data_table]], sizing_mode='stretch_both')

    ########## RENDER PLOTS ################
    ###### -- Define our html template for out plots -- ########
    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
        <title>'CTD {{filename}}'</title>
            {{ js_resources }}
            {{ css_resources }}
        <style>
        	h1 {font-family: 'segoe ui', sans-serif;
                display: block;
                font-size: 160%;
                margin-block-start: 0em;
                margin-block-end: 0em;
                margin-inline-start: 0px;
                margin-inline-end: 0px;
                font-weight: bold;
                padding-top: 7px;
		        }
            h2 	{font-family: 'segoe ui', sans-serif;
                color: #ffffff;
                margin: 60px 0px 0px 0px;
                padding: 0px 0px 6px 150px;
                font-size: 35px;
                line-height: 48px;
                letter-spacing: -2px;
                font-weight: bold;
                background-color: #011E41;
                }
            h3  {font-family: 'segoe ui', sans-serif;
                color: #011E41;
                margin: 20px 0px 0px 15px;
                padding: 0px 0px 6px 0px;
                font-size: 28px;
                line-height: 44px;
                letter-spacing: -2px;
                #font-weight: bold;
                }
            h4  {font-family: 'segoe ui', sans-serif;
                color: #011E41;
                margin: 0px 0px 10px 15px;
                padding: 0px 0px -5px 0px;
                font-size: 24px;
                line-height: 44px;
                letter-spacing: -2px;
                font-style: italic;
                border-bottom-style: solid;
                border-width: 2px;
                border-color: #011E41;
                }
            p {font-family: 'segoe ui', sans-serif;
                font-size: 16px;
                line-height: 24px;
                margin: 0 0 24px 15px;
                text-align: left;
                ///text-justify: inter-word;
                }
            ul {font-family: 'segoe ui', sans-serif;
                font-size: 16px;
                line-height: 24px;
                margin: 0 0 24px;
                text-align: left;
                ///text-justify: inter-word;
                }
            p.TableText, li.TableText, div.TableText
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
                }
            p.TableNote, li.TableNote, div.TableNote
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                line-height:12pt;
                font-size:8.0pt;
                font-family:"Segoe UI",sans-serif;
                color:#808080;
                }
            .TableText.Centre
                {text-align:center;
                }                
            p.TableHeading, li.TableHeading, div.TableHeading
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                font-size:9.0pt;
                font-family:"Segoe UI Semibold",sans-serif;
                }
            .TableHeading.Centre
                {text-align:center;
                }   
            td.TableHeadingGridTable
                {border:solid #6788B1 1.0pt;
                border-right:solid white 1.0pt;
                background:#6788B1;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableTextGridTable
                {border-top:none;
                border-left:none;
                border-bottom:solid #6788B1 1.0pt;
                border-right:solid #6788B1 1.0pt;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableHeadingLinedTable
                {border:none;
                border-bottom:solid #6788B1 1.0pt;
                background:white;
                vertical-align: bottom;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableTextLinedTable
                {border:none;
                border-bottom:solid #7F7F7F 1.0pt;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            .app_header {
                height:80px;
                width: 100%;
                background-color:#011E41;
                color:#eee;
                margin-left: auto;
                margin-right: auto;
            }
            @media screen and (min-width : 1024px) {
                .app_header {
                    width: 100%;
                }
            }
            .app_header a {
                color: #900;
            }
            .app_header_icon {			
                background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAABDCAYAAABX2cG8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAALiMAAC4jAXilP3YAAASVSURBVHhe7ZxdiFVVFMfnq0LSJsI0CpKwhzJ6iXwYLQiiCAYCn4QeRJLoqbRUjKC0t6EPwd4iKiMsSsge+kA0kiIjQQoSpMwIYYixtI9RCZM7/dY+y+s995572feMZz72/H/wZ++19jr77LPX3fuec7xjjxBCCCGEEEIIIYQQQghRMb1eVkatVnuQ4g10Q3B0z7G+vr5lXhcziYmJiX4SPEZZGo7/0bsTJejzsioW9Pb2LvK6mAYq3aJZgNdS/JlZeWgbpfg+szoyyhb9uNfFTMISbNtsEWy9qz1MVEjVW3Qn/vNSVEjXWzSLbyGKPW6Q7+BjXs9BH49SfJJZnWGLPulVuyu/jmIgsy7Bec6gc24GPLY/s6I4x7nOej1AH6XvIWw8Ni4369j82TxSjZ5/+jmNLrhZHVzwGQY31dR3Gs5/2H058K/3EJvAQewvspZ4OOY8et67CWDXvLlrOPQC+pDqoHdn/S1FR7OIeDhmFA15N9FM5xZ9uZnw0hK8kU/7fW5GwzFXoBeYyDvdNSnoqx+tYjzPuMt4Ed9tXo+GY26keD2z4ul6i+bi3+FkV7nZES5swC7QzRy0fUvbCTfNvgX7bjebsYmqWYXzH6Z+V/A2wPHr2V5ftToxbxGzNjQ0QdwPFMfREDGLg7MJYobp61Or01eNuJZ5IuZ9in2Z1WPb7bOEXZOZeYh9j/4esTrdHSJueWhogBj7gO5BY2g1Mfb1koOQcfopPMe0wIDm28CL4ELDBV8Ee503FRGzRT/pISHB7m7mAArJImYx+hodLFB9K6ReuEXj3uAhAeyt3tQCbe96mMUdcnczOz3EYh5wXw78/3hINElu0e1gjn5iZYQ4VsIYWolWFOibcEB3nPeyFIztO68aR72cNCklOBomcxur4ecOGvbQTiyzONca7NyKbqLwZc9UMKdW8EVI8EJW8tJ2ImR+Ftke4h5DH7veRoWPU5zrOG2vuBlLuN+4HMzJFcyEv8zED6E/3NU1HNvxRQ3tI+geznU7+sXdU86sSDATdauXV1LcbPWShFXGhP+KjlC92uySvMR47G68Hes4xyiKfWPXuAPc5OWkmS0r+AO+555gQvcwYfZIUkTMtvYw/byGNtDXXvqa5/4y/I6G6edUZuah7+tp+4hzxX6IniJ+hPjN1Hdlrhaiv4amBAbczWPSCm8qS/3Fhk2S+0rB8fV/CKHe8TGJ8l70r7tboG03Rf05mvrO0FAC+vrSu4lmxqxgHk0Ocg0bkf1AwF6Hxuok2sKKOeBd2erZge9N9JfHNOs0eg7tavDVRReN73xb2j0mbL2M+yuKtfjGm2NMtD1E+bTFOpuwP0OF8W1k493Pddnd+syBQUWvYFENc/Iuei6hBCeOEpw4SnDiKMGJowQnjhKcOEpw4ijBiaMEJ44SnDhKcOIowYmjBCeOEpw4SnDiKMGJU3WC7df+f2fVFuxHa2K2U8t+wZgD3+feLGY75HOAhB7JUhuSa3+De4c3ixQgofd7fi3B290tUoLE7ka/keP6X7uLhCC5S5D+Zx0hhBBCCCGEEEIIIYQQIil6ev4H0L1DGlhlR+UAAAAASUVORK5CYII=')
                no-repeat;

                /* margin:-29px; */
                margin-top: 5px;
                margin-left:5px;
                margin-right: 70px;
                float:left;
                width: 120px;
                height: 67px;
            }
            .app_header_search {
                float:right;
                padding:15px;
            }
            .slick-header-column {
                background-color: #6788B1 !important;
                background-image: none !important;
                color: white !important;
                font-size:9.0pt;
                font-family:"Segoe UI Semibold",sans-serif;
            }
            .slick-row {
                background-color: white !important;
                background-image: none !important;
                color:black !important;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
            }
            .bk-cell-index {
                background-color: white !important;
                background-image: none !important;
                color:black !important;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
            }
        </style>
        </head>
        <body>
        <div id="app_header" class="app_header">		
			<span class="app_header_icon"></span>
			<h1>{{ title }}</h1>
		</div>
        <h3>Executive Summary</h3>
        <h4></h4>
        <p>The CTD was collected on the {{ date }} using a {{ instrument }}.</p> 
        <p>The recommended United Nations Educational, Scientific and Cultural Organisation (UNESCO) formulae was used to process the data and can be found in the <a href="http://unesdoc.unesco.org/images/0005/000598/059832eb.pdf">UNESCO technical papers in marine science 44</a>.
        <br>{{velCalc}} formula was use to determided sound velocity from the CTD data.
        </p>
        <table class=FugroGridTable border=1 cellspacing=0 cellpadding=0
        style='border-collapse:collapse;border:none;margin-left:15px'>
        <thead>
        <tr>
        <td class=TableHeadingGridTable>
        <p class=TableHeading><span style='color:white'>CTD Number</span></p>
        </td>
        <td class=TableHeadingGridTable>
        <p class=TableHeading><span style='color:white'>Date</span></p>
        </td>
        <td class=TableHeadingGridTable>
        <p class=TableHeading><span style='color:white'>Time</span></p>
        </td>
        <td class=TableHeadingGridTable>
        <p class=TableHeading><span style='color:white'>Instrument</span></p>
        </td>
        </tr>
        </thead>
        <tr>
        <td style='border:solid #6788B1 1.0pt;
        border-top:none;padding:0cm 0cm 0cm 0cm'>
        <p class=TableText>{{ filename }}</p>
        </td>
        <td class=TableTextGridTable>
        <p class=TableText>{{ date }}</p>
        </td>
        <td class=TableTextGridTable>
        <p class=TableText>{{ time }}</p>
        </td>
        <td class=TableTextGridTable>
        <p class=TableText>{{ instrument }}</p>
        </td>
        </tr>
        </table>
        <p></p>
        <table class=FugroLinedTable border=1 cellspacing=0 cellpadding=0
        style='border-collapse:collapse;border:none;margin-left:15px'>
        <thead>
        <tr>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Latitude</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Longitude</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Easting &#91;m&#93;</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Northing &#91;m&#93;</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Max. Depth &#91;m&#93;</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Average SV &#91;m/s&#93;</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>SV at Seabed &#91;m/s&#93;</span></p>
        </td>
        <td class=TableHeadingLinedTable>
        <p class="TableHeading Centre"><span style='color:#6788B1'>Temperature at Seabed &#91;&#176;C&#93;</span></p>
        </td>
        </tr>
        </thead>
        <tr>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ lat }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ lon }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ easting }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ northing }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ depth }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ avSV }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ SVS }}</p>
        </td>
        <td class=TableTextLinedTable>
        <p class="TableText Centre">{{ temp }}</p>
        </td>
        </tr>
        <tr>
        <td colspan=8 class=TableTextLinedTable>
        <p class=TableNote>Note:
        <br>Geodetic Parameters = {{ geodetic }}
        <br>Sound Velocity Calculation = {{ velCalc }}</p>
        </td>
        </tr>
        </table>
        <p></p>
        <h3>Interactive Plots</h3>
        <h4></h4>
        <div style="margin-left: 15px;">
        {{ plot_div.p }}
        </div>
        <h3>Interactive Table</h3>
        <h4></h4>
        <div style="margin-left: 15px;">
        {{ plot_div.tbl }}
        </div>
        {{ plot_script }}
        </body>
    </html>
    ''')

    resources = INLINE

    js_resources = resources.render_js()
    css_resources = resources.render_css()

    script, div = components({'p': p, 'tbl': datatbl})
    
    html = template.render(js_resources=js_resources,css_resources=css_resources,plot_script=script,plot_div=div,velCalc=velCalc,
                           title=htmltitle,filename=filename,location=Area,lat=Lat,lon=Lon,easting=Easting,northing=Northing,
                           instrument=instrument,geodetic=geodetic,date=Date,time=Time,temp=temp,avSV=avSV,SVS=seabedvel,depth=depth
                           )
    ###### -- end -- ########

    ###### -- save the document in a HTML -- ########
    with open(htmlfile, 'w', encoding="utf-8") as f:
        f.write(html)

    ###### -- end -- ########

    reset_output()


def multiplegraph(velFilesSelect, outputFolder, velCalc, instrument, geodetic):
    if len(velFilesSelect) == 1:
        filename = os.path.splitext(os.path.basename(velFilesSelect[0]))[0]   
    else:
        filename = str(os.path.splitext(os.path.basename(velFilesSelect[0]))[0]) + '_to_' + str(os.path.splitext(os.path.basename(velFilesSelect[-1]))[0])
    
    dfinfo = pd.DataFrame(columns = ['CTD Name', 'Date', 'Time', 'Latitude', 'Longitude', 'Easting [m]', 'Northing [m]', 
                                     'Max. Depth [m]', 'Average SV [m/s]', 'SV at Seabed [m/s]', 'Temperature at Seabed [degC]'])
    
    
    svp = "Sound Velocity [" + velCalc + ", m/s]" if velCalc is not None else "Sound Velocity [m/s]"
    htmlfile = outputFolder + '\\' + filename + '.html'
    
    for index, f in enumerate(velFilesSelect):
        # get info from file      
        fn, Job_Number, Date, Time, Vessel, Area, Client, Easting, Northing, Lat, Lon = lsinfo(f)    
        # Parameters
        htmltitle = Client + " – " + Area
        # get data
        dfvelu = pd.read_csv(f, skiprows=5, sep=" ", header=None, usecols=[3,4,6]) #[3]=depth, [4]=velocity, [6]=temperature       
        dfvelu[3] = dfvelu[3] * -1
        temp = round(dfvelu[6].mean(),2) # Temperature at Seabed [°C]
        avSV = round(dfvelu[4].mean(),2) # Average SV [m/s] 
        seabedvel = round(dfvelu[4].iloc[-1],2) # SV at Seabed [m/s]
        depth = round(dfvelu[3].min(),2) # Max. Depth [m]
        dfinfo = dfinfo.append(pd.Series([fn, Date, Time, Lat, Lon, Easting, Northing,
                                          depth, avSV, seabedvel, temp], index=dfinfo.columns), ignore_index=True)
        
    dfvel = pd.concat([pd.read_csv(f, skiprows=5, sep=" ", header=None, usecols=[3,4,6], names=['depth', 'velocity', 'temperature'])
                       .assign(file=os.path.basename(f)) for f in velFilesSelect])
    dfvel['depth'] = dfvel['depth'] * -1
    dfvel.sort_values(['file', 'depth'], ascending=[True, False], inplace=True)

    ################ PLOTS PARAMETERS ################
    plot_options = dict(y_axis_label='Depth [Hydrostatic, m]',
                        background_fill_color='#F4ECDC',
                        width=600,
                        height=600,
                        title="",
                        toolbar_location=None,
                        #tools='crosshair,pan,wheel_zoom,box_zoom,reset,hover,save'
                        )

    ################ PLOTS ################
    ###### -- Figure -- ########
    renderer_list = []
    legend_items = []
    line0 = figure(**plot_options)#, tooltips=vToolTips)
    line1 = figure(y_range=line0.y_range, **plot_options)#, tooltips=tToolTips)
    
    for (name, group), color in zip(dfvel.groupby('file'), FugroColorList):
        source = ColumnDataSource(dict(Depth=group.depth,
                            Sound_Velocity=group.velocity,
                            Temperature=group.temperature))
        l0 = line0.line(x="Sound_Velocity", y="Depth", color=color, source=source)
        line0.xaxis.axis_label = svp
        line0.x_range.bounds = 'auto'
        line0.y_range.bounds = 'auto'
        line0.axis.axis_label_text_font_size = "14pt"
        line0.axis.axis_label_text_font_style = "bold"
        
        l1 = line1.line(x="Temperature", y="Depth", color=color, source=source)
        line1.xaxis.axis_label = "Temperature [°C]"
        line1.x_range.bounds = 'auto'
        line1.y_range.bounds = 'auto'
        line1.axis.axis_label_text_font_size = "14pt"
        line1.axis.axis_label_text_font_style = "bold"
        
        line0.add_tools(HoverTool(renderers=[l0], 
                                  tooltips=[("CTD", name),
                                            ("Depth", "$y{0.1f} m"),
                                            ("SV", "$x{0.1f} m/s"),
                                            ("Temp.", "@Temperature{0.1f} °C")],
                                  mode='mouse',
                                  line_policy="interp"))
        line1.add_tools(HoverTool(renderers=[l1],
                                  tooltips=[("CTD", name),
                                            ("Depth", "$y{0.1f} m"),
                                            ("SV", "@Sound_Velocity{0.1f} m/s"),
                                            ("Temp.", "$x{0.1f} °C")],
                                  mode='mouse',
                                  line_policy="interp"))
    
        
        renderer_list += [l0, l1]
        legend_items.append(LegendItem(label=name, renderers=[l0, l1]))
  
    # https://stackoverflow.com/questions/56825350/how-to-add-one-legend-for-that-controlls-multiple-bokeh-figures
    # https://stackoverflow.com/questions/61115734/how-to-work-with-columndatasource-and-legenditem-together-in-bokeh

    ## Use a dummy figure for the LEGEND
    dum_fig = figure(plot_width=300,plot_height=600,outline_line_alpha=0,toolbar_location=None)
    # set the components of the figure invisible
    for fig_component in [dum_fig.grid[0],dum_fig.ygrid[0],dum_fig.xaxis[0],dum_fig.yaxis[0]]:
        fig_component.visible = False
    # The glyphs referred by the legend need to be present in the figure that holds the legend, so we must add them to the figure renderers
    dum_fig.renderers += renderer_list
    # set the figure range outside of the range of all glyphs
    dum_fig.x_range.end = 1005
    dum_fig.x_range.start = 1000
    # add the legend
    dum_fig.add_layout(Legend(click_policy='hide',location='top_left',border_line_alpha=0,items=legend_items))

    figrid = gridplot([line0, line1],ncols=2)
    final = gridplot([[figrid,dum_fig]],toolbar_location=None)

    ################ TABLES ################
    ###### Data Table ###### 
   
    #datatbl = gridplot(tbData, ncols=3, sizing_mode='stretch_both')
    # https://gist.github.com/dennisobrien/450d7da20daaba6d39d0
    source = ColumnDataSource(dict(Depth=dfvel['depth'],
                              Sound_Velocity=dfvel['velocity'],
                              Temperature=dfvel['temperature'],
                              CTD_Number=dfvel['file']))
    original_source = ColumnDataSource(dict(Depth=dfvel['depth'],
                                       Sound_Velocity=dfvel['velocity'],
                                       Temperature=dfvel['temperature'],
                                       CTD_Number=dfvel['file']))
    
    columns = [TableColumn(field="Depth", title="Depth [m]", formatter=NumberFormatter(format="0.00"), width=None),
                TableColumn(field="Sound_Velocity", title=svp, formatter=NumberFormatter(format="0.00"), width=None),
                TableColumn(field="Temperature", title="Temperature [°C]", formatter=NumberFormatter(format="0.00"), width=None),
                TableColumn(field="CTD_Number", title="CTD Number", width=None),
                ]
    data_table = DataTable(source=source, columns=columns, sizing_mode="stretch_width")
    
    # callback code to be used by all the filter widgets
    # requires (source, original_source, ctd_select_obj)
    combined_callback_code = """
    var data = source.data;
    var original_data = original_source.data;
    var CTD_Number = ctd_select_obj.value;
    console.log("CTD Number: " + CTD_Number);
    for (var key in original_data) {
        data[key] = [];
        for (var i = 0; i < original_data['CTD_Number'].length; ++i) {
            if (CTD_Number === "ALL" || original_data['CTD_Number'][i] === CTD_Number) {
                data[key].push(original_data[key][i]);
            }
        }
    }

    source.change.emit();
    target_obj.change.emit();
    """

    # define the filter widgets, without callbacks for now
    if len(dfvel['file'].unique()) == 1:
        ctd_list = dfvel['file'].unique().tolist()
    else:
        ctd_list = ['ALL'] + dfvel['file'].unique().tolist()
    ctd_select = Select(title="CTD Number:", value=ctd_list[0], options=ctd_list)

    # now define the callback objects now that the filter widgets exist
    generic_callback = CustomJS(
        args=dict(source=source, 
                original_source=original_source, 
                ctd_select_obj=ctd_select, 
                target_obj=data_table),
        code=combined_callback_code
    )
    
    # finally, connect the callbacks to the filter widgets
    ctd_select.js_on_change('value', generic_callback)
   
    # https://discourse.bokeh.org/t/extract-csv-from-button-in-bokeh-2-1-1/5980/8

    button = Button(label="Download", button_type="success")

        # var ordercolumns = [{
        #     'CTD Number': columns.CTD_Number,
        #     'Depth [m]': columns.Depth,
        #     'Sound Velocity [m/s]': columns.Sound_Velocity,
        #     'Temperature [°s]': columns.Temperature,
        #     }]

    # Not very nice but this order the csv file and rename the colunms properly
    javaScript="""
    function table_to_csv(source) {
        const columns = Object.keys(source.data)
        const nrows = source.get_length()
        const lines = [['CTD Number','Depth [m]','Sound Velocity [m/s]','Temperature [degC]'].join(',')]

        for (let i = 0; i < nrows; i++) {
            let row = [];
            row.push(source.data['CTD_Number'][i].toString())
            row.push(source.data['Depth'][i].toString())
            row.push(source.data['Sound_Velocity'][i].toString())
            row.push(source.data['Temperature'][i].toString())
            lines.push(row.join(','))
        }
        return lines.join('\\n').concat('\\n')
    }

    var filetext = table_to_csv(source)
    var CTD_Number = ctd_select_obj.value.replace('.vel','')
    const fname = CTD_Number + '_CTD_Data.csv'
    const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

    //addresses IE
    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, fname)
    } else {
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = fname
        link.target = '_blank'
        link.style.visibility = 'hidden'
        link.dispatchEvent(new MouseEvent('click'))
    }
    """

    button.js_on_click(CustomJS(args=dict(source=source, ctd_select_obj=ctd_select),code=javaScript))
    
    widgets = column([ctd_select, button], height=250, width=300)
    datatbl = column(row(widgets, data_table), sizing_mode="stretch_both")

    ###### Info Table ######   
    columnsInfo = [TableColumn(field=Ci, title=Ci, width=None) for Ci in dfinfo.columns] # bokeh columns
    info_table = DataTable(columns=columnsInfo, source=ColumnDataSource(dfinfo), autosize_mode="fit_columns", 
                           height=25*len(dfinfo)+25) # bokeh table
    
    saveinfo =Button(label="Download", button_type="success", height=30, width=90)
    
    # Not very nice but this order the csv file and rename the colunms properly
    javaScript="""
    function table_to_csv(source) {
        const columns = Object.keys(source.data)
        const nrows = source.get_length()
        const lines = [['CTD Name', 'Date', 'Time', 'Latitude', 'Longitude', 'Easting [m]', 'Northing [m]', 
                        'Max. Depth [m]', 'Average SV [m/s]', 'SV at Seabed [m/s]', 'Temperature at Seabed [degC]'].join(',')]

        for (let i = 0; i < nrows; i++) {
            let row = [];
            row.push(source.data['CTD Name'][i].toString())
            row.push(source.data['Date'][i].toString())
            row.push(source.data['Time'][i].toString())
            row.push(source.data['Latitude'][i].toString())
            row.push(source.data['Longitude'][i].toString())
            row.push(source.data['Easting [m]'][i].toString())
            row.push(source.data['Northing [m]'][i].toString())
            row.push(source.data['Max. Depth [m]'][i].toString())
            row.push(source.data['Average SV [m/s]'][i].toString())
            row.push(source.data['SV at Seabed [m/s]'][i].toString())
            row.push(source.data['Temperature at Seabed [degC]'][i].toString())
            lines.push(row.join(','))
        }
        return lines.join('\\n').concat('\\n')
    }
    var filetext = table_to_csv(source)
    const fname = 'CTD_SummaryTable.csv'
    const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

    //addresses IE
    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, fname)
    } else {
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = fname
        link.target = '_blank'
        link.style.visibility = 'hidden'
        link.dispatchEvent(new MouseEvent('click'))
    }
    """

    saveinfo.js_on_click(CustomJS(args=dict(source=ColumnDataSource(dfinfo)),code=javaScript))
    
    widgets = row([saveinfo], height=33)
    infotbl = layout([widgets, info_table], sizing_mode="stretch_width")
    
    #infotbl = layout([[info_table]], sizing_mode='stretch_width')

    ########## RENDER PLOTS ################
    ###### -- Define our html template for out plots -- ########
    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
        <title>'CTD {{filename}}'</title>
            {{ js_resources }}
            {{ css_resources }}
        <style>
        	h1 {font-family: 'segoe ui', sans-serif;
                display: block;
                font-size: 160%;
                margin-block-start: 0em;
                margin-block-end: 0em;
                margin-inline-start: 0px;
                margin-inline-end: 0px;
                font-weight: bold;
                padding-top: 7px;
		        }
            h2 	{font-family: 'segoe ui', sans-serif;
                color: #ffffff;
                margin: 60px 0px 0px 0px;
                padding: 0px 0px 6px 150px;
                font-size: 35px;
                line-height: 48px;
                letter-spacing: -2px;
                font-weight: bold;
                background-color: #011E41;
                }
            h3  {font-family: 'segoe ui', sans-serif;
                color: #011E41;
                margin: 20px 0px 0px 15px;
                padding: 0px 0px 6px 0px;
                font-size: 28px;
                line-height: 44px;
                letter-spacing: -2px;
                #font-weight: bold;
                }
            h4  {font-family: 'segoe ui', sans-serif;
                color: #011E41;
                margin: 0px 0px 10px 15px;
                padding: 0px 0px -5px 0px;
                font-size: 24px;
                line-height: 44px;
                letter-spacing: -2px;
                font-style: italic;
                border-bottom-style: solid;
                border-width: 2px;
                border-color: #011E41;
                }
            p {font-family: 'segoe ui', sans-serif;
                font-size: 16px;
                line-height: 24px;
                margin: 0 0 24px 15px;
                text-align: left;
                ///text-justify: inter-word;
                }
            p.noteSmall {font-size:8.0pt;
                    line-height:12pt;
                    color:#808080;                
                }
            p.noteNormal {font-size:10.0pt;
                    color:#808080;                
                }
            ul {font-family: 'segoe ui', sans-serif;
                font-size: 16px;
                line-height: 24px;
                margin: 0 0 24px;
                text-align: left;
                ///text-justify: inter-word;
                }
            p.TableText, li.TableText, div.TableText
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
                }
            p.TableNote, li.TableNote, div.TableNote
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                line-height:12pt;
                font-size:8.0pt;
                font-family:"Segoe UI",sans-serif;
                color:#808080;
                }
            .TableText.Centre
                {text-align:center;
                }                
            p.TableHeading, li.TableHeading, div.TableHeading
                {margin-top:3.0pt;
                margin-right:5.65pt;
                margin-bottom:3.0pt;
                margin-left:5.65pt;
                font-size:9.0pt;
                font-family:"Segoe UI Semibold",sans-serif;
                }
            .TableHeading.Centre
                {text-align:center;
                }   
            td.TableHeadingGridTable
                {border:solid #6788B1 1.0pt;
                border-right:solid white 1.0pt;
                background:#6788B1;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableTextGridTable
                {border-top:none;
                border-left:none;
                border-bottom:solid #6788B1 1.0pt;
                border-right:solid #6788B1 1.0pt;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableHeadingLinedTable
                {border:none;
                border-bottom:solid #6788B1 1.0pt;
                background:white;
                vertical-align: bottom;
                padding:0cm 0cm 0cm 0cm;
                }
            td.TableTextLinedTable
                {border:none;
                border-bottom:solid #7F7F7F 1.0pt;
                vertical-align: top;
                padding:0cm 0cm 0cm 0cm;
                }
            .app_header {
                height:80px;
                width: 100%;
                background-color:#011E41;
                color:#eee;
                margin-left: auto;
                margin-right: auto;
            }
            @media screen and (min-width : 1024px) {
                .app_header {
                    width: 100%;
                }
            }
            .app_header a {
                color: #900;
            }
            .app_header_icon {			
                background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAABDCAYAAABX2cG8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAALiMAAC4jAXilP3YAAASVSURBVHhe7ZxdiFVVFMfnq0LSJsI0CpKwhzJ6iXwYLQiiCAYCn4QeRJLoqbRUjKC0t6EPwd4iKiMsSsge+kA0kiIjQQoSpMwIYYixtI9RCZM7/dY+y+s995572feMZz72/H/wZ++19jr77LPX3fuec7xjjxBCCCGEEEIIIYQQQghRMb1eVkatVnuQ4g10Q3B0z7G+vr5lXhcziYmJiX4SPEZZGo7/0bsTJejzsioW9Pb2LvK6mAYq3aJZgNdS/JlZeWgbpfg+szoyyhb9uNfFTMISbNtsEWy9qz1MVEjVW3Qn/vNSVEjXWzSLbyGKPW6Q7+BjXs9BH49SfJJZnWGLPulVuyu/jmIgsy7Bec6gc24GPLY/s6I4x7nOej1AH6XvIWw8Ni4369j82TxSjZ5/+jmNLrhZHVzwGQY31dR3Gs5/2H058K/3EJvAQewvspZ4OOY8et67CWDXvLlrOPQC+pDqoHdn/S1FR7OIeDhmFA15N9FM5xZ9uZnw0hK8kU/7fW5GwzFXoBeYyDvdNSnoqx+tYjzPuMt4Ed9tXo+GY26keD2z4ul6i+bi3+FkV7nZES5swC7QzRy0fUvbCTfNvgX7bjebsYmqWYXzH6Z+V/A2wPHr2V5ftToxbxGzNjQ0QdwPFMfREDGLg7MJYobp61Or01eNuJZ5IuZ9in2Z1WPb7bOEXZOZeYh9j/4esTrdHSJueWhogBj7gO5BY2g1Mfb1koOQcfopPMe0wIDm28CL4ELDBV8Ee503FRGzRT/pISHB7m7mAArJImYx+hodLFB9K6ReuEXj3uAhAeyt3tQCbe96mMUdcnczOz3EYh5wXw78/3hINElu0e1gjn5iZYQ4VsIYWolWFOibcEB3nPeyFIztO68aR72cNCklOBomcxur4ecOGvbQTiyzONca7NyKbqLwZc9UMKdW8EVI8EJW8tJ2ImR+Ftke4h5DH7veRoWPU5zrOG2vuBlLuN+4HMzJFcyEv8zED6E/3NU1HNvxRQ3tI+geznU7+sXdU86sSDATdauXV1LcbPWShFXGhP+KjlC92uySvMR47G68Hes4xyiKfWPXuAPc5OWkmS0r+AO+555gQvcwYfZIUkTMtvYw/byGNtDXXvqa5/4y/I6G6edUZuah7+tp+4hzxX6IniJ+hPjN1Hdlrhaiv4amBAbczWPSCm8qS/3Fhk2S+0rB8fV/CKHe8TGJ8l70r7tboG03Rf05mvrO0FAC+vrSu4lmxqxgHk0Ocg0bkf1AwF6Hxuok2sKKOeBd2erZge9N9JfHNOs0eg7tavDVRReN73xb2j0mbL2M+yuKtfjGm2NMtD1E+bTFOpuwP0OF8W1k493Pddnd+syBQUWvYFENc/Iuei6hBCeOEpw4SnDiKMGJowQnjhKcOEpw4ijBiaMEJ44SnDhKcOIowYmjBCeOEpw4SnDiKMGJU3WC7df+f2fVFuxHa2K2U8t+wZgD3+feLGY75HOAhB7JUhuSa3+De4c3ixQgofd7fi3B290tUoLE7ka/keP6X7uLhCC5S5D+Zx0hhBBCCCGEEEIIIYQQIil6ev4H0L1DGlhlR+UAAAAASUVORK5CYII=')
                no-repeat;

                /* margin:-29px; */
                margin-top: 5px;
                margin-left:5px;
                margin-right: 70px;
                float:left;
                width: 120px;
                height: 67px;
            }
            .app_header_search {
                float:right;
                padding:15px;
            }
            .slick-header-column {
                background-color: #6788B1 !important;
                background-image: none !important;
                color: white !important;
                font-size:9.0pt;
                font-family:"Segoe UI Semibold",sans-serif;
            }
            .slick-row {
                background-color: white !important;
                background-image: none !important;
                color:black !important;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
            }
            .bk-cell-index {
                background-color: white !important;
                background-image: none !important;
                color:black !important;
                font-size:9.0pt;
                font-family:"Segoe UI",sans-serif;
            }
        </style>
        </head>
        <body>
        <div id="app_header" class="app_header">		
			<span class="app_header_icon"></span>
			<h1>{{ title }}</h1>
		</div>
        <h3>Executive Summary</h3>
        <h4></h4>
        <p>The CTD was collected on the {{ date }} using a {{ instrument }}.</p> 
        <p>The recommended United Nations Educational, Scientific and Cultural Organisation (UNESCO) formulae was used to process the data and can be found in the <a href="http://unesdoc.unesco.org/images/0005/000598/059832eb.pdf">UNESCO technical papers in marine science 44</a>.
        <br>{{velCalc}} formula was use to determided sound velocity from the CTD data.
        </p>
        <div style="margin-left: 15px;">
        {{ plot_div.tblInfo }}
        <hr>  
        </div>              
        <p class=noteSmall>Note:
        <br>Geodetic Parameters = {{ geodetic }}
        <br>Sound Velocity Calculation = {{ velCalc }}</p>
        <p></p>
        <h3>Interactive Plots</h3>
        <h4></h4>
        <p class=noteNormal>The graphs are interactive with the option of zoom in and out, move, save a image and have o hover tooltips.
        <br>The legend is interative too and by clicking on a item the data in the graph will be hidden.</p>        
        <div style="margin-left: 15px;">
        {{ plot_div.p }}
        </div>
        <h3>Interactive Table</h3>
        <h4></h4>
        <div style="margin-left: 15px;">
        {{ savebt }}
        {{ plot_div.tblData }}
        </div>
        {{ plot_script }}
        </body>
    </html>
    ''')

    resources = INLINE

    js_resources = resources.render_js()
    css_resources = resources.render_css()

    script, div = components({'p': final, 'tblData': datatbl, 'tblInfo': infotbl})
    
    html = template.render(js_resources=js_resources,css_resources=css_resources,plot_script=script,plot_div=div,velCalc=velCalc,
                           title=htmltitle,filename=filename,location=Area,lat=Lat,lon=Lon,easting=Easting,northing=Northing,
                           instrument=instrument,geodetic=geodetic,date=Date,time=Time,temp=temp,avSV=avSV,SVS=seabedvel,
                           depth=depth)
    ###### -- end -- ########

    ###### -- save the document in a HTML -- ########
    with open(htmlfile, 'w', encoding="utf-8") as f:
        f.write(html)

    ###### -- end -- ########

    reset_output()

# Others function
# https://stackoverflow.com/questions/42915638/bokeh-datatables-overlapping-in-both-row-and-gridplot#
def multi_table(d,sv,t,svp):
    source = ColumnDataSource(data=dict())
    source.data = {'Depth': d, 'SoundVelocity': sv, 'Temperature': t}
    columns = [TableColumn(field="Depth", title="Depth [m]", formatter=NumberFormatter(format="0.00"), width=None),
                TableColumn(field="SoundVelocity", title=svp, formatter=NumberFormatter(format="0.00"), width=None),
                TableColumn(field="Temperature", title="Temperature [°C]", formatter=NumberFormatter(format="0.00"), width=None),
                ]
    data_table = DataTable(source=source, columns=columns, autosize_mode="fit_columns")
    return data_table

# from https://www.pakstech.com/blog/python-gooey/
def print_progress(index, total):
    print(f"progress: {index+1}/{total}", flush=True)
    
# Progrees bar GUI and CMD
def progressBar(cmd, pbar, index, ls):
    if cmd:
        pbar.update(1)
    else:
        print_progress(index, len(ls)) # to have a nice progress bar in the GU            
        if index % math.ceil(len(ls)/10) == 0: # decimate print
            print(f"Files Process: {index+1}/{len(ls)}", flush=True) 

if __name__ == "__main__":
    now = datetime.datetime.now() # time the process
    main()
    print('', flush=True)
    print("Process Duration: ", (datetime.datetime.now() - now), flush=True) # print the processing time. It is handy to keep an eye on processing performance.