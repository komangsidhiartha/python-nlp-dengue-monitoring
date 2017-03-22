
from __future__ import division
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import request
import sys
import decimal
import collections
from collections import OrderedDict
import os
import datetime

dir_of_interest = "/Users/rpl/projects/python/monitoring-dbd/Program_NER/ner_maxent"
sys.path.append(dir_of_interest)

import dbmodel as db
import gazetter
import tahun as th


def create_app(configfile=None):    

    app = Flask(__name__, template_folder="templates")

    # you can set key as config
    app.config['GOOGLEMAPS_KEY'] = "AIzaSyC_B20lmmVGDmtic8ZOm5SSIYohoryZf6w"

    # you can also pass key here
    GoogleMaps(app, key="AIzaSyC_B20lmmVGDmtic8ZOm5SSIYohoryZf6w")

    dbmodel = db.DBModel()

    @app.route("/", methods=['GET', 'POST'])
    def mapview():
        gaz_mon_num = gazetter.month_num
        gaz_month = gazetter.month
        gaz_month_ind = gazetter.month_index

        now = datetime.datetime.now()

        get_year = request.args.get('year')
        if get_year == None or int(get_year) > now.year:
            get_year = str(now.year)

        tahun = get_year

        fwc_db = "%s_fwc"%tahun
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nop', 'dec']
        y_dropdown = [(now.year - i) for i in range(5, -1, -1) ]
        print months
        if tahun == '' or months == False :
            command = "Pastikan setting tahun pada file ner_maxent/tahun.py sudah benar !"
            return render_template('warning.html', command=command)

        #Setting menu dropdown
        temp_month = {}
        for month in months:
            key = gaz_mon_num.index(month)
            temp_month[key] = gaz_month[month]

        get_month = request.args.get('month')
        get_ai = request.args.get('ai')

        location_form = request.form

        if get_month != None:
            dynamic_month = gaz_mon_num[int(get_month)]
            dropdown = gaz_month[dynamic_month]
        else:
            dynamic_month = gaz_mon_num[now.month - 1]
            dropdown = gaz_month[dynamic_month]

        if "location" in location_form:
            locs = request.form["location"].lower()
            title = "Persebaran Penyakit Demam Berdarah di "+locs.title()+" Pada Bulan "+dropdown.title()
            dropdown = request.form["month_form"]
            for index, month in gaz_month.iteritems():
                if month == dropdown:
                    dynamic_month = index
            datas = dbmodel.get_location_by_name_and_month(fwc_db,locs,dynamic_month)

        elif get_ai != None:
            get_month = request.args.get('m')
            dynamic_month = gaz_month_ind[get_month]
            dropdown = gaz_month[dynamic_month]
            if get_ai == "tinggi":
                title = "Persebaran Penyakit Demam Berdarah Resiko Tinggi di Bulan "+get_month
                datas = dbmodel.get_location_by_ai_and_month(fwc_db,"tinggi",dynamic_month)
            elif get_ai == "sedang":
                title = "Persebaran Penyakit Demam Berdarah Resiko Sedang di Bulan "+get_month
                datas = dbmodel.get_location_by_ai_and_month(fwc_db,"sedang",dynamic_month)
            else :
                title = "Persebaran Penyakit Demam Berdarah Resiko Rendah di Bulan "+get_month
                datas = dbmodel.get_location_by_ai_and_month(fwc_db,"rendah",dynamic_month)
        else:
            title = "Persebaran Penyakit Demam Berdarah di Negara Indonesia Pada Bulan "+dropdown.title()
            datas = dbmodel.top_location_of_month(fwc_db,dynamic_month)

        # creating a map in the view
        mark = []
        history = {}
        temp_uniqe_coordinate = []
        graph_all = {}
        label_graph = []
        data_graph = []
        for data in datas:
            location = data["_id"]
            label_graph.append(location)
            data_graph.append(data["NUM"])
            # print data["data"][0]["url_duplicate"]
            coordinate = list(dbmodel.get_lat_long_location("bigcities","cities", location))
            data_locations = {}
            for loc in coordinate:
                temp_long = loc["longitude"].encode('ascii', 'ignore').replace("'","").replace("o"," ").split(" ")
                s = decimal.Decimal(int(temp_long[3])/60)
                m = decimal.Decimal((int(temp_long[2])+s)/60)
                d = decimal.Decimal(int(temp_long[1])+m)
                if temp_long[0] == 'S' or temp_long[0] == 'W':
                    longitude = 0 - d
                else:
                    longitude = d

                temp_lat = loc["latitude"].encode('ascii', 'ignore').replace("'","").replace("o"," ").split(" ")
                s = decimal.Decimal(int(temp_lat[3])/60)
                m = decimal.Decimal((int(temp_lat[2])+s)/60)
                d = decimal.Decimal(int(temp_lat[1])+m)
                if temp_lat[0] == 'S' or temp_lat[0] == 'W':
                    latitude = 0 - d
                else:
                    latitude = d

                if data["NUM"] > 55 :
                    btn_style = "btn-danger"
                    data_locations["icon"] = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                elif data["NUM"] > 19 :
                    btn_style = "btn-warning"
                    data_locations["icon"] = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
                else:
                    btn_style = "btn-success"
                    data_locations["icon"] = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"

                data_locations["lat"] = float(latitude)
                data_locations["lng"] = float(longitude)
                str_temp_coordinate = str(data_locations["lat"])+"_"+str(data_locations["lng"])
                # url = data["url_duplicate"]
                split_location = location.split(" ")
                if len(split_location) > 1 :
                    for spl_loc in split_location :
                        location_element += spl_loc.encode("utf8")
                else :
                    location_element = location.encode("utf8")

                data_locations["infobox"] = '<button type="button" class="btn '+btn_style+' btn-lg btn-detail-history" data-toggle="modal" id="bt_'+location_element+'" data-target="#modalHistory_'+location_element+'">'+location.encode("utf8").title()+' : '+str(data["NUM"])+' Penderita</button>'
                # data_locations["infobox"] = location.encode("utf8")

            if len(data_locations)>=1:
                if len(coordinate)==1 and str_temp_coordinate not in temp_uniqe_coordinate: 
                    mark.append(data_locations)
                    data = dbmodel.get_history_incident_by_location(fwc_db, dynamic_month, location.lower())
                    # print data
                    history[location_element] = data
                else:
                    if loc["populasi"].encode("utf8") != "" and str_temp_coordinate not in temp_uniqe_coordinate:
                       mark.append(data_locations) 
                       data = dbmodel.get_history_incident_by_location(fwc_db, dynamic_month, location.lower())
                       history[location_element] = data

                temp_uniqe_coordinate.append(str_temp_coordinate)

            # print history

        graph_all["label_chart"] = label_graph 
        graph_all["data_chart"] = data_graph 

        fullmap = Map(
            identifier="fullmap",
            style=(
                "height:90%;"
                "width:100%;"
                "bottom:10%;"
                "top:7%;"
                "right:0;"
                "position:absolute;"
                "z-index:0;"
            ),
            lat=-0.059531,
            lng=118.957520,
            markers=mark,
            cluster=True,
            cluster_gridsize=30,
            zoom="5"
        )

        m = collections.OrderedDict(sorted(temp_month.items()))



        return render_template('point.html', fullmap=fullmap, m=m, dropdown=dropdown, month_index=gaz_mon_num.index(dynamic_month), title=title, graph_data =graph_all, history=history, y=tahun, y_dropdown=y_dropdown)


    @app.route("/retrieve", methods=['POST'])
    def retrieve_data_from_twitter():
        post_year = request.form['year_form']
        post_month = request.form["month_form"]

        print post_year
        print post_month

        return render_template('retrieve.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)