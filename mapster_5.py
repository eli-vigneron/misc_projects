from __future__ import (absolute_import, division, print_function)
from tkinter import *
from tempfile import TemporaryFile
import os.path
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import folium
from folium import plugins
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt
from folium.map import *
from branca.element import CssLink, Figure, JavascriptLink, MacroElement
from jinja2 import Template
from folium.plugins import Draw
from folium.plugins import MarkerCluster
import glob
import branca
import html
from branca.element import Template, MacroElement
import json
import io


def sequence(*functions):
    """
    Combines two functions (useful for running two functions with one button press)
    :param functions:
    :return:
    """

    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value

    return func


class Search(MacroElement):
    """
    Adds a search tool to the map
    Parameters
    ----------
    position : str
          change the position of the search bar, can be:
          'topleft', 'topright', 'bottomright' or 'bottomleft'
          default: 'topleft'
    See https://github.com/stefanocudini/leaflet-search for more information.
    """

    def __init__(self, data, search_zoom=12, search_label='name', geom_type='Point',
                 position='topleft', popup_on_found=True):
        super(Search, self).__init__()
        self.position = position
        self.data = data
        self.search_label = search_label
        self.search_zoom = search_zoom
        self.geom_type = geom_type
        self.popup_on_found = popup_on_found
        self._template = Template("""
        {% macro script(this, kwargs) %}
             var {{this.get_name()}} = new L.geoJson.css({{this.data}});
             {{this._parent.get_name()}}.addLayer({{this.get_name()}});
             if ('{{this.geom_type}}' == 'Point'){
                var searchControl = new L.Control.Search({
                    layer: {{this.get_name()}},
                    propertyName: '{{this.search_label}}',
                    initial: false,
                    zoom: {{this.search_zoom}},
                    position:'{{this.position}}',
                    hideMarkerOnCollapse: true
                });
                if ({{'true' if this.popup_on_found else 'false'}}) {
                    searchControl.on('search:locationfound', function(e) {
                         if(e.layer._popup)
                            e.layer.openPopup();
                     });
                };
             } else if ('{{this.geom_type}}' == 'Polygon') {
                var searchControl = new L.Control.Search({
                    layer: {{this.get_name()}},
                    propertyName: '{{this.search_label}}',
                    marker: false,
                    position:'{{this.position}}',
                    moveToLocation: function(latlng, title, map) {
                        var zoom = {{this._parent.get_name()}}.getBoundsZoom(latlng.layer.getBounds());
                        {{this._parent.get_name()}}.setView(latlng, zoom); // access the zoom
                    }
                });
                 searchControl.on('search:locationfound', function(e) {
                     e.layer.setStyle({fillColor: '#3f0', color: '#0f0'});
                    if(e.layer._popup)
                        e.layer.openPopup();
                 }).on('search:collapsed', function(e) {
                     {{this.get_name()}}.eachLayer(function(layer) {   //restore feature color
                        {{this.get_name()}}.resetStyle(layer);
                    }); 
                });
            }

            {{this._parent.get_name()}}.addControl( searchControl ); 
         {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        super(Search, self).render()
        figure = self.get_root()

        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.3.6/dist/leaflet-search.min.js'),  # noqa
            name='Leaflet.Search.js'
        )
        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.3.6/dist/leaflet-search.min.css'),  # noqa
            name='Leaflet.Search.css'
        )
        figure.header.add_child(
            JavascriptLink('https://cdn.rawgit.com/albburtsev/Leaflet.geojsonCSS/master/leaflet.geojsoncss.min.js'),
            # noqa
            name='Leaflet.GeoJsonCss.js'
        )


class MainClass:

    def __init__(self, master):
        self.parent = master
        self.gui()

    def gui(self):
        # adds in a grip box
        gripframe = ttk.Frame()
        gripframe.grid(row=100, column=100)
        ttk.Sizegrip(gripframe).grid(row=100, column=100)

        # initialize progress bar
        self.progress_frame = ttk.Frame()
        self.progress_frame.grid(row=5, column=2)
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=150, mode="determinate")

        # -------------------------------------------------------------------------------------------------------
        buttonframe = ttk.Frame()
        buttonframe.grid(row=4, column=2, sticky=W)

        # open button
        open_excel = ttk.Button(buttonframe, text="Open", command=self.excel_rolls)
        open_excel.grid(row=4, column=2, sticky=E)

        # -------------------------------------------------------------------------------------------------------
        # close button
        close = ttk.Button(buttonframe, text="Close", command=myGUI.destroy)
        close.grid(row=4, column=3, sticky=E)

        # -------------------------------------------------------------------------------------------------------
        # market drop-down menu
        market = Label(myGUI, text='Market:  ', anchor="w", bg="gray99").grid(row=2, column=1, sticky=W)

        options3 = ['                                         ',
                    'Commercial Land', 'Industrial Land', 'Industrial Warehouse',
                    'Multi-Res Land', 'Commercial Study Area',
                    'COMAREA003',
                    'COMAREA002',
                    'COMAREA070',
                    'COMAREA143',
                    'COMAREA210',
                    'COMAREA026',
                    'COMAREA050',
                    'COMAREA110',
                    'COMAREA157',
                    'COMAREA120',
                    'COMAREA024',
                    'COMAREA102']

        self.value4 = tk.StringVar()
        self.value4.set(options3[0])

        masterframe4 = ttk.Frame()
        masterframe4.grid(row=2, column=2, sticky=W)

        dropdown4 = ttk.Combobox(masterframe4, textvariable=self.value4, values=options3)
        dropdown4.grid(row=2, column=2)

        # -------------------------------------------------------------------------------------------------------
        # clusters option
        self.cluster_boolean = IntVar()
        self.cluster_boolean.set(0)

        # check box
        checkBox1 = ttk.Checkbutton(myGUI, variable=self.cluster_boolean, onvalue=1, offvalue=0, text="Clusters ") \
            .grid(row=3, column=2, sticky=E)

    def excel_rolls(self, event=None):
        """ function that is called when the open button is pressed that takes in a list of rolls and
            finds them in the sales sheet / assessment sheet
        """

        try:
            # open the system dialog box
            file_path = filedialog.askopenfilename()
        except:     # if the user closes the dialog box
            return 0

        # ---------------------------------------------------------------------------------------
        # read in the sales sheet and the assessment sheet, the sheets need to contain the longitude/latitude

        # covid data
        sales = pd.read_excel(".../conposcovidloc.csv")

        # ----------------------------------------------------------------------------
        # create the map, based on center coordinate

        m = folium.Map([53.540623875, -113.5144126344], zoom_start=11)

        # add in the market areas based on the user input, note that the geojson files will need to be updated as
        # as the market areas change

        if self.value4.get() == 'Multi-Res Land':
            m.choropleth(
                geo_data=".../multires_land_1A.geojson",
                fill_color='purple',
                fill_opacity=0.5, line_opacity=6, name='1A')

            m.choropleth(
                geo_data=".../multires_land_1B.geojson",
                fill_color='#1c965f',
                fill_opacity=0.7, line_opacity=6, name='1B')

            m.choropleth(
                geo_data=".../multires_land_1C.geojson",
                fill_color='#3e6b00',
                fill_opacity=0.6, line_opacity=6, name='1C')

            m.choropleth(
                geo_data=".../multires_land_5A.geojson",
                fill_color='#529954',
                fill_opacity=0.5, line_opacity=6, name='5A')

            m.choropleth(
                geo_data=".../multires_land_6.geojson",
                fill_color='#e5b300',  # blue
                fill_opacity=0.5, line_opacity=6, name='6')

            m.choropleth(
                geo_data=".../multires_land_7.geojson",
                fill_color='#9e0636',
                fill_opacity=0.5, line_opacity=6, name='7')

            m.choropleth(
                geo_data=".../multires_land_7A.geojson",
                fill_color='#4a0068',
                fill_opacity=0.5, line_opacity=6, name='7A')

            m.choropleth(
                geo_data=".../multires_land_8.geojson",
                fill_color='cyan',
                fill_opacity=0.5, line_opacity=6, name='8')

            m.choropleth(
                geo_data=".../multires_land_8A.geojson",
                fill_color='#13c170',
                fill_opacity=0.5, line_opacity=6, name='8A')

            m.choropleth(
                geo_data=".../multires_land_9.geojson",
                fill_color='orange',  # blue
                fill_opacity=0.5, line_opacity=6, name='9')

            m.choropleth(
                geo_data=".../multires_land_10.geojson",
                fill_color='#c18f13',
                fill_opacity=0.5, line_opacity=6, name='10')

            m.choropleth(
                geo_data=".../multires_land_12A.geojson",
                fill_color='#ff35f8',
                fill_opacity=0.5, line_opacity=6, name='12A')

        if self.value4.get() == 'Commercial Land':
            m.choropleth(
                geo_data=".../commercial_land0.geojson",
                fill_color='orange',
                fill_opacity=0.5, line_opacity=6, name='Group 1')

            m.choropleth(
                geo_data=".../commercial_land1.geojson",
                fill_color='#00fcfc',  # cyan
                fill_opacity=0.7, line_opacity=6, name='Group 2')

            m.choropleth(
                geo_data=".../commercial_land2.geojson",
                fill_color='#fc0000',  # dark red
                fill_opacity=0.6, line_opacity=6, name='Group 3')

            m.choropleth(
                geo_data=".../commercial_land3.geojson",
                fill_color='#634412',  # shit colour
                fill_opacity=0.6, line_opacity=6, name='Group 4')

            m.choropleth(
                geo_data=".../commercial_land4.geojson",
                fill_color='#034da8',  # blue
                fill_opacity=0.5, line_opacity=6, name='Group 5')

            m.choropleth(
                geo_data=".../commercial_land5.geojson",
                fill_color='#fc009b',
                fill_opacity=0.5, line_opacity=6, name='Group 6')


        if self.value4.get() == 'Industrial Land':
            m.choropleth(
                geo_data=".../industrial_land0.geojson",
                fill_color='orange',
                fill_opacity=0.5, line_opacity=6, name='1')

            m.choropleth(
                geo_data=".../industrial_land1.geojson",
                fill_color='#00fcfc',  # cyan
                fill_opacity=0.7, line_opacity=6, name='2')

      

        # ----------------------------------------------------------------------------
        # Turn on or off depending on whether clusters are desired or not
        if self.cluster_boolean.get() == 0:
            assessment_group = FeatureGroup(name='Assessments')
        else:
            assessment_group = MarkerCluster(name='Assessments')

        # ----------------------------------------------------------------------------
        # mark each assessment as a point with popup box etc.

        points = []     # will contain searchable information for each roll
        count = 0
        total = len(list(filtered_assess.iterrows()))
        value5 = StringVar()
        value5.set(0)

        for index, row in filtered_assess.iterrows():

            # progress_bar that updates on each iteration (visible on the tkinter gui)
            # set the progress bar value
            self.progress["value"] = 0
            self.progress["maximum"] = str(total)
            self.progress.grid(row=5, column=2)
            self.progress["value"] = str(count)
            myGUI.update()

            # format the popup text (HTML formatting works) {formatted as columns}
            # the names here will have to be the same as the headers in the assessment excel sheet otherwise an error
            # will be thrown
            test_df0 = pd.DataFrame(row[['Roll', 'Assessed Value', 'Lot Size (F2)', 'Property Type', 'Zone',
                                         'Market Area', 'Full Address', 'Main floor (Ft2)', 'Main floor finished (Ft2)',
                                         'Upper Finished (Ft2)', 'Total Building Area', 'Effective Year',
                                         'Condition', 'Rear Building', 'Traffic Influence', 'Shape',
                                         'Topography', 'Access Adjustment', 'Functional Obsolescence',
                                         'Landfill Influence', 'Easement', 'Contamination', 'Site Coverage',
                                         'Cost Building', 'Service Road', 'Building Total']])

            # html formatting for the tables that are displayed in the popup
            str_io0 = io.StringIO() # contains the roll
            test_df0.to_html(buf=str_io0, classes='table table-striped', header=False)
            html_str0 = '<div style="overflow-y: scroll; height: 100px;">\n' + str_io0.getvalue() + '\n</div>'
            popuptext = html_str0

            # scale the radius of the marker
            '''
            radius = 0
            if int(row['Lot Size (F2)'].replace(',', '')) / 10000 >= 4:
                radius = int(row['Lot Size (F2)'].replace(',', '')) / 10000
            elif int(row['Lot Size (F2)'].replace(',', '')) / 10000 <= 4:
                radius = 2 + int(row['Lot Size (F2)'].replace(',', '')) / 10000
            '''
            # create the markers (circle markers)
            assessment_group.add_child(folium.CircleMarker([row['Latitude'], row['Longitude']],
                                                           radius=5,
                                                           popup=folium.Popup(popuptext, sticky=True),
                                                           # str(row['Assessed Value']),
                                                           color="blue",
                                                           fill_color="blue"))

            # creates geojson tags for each point so that the seach bar will be able to find them
            #   the name is set to be the roll number and address, can be set to whatever
            #   it is creating blue markers and then shrinking them which is hacky
            #   properties should have a "popup" option, but it wont render when text is put there (apparently
            #   a common bug that has yet to be fixed)
            #   need to resize the names of the labels
            #
            points.append({
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "name": str(row["Roll"]) + ', ' + str(row["Full Address"])
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [row['Longitude'], row['Latitude']]
                        },
                        "style": {
                            "icon": {
                                "iconUrl": "null",
                                "iconSize": [0, 0],
                                "iconAnchor": [0, 0]
                            }
                        }
                    }]
            })
            count += 1

        # remove all the points outside the current view (TBA)

        # add the assessment markers to the map
        m.add_child(assessment_group)

        # ----------------------------------------------------------------------------
        # mark each sale as a point with popup box etc.

        sales_group = FeatureGroup(name='Sales')

        # code to add in the assessment detail reports
        """ popup=folium.Popup(popuptext + ',  ' + '<a href="' + 'path' +
                           '"target="_blank">' + 'Assessment Detail'
                           + '</a>', sticky=True)
        """

        for index, row in filtered_sales.iterrows():
            # format the popup text (HTML formatting works) {formatted as columns}
            # the names here will have to be the same as the headers in the sales excel sheet otherwise an error
            # will be thrown
            test_df = pd.DataFrame(row[['Roll', 'Assessed Value', 'Land Size', 'TASP', 'TASP/Total', 'Zoning',
                                        'Property Class', 'Address', 'Legal', 'Market Area']])

            # html formatting for the tables that are displayed in the popup
            str_io = io.StringIO()
            test_df.to_html(buf=str_io, classes='table table-striped', header=False)
            html_str = '<div style="overflow-y: scroll; height: 100px;">\n' + str_io.getvalue() + '\n</div>'
            popuptext = html_str

            # create the markers (circle markers)
            sales_group.add_child(folium.CircleMarker([row['Latitude'], row['Longitude']],
                                                      radius=2,
                                                      popup=folium.Popup(popuptext, sticky=True),
                                                      color="#ef0300",
                                                      fill_color="#dd6108",  # divvy color
                                                      ))

            # creates geojson tags for each point so that the seach bar will be able to find them
            points.append({
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "name": str(row["Roll"]) + ', ' + str(row["Address"])
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [row['Longitude'], row['Latitude']]
                        },
                        "style": {
                            "icon": {
                                "iconUrl": "null",
                                "iconSize": [0, 0],
                                "iconAnchor": [0, 0]
                            }
                        }
                    }]
            })

        # hide the progress bar
        self.progress_frame.grid_forget()
        myGUI.update()

        # add the sales group to the map and turn on the layer selector in the top right
        m.add_child(sales_group)
        m.add_child(folium.map.LayerControl())

        # ----------------------------------------------------------------------------
        # add the toolbar on the left
        draw = Draw()

        # creates the search box
        Search(data=points, search_zoom=14, geom_type="Point", popup_on_found=True).add_to(m)

        # adds the toolbar on the left (search bar will not render if it isn't between when draw is initialized
        draw.add_to(m)

        # ----------------------------------------------------------------------------
        # add a legend
        # old legend
        '''
        legend_html = """
             <div style="position: fixed; 
             bottom: 50px; right: 50px; width: 120px; height: 40px; 
             border:3px solid grey; z-index:9999; font-size:12px;
             "><b>
             &nbsp; Assessment: &nbsp; <i class="fa fa-circle fa-1x"
                          style="color:blue"></i><br>
             &nbsp; &emsp; &emsp; &emsp; Sale: &nbsp; <i class="fa fa-circle fa-1x"
                          style="color:red"></i>
              </div>
             """

        m.get_root().html.add_child(folium.Element(legend_html))
        # the js
        '''

        # alternate legend (movable via click and drag)
        '''
        template = """
        {% macro html(this, kwargs) %}

        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>jQuery UI Draggable - Default functionality</title>
          <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

          <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
          <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

          <script>
          $( function() {
            $( "#maplegend" ).draggable({
                            start: function (event, ui) {
                                $(this).css({
                                    right: "auto",
                                    top: "auto",
                                    bottom: "auto"
                                });
                            }
                        });
        });

          </script>
        </head>
        <body>


        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
             border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

        <div class='legend-title'></div>
        <div class='legend-scale'>
          <ul class='legend-labels'>
            <li><span class="fa fa-circle fa-1x" style='color:blue'></span>Assessment</li>
            <li><span class="fa fa-circle fa-1x" style='color:red'></span>Sale</li>
          </ul>
        </div>
        </div>

        </body>
        </html>

        <style type='text/css'>
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
          .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
          .maplegend a {
            color: #777;
            }
        </style>
        {% endmacro %}"""

        macro = MacroElement()
        macro._template = Template(template)

        m.get_root().add_child(macro)
        '''
        # ----------------------------------------------------------------------------
        # Saves the map as the name of the inputted excel spreadsheet with mapster appended to the end
        # check if an output file already exists, if so make a new one with an incremented number

        os.chdir(file_path.replace(file_path.split("/")[-1], ''))

        number = len(glob.glob(file_path.split("/")[-1].replace(".xlsx", '') + " MAPSTER*.html")) + 1

        file_name = file_path.split("/")[-1].replace(".xlsx", '') + " MAPSTER" + ".html"

        if os.path.isfile(file_name):
            m.save(file_name.replace(".html", " (" + str(number) + ")") + ".html")
        else:
            m.save(file_name)

        m.save(TemporaryFile())


if __name__ == '__main__':
    # initialize the GUI
    myGUI = Tk()
    app = MainClass(myGUI)
    myGUI.title('Mapster Editor')
    myGUI['bg'] = "gray99"
    # myGUI.geometry("250x150")
    myGUI.mainloop()
