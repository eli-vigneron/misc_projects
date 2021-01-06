from tkinter import *
from urllib.request import urlopen
import os.path
from tkinter import ttk
import glob
from tkinter import filedialog
import time
import pandas as pd
from pandas import DataFrame as df
from pandas import ExcelWriter
from urllib.request import urlopen
from xlrd import open_workbook


def get_assessment_tab(roll):
    """
    :param roll:
    :return: list containing the raw data from the assessment tab when the roll number is searched
    """

    # url depending on the inputted roll number
    url = "https://maps.edmonton.ca/api/rest/assessment.ashx?request=getasm&arg=" + str(roll) + \
          "&callback=SM._c(%2715%27).success&errCallBack=SM._c(%2715%27).fail&NaCl=1811283294847965"

    # open the url and split it into a comma separated list
    opened_url = urlopen(url)
    read_url = opened_url.read()
    assessment_tab = read_url.decode("utf-8")
    assessment_tab_list = assessment_tab.split(',')
    return assessment_tab_list


def parse_assess_tab(some_list):
    """
    :param some_list: takes in assessment tab in the form of a list
    :return: dictionary with all the data in it
    """

    # dictionary with labels and values
    output_dic = {}

    for i in some_list:

        if "ASSESSEDVALUE" in i:
            assessedvalue = i.split(':')[1].replace('"', '')
            try:
                assessedvalue = '${:,.0f}'.format(float(assessedvalue))
            except ValueError:
                pass

            output_dic.update({'Assessment': assessedvalue})
            continue

        if "MASTERTAXROLLNUMBER" in i:
            taxroll = i.split(':')[1].replace('"', '')
            output_dic.update({'Roll': taxroll})
            continue

        if "PROPERTYTYPE" in i:
            property_type = i.split(':')[1].title().replace('"', '')
            output_dic.update({'Property Type': property_type})
            continue

        if "EFFECTIVEBUILDYEAR" in i:
            effective_build_year = i.split(':')[1].replace('"', '')
            output_dic.update({'Effective Year': effective_build_year})
            continue

        if "NEIGHBOURHOOD" in i:
            neighbourhood = i.split(':')[1].title().replace('"', '')
            output_dic.update({'Neighbourhood': neighbourhood})
            continue

        if "FULLADDRESS" in i:
            fulladdress = i.split(':')[1].replace('"', '')
            output_dic.update({'Address': fulladdress})
            continue

        # new -------------------------------------------------
        if "FULLYTAXABLE" in i:
            taxable = i.split(':')[1].replace('"', '')
            output_dic.update({'Taxable': taxable})
            continue

        if "FULLYCOMPLETE" in i:
            complete = i.split(':')[1].replace('"', '')
            output_dic.update({'Complete': complete})
            continue

        if "LANDUSEDESCRIPTION" in i:
            ludesc = i.split(':')[1].replace('"', '')
            output_dic.update({'Land Use': ludesc})
            continue

        # -----------------------------------------------------

        if "LOTSIZE" in i:
            # continue into three labels
            # m2, f2, ac

            lotsize = i.split(':')[1].replace('"', '')
            lotlist = lotsize.split('/')
            try:
                m2 = lotlist[0].strip().replace(' M2', '')
                ft2 = lotlist[1].strip().replace(' FT2', '')
                ac = lotlist[2].strip().replace(' AC', '')
                m2 = '{:,.0f}'.format(float(m2))
                ft2 = '{:,.0f}'.format(float(ft2))
                ac = '{:,.0f}'.format(float(ac))

            except:
                m2 = 'null'
                ft2 = 'null'
                ac = 'null'

            output_dic.update({'Lot Size (M2)': m2})
            output_dic.update({'Lot Size (Ft2)': ft2})
            output_dic.update({'Lot Size (AC)': ac})
            continue

        if "DISPLAY_TYPE" in i:
            display_type = i.split(':')[1].replace('"', '')
            output_dic.update({'Assessment Class': display_type})
            continue

        if "TOT_GROSS_AREA_DESCRIPTION" in i:
            # two lables
            tot_gross_area = i.split(':')[1].replace('"', '')
            tot_gross_area = tot_gross_area.split('/')

            try:
                g_m2 = tot_gross_area[0].strip().replace(' M2', '')
                g_ft2 = tot_gross_area[1].strip().replace(' FT2', '')
                g_m2 = '{:,.0f}'.format(float(g_m2))
                g_ft2 = '{:,.0f}'.format(float(g_ft2))

            except:
                g_m2 = 'null'
                g_ft2 = 'null'

            output_dic.update({'Gross Area (M2)': g_m2})
            output_dic.update({'Gross Area (Ft2)': g_ft2})
            continue

        if "NETAREA" in i:
            netarea = i.split(':')[1].replace('"', '')
            output_dic.update({'Net Area': netarea})
            continue

        if "HOUSESUIT" in i:
            housesuite = i.split(':')[1].replace('"', '')
            output_dic.update({'Suite': housesuite})
            continue

        if "HOUSENUM" in i:
            housenum = i.split(':')[1].replace('"', '')
            output_dic.update({'House Number': housenum})
            continue

        if "HOUSESUFF" in i:
            housesuff = i.split(':')[1].replace('"', '')
            output_dic.update({'House Suffix': housesuff})
            continue

        if "STREETNAME" in i:
            streetname = i.split(':')[1].replace('"', '')
            output_dic.update({'Street': streetname})
            continue

        if "POSTALCODE" in i:
            postal = i.split(':')[1].replace('"', '')
            output_dic.update({'Postal Code': postal})
            continue

        if "BUILDINGCOUNT" in i:
            bcount = i.split(':')[1].replace('"', '')
            output_dic.update({'Building Count': bcount})
            continue

        if "VALUATION_GROUP" in i:
            valgroup = i.split(':')[1].title().replace('"', '')
            output_dic.update({'Val Group': valgroup})
            continue

        if "RESULTMESSAGE" in i:
            resultmssg = i.split(':')[1].replace('"', '')
            output_dic.update({'Result Message': resultmssg})
            continue

        if "RESULTDESCRIPTION" in i:
            resultdesc = i.split(':')[1].replace('"', '').replace('.}])', '')
            output_dic.update({'Result Description': resultdesc})
            continue

        if '"Lat"' in i:
            lat = i.split(':')[-1]
            output_dic.update({'Latitude': lat})
            continue

        if '"Lon"' in i:
            lon = i.split(':')[-1]
            output_dic.update({'Longitute': lon})

    try:
        # open the address search tab to get zoning, legal, year

        if housesuff != 'null':
            housenum = housenum + housesuff

        url2 = "https://maps.edmonton.ca/api/rest/address.ashx?request=getaddressgeometry&arg=" \
               "%7B%22SubAddress%22%3A%22%22%2C%22HouseNoAndSuffix%22%3A%22" + str(housenum) + \
               "%22%2C%22StreetNameAndQuadrant%22%3A%22" + streetname.replace(' ', '%20') + \
               "%22%2C%22City%22%3A%22Edmonton%22%2C%22PostalCode%22%3A%22%22%2C%22POSSEFormat" \
               "%22%3A%22%22%7D&callback=SM._c(%2733%27).success&errCallBack=SM._c(%2733%27)." \
               "fail&NaCl=02198251241913396"

        if housesuite != 'null':
            url2 = "https://maps.edmonton.ca/api/rest/address.ashx?request=getaddressgeometry&arg=" \
                   "%7B%22SubAddress%22%3A%22" + housesuite + "%22%2C%22HouseNoAndSuffix%22%3A%22" + \
                   str(housenum) + "%22%2C%22StreetNameAndQuadrant%22%3A%22" + streetname.replace(' ', '%20') \
                   + "%22%2C%22City%22%3A%22Edmonton%22%2C%22PostalCode%22%3A%22%22%2C%22POSSEFormat" \
                     "%22%3A%22%22%7D&callback=SM._c(%2733%27).success&errCallBack=SM._c(%2733%27)." \
                     "fail&NaCl=02198251241913396"

        # open the address tab url
        address_tab = urlopen(url2)

        # read it and put it into a list
        address_tab = address_tab.read()
        address_tab = address_tab.decode("utf-8")
        address_tab_list = address_tab.split(',')

        # catch multiple zones returned and return only the unique ones
        zone_list = []
        zone_indicies = list_duplicates_of(address_tab_list, '{"FeatureClassName":"OFFICIAL ZONING"')
        for i in zone_indicies:
            zone_list.append(address_tab_list[i + 1].split(':')[1].replace('"', ''))

        # turn the list into a string to be displayed
        zone_list = str(list(set(zone_list))).replace('[', '').replace(']', '').replace("'", "")

        output_dic.update({'Zone': zone_list})

        # ----------------------------------------------------------------------------------------------
        legal_found = False
        year_found = False

        # search for the legal and the year
        for i, element in enumerate(address_tab_list):

            if "LEGAL DESCRIPTIONS" in element and legal_found is False:
                legaldescription = address_tab_list[i + 2].split(':')[1].replace('"', '')\
                                   + ', ' + address_tab_list[i + 3].replace('"', '')\
                                   + ', ' + address_tab_list[i + 4].replace('"', '')

                legaldescription = legaldescription.split(',')[2].strip() + ",  "\
                                   + legaldescription.split(',')[1].strip() + ",  "\
                                   + legaldescription.split(',')[0].strip()

                legaldescription = legaldescription.replace("Plan", "Plan:")
                legaldescription = legaldescription.replace("Block", "Block:")
                legaldescription = legaldescription.replace("Lot", "Lot:")
                legaldescription = legaldescription.replace("Unit", "Unit:")

                output_dic.update({'Legal': legaldescription})
                legal_found = True

            if "YearBuilt" in element and year_found is False:
                yrbuilt = element.split(':')[1].replace('"', '')
                yrbuilt = yrbuilt.strip("}")
                yrbuilt = yrbuilt.replace('}]', '')
                output_dic.update({'Year Built': yrbuilt})
                year_found = True

        if legal_found is False:
            legaldescription = 'null'
            output_dic.update({'Legal': legaldescription})

        if year_found is False:
            yrbuilt = "null"
            output_dic.update({'Year Built': yrbuilt})

    except:     # unbound local error

        legaldescription = "null"
        output_dic.update({'Legal': legaldescription})
        yrbuilt = "null"
        output_dic.update({'Year Built': yrbuilt})
        zone_list = 'null'
        output_dic.update({'Zone': zone_list})

    return output_dic


def list_duplicates_of(seq, item):
    # finds the duplicates in a roll

    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


class MainClass():

    def __init__(self, master):
        self.parent = master
        self.gui()

    def gui(self):
        """
        Tkinter main gui definitions of labels and geometry
        :return:
        """

        myGUI['bg'] = "gray99"  # colour of frame

        # initialize progress bar
        self.progress_frame = ttk.Frame()
        self.progress_frame.grid(row=0, column=4, sticky='W')
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=120, mode="determinate")

        # roll label
        Label(myGUI, text='Roll:', anchor="w", bg="gray99").grid(row=0, column=1)

        self.Source = StringVar()   # dummy to catch input roll

        # input box for roll number (unwanted input is handled in the seach function that is called when the button is
        # pressed)
        ttk.Entry(myGUI, textvariable=self.Source).grid(row=0, column=2)

        # seach button (bound to the search function defined below via command=)
        ttk.Button(myGUI, text="  Search  ", command=self.search).grid(row=0, column=3)

        # call the search function when the enter key is pressed
        myGUI.bind('<Return>', self.search)

        # label for opening an excel file containing a list of roll numbers
        Label(myGUI, text='  \tRoll List:', anchor="e", bg="gray99").grid(row=1, column=2)

        roll_list_button = ttk.Button(myGUI, text="  Open  ", command=self.import_export)
        roll_list_button.grid(row=1, column=3)

        # ----------------------------------------------------------------------------------------------------
        # labels on the left (there is a frame for every other label so that it can be coloured a darker gray)
        # probably a better way to do this
        Label(myGUI, text="Roll Number: ", bg="gray99").grid(sticky="W", row=2, columnspan=3)

        nbhd_frame = Frame(myGUI, bg="gray95")
        nbhd_frame.grid(row=3, column=0, columnspan=8, sticky="ew")
        Label(nbhd_frame, text="Neighbourhood: ", bg="gray95").grid(sticky="W", row=3, columnspan=3)

        Label(myGUI, text="Assessment Class: ", bg="gray99").grid(sticky="W", row=4, columnspan=3)

        assess_frame = Frame(myGUI, bg="gray95")
        assess_frame.grid(row=5, column=0, columnspan=8, sticky="ew")
        Label(assess_frame, text="Assessed Value: ", relief=FLAT, bg="gray95").grid(sticky="W", row=5, columnspan=3)

        Label(myGUI, text="Lot Size (M2): ", bg="gray99").grid(sticky="W", row=6, columnspan=3)

        lot_frame2 = Frame(myGUI, bg="gray95")
        lot_frame2.grid(row=7, column=0, columnspan=8, sticky="ew")
        Label(lot_frame2, text="Lot Size (FT2): ", bg="gray95").grid(sticky="W", row=7, columnspan=3)

        Label(myGUI, text="Lot Size (AC): ", bg="gray99").grid(sticky="W", row=8, columnspan=3)

        addr_frame = Frame(myGUI, bg="gray95")
        addr_frame.grid(row=9, column=0, columnspan=8, sticky="ew")
        Label(addr_frame, text="Full Address: ", bg="gray95").grid(sticky="W", row=9, columnspan=3)

        Label(myGUI, text="Legal Description: ", bg="gray99").grid(sticky="W", row=10, columnspan=3)

        prop_frame = Frame(myGUI, bg="gray95")
        prop_frame.grid(row=11, column=0, columnspan=8, sticky="ew")
        Label(prop_frame, text="Property Type: ", bg="gray95").grid(sticky="W", row=11, columnspan=3)

        Label(myGUI, text="Valuation Group: ", bg="gray99").grid(sticky="W", row=12, columnspan=3)

        zone_frame = Frame(myGUI, bg="gray95")
        zone_frame.grid(row=13, column=0, columnspan=8, sticky="ew")
        Label(zone_frame, text="Zoning: ", bg="gray95").grid(sticky="W", row=13, columnspan=3)

        Label(myGUI, text="Year Built: ", bg="gray99").grid(sticky="W", row=14, columnspan=3)

        eyear_frame = Frame(myGUI, bg="gray95")
        eyear_frame.grid(row=15, column=0, columnspan=8, sticky="ew")
        Label(eyear_frame, text="Effective Build Year: ", bg="gray95").grid(sticky="W", row=15, columnspan=3)

        Label(myGUI, text="Gross Area (M2): ", bg="gray99").grid(sticky="W", row=16, columnspan=3)

        ga_frame = Frame(myGUI, bg="gray95")
        ga_frame.grid(row=17, column=0, columnspan=8, sticky="ew")
        Label(ga_frame, text="Gross Area (FT2): ", bg="gray95").grid(sticky="W", row=17, columnspan=3)

        Label(myGUI, text="Net Area: ", bg="gray99").grid(sticky="W", row=18, columnspan=3)

        hnum_frame = Frame(myGUI, bg="gray95")
        hnum_frame.grid(row=19, column=0, columnspan=8, sticky="ew")
        Label(hnum_frame, text="House Number: ", bg="gray95").grid(sticky="W", row=19, columnspan=3)

        Label(myGUI, text="House Suite: ", bg="gray99").grid(sticky="W", row=20, columnspan=3)

        hsuf_frame = Frame(myGUI, bg="gray95")
        hsuf_frame.grid(row=21, column=0, columnspan=8, sticky="ew")
        Label(hsuf_frame, text="House Suffix: ", bg="gray95").grid(sticky="W", row=21, columnspan=3)

        Label(myGUI, text="Street Name: ", bg="gray99").grid(sticky="W", row=22, columnspan=3)

        pcod_frame = Frame(myGUI, bg="gray95")
        pcod_frame.grid(row=23, column=0, columnspan=8, sticky="ew")
        Label(pcod_frame, text="Postal Code: ", bg="gray95").grid(sticky="W", row=23, columnspan=3)

        Label(myGUI, text="Building Count: ", bg="gray99").grid(sticky="W", row=24, columnspan=3)

        rslt_frame = Frame(myGUI, bg="gray95")
        rslt_frame.grid(row=25, column=0, columnspan=8, sticky="ew")
        Label(rslt_frame, text="Result Message: ", bg="gray95").grid(sticky="W", row=25, columnspan=3)

        Label(myGUI, text="Result Description: ", bg="gray99").grid(sticky="W", row=26, columnspan=3)

        Label(myGUI, text="Count: ", bg="gray99").grid(row=1, column=4)
        # ----------------------------------------------------------------------------------------------------

    def set_all_fields_to_null(self):
        # set all the fields blank
        null_value = StringVar()
        null_value.set('null')

        assessed_value_rslt.configure(textvariable=null_value, relief=FLAT)
        prop_type_rslt.configure(textvariable=null_value, relief=FLAT)
        eff_yr_rslt.configure(textvariable=null_value, relief=FLAT)
        nbhd_rslt.configure(textvariable=null_value, relief=FLAT)
        full_address_rslt.configure(textvariable=null_value, relief=FLAT)
        lotsize_m2_rslt.configure(textvariable=null_value, relief=FLAT)
        lotsize_ft2_rslt.configure(textvariable=null_value, relief=FLAT)
        lotsize_ac_rslt.configure(textvariable=null_value, relief=FLAT)
        class_rslt.configure(textvariable=null_value, relief=FLAT)
        grossarea_m2_rslt.configure(textvariable=null_value, relief=FLAT)
        grossarea_ft2_rslt.configure(textvariable=null_value, relief=FLAT)
        net_area_rslt.configure(textvariable=null_value, relief=FLAT)
        hsuite_rslt.configure(textvariable=null_value, relief=FLAT)
        hnum_rslt.configure(textvariable=null_value, relief=FLAT)
        hsuf_rslt.configure(textvariable=null_value, relief=FLAT)
        stname_rslt.configure(textvariable=null_value, relief=FLAT)
        pstalcode_rslt.configure(textvariable=null_value, relief=FLAT)
        bcount_rslt.configure(textvariable=null_value, relief=FLAT)
        valgroup_rslt.configure(textvariable=null_value, relief=FLAT)
        rslt_desc_rslt.configure(textvariable=null_value, relief=FLAT)
        zone_rslt.configure(textvariable=null_value, relief=FLAT)
        legal_rslt.configure(textvariable=null_value, relief=FLAT)
        yrbuilt_rslt.configure(textvariable=null_value, relief=FLAT)

    def search(self, event=None):
        """
        :param event: None
        Function to handle a single roll searched in the search box
        """

        # capture the stuff entered by the user
        input_roll = str(self.Source.get()).strip()

        try:        # try casting the input as an integer
            int(input_roll)

        except ValueError:
            self.set_all_fields_to_null()
            # error message
            error0 = StringVar()
            error0_message = 'Invalid Roll'
            error0.set(error0_message)
            rslt_msg_rslt.configure(textvariable=error0, width=len(error0_message) + 4, fg='red', relief=FLAT)
            myGUI.update()
            return 0

        value0 = StringVar()
        value0.set(input_roll)
        roll_rslt.configure(textvariable=value0, width=len(input_roll) + 4, relief=FLAT)

        assessment_tab_list = get_assessment_tab(input_roll)

        if len(assessment_tab_list) > 1:       # ensure that something was returned
            myGUI.update()

            # parse the list and configure the labels

            # Initialize dummy value types for tkinter gui output
            value1 = StringVar()
            value2 = StringVar()
            value3 = StringVar()
            value4 = StringVar()
            value5 = StringVar()
            value6 = StringVar()
            value7 = StringVar()
            value8 = StringVar()
            value9 = StringVar()
            value10 = StringVar()
            value11 = StringVar()
            value12 = StringVar()
            value13 = StringVar()
            value14 = StringVar()
            value15 = StringVar()
            value16 = StringVar()
            value17 = StringVar()
            value18 = StringVar()
            value19 = StringVar()
            value20 = StringVar()
            value21 = StringVar()
            value22 = StringVar()
            value23 = StringVar()
            value24 = StringVar()
            value25 = StringVar()
            value26 = StringVar()
            value27 = StringVar()
            value28 = StringVar()

            dictionary_data = parse_assess_tab(assessment_tab_list)     # dictionary with all the labels and values

            taxroll = dictionary_data["Roll"]
            value12.set(taxroll)
            # overwrite the inputted roll if the same thing is returned from the city
            if value0 == value12:
                roll_rslt.configure(textvariable=value12, width=len(taxroll) + 4, relief=FLAT)

            assessedvalue = dictionary_data["Assessment"]
            value1.set(assessedvalue)
            assessed_value_rslt.configure(textvariable=value1, width=len(assessedvalue), relief=FLAT)

            property_type = dictionary_data["Property Type"]
            value2.set(property_type)
            prop_type_rslt.configure(textvariable=value2, width=len(property_type) + 4, relief=FLAT)

            effective_build_year = dictionary_data["Effective Year"]
            value3.set(effective_build_year)
            eff_yr_rslt.configure(textvariable=value3, width=len(effective_build_year) + 4, relief=FLAT)

            neighbourhood = dictionary_data["Neighbourhood"]
            value4.set(neighbourhood)
            nbhd_rslt.configure(textvariable=value4, width=len(neighbourhood) + 4, relief=FLAT)

            fulladdress = dictionary_data["Address"]
            value5.set(fulladdress)
            full_address_rslt.configure(textvariable=value5, width=len(fulladdress) + 8, relief=FLAT)

            m2 = dictionary_data["Lot Size (M2)"]
            value6.set(m2)
            lotsize_m2_rslt.configure(textvariable=value6, width=len(m2) + 4, relief=FLAT)

            ft2 = dictionary_data["Lot Size (Ft2)"]
            value7.set(ft2)
            lotsize_ft2_rslt.configure(textvariable=value7, width=len(ft2) + 4, relief=FLAT)

            ac = dictionary_data["Lot Size (AC)"]
            value8.set(ac)
            lotsize_ac_rslt.configure(textvariable=value8, width=len(ac) + 4, relief=FLAT)

            display_type = dictionary_data["Assessment Class"]
            value9.set(display_type)
            class_rslt.configure(textvariable=value9, width=len(display_type) + 4, relief=FLAT)

            g_m2 = dictionary_data["Gross Area (M2)"]
            value10.set(g_m2)
            grossarea_m2_rslt.configure(textvariable=value10, width=len(g_m2) + 4, relief=FLAT)

            g_ft2 = dictionary_data["Gross Area (Ft2)"]
            value11.set(g_ft2)
            grossarea_ft2_rslt.configure(textvariable=value11, width=len(g_ft2) + 4, relief=FLAT)

            netarea = dictionary_data["Net Area"]
            value13.set(netarea)
            net_area_rslt.configure(textvariable=value13, width=len(netarea) + 4, relief=FLAT)

            housesuite = dictionary_data["Suite"]
            value14.set(housesuite)
            hsuite_rslt.configure(textvariable=value14, width=len(housesuite) + 4, relief=FLAT)

            housenum = dictionary_data["House Number"]
            value15.set(housenum)
            hnum_rslt.configure(textvariable=value15, width=len(housenum) + 4, relief=FLAT)

            housesuff = dictionary_data["House Suffix"]
            value16.set(housesuff)
            hsuf_rslt.configure(textvariable=value16, width=len(housesuff) + 4, relief=FLAT)

            streetname = dictionary_data["Street"]
            value17.set(streetname)
            stname_rslt.configure(textvariable=value17, width=len(streetname) + 4, relief=FLAT)

            postal = dictionary_data["Postal Code"]
            value18.set(postal)
            pstalcode_rslt.configure(textvariable=value18, width=len(postal) + 4, relief=FLAT)

            bcount = dictionary_data["Building Count"]
            value19.set(bcount)
            bcount_rslt.configure(textvariable=value19, width=len(bcount) + 4, relief=FLAT)

            valgroup = dictionary_data["Val Group"]
            value20.set(valgroup)
            valgroup_rslt.configure(textvariable=value20, width=len(valgroup) + 4, relief=FLAT)

            resultmssg = dictionary_data["Result Message"]
            value21.set(resultmssg)
            rslt_msg_rslt.configure(textvariable=value21, width=len(resultmssg) + 4, fg='black', relief=FLAT)

            resultdesc = dictionary_data["Result Description"]
            value22.set(resultdesc)
            rslt_desc_rslt.configure(textvariable=value22, width=len(resultdesc) + 4, relief=FLAT)

            zone_list = dictionary_data["Zone"]
            value23.set(zone_list)
            zone_rslt.configure(textvariable=value23, width=len(zone_list) + 4, relief=FLAT)

            legaldescription = dictionary_data["Legal"]
            value24.set(legaldescription)
            legal_rslt.configure(textvariable=value24, width=len(legaldescription) + 4, relief=FLAT)

            yrbuilt = dictionary_data["Year Built"]
            value25.set(yrbuilt)
            yrbuilt_rslt.configure(textvariable=value25, width=len(yrbuilt) + 4, relief=FLAT)


        elif len(assessment_tab_list) <= 1:     # if nothing is returned on the city website
            # set fields blank
            self.set_all_fields_to_null()

            # Error message
            error1 = StringVar()
            error1_message = 'The roll number that you entered does not exist on the city website'
            error1.set(error1_message)
            rslt_msg_rslt.configure(textvariable=error1, width=len(error1_message) + 4, fg='red', relief=FLAT)

            myGUI.update()

    def import_export(self, event=None):
        """
        :param event: None
        :return: function to handle an inputted excel sheet with rolls
        """

        # opens the windows file dialog window and captures the path to the file selected
        file_path = filedialog.askopenfilename()

        # create a list containing the rolls in the opened spreadsheet
        xls = open_workbook(file_path)
        sheet1 = xls.sheet_by_index(0)
        rolls = list(sheet1.get_rows())

        # --------------------------------------------------------------------------------------------
        # remove any elements in the list that are not roll numbers
        indicies_to_delete = []
        for row in rolls:
            for i, element in enumerate(row):
                if ',' not in str(element.value):
                    try:

                        row[i] = str(int(element.value))

                    except:
                        indicies_to_delete.append(rolls.index(row))
                if ',' in str(element.value) and str(re.search('[a-zA-Z]', str(element.value))) != 'None':
                    try:

                        row[i] = str(int(element.value))

                    except:
                        indicies_to_delete.append(rolls.index(row))

        delet_rolls = []
        for i in indicies_to_delete:
            delet_rolls.append(rolls[i])

        rolls = [item for item in rolls if item not in delet_rolls]

        # --------------------------------------------------------------------------------------------

        count = 1   # keep track of what roll number is being processed
        total = len(rolls)  # total number of roll numbers to be computed

        value5 = StringVar()
        value6 = StringVar()

        bunch_of_dics = []      # will contain all the dictionaries with data for each roll

        try:
            for roll in rolls:
                # start a timer
                start_time = time.time()

                # ---------------------------------------------------------------------------
                # progress_bar that updates on each iteration (visible on the tkinter gui)

                self.progress["value"] = 0      # set the progress bar value
                self.progress["maximum"] = str(total)
                self.progress.grid(row=0, column=4, sticky='W')     # place the progress bar
                self.progress["value"] = str(count)
                myGUI.update()      # refresh

                value5.set("              " + str(count) + "/" + str(total))

                count_rslt.configure(textvariable=value5, relief=FLAT)
                myGUI.update()
                # ---------------------------------------------------------------------------
                # code to handle multi-parcel sales of the form roll_1, roll_2,...

                if ',' in str(roll[0]):

                    multirolls = roll[0].value.split(',')
                    multirolls = [[i.strip()] for i in multirolls]

                    #multi_dics = []

                    for roll1 in multirolls:

                        try:
                            a_list = get_assessment_tab(roll1[0])
                        except:
                            # try again
                            time.sleep(0.5)
                            a_list = get_assessment_tab(roll1[0])

                        #multi_dics.append(parse_assess_tab(a_list))

                        bunch_of_dics.append(parse_assess_tab(a_list))

                elif ',' not in str(roll[0]):

                    try:
                        a_list = get_assessment_tab(roll[0])
                    except:
                        time.sleep(0.5)
                        a_list = get_assessment_tab(roll[0])

                    # roll.extend(list(parse_assess_tab(a_list).values()))
                    bunch_of_dics.append(parse_assess_tab(a_list))
                    count += 1

                # make sure we have the at least 5ms pause between requests
                elapsed = time.time() - start_time
                if elapsed <= 0.5:
                    time.sleep(abs(0.5 - elapsed))

        except:     # catch the case where it hangs or someone exits the app while it is still running

            output_dataframe = pd.DataFrame(bunch_of_dics)    # dataframe containing all the data to be written to excel

            # ----------------------------------------------------------------------------------------
            # check if an output file already exists, if so make a new one with an incremented number
            os.chdir(file_path.replace(file_path.split("/")[-1], ''))

            # increment(ing) number for the end of the file name
            number = len(glob.glob(file_path.split("/")[-1].replace(".xlsx", '') + " OUTPUT*.xlsx")) + 1

            file_name = file_path.split("/")[-1].replace(".xlsx", '') + " OUTPUT" + ".xlsx"

            if os.path.isfile(file_name):
                writer = ExcelWriter(file_name.replace(".xlsx", " (" + str(number) + ")") + ".xlsx")
                output_dataframe.to_excel(writer, index=False)
                writer.save()
            else:
                writer = ExcelWriter(file_name)
                output_dataframe.to_excel(writer, index=False)
                writer.save()
            # ----------------------------------------------------------------------------------------

        # configure the complete message
        value6.set("         Complete")
        count_rslt.configure(textvariable=value6, relief=FLAT)
        self.progress_frame.grid_forget()

        output_dataframe = pd.DataFrame(bunch_of_dics)

        # ----------------------------------------------------------------------------------------
        # redundant should probably write a function

        # check if an output file already exists, if so make a new one with an incremented number
        os.chdir(file_path.replace(file_path.split("/")[-1], ''))

        # increment(ing) number for the end of the file name
        number = len(glob.glob(file_path.split("/")[-1].replace(".xlsx", '') + " OUTPUT*.xlsx")) + 1

        file_name = file_path.split("/")[-1].replace(".xlsx", '') + " OUTPUT" + ".xlsx"

        if os.path.isfile(file_name):
            writer = ExcelWriter(file_name.replace(".xlsx", " (" + str(number) + ")") + ".xlsx")
            output_dataframe.to_excel(writer, index=False)
            writer.save()
        else:
            writer = ExcelWriter(file_name)
            output_dataframe.to_excel(writer, index=False)
            writer.save()
        # ----------------------------------------------------------------------------------------


if __name__ == '__main__':

    counts = 0

    myGUI = Tk()
    app = MainClass(myGUI)
    myGUI.title('Roll Searcher 5.0')

    # ------------------------------------------------------------------------------------
    # labels on the right that are to be updated

    # initialize the textvariable
    value = 0

    roll_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    roll_rslt.grid(sticky="W", row=2, column=4)

    nbhd_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    nbhd_rslt.grid(sticky="W", row=3, column=4)

    class_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    class_rslt.grid(sticky="W", row=4, column=4)

    assessed_value_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    assessed_value_rslt.grid(sticky="W", row=5, column=4)

    lotsize_m2_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    lotsize_m2_rslt.grid(sticky="W", row=6, column=4)

    lotsize_ft2_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    lotsize_ft2_rslt.grid(sticky="W", row=7, column=4)

    lotsize_ac_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    lotsize_ac_rslt.grid(sticky="W", row=8, column=4)

    full_address_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    full_address_rslt.grid(sticky="W", row=9, column=4)

    legal_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    legal_rslt.grid(sticky="W", row=10, column=4)

    prop_type_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    prop_type_rslt.grid(sticky="W", row=11, column=4)

    valgroup_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    valgroup_rslt.grid(sticky="W", row=12, column=4)

    zone_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    zone_rslt.grid(sticky="W", row=13, column=4)

    yrbuilt_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    yrbuilt_rslt.grid(sticky="W", row=14, column=4)

    eff_yr_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    eff_yr_rslt.grid(sticky="W", row=15, column=4)

    grossarea_m2_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    grossarea_m2_rslt.grid(sticky="W", row=16, column=4)

    grossarea_ft2_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    grossarea_ft2_rslt.grid(sticky="W", row=17, column=4)

    net_area_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    net_area_rslt.grid(sticky="W", row=18, column=4)

    hnum_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    hnum_rslt.grid(sticky="W", row=19, column=4)

    hsuite_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    hsuite_rslt.grid(sticky="W", row=20, column=4)

    hsuf_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    hsuf_rslt.grid(sticky="W", row=21, column=4)

    stname_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    stname_rslt.grid(sticky="W", row=22, column=4)

    pstalcode_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    pstalcode_rslt.grid(sticky="W", row=23, column=4)

    bcount_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    bcount_rslt.grid(sticky="W", row=24, column=4)

    rslt_msg_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray95")
    rslt_msg_rslt.grid(sticky="W", row=25, column=4)

    rslt_desc_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99")
    rslt_desc_rslt.grid(sticky="W", row=26, column=4)

    count_rslt = Entry(myGUI, textvariable=value, state="readonly", readonlybackground="gray99", relief=FLAT)
    count_rslt.grid(row=1, column=4, columnspan=1)

    # ------------------------------------------------------------------------------------

    myGUI.mainloop()
