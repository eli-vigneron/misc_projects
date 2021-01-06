# -*- coding: utf-8 -*-

import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

"""
# calculator gui that takes in a property type: Industrial Land, commercial land, multi-res land,
# the market/study area, the lotzise and returns the city PSF, also have radio boxes for all the adjustments
# including traffic adjustments, IM to IB etc, all the adjustments in the city briefs
"""


def pdf_to_notice_name(pth):
    return roll_address


class MainClass:

    def __init__(self, master):
        self.parent = master
        self.gui()

        # initialize progress bar
        self.progress_frame = ttk.Frame()
        self.progress_frame.grid(row=6, column=2)
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=150, mode="determinate")

        self.error_frame = ttk.Frame()
        self.error_frame.grid(row=5, column=2, columnspan=1)

    def gui(self):
        # adds in a grip box
        gripframe = ttk.Frame()
        gripframe.grid(row=100, column=100)
        ttk.Sizegrip(gripframe).grid(row=100, column=100)

        # --------------------------------------------------------------------------------------------------------
        title = ttk.LabelFrame(myGUI, text='Title')
        title.grid(row=0, column=1, columnspan=1, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        # --------------------------------------------------------------------------------------------------------
        # property type drop-down menu
        market = Label(title, text='Property Type: ', anchor="e").grid(row=0, column=1, sticky=W)

        options3 = ['', 'Industrial Land', 'Commercial Land', 'Multi-Res Land']

        self.value4 = tk.StringVar()
        self.value4.set(options3[0])

        masterframe4 = ttk.Frame()
        masterframe4.grid(row=0, column=1, sticky=E)

        dropdown4 = ttk.Combobox(title, textvariable=self.value4, values=options3)
        dropdown4.grid(row=0, column=2)

        # -------------------------------------------------------------------------------------------------------

        self.Source = StringVar()

        # Lot Size label
        suffix_frame = ttk.Frame()
        suffix_frame.grid(row=2, column=1, sticky=W, columnspan=1)
        suffix_label = Label(title, text="Lot Size: ")
        suffix_label.grid(row=2, column=1, sticky=W)

        suffix_entry = ttk.Entry(title, textvariable=self.Source)
        suffix_entry.config(width=23)
        suffix_entry.grid(row=2, column=2, sticky=E)

        # -------------------------------------------------------------------------------------------------------

        # Market Area drop-down menu
        market1 = Label(title, text='Market Area: ', anchor="e")
        market1.grid(row=1, column=1, sticky=W)

        options12 = ['', '1', '1A', '1B', '1C', '2', '3', '4', '5', '6', '7', '8', '8A', '9', '10', '10A',
                     '11', '11A', '11B', '11C', '12']

        self.Source2 = tk.StringVar()
        self.Source2.set(options12[0])

        masterframe5 = ttk.Frame()
        masterframe5.grid(row=1, column=1, sticky=E)

        dropdown5 = ttk.Combobox(title, textvariable=self.Source2, values=options12)
        dropdown5.grid(row=1, column=2)

        # -------------------------------------------------------------------------------------------------------
        # zone drop-down menu
        market2 = Label(title, text='Zone: ', anchor="e").grid(row=3, column=1, sticky=W)

        options22 = ['', 'IM', 'IB', 'IH', 'RA9', 'RA8', 'RA7', 'RF6', 'RF5', 'RMU']

        self.Source3 = tk.StringVar()
        self.Source3.set(options22[0])

        masterframe5 = ttk.Frame()
        masterframe5.grid(row=3, column=1, sticky=E)

        dropdown5 = ttk.Combobox(title, textvariable=self.Source3, values=options22)
        dropdown5.grid(row=3, column=2)

        # --------------------------------------------------------------------------------------------------------
        # zoning conversions
        market = Label(title, text='Zoning Conversions: ', anchor="e").grid(row=4, column=1, sticky=W)

        options4 = ['', 'IM to IB', 'IM to IH', 'IH to IM', 'IH to IB', 'IB to IM', 'IB to IH']

        self.value5 = tk.StringVar()
        self.value5.set(options4[0])

        masterframe5 = ttk.Frame()
        masterframe5.grid(row=4, column=1, sticky=E)

        dropdown5 = ttk.Combobox(title, textvariable=self.value5, values=options4)
        dropdown5.grid(row=4, column=2)

        # --------------------------------------------------------------------------------------------------------
        # study areas
        market = Label(title, text='Study Area:                    ', anchor="e").grid(row=5, column=1, sticky=W)

        options31 = ['',
                    'COMAREA000',
                    'COMAREA001',
                    'COMAREA003',
                    'COMAREA360']

        self.value41 = tk.StringVar()
        self.value41.set(options31[0])

        masterframe41 = ttk.Frame()
        masterframe41.grid(row=5, column=1, sticky=E)

        dropdown41 = ttk.Combobox(title, textvariable=self.value41, values=options31)
        dropdown41.grid(row=5, column=2)

        # --------------------------------------------------------------------------------------------------------
        # adjust down or up
        self.adjust_up = IntVar()
        self.adjust_up.set(0)
        ttk.Checkbutton(title, text='Invert Adjustments', variable=self.adjust_up, onvalue=1, offvalue=0).grid(
            row=6, column=2, sticky=W)
        # --------------------------------------------------------------------------------------------------------
        # Adjustments
        ac = ttk.LabelFrame(myGUI, text="Adjustments: ")
        ac.grid(row=5, column=1, columnspan=1, sticky='WE', padx=3, pady=5, ipadx=5, ipady=5)

        # --------------------------------------------------------------------------------------------------------
        # traffic adjustments
        market = Label(ac, text='Traffic Adjustment: ', anchor="e").grid(row=5, column=1, sticky=W)

        options5 = ['', 'None to Major', 'None to Moderate', 'Moderate to Major']

        self.value6 = tk.StringVar()
        self.value6.set(options5[0])

        dropdown6 = ttk.Combobox(ac, textvariable=self.value6, values=options5)
        dropdown6.grid(row=5, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Access adjustments

        marketc6 = Label(ac, text='Access Adjustment: ', anchor="e").grid(row=6, column=1, sticky=W)

        optionsc6 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec6 = tk.StringVar()
        self.valuec6.set(options5[0])

        dropdownc6 = ttk.Combobox(ac, textvariable=self.valuec6, values=optionsc6)
        dropdownc6.grid(row=6, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Easement

        marketc7 = Label(ac, text='Easement Adjustment: ', anchor="e").grid(row=7, column=1, sticky=W)

        optionsc7 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec7 = tk.StringVar()
        self.valuec7.set(options5[0])

        dropdownc7 = ttk.Combobox(ac, textvariable=self.valuec7, values=optionsc7)
        dropdownc7.grid(row=7, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Restrictive

        marketc8 = Label(ac, text='Restrictive Covenant: ', anchor="e").grid(row=8, column=1, sticky=W)

        optionsc8 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec8 = tk.StringVar()
        self.valuec8.set(options5[0])

        dropdownc8 = ttk.Combobox(ac, textvariable=self.valuec8, values=optionsc8)
        dropdownc8.grid(row=8, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Shape

        marketc9 = Label(ac, text='Shape: ', anchor="e").grid(row=9, column=1, sticky=W)

        optionsc9 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec9 = tk.StringVar()
        self.valuec9.set(options5[0])

        dropdownc9 = ttk.Combobox(ac, textvariable=self.valuec9, values=optionsc9)
        dropdownc9.grid(row=9, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Topography

        marketc10 = Label(ac, text='Topography: ', anchor="e").grid(row=10, column=1, sticky=W)

        optionsc10 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec10 = tk.StringVar()
        self.valuec10.set(options5[0])

        dropdownc10 = ttk.Combobox(ac, textvariable=self.valuec10, values=optionsc10)
        dropdownc10.grid(row=10, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Large parcel adjustment

        marketc11 = Label(ac, text='Large Parcel: ', anchor="e").grid(row=11, column=1, sticky=W)

        optionsc11 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec11 = tk.StringVar()
        self.valuec11.set(options5[0])

        dropdownc11 = ttk.Combobox(ac, textvariable=self.valuec11, values=optionsc11)
        dropdownc11.grid(row=11, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Remnant Lot

        marketc12 = Label(ac, text='Remnant Lot: ', anchor="e").grid(row=12, column=1, sticky=W)

        optionsc12 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec12 = tk.StringVar()
        self.valuec12.set(options5[0])

        dropdownc12 = ttk.Combobox(ac, textvariable=self.valuec12, values=optionsc12)
        dropdownc12.grid(row=12, column=2)

        # --------------------------------------------------------------------------------------------------------
        # Contamination

        marketc13 = Label(ac, text='Contamination: ', anchor="e").grid(row=13, column=1, sticky=W)

        optionsc13 = ['', 'Minor', 'Moderate', 'Major', 'Extreme']

        self.valuec13 = tk.StringVar()
        self.valuec13.set(options5[0])

        dropdownc13 = ttk.Combobox(ac, textvariable=self.valuec13, values=optionsc13)
        dropdownc13.grid(row=13, column=2)

        # --------------------------------------------------------------------------------------------------------

        lf = ttk.LabelFrame(myGUI, text="Servicing: ")
        lf.grid(row=0, column=2, columnspan=1, padx=5, ipadx=5, ipady=5)

        # clusters option
        self.cluster_boolean = IntVar()
        self.cluster_boolean.set(0)

        self.cluster_boolean2 = IntVar()
        self.cluster_boolean2.set(0)

        self.cluster_boolean3 = IntVar()
        self.cluster_boolean3.set(0)

        self.cluster_boolean4 = IntVar()
        self.cluster_boolean4.set(0)

        self.cluster_boolean5 = IntVar()
        self.cluster_boolean5.set(0)

        self.cluster_boolean6 = IntVar()
        self.cluster_boolean6.set(0)

        self.cluster_boolean7 = IntVar()
        self.cluster_boolean7.set(0)

        # check boxes

        checkBox1 = ttk.Checkbutton(lf, variable=self.cluster_boolean, onvalue=1, offvalue=0,
                                    text="No street lighting ").grid(row=14, column=2, sticky=W)

        checkBox2 = ttk.Checkbutton(lf, variable=self.cluster_boolean2, onvalue=1, offvalue=0,
                                    text="No sanitary sewer ").grid(row=15, column=2, sticky=W)

        checkBox3 = ttk.Checkbutton(lf, variable=self.cluster_boolean3, onvalue=1, offvalue=0,
                                    text="No storm sewer service ").grid(row=16, column=2, sticky=W)

        checkBox4 = ttk.Checkbutton(lf, variable=self.cluster_boolean4, onvalue=1, offvalue=0,
                                    text="No water service ").grid(row=17, column=2, sticky=W)

        checkBox5 = ttk.Checkbutton(lf, variable=self.cluster_boolean5, onvalue=1, offvalue=0,
                                    text="No paving ").grid(row=18, column=2, sticky=W)

        checkBox6 = ttk.Checkbutton(lf, variable=self.cluster_boolean6, onvalue=1, offvalue=0,
                                    text="No sidewalk, curb gutter ").grid(row=19, column=2, sticky=W)

        checkBox7 = ttk.Checkbutton(lf, variable=self.cluster_boolean7, onvalue=1, offvalue=0,
                                    text="Unserviced ").grid(row=20, column=2, sticky=W)

        # -------------------------------------------------------------------------------------------------------
        # Calculate / close button frame
        buttonframe = ttk.Frame()
        buttonframe.grid(row=21, column=2, sticky=E)

        open_excel = ttk.Button(buttonframe, text="Enter", command=self.calculate)
        open_excel.grid(row=21, column=2, sticky=E)

        # -------------------------------------------------------------------------------------------------------
        # close button
        close = ttk.Button(buttonframe, text="Clear", command=self.clear_text)
        close.grid(row=21, column=3, sticky=E)

        # -------------------------------------------------------------------------------------------------------
        # clear button

    def clear_text(self):
        self.value41.set('')
        self.value4.set('')
        self.value5.set('')
        self.value6.set('')
        self.Source.set('')
        self.Source2.set('')
        self.Source3.set('')

        self.valuec6.set('')
        self.valuec7.set('')
        self.valuec8.set('')
        self.valuec9.set('')
        self.valuec10.set('')
        self.valuec11.set('')
        self.valuec12.set('')
        self.valuec13.set('')

        self.adjust_up.set(0)
        self.cluster_boolean.set(0)
        self.cluster_boolean2.set(0)
        self.cluster_boolean3.set(0)
        self.cluster_boolean4.set(0)
        self.cluster_boolean5.set(0)
        self.cluster_boolean6.set(0)
        self.cluster_boolean7.set(0)
        self.error_frame.grid_forget()
        myGUI.update()

    def calculate(self):
        self.error_frame.grid(row=5, column=2, columnspan=1)

        # Calculations
        assessed = ''

        ind_land_base_rates = {'1': 22.784713, '2': 22.784672, '3': 20.930791,
                               '4': 17.773414, '5': 22.94745, '6': 22.809815,
                               '7': 28.564704, '8': 18.06741, '9': 24.624537,
                               '11': 22.7845744}  # 22.784552}
        ind_median = 32660

        # Traffic
        none_maj = 1.15373
        none_mod = 1.051988587

        # scale
        scale = -0.16

        # CATCH ERRORS!!!!!!!!!!
        mk_area = self.Source2.get().strip()
        size = self.Source.get().strip()

        # -------------------------------------------------------------------------------------------------------
        for size1 in range(10000, 200000, 100):

            if self.value4.get() == 'Industrial Land':
                ind_base = ind_land_base_rates[mk_area]
                assessed = ind_base * (int(size1) / ind_median) ** scale

                # -------------------------------------------------------------------------------------------------------
                # Zoning Conversions

                im_ib = 1.035862
                im_ih = 0.911749
                ih_im = 1.096793
                ih_ib = 1.136133
                ib_im = 0.965379
                ib_ih = 0.880178

                if self.Source3.get() == 'IB':
                    assessed *= im_ib

                if self.Source3.get() == 'IH':
                    assessed *= im_ih

                if self.value5.get() == 'IM to IB':
                    assessed *= im_ib

                if self.value5.get() == 'IM to IH':
                    assessed *= im_ih

                if self.value5.get() == 'IH to IM':
                    assessed *= ih_im

                if self.value5.get() == 'IH to IB':
                    assessed *= ih_ib

                if self.value5.get() == 'IB to IM':
                    assessed *= ib_im

                if self.value5.get() == 'IB to IH':
                    assessed *= ib_ih

                # -------------------------------------------------------------------------------------------------------
                # Traffic Adjustments

                if self.value6.get() == 'None to Major':
                    if self.adjust_up.get() == 1:  # undo checked services
                        assessed *= 1/none_maj
                    else:
                        assessed *= none_maj

                if self.value6.get() == 'None to Moderate':
                    if self.adjust_up.get() == 1:  # undo checked services
                        assessed *= 1/none_mod
                    else:
                        assessed *= none_mod

                if self.value6.get() == 'Moderate to Major':
                    if self.adjust_up.get() == 1:  # undo checked services
                        assessed *= 1/none_maj
                        assessed *= none_mod



                    assessed *= 1/none_mod  # undoes the moderate adjustment
                    assessed *= none_maj  # applies a major adjustment



                # -------------------------------------------------------------------------------------------------------
                # needs to be fixed!!!

                serv_adj = 0
                # Service Adjustments

                if self.cluster_boolean.get() == 1:
                    serv_adj += 0.006

                if self.cluster_boolean2.get() == 1:
                    serv_adj += 0.063

                if self.cluster_boolean3.get() == 1:
                    serv_adj += 0.114

                if self.cluster_boolean4.get() == 1:
                    serv_adj += 0.063

                if self.cluster_boolean5.get() == 1:
                    serv_adj += 0.036

                if self.cluster_boolean6.get() == 1:
                    serv_adj += 0.018

                if self.cluster_boolean7.get() == 1:
                    serv_adj += 0.30

                if self.adjust_up.get() == 1: # undo checked services
                    assessed = assessed * 1/(1 - serv_adj)

                assessed = assessed * (1 - serv_adj)

                # -------------------------------------------------------------------------------------------------------
                # other adjustments

                ot_adj = 0

                if self.valuec6.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec6.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec6.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec6.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec7.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec7.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec7.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec7.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec8.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec8.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec8.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec8.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec9.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec9.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec9.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec9.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec10.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec10.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec10.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec10.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec11.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec11.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec11.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec11.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec12.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec12.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec12.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec12.get() == 'Extreme':
                    ot_adj += 0.20

                if self.valuec13.get() == 'Minor':
                    ot_adj += 0.05

                if self.valuec13.get() == 'Moderate':
                    ot_adj += 0.10

                if self.valuec13.get() == 'Major':
                    ot_adj += 0.15

                if self.valuec13.get() == 'Extreme':
                    ot_adj += 0.20

                assessed = assessed * (1 - ot_adj)

                if self.adjust_up.get() == 1:
                    assessed = assessed * 1/(1 - ot_adj)

                print(size1, assessed)

        multi_base = {'1A': {'RA9': 54.37653, 'RA8': 53.32904, 'RF5': 38.77093},
                      '1C': {'RA9': 119.6161, 'RF6': 71.82274},
                      '2': {'RA9': 88.05928, 'RA8': 72.72245, 'RA7': 58.01689, 'RF5': 48.92829, 'RMU': 165.1105},
                      '3': {'RA9': 109.4269, 'RA8': 90.37575, 'RA7': 90.11572, 'RF6': 82.12242},
                      '4': {'RA9': 87.70609, 'RA7': 57.77998, 'RF5': 48.73059},
                      '5': {'RA7': 57.78005},
                      '5A': {'RA7': 57.77785},
                      '6': {'RA7': 39.56537, 'RF5': 37.07546},
                      '7': {'RA9': 54.37817, 'RA7': 40.30477, 'RF5': 37.76762},
                      '7A': {'RA7': 73.22379},
                      '8': {'RA7': 88.71046},
                      '9': {'RA7': 41.14898, 'RF6': 39.47578, 'RF5': 36.53319},
                      '10': {'RA9': 60.38192, 'RA8': 49.86341, 'RMU': 50.17463},
                      '10A': {'RA9': 50.12218, 'RA8': 41.3915, 'RA7': 33.0247, 'RF5': 27.85112},
                      '11A': {'RA8': 59.52095, 'RA7': 47.48431, 'RF5': 44.49386},
                      '11B': {'RF6': 36.28249, 'RF5': 33.57436},
                      '11C': {'RA7': 39.80955},
                      '12': {'RA7': 44.45555, 'RF6': 40.51671, 'RF5': 37.49355}}

        multi_med = 3172.5
        multi_scale = -0.176
        zone = self.Source3.get().strip()

        if self.value4.get() == 'Multi-Res Land':
            multi_base_2 = multi_base[mk_area][zone]
            assessed = multi_base_2 * (int(size) / multi_med) ** multi_scale

            serv_adj = 0
            # Service Adjustments

            if self.cluster_boolean.get() == 1:
                serv_adj += 0.006

            if self.cluster_boolean2.get() == 1:
                serv_adj += 0.063

            if self.cluster_boolean3.get() == 1:
                serv_adj += 0.114

            if self.cluster_boolean4.get() == 1:
                serv_adj += 0.063

            if self.cluster_boolean5.get() == 1:
                serv_adj += 0.036

            if self.cluster_boolean6.get() == 1:
                serv_adj += 0.018

            if self.cluster_boolean7.get() == 1:
                serv_adj += 0.30

            if self.adjust_up.get() == 1: # undo checked services
                assessed = assessed * 1/(1 - serv_adj)

            assessed = assessed * (1 - serv_adj)

            # -------------------------------------------------------------------------------------------------------
            # other adjustments

            ot_adj = 0

            if self.valuec6.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec6.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec6.get() == 'Major':
                ot_adj += 0.15

            if self.valuec6.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec7.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec7.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec7.get() == 'Major':
                ot_adj += 0.15

            if self.valuec7.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec8.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec8.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec8.get() == 'Major':
                ot_adj += 0.15

            if self.valuec8.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec9.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec9.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec9.get() == 'Major':
                ot_adj += 0.15

            if self.valuec9.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec10.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec10.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec10.get() == 'Major':
                ot_adj += 0.15

            if self.valuec10.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec11.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec11.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec11.get() == 'Major':
                ot_adj += 0.15

            if self.valuec11.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec12.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec12.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec12.get() == 'Major':
                ot_adj += 0.15

            if self.valuec12.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec13.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec13.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec13.get() == 'Major':
                ot_adj += 0.15

            if self.valuec13.get() == 'Extreme':
                ot_adj += 0.20

            if self.adjust_up.get() == 1: # undo checked services
                assessed = assessed * 1/(1 - ot_adj)

            assessed = assessed * (1 - ot_adj)

        comm_med = 6199
        comm_scale = -0.155
        zone = self.Source3.get().strip()

        comm_factors = {'COMAREA000': 167.6894957,
                        'COMAREA001': 186.3614192,
                        'COMAREA003': 76.5161501,
                        'COMAREA011': 167.7261559,
                        'COMAREA025': 59.63382243,
                        'COMAREA028': 95.64924606,
                        'COMAREA030': 69.88941063,
                        'COMAREA031': 59.60317477,
                        'COMAREA032': 58.91705817,
                        'COMAREA040': 59.63505598,
                        'COMAREA050': 76.52031772,
                        'COMAREA055': 76.56278135,
                        'COMAREA070': 45.32061761,
                        'COMAREA080': 45.31863785,
                        'COMAREA100': 27.19084353,
                        'COMAREA101': 38.51922713,
                        'COMAREA102': 43.05293872,
                        'COMAREA110': 45.31807013,
                        'COMAREA112': 38.50075286,
                        'COMAREA130': 33.98811566,
                        'COMAREA132': 45.32100406,
                        'COMAREA136': 45.32015792,
                        'COMAREA137': 41.69236167,
                        'COMAREA138': 45.31874899,
                        'COMAREA142': 43.68459711,
                        'COMAREA149': 85.24953065,
                        'COMAREA150': 43.68661732,
                        'COMAREA151': 43.6857162,
                        'COMAREA160': 43.68412111,
                        'COMAREA163': 58.32811394,
                        'COMAREA164': 22.65952215,
                        'COMAREA180': 68.22233018,
                        'COMAREA190': 60.0201066,
                        'COMAREA200': 85.24867861,
                        'COMAREA201': 85.24689412,
                        'COMAREA202': 58.33072535,
                        'COMAREA210': 60.02062242,
                        'COMAREA270': 60.01533271,
                        'COMAREA350': 45.84511214,
                        'COMAREA360': 50.43166214}

        if self.value4.get() == 'Commercial Land':
            stdy_area = self.value41.get()
            comm_base = comm_factors[stdy_area]

            assessed = comm_base * (int(size) / comm_med) ** comm_scale

            serv_adj = 0
            # Service Adjustments

            if self.cluster_boolean.get() == 1:
                serv_adj += 0.006

            if self.cluster_boolean2.get() == 1:
                serv_adj += 0.063

            if self.cluster_boolean3.get() == 1:
                serv_adj += 0.114

            if self.cluster_boolean4.get() == 1:
                serv_adj += 0.063

            if self.cluster_boolean5.get() == 1:
                serv_adj += 0.036

            if self.cluster_boolean6.get() == 1:
                serv_adj += 0.018

            if self.cluster_boolean7.get() == 1:
                serv_adj += 0.30

            if self.adjust_up.get() == 1: # undo checked services
                assessed = assessed * 1/(1 - serv_adj)

            assessed = assessed * (1 - serv_adj)

            # -------------------------------------------------------------------------------------------------------
            # other adjustments

            ot_adj = 0

            if self.valuec6.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec6.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec6.get() == 'Major':
                ot_adj += 0.15

            if self.valuec6.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec7.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec7.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec7.get() == 'Major':
                ot_adj += 0.15

            if self.valuec7.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec8.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec8.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec8.get() == 'Major':
                ot_adj += 0.15

            if self.valuec8.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec9.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec9.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec9.get() == 'Major':
                ot_adj += 0.15

            if self.valuec9.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec10.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec10.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec10.get() == 'Major':
                ot_adj += 0.15

            if self.valuec10.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec11.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec11.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec11.get() == 'Major':
                ot_adj += 0.15

            if self.valuec11.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec12.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec12.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec12.get() == 'Major':
                ot_adj += 0.15

            if self.valuec12.get() == 'Extreme':
                ot_adj += 0.20

            if self.valuec13.get() == 'Minor':
                ot_adj += 0.05

            if self.valuec13.get() == 'Moderate':
                ot_adj += 0.10

            if self.valuec13.get() == 'Major':
                ot_adj += 0.15

            if self.valuec13.get() == 'Extreme':
                ot_adj += 0.20

            if self.adjust_up.get() == 1: # undo checked services
                assessed = assessed * 1/(1 - ot_adj)


            assessed = assessed * (1 - ot_adj)

            # Traffic Adjustments
            none_maj = 1.1114
            if self.value6.get() == 'None to Major':
                assessed *= none_maj

            if self.value6.get() == 'Major to None':
                assessed *= 1/none_maj

        try:
            total = float(size) * float(assessed)
        except ValueError:
            total = ''
        try:
            assessed = '${:,.8f}'.format(assessed)
            total = '${:,.8f}'.format(total)
        except ValueError:
            pass
        txt = Text(self.error_frame, width=20, height=13)
        txt.grid(row=22, column=2, columnspan=1)
        txt.insert('end', 'PSF: ' + str(assessed) + '\n')
        txt.insert('end', 'Asmt:' + str(total) + '\n')
        myGUI.update()


if __name__ == '__main__':
    # initialize the GUI
    myGUI = Tk()
    app = MainClass(myGUI)
    myGUI.title('Land Calculator')
    myGUI['bg'] = "gray99"
    # myGUI.geometry("250x150")
    myGUI.mainloop()

