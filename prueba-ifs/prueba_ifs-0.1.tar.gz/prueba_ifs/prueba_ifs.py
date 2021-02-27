from tkinter import filedialog
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from astropy.io import fits
import matplotlib.colors
import cv2
from astropy.visualization.mpl_normalize import simple_norm
import math
from skimage import exposure
from astropy.wcs import WCS
import os
import warnings
from tkinter import messagebox as MessageBox
from astropy.stats import sigma_clip
from scipy import interpolate
import ctypes
from astropy.coordinates import SkyCoord
from PIL import Image
from PIL import ImageTk
import matplotlib.patches as patches
from tkinter import scrolledtext
import tkinter.font as tkFont
import platform



class prueba_ifs():
    canvas = 0
    f2 = ''
    file_dir = ''
    band = 0
    arr_w  = np.zeros(2)
    arr_f = np.zeros(2)
    name = ''
    hi_data = ''
    data = ''
    header_file = ''
    wcs_header = ''
    crval  = 0
    cdelt  = 0
    crpix  = 0
    size_x  = 0
    size_y  = 0
    pixels = 1
    x_ticks = []
    y_ticks = []
    x_ticks_l = []
    y_ticks_l = []
    Integrated_spectrum =[]
    integrated_x = []
    integrated_y = []
    
    Dec = 0
    RA = 0
    wcs = 0 
    arrlambda = np.zeros(pixels) 
    array_data = 0
    dband=0
    res = []
    cir_x = 0
    cir_y = 0
    name_f = "" 
    
    
    sout = 0
    infinite= 0
    spectrum= 0    
    min_value_da= 0
    max_value_da= 0
    
    
    #--------banderas
    
    flag_explorer = 0
    flag_flux=0
    flag_wave=0
    flag_band=0
    flag_file=0
  #  band_sticks = 0
    flag_integrate_region = 0
    flag_integrate_region2 = 0
    flag_create_fits = 0
    flag_system = 0 # 0 windows 1 ubuntu/mac
 #   operative_system()
    
    #parte auxiliar
    
    red_marks = []
    maps_array = []
    maps_array_inv = []
    ax1 = 0
    ax0 = 0
    saved_image = 0
    
    #parte para crear los mapas solo una vez:
    prism = matplotlib.colors.LinearSegmentedColormap.from_list('custom prism', [(0,    "white"),(0.2, '#000000'),(0.4, '#8b0000'),(0.6, '#f63f2b'),(0.8, '#15E818'),(1, '#1139d9'  )], N=256)
    stern = matplotlib.colors.LinearSegmentedColormap.from_list('custom stern',[(0,    "white"),(0.2, '#8b0000'),(0.3, '#e42121'),(0.4, '#252850'),(0.6, '#0588EF'), (0.8, '#3b83bd'),(1, '#c6ce00'  )], N=256)
    std = matplotlib.colors.LinearSegmentedColormap.from_list('custom Std-Gamma', [(0,    "white"),(0.2, '#0000ff'),(0.4, '#2178E4'),(0.6, '#ff0000'),(0.8, '#ff8000'),(1, '#ffff00'  )], N=256)
    BGRY = matplotlib.colors.LinearSegmentedColormap.from_list('custom BGRY', [(0,    "white"),(0.2, '#ff8000'),(0.4, '#EFEE05'),(0.6, '#EF5A05'),(0.8, '#51EF05'),(1, '#0000ff'  )], N=256)
    califa = matplotlib.colors.LinearSegmentedColormap.from_list('custom CALIFA special', [(0,    "white"),(0.25, '#00008B'),(0.5, '#B2FFFF'),(0.62, '#B2FFFF'),(0.75, '#ff4000'),(1, '#008f39'  )], N=256)
    ping = matplotlib.colors.LinearSegmentedColormap.from_list('custom Pingsoft-special', [(0,    "white"),(0.25, '#00008B'),(0.5, '#3b83bd'),(0.75, '#ff8000'),(1, '#ffff00'  )], N=256)
    
    
    prism_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom prism inv', [(0,    '#1139d9'),(0.2, '#15E818'),(0.4, '#f63f2b'),(0.6, '#8b0000'),(0.8, '#000000'),(1, "white"  )], N=256)
    stern_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom strn inv', [(0,    '#c6ce00'),(0.2, '#3b83bd'),(0.3, '#0588EF'),(0.4, '#252850'),(0.6, '#e42121'),(0.8, '#8b0000'),(1, "white"  )], N=256)
    std_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom std inv', [(0,    '#ffff00'),(0.2, '#ff8000'),(0.4, '#ff0000'),(0.6, '#2178E4'),(0.8, '#0000ff'),(1, "white"  )], N=256)
    BGRY_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom BGRY inv', [(0,    '#0000ff'),(0.2, '#51EF05'),(0.4, '#EF5A05'),(0.6, '#EFEE05'),(0.8, '#ff8000'),(1, "white"  )], N=256)
    califa_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom CALIFA inv', [(0,    '#008f39'),(0.25, '#ff4000'),(0.5, '#B2FFFF'),(0.62, '#B2FFFF'),(0.75, '#00008B'),(1, "white"  )], N=256)
    ping_r= matplotlib.colors.LinearSegmentedColormap.from_list('custom Pingsoft inv', [(0,    '#ffff00'),(0.25, '#ff8000'),(0.5, '#3b83bd'),(0.75, '#00008B'), (1, "white"  )], N=256)
    
    maps_array.append('Blues')
    maps_array.append('Reds')
    maps_array.append('Greens')
    maps_array.append('Greys')
    maps_array.append(ping)
    maps_array.append(califa)
    maps_array.append('rainbow')
    maps_array.append(BGRY)
    maps_array.append(prism)
    maps_array.append(stern)
    maps_array.append(std)
    maps_array_inv.append('Blues_r')
    maps_array_inv.append('Reds_r')
    maps_array_inv.append('Greens_r')
    maps_array_inv.append('Greys_r')
    maps_array_inv.append(ping_r)
    maps_array_inv.append(califa_r)
    maps_array_inv.append('rainbow_r')
    maps_array_inv.append(BGRY_r)
    maps_array_inv.append(prism_r)
    maps_array_inv.append(stern_r)
    maps_array_inv.append(std_r)
    imagen_final = 0
    cmap = maps_array[0]
    color = "#E6E6FA"
    
    
    #de elementos graficos
    window = Tk()
    window.title("IFS Explorer")
    window.geometry("1190x805") #Configurar tamaño
    window.resizable(0, 0)
    radius_ = IntVar()
    band_sticks = IntVar()
    min_value_la = 0
    max_value_la = 0
    varla1 = StringVar()
    varla2 = StringVar()
    varlaflux = StringVar() 
    varla3 = DoubleVar()
    varla4 = DoubleVar()
    varlawave = StringVar()
    varla5 = IntVar()
    varla6 = IntVar()
    varla7 = StringVar()
    varla8 = StringVar()
    varla9 = StringVar()
    varla10 = StringVar()
    varla11 = DoubleVar()
    varla12 = IntVar()
    var = IntVar() 
    var.set(1)
    var3 = StringVar()
    var3 = StringVar()
    sp = IntVar()
    sp1 = IntVar()
    
    
    
    
    def __init__(self): 
        def onclick_(event):
            print("click")
        def move_mouse(event):
            m = 1
        def set_wavelength_range():
            print("set wave")
        def reset_wavelength_range():
            print("reset wave")
        def set_flux_range():
            print("set flux range")
        def reset_flux_range():
            print("reset flux")
        def set_bar(bar_1):
            print("set bar")
        def set_band():
            print("set band")
        def set_scaling():
            print("set scaling")
            
        def set_filter(event):
            print("set filter")
        def set_color_map(event=''):
            print("set color map")
        def set_mark_wavelength():
            print("set")
        def mark_wavelength():
            print("mark")
        
        def set_offsets():
            print("set off")
        
        def create_files():
            print("cretaed")
        def reset_integrated_region():
            print("reset integrated region")
        def button_quit_destroy():
            print("quit")
        
        
        def new_file():
       #     global size_x,size_y
            py_exts = r"*.fits  *.fits.gz *.fits.rar"
            folder_selected = filedialog.askopenfile(mode="r", filetypes = (("fits files",py_exts),("all files","*.*")))
            file_dir = os.path.abspath(folder_selected.name)
            name=folder_selected.name
            nombre2=name.split('/')
            n=nombre2[len(nombre2)-1]
            (prueba_ifs.varla1).set(n)
            name = n
            hi_data = fits.open(file_dir)
            (prueba_ifs.data) = hi_data[0].data
            
            (prueba_ifs.min_value_da)=np.amin((prueba_ifs.data))
            (prueba_ifs.max_value_da)=np.amax((prueba_ifs.data))
            hi_data.info()
            header_file = hi_data[0].header
            
            (prueba_ifs.band_sticks).set(0)
            integrated_x = []
            integrated_y = []
            try:
                crval  = header_file['CRVAL3']
                cdelt  = header_file['CDELT3']
                crpix  = header_file['CRPIX3']
                (prueba_ifs.size_x)  = header_file['NAXIS1']
                (prueba_ifs.size_y)  = header_file['NAXIS2']
                (prueba_ifs.pixels) = header_file['NAXIS3']
                
                    
                    
                create_label_offset()        
                wcs_header = WCS(header_file)
                Dec = 0
                RA = 0
                try:
                    Dec = header_file['CRVAL2']
                    RA = header_file['CRVAL1']
                except KeyError as e:
                    print("no header")
                if RA <= 0: 
                    wcs = 0 
                    (prueba_ifs.varla7).set("     Spaxel        ID           ")
                else: 
                    wcs = 1
                    (prueba_ifs.varla7).set("      Spaxel             ID                        RA                                    DEC                      RA-deg                DEC-deg")
                try:
                    (prueba_ifs.varla9).set("Object: %s"%(header_file['OBJECT']))
                except Exception as e:  
                    try:
                        (prueba_ifs.varla9).set("Object: %s"%(header_file['OBJNAME']))
                    except Exception as e: 
                        (prueba_ifs.varla9).set("Object:  %s "%(name))  
                (prueba_ifs.arrlambda) = np.zeros((prueba_ifs.pixels)) 
                if cdelt == 0:
                    cdelt = 1
                    
                for x in range((prueba_ifs.pixels)):
                    (prueba_ifs.arrlambda)[x] = (crval + x*cdelt)-(crpix-1)*cdelt
                promedio = np.mean((prueba_ifs.arrlambda))
                if promedio < 100:
                    (prueba_ifs.arrlambda) = (prueba_ifs.arrlambda)*10000
                
                (prueba_ifs.f2).clf()
                (prueba_ifs.ax1) = (prueba_ifs.f2).add_subplot(projection=wcs_header, slices=('x', 'y', 2))
                
                update_graph() 
                #extra
                (prueba_ifs.flag_file)=1
            except KeyError as e:
                MessageBox.showerror("Error!",e)
                
        def update_graph():
         #   (prueba_ifs.ax0).cla()
        #    global size_x,size_y
            if (prueba_ifs.flag_file)==1:
                (prueba_ifs.ax0).cla()
            (prueba_ifs.ax0).set_xlabel( 'Wavelength' )
            (prueba_ifs.ax0).set_ylabel( 'Flux' )
            spectrum=(prueba_ifs.data)[:,int((prueba_ifs.size_x)/2),int((prueba_ifs.size_y)/2)]
            spectrum=np.nan_to_num(spectrum)   
            for i in range(0,(prueba_ifs.pixels)):
                if (abs(spectrum[i])>1e30):
                    spectrum[i]=0
            (prueba_ifs.ax0).plot((prueba_ifs.arrlambda),spectrum,color='blue')
            (prueba_ifs.canvas).draw()
            
        def create_label_offset():
            print("labels")
        def integrated_region():
            print("integrated region")
            print((prueba_ifs.min_value_da))
            print((prueba_ifs.max_value_da))
            
        print("iniciando")
        color = "#E6E6FA"
        image_dir=os.getcwd()
        image_ico = image_dir+'\\Img\\logoIFSexplorer.ico'
        (prueba_ifs.window).iconbitmap(image_ico) #Cambiar el icono
        
        image_dir=os.getcwd()
        (prueba_ifs.window).config(bg=color) #Cambiar color de fondo
        image_dir=os.getcwd()
        image_dir = image_dir+'\\Img\\logoIFSexplorer.png'
        image=Image.open(image_dir)
        img = image.resize((150,150))
        photo = ImageTk.PhotoImage(img) 
        label = Label((prueba_ifs.window), image = photo) 
        label.pack()
        label.place_configure(x=15,y=30,width=150,height=150) 
    #    self.main()
    #    imprimir()
        
         #------------------------------
    
        #----  Widget Abrir Fits -----------------------------
        lblframe_widget = LabelFrame((prueba_ifs.window), text = "")
        lblframe_widget.pack ()
        lblframe_widget.place_configure(x=170, y=5, height= 205, width=425)
        lblframe_widget.config(bg=color)
        
        #---------- Label Fits --------------
        lbl_Fits = Label (lblframe_widget, text = "FITS")
        lbl_Fits.pack ()
        lbl_Fits.place_configure(x=4, y= 5)
        lbl_Fits.config(bg=color)
        
        #----------- Objecto Fits  -----------------
        entry_fits =Entry (lblframe_widget,state=DISABLED,textvariable=(prueba_ifs.varla1))
        entry_fits.insert (0, "")
        entry_fits.pack ()
        entry_fits.place_configure(x=40, y=5, height= 25, width=245)
        
        #------- Boton Browse  ---------------
        button_browse = Button (lblframe_widget,text = "Browse", command= new_file)
        button_browse.pack ()
        button_browse.place_configure(x=294, y=5, height= 25, width=60)
            
        #------- Boton Quit  ---------------
        button_quit_i = Button (lblframe_widget,text = "Quit", command= button_quit_destroy)
        button_quit_i.pack ()
        button_quit_i.place_configure(x=360, y=5, height= 25, width=50)
        
        #------- Frame descripcion del Objeto ---------------

        #----------- Entry Objecto Fits  -----------------
        entry_obj =Entry (lblframe_widget,state=DISABLED, textvariable=(prueba_ifs.varla9))
        entry_obj.insert (0, "")
        entry_obj.pack ()
        entry_obj.place_configure(x=5, y=35, height= 24, width=405)
        
        #----------- Entry Objecto Fits  -----------------
        entry_intFlux =Entry (lblframe_widget,state=DISABLED, textvariable=(prueba_ifs.varla10))
        entry_intFlux.insert (0, "")
        entry_intFlux.pack ()
        entry_intFlux.place_configure(x=5, y=55, height= 24, width=405)
        
        
        
        #------- Entrada de Descripcion del Objeto ----------
        box_entry = scrolledtext.ScrolledText(lblframe_widget)
        box_entry.configure(state='disabled',yscrollcommand=TRUE)
        box_entry.pack ()
        box_entry.place_configure(x=5, y=85, height= 110, width=405)
        
        
            #--------  Integrate Region ----------------------------------------------------
        lblfr_WIntg= LabelFrame((prueba_ifs.window), text = "")
        lblfr_WIntg.pack ()
        lblfr_WIntg.place_configure(x=610, y=5, height= 230, width=120)
        lblfr_WIntg.config(bg=color)
        
        #-------- Boton Radius ----------------
        btn_Radius = Button(lblfr_WIntg, text="Integrated Region",command=integrated_region)
        btn_Radius.pack()
        btn_Radius.place_configure(x=4, y=5, height= 25, width=110)
        
        #-------- Label Radius ----------------
        lbl_Radius = Label (lblfr_WIntg, text = "Radius")
        lbl_Radius.pack ()
        lbl_Radius.place_configure(x=25, y= 32)
        lbl_Radius.config(bg=color)
        
        #-------- Entry Radius ----------------
        entry_Radius = Entry(lblfr_WIntg,textvariable=(prueba_ifs.radius_))
        entry_Radius.pack()
        entry_Radius.place_configure(x=5, y=54, height= 20, width=50)
        entry_Radius.config(state=DISABLED)
        
        
         #-------- Boton Radius ----------------
        btn_Radius = Button(lblfr_WIntg, text="Reset",command=reset_integrated_region)
        btn_Radius.pack()
        btn_Radius.place_configure(x=60, y=54, height= 20, width=50)
        
        #-------- Created Files ----------------
        btn_Radius = Button(lblfr_WIntg, text="Create Files",command=create_files)
        btn_Radius.pack()
        btn_Radius.place_configure(x=16, y=85, height= 20, width=80)
        
        #-------- Display Axes ---------------
        lblfr_DisAx= LabelFrame((prueba_ifs.window), text = "Display axis")
        lblfr_DisAx.pack()
        lblfr_DisAx.place_configure(x=610, y=120, height= 110, width=120)
        lblfr_DisAx.config(bg=color)
        
        rb1= Radiobutton(lblfr_DisAx, text="RA-Dec", variable=(prueba_ifs.band_sticks), value=0, command=set_offsets)
        rb2= Radiobutton(lblfr_DisAx, text="Offset", variable=(prueba_ifs.band_sticks), value=1, command=set_offsets)
        
        rb1.pack()
        rb2.pack()
        
        rb1.place_configure(x=5, y=4)
        rb2.place_configure(x=5, y=24)
        
        rb1.config(bg=color)
        rb2.config(bg=color)
        
        
        #-------- Mark Wavelenght ---------------
        lblfr_MWave= LabelFrame((prueba_ifs.window), text = "Mark Wavelenght")
        lblfr_MWave.pack()
        lblfr_MWave.place_configure(x=610, y=185, height= 80, width=120)
        lblfr_MWave.config(bg=color)
        
        #-------- Entry Mark Wavelenght  ----------------- 
        entry_MWave = Entry (lblfr_MWave,textvariable=(prueba_ifs.var3))
        entry_MWave.insert (0, "")
        entry_MWave.pack ()
        entry_MWave.place_configure(x=5, y=8, height= 20, width=100)
        entry_MWave.config(state=DISABLED)
        
        btn_set = Button (lblfr_MWave, text = "Set", command=mark_wavelength)
        btn_set.pack ()
        btn_set.place_configure(x=5, y=36, height= 20, width=50)
        
        btn_set = Button (lblfr_MWave, text = " Reset", command=set_mark_wavelength)
        btn_set.pack ()
        btn_set.place_configure(x=60, y=36, height= 20, width=50)
        
        
         #--------- label frame Display --------
        lblfr_Display= LabelFrame((prueba_ifs.window), text = "Display")
        lblfr_Display.pack()
        lblfr_Display.place_configure(x=740, y=40, height= 160, width=210)
        lblfr_Display.config(bg=color)
        
        lbl_Clr = Label (lblfr_Display, text = "Color Map")
        lbl_Clr.pack ()
        lbl_Clr.place_configure(x=5, y =5)
        lbl_Clr.config(bg=color)
        
        combo1 = ttk.Combobox((prueba_ifs.window),state="readonly",background=color) 
        combo1['values'] = ( 'Blue scaling', 
                                            'Red scaling',
                                            'Green scaling',
                                            'Grayscale',
                                            'PINGSoft special',
                                            'CALIFA-special',
                                            'Rainbow',
                                            'BGRY',
                                            'Prism',
                                            'Stern',
                                            'Std-Gamma')   
        combo1.current(0)
        combo1.bind("<<ComboboxSelected>>", set_color_map)
        combo1.place_configure(x=750, y=85, width= 150, height=28)
     #   combo1.config(bg="#E6E6FA")
        
        
        lbl_filter = Label (lblfr_Display, text = "Filter")
        lbl_filter.pack ()
        lbl_filter.place_configure(x=5, y =60)
        lbl_filter.config(bg=color)
        combo2 = ttk.Combobox(lblfr_Display,state="readonly",background="#E6E6FA") 
        combo2['values'] = ( 'Halpha-KPN0 6547-80A', 
                                            'HALPHA-CTI0 6586-20A',
                                            'B-Johnson (1965)',
                                            'V-Johnson',
                                            'u-SDSS-III',
                                            'g-SDSS-III',
                                            'r-SDSS-III',
                                            'i-SDSS-III',
                                            'B-Bessell (1990)',
                                            'V-Bessell',
                                            'R-Bessell',
                                            'B-KPN0-Harris',
                                            'V-KPN0-Harris',
                                            'R-KPN0-Harris')   
        combo2.current(0)
        combo2.bind("<<ComboboxSelected>>", set_filter)
        combo2.place_configure(x=5, y=80, width= 195, height=28)
        
        checkbtn_InvColMap = Checkbutton(lblfr_Display, text="Invert color map",variable=(prueba_ifs.sp1), onvalue=1, offvalue=0, command=set_color_map)
        checkbtn_InvColMap.select()
        checkbtn_InvColMap.pack()
        checkbtn_InvColMap.place_configure(x=5,y=110)
        checkbtn_InvColMap.config(bg=color)
        
        #----------  label Frame Scalling  ----------------
        lblfr_Scal= LabelFrame((prueba_ifs.window), text = "Scaling")
        lblfr_Scal.pack()
        lblfr_Scal.place_configure(x=960, y=40, height= 160, width=215)
        lblfr_Scal.config(bg=color)
        linear = Radiobutton(lblfr_Scal, text="Linear", variable=(prueba_ifs.var), value=1, command=set_scaling)
        clipping= Radiobutton(lblfr_Scal, text="2% Clipping", variable=(prueba_ifs.var), value=2, command=set_scaling)
        asinh= Radiobutton(lblfr_Scal, text="Asinh", variable=(prueba_ifs.var), value=3, command=set_scaling)
        powerl= Radiobutton(lblfr_Scal, text="Power-Law", variable=(prueba_ifs.var), value=4, command=set_scaling)
        sqRoot= Radiobutton(lblfr_Scal, text="Square Root", variable=(prueba_ifs.var), value=5, command=set_scaling)
        hEqual= Radiobutton(lblfr_Scal, text="Hist Equal", variable=(prueba_ifs.var), value=6, command=set_scaling)
        gaussian= Radiobutton(lblfr_Scal, text="Gaussian", variable=(prueba_ifs.var), value=7, command=set_scaling)
        logarithmic= Radiobutton(lblfr_Scal, text="Logarithmic", variable=(prueba_ifs.var), value=8, command=set_scaling)
        
        linear.pack()
        clipping.pack()
        asinh.pack()
        powerl.pack()
        sqRoot.pack()
        hEqual.pack()
        gaussian.pack()
        logarithmic.pack()
        
        linear.place_configure(x=5, y=20)
        clipping.place_configure(x=5, y=40)
        asinh.place_configure(x=5, y=60)
        powerl.place_configure(x=5, y=80)
        sqRoot.place_configure(x=100, y=20)
        hEqual.place_configure(x=100, y=40)
        gaussian.place_configure(x=100, y=60)
        logarithmic.place_configure(x=100, y=80)
        
        linear.config(bg=color)
        clipping.config(bg=color)
        asinh.config(bg=color)
        powerl.config(bg=color)
        sqRoot.config(bg=color)
        hEqual.config(bg=color)
        gaussian.config(bg=color)
        logarithmic.config(bg=color)
        
        opScal = Label(lblfr_Scal)
        opScal.pack()
        opScal.place_configure(x=5,  y= 100)
        opScal.config(bg=color)
        
        #--------- 
        lblframe_info = LabelFrame((prueba_ifs.window),text="")
        lblframe_info.pack()
        lblframe_info.place_configure(x=15, y=270, width=715, height=100)
        lblframe_info.config(bg=color)
        
        #--------------- Entry Informacion ------------------
        entry_wcs = Entry(lblframe_info, textvariable=(prueba_ifs.varla7),state=DISABLED)
        entry_wcs.insert(0, "")
        entry_wcs.pack()
        entry_wcs.place_configure(x=5, y= 5, width=700, height=20)
        
        entry_coord = Entry(lblframe_info,textvariable=(prueba_ifs.varla8),state=DISABLED)
        entry_coord.insert(0, "")
        entry_coord.pack()
        entry_coord.place_configure(x=5, y= 25, width=700, height=20)
        
        #-------------- Label Shift Filter ------------------
        lbl_shFilter = Label(lblframe_info, text="Shift Filter")
        lbl_shFilter.pack()
        lbl_shFilter.place_configure(x=5, y=50)
        lbl_shFilter.config(bg=color)
        
        #-------------- Entry Shift Filter ------------------
        entry_shFilt = Entry(lblframe_info,state=DISABLED, textvariable=(prueba_ifs.varla11))
        entry_shFilt .insert(0, "0.0")
        entry_shFilt .pack()
        entry_shFilt .place_configure(x=74, y=50, width=60, height=20)
        
        #-------------- Scale -----------------------
        bar_ = Scale(lblframe_info, orient = HORIZONTAL, showvalue= 0, from_=(prueba_ifs.min_value_la)+1, to=(prueba_ifs.max_value_la)-1, sliderlength = 30,command = set_bar )
        bar_.pack()
        bar_.place_configure(x=140, y=50, width= 510)
        bar_.config(bg=color)
        
        #------------ Boton Apply ----------------
        btn_apply = Button(lblframe_info, text="Apply", command=set_band)
        btn_apply.pack()
        btn_apply.place_configure(x=655, y=50, width=50, height=25)
        
        #------------ label frame Flux range ------------------------------------------
        lblframe_flR = LabelFrame((prueba_ifs.window),text="")
        lblframe_flR.pack()
        lblframe_flR.place_configure(x=15, y=215, width=295, height=50)
        lblframe_flR.config(bg=color)
        
        #------------ label Flux range -----------------
        lbl_fluxR = Label(lblframe_flR, text="Flux range")
        lbl_fluxR.pack()
        lbl_fluxR.place_configure(x=5, y=10)
        lbl_fluxR.config(bg=color)
        
        #------------ Entry Flux Range  -----------------
        entry_shFilt = Entry(lblframe_flR,textvariable=(prueba_ifs.varlaflux))
        entry_shFilt.config(state=DISABLED)
        entry_shFilt .pack()
        entry_shFilt .place_configure(x=75, y=10, width=90, height=20)
        
        #------------ Boton set de Flux Range ------------ 
        btn_setFR = Button(lblframe_flR, text="Set",command=set_flux_range)
        btn_setFR.pack()
        btn_setFR.place_configure(x=175, y=10, width=50, height=25)
        
        #------------ Boton reset de Flux Range ------------ 
        btn_resetFR = Button(lblframe_flR, text="Reset",command=reset_flux_range)
        btn_resetFR.pack()
        btn_resetFR.place_configure(x=235, y=10, width=50, height=25)
        
        #--------------------------------------------------------------------------------
         #------------ label frame Wavelenght --------------------------------------------
        lblframe_wave = LabelFrame((prueba_ifs.window),text="")
        lblframe_wave.pack()
        lblframe_wave.place_configure(x=315, y=215, width=285, height=50)
        lblframe_wave.config(bg=color)
        
        #-------------- label Wavelenght range -------------
        lbl_wavelen = Label(lblframe_wave , text="Wavelenght\nrange")
        lbl_wavelen.pack()
        lbl_wavelen.place_configure(x=2, y=5)
        lbl_wavelen.config(bg=color)
        
        #------------ Entry Wavelenght range  -----------------
        entry_wavelen = Entry(lblframe_wave,textvariable=(prueba_ifs.varlawave))
        entry_wavelen .pack()
        entry_wavelen .place_configure(x=80, y=10, width=80, height=20)
        entry_wavelen.config(state=DISABLED)
        
        #------------ Boton set de Wavelenght range ------------ 
        btn_setWl = Button(lblframe_wave, text="Set",command=set_wavelength_range)
        btn_setWl.pack()
        btn_setWl.place_configure(x=166, y=10, width=50, height=25)
        
        #------------ Boton reset de Wavelenght range ------------ 
        btn_resetWl = Button(lblframe_wave, text="Reset",command= reset_wavelength_range)
        btn_resetWl.pack()
        btn_resetWl.place_configure(x=225, y=10, width=50, height=25)
        
        
        f = Figure( figsize=(10.3, 3.7), dpi=80 )
        (prueba_ifs.ax0) = f.add_axes( (0.088, .15, .90, .80), frameon=False)
        
        (prueba_ifs.canvas) = FigureCanvasTkAgg(f, master=(prueba_ifs.window))
        (prueba_ifs.canvas).get_tk_widget().pack()
        (prueba_ifs.canvas).get_tk_widget().place_configure(x=15, y=380, width=715, height=300)
        (prueba_ifs.canvas).draw()
        toolbar = NavigationToolbar2Tk((prueba_ifs.canvas),(prueba_ifs.window) )
        toolbar.pack()
        toolbar.place_configure(x=15, y=670)#, width=715, height=300)
        
        (prueba_ifs.f2) = Figure( figsize=(6.5, 4.8), dpi=80 )
        saved_image = 0 
        canvas2 = FigureCanvasTkAgg((prueba_ifs.f2), master=(prueba_ifs.window))
        canvas2.get_tk_widget().pack()
        canvas2.get_tk_widget().place_configure(x=740, y=270, width=440, height=400)
        canvas2.mpl_connect("motion_notify_event", move_mouse)
        canvas2.mpl_connect("button_press_event", onclick_)
        canvas2.draw()
        toolbar2 = NavigationToolbar2Tk(canvas2,(prueba_ifs.window))
        toolbar2.pack()
        toolbar2.place_configure(x=740, y=670)
        toolbar2.update() 
        
        (prueba_ifs.window).mainloop()
        
        
        
        
    def imprimir(self):
            print("imprimir")
            (prueba_ifs.varla1).set("Holaaaa")
            print((prueba_ifs.varla1).get())
        #    print(self.var3.get())
    
        
        
        
