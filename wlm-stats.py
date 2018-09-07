#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012-2018 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import os
import oursql
import re
import time

#wlm counter con contador de subidas y megabytes
#http://commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_2012/CentralNotice

"""
yuvipanda request ranking of mobile users
select page_title,  
(select  rev_user_text from revision where rev_page = page_id order by rev_timestamp  limit 1 ) as original 
from iwlinks join page on iwl_from=page_id join revision on page_latest = rev_id where iwl_prefix='mw' and iwl_title='Wiki_Loves_Monuments_mobile_application' and page_namespace=6
"""

year = u'2018'
path = "/data/project/wlm-stats/public_html"
uploadcats = { 
    u'albania': u'Images from Wiki Loves Monuments %s in Albania' % (year), 
    u'algeria': u'Images from Wiki Loves Monuments %s in Algeria' % (year), 
    #u'andorra': u'Images from Wiki Loves Monuments %s in Andorra' % (year), 
    #u'antarctica': u'Images from Wiki Loves Monuments %s in Antarctica' % (year), 
    #u'argentina': u'Images from Wiki Loves Monuments %s in Argentina' % (year), 
    #u'armenia': u'Images from Wiki Loves Monuments %s in Armenia' % (year), 
    #u'armenia-nagorno': u'Images from Wiki Loves Monuments %s in Armenia & Nagorno-Karabakh' % (year), 
    u'aruba': u'Images from Wiki Loves Monuments %s in Aruba' % (year), 
    u'australia': u'Images from Wiki Loves Monuments %s in Australia' % (year), 
    u'austria': u'Images from Wiki Loves Monuments %s in Austria' % (year), 
    #u'austria': u'Media from WikiDaheim %s in Austria/Cultural heritage monuments' % (year), 
    u'azerbaijan': u'Images from Wiki Loves Monuments %s in Azerbaijan' % (year), 
    u'bangladesh': u'Images from Wiki Loves Monuments %s in Bangladesh' % (year), 
    #u'belarus': u'Images from Wiki Loves Monuments %s in Belarus' % (year), 
    #u'belgium': u'Images from Wiki Loves Monuments %s in Belgium' % (year), 
    u'bolivia': u'Images from Wiki Loves Monuments %s in Bolivia' % (year), 
    u'brazil': u'Images from Wiki Loves Monuments %s in Brazil' % (year), 
    #u'bulgaria': u'Images from Wiki Loves Monuments %s in Bulgaria' % (year), 
    #u'cambodia': u'Images from Wiki Loves Monuments %s in Cambodia' % (year), 
    #u'cameroon': u'Images from Wiki Loves Monuments %s in Cameroon' % (year), 
    u'canada': u'Images from Wiki Loves Monuments %s in Canada' % (year), 
    #u'chile': u'Images from Wiki Loves Monuments %s in Chile' % (year), 
    #u'china': u'Images from Wiki Loves Monuments %s in China' % (year), 
    #u'colombia': u'Images from Wiki Loves Monuments %s in Colombia' % (year), 
    u'croatia': u'Images from Wiki Loves Monuments %s in Croatia' % (year), 
    #u'czechrepublic': u'Images from Wiki Loves Monuments %s in the Czech Republic' % (year), 
    u'denmark': u'Images from Wiki Loves Monuments %s in Denmark' % (year), 
    #u'dutch-caribbean': u'Images from Wiki Loves Monuments %s in the Dutch Caribbean' % (year), 
    u'egypt': u'Images from Wiki Loves Monuments %s in Egypt' % (year), 
    #u'elsalvador': u'Images from Wiki Loves Monuments %s in El Salvador' % (year), 
    #u'estonia': u'Images from Wiki Loves Monuments %s in Estonia' % (year), 
    u'finland': u'Images from Wiki Loves Monuments %s in Finland' % (year), 
    u'france': u'Images from Wiki Loves Monuments %s in France' % (year), 
    u'georgia': u'Images from Wiki Loves Monuments %s in Georgia' % (year), 
    u'germany': u'Images from Wiki Loves Monuments %s in Germany' % (year), 
    #u'ghana': u'Images from Wiki Loves Monuments %s in Ghana' % (year), 
    u'greece': u'Images from Wiki Loves Monuments %s in Greece' % (year), 
    #u'hongkong': u'Images from Wiki Loves Monuments %s in Hong Kong' % (year), 
    #u'hungary': u'Images from Wiki Loves Monuments %s in Hungary' % (year), 
    u'india': u'Images from Wiki Loves Monuments %s in India' % (year), 
    u'iran': u'Images from Wiki Loves Monuments %s in Iran' % (year), 
    u'iraq': u'Images from Wiki Loves Monuments %s in Iraq' % (year), 
    u'ireland': u'Images from Wiki Loves Monuments %s in Ireland' % (year), 
    u'israel': u'Images from Wiki Loves Monuments %s in Israel' % (year), 
    u'italy': u'Images from Wiki Loves Monuments %s in Italy' % (year), 
    u'jordan': u'Images from Wiki Loves Monuments %s in Jordan' % (year), 
    #u'kenya': u'Images from Wiki Loves Monuments %s in Kenya' % (year), 
    u'kosovo': u'Images from Wiki Loves Monuments %s in Kosovo' % (year), 
    u'latvia': u'Images from Wiki Loves Monuments %s in Latvia' % (year), 
    u'lebanon': u'Images from Wiki Loves Monuments %s in Lebanon' % (year), 
    #u'liechtenstein': u'Images from Wiki Loves Monuments %s in Liechtenstein' % (year), 
    #u'luxembourg': u'Images from Wiki Loves Monuments %s in Luxembourg' % (year), 
    #u'macedonia': u'Images from Wiki Loves Monuments %s in Macedonia' % (year), 
    #u'madagascar': u'Images from Wiki Loves Monuments %s in Madagascar' % (year), 
    u'malaysia': u'Images from Wiki Loves Monuments %s in Malaysia' % (year), 
    u'malta': u'Images from Wiki Loves Monuments %s in Malta' % (year), 
    u'mexico': u'Images from Wiki Loves Monuments %s in Mexico' % (year), 
    u'morocco': u'Images from Wiki Loves Monuments %s in Morocco' % (year), 
    u'nepal': u'Images from Wiki Loves Monuments %s in Nepal' % (year), 
    #u'netherlands': u'Images from Wiki Loves Monuments %s in the Netherlands' % (year), 
    u'nigeria': u'Images from Wiki Loves Monuments %s in Nigeria' % (year), 
    u'norway': u'Images from Wiki Loves Monuments %s in Norway' % (year), 
    u'pakistan': u'Images from Wiki Loves Monuments %s in Pakistan' % (year), 
    u'palestine': u'Images from Wiki Loves Monuments %s in Palestine' % (year), 
    #u'panama': u'Images from Wiki Loves Monuments %s in Panama' % (year), 
    u'peru': u'Images from Wiki Loves Monuments %s in Peru' % (year), 
    u'philippines': u'Images from Wiki Loves Monuments %s in the Philippines' % (year), 
    u'poland': u'Images from Wiki Loves Monuments %s in Poland' % (year), 
    u'portugal': u'Images from Wiki Loves Monuments %s in Portugal' % (year), 
    #u'qatar': u'Images from Wiki Loves Monuments %s in Qatar' % (year), 
    u'romania': u'Images from Wiki Loves Monuments %s in Romania' % (year), 
    u'russia': u'Images from Wiki Loves Monuments %s in Russia' % (year), 
    #u'saudiarabia': u'Images from Wiki Loves Monuments %s in Saudi Arabia' % (year), 
    #u'serbia': u'Images from Wiki Loves Monuments %s in Serbia' % (year), 
    #u'slovakia': u'Images from Wiki Loves Monuments %s in Slovakia' % (year), 
    #u'southafrica': u'Images from Wiki Loves Monuments %s in South Africa' % (year), 
    #u'southkorea': u'Images from Wiki Loves Monuments %s in South Korea' % (year), 
    #u'southtyrol': u'Images from Wiki Loves Monuments %s in South Tyrol' % (year), 
    u'spain': u'Images from Wiki Loves Monuments %s in Spain' % (year), 
    u'sweden': u'Images from Wiki Loves Monuments %s in Sweden' % (year), 
    u'switzerland': u'Images from Wiki Loves Monuments %s in Switzerland' % (year), 
    u'syria': u'Images from Wiki Loves Monuments %s in Syria' % (year), 
    u'taiwan': u'Images from Wiki Loves Monuments %s in Taiwan' % (year), 
    u'thailand': u'Images from Wiki Loves Monuments %s in Thailand' % (year), 
    u'tunisia': u'Images from Wiki Loves Monuments %s in Tunisia' % (year), 
    #u'turkey': u'Images from Wiki Loves Monuments %s in Turkey' % (year), 
    u'uganda': u'Images from Wiki Loves Monuments %s in Uganda' % (year), 
    u'ukraine': u'Images from Wiki Loves Monuments %s in Ukraine' % (year), 
    u'unitedarabemirates': u'Images from Wiki Loves Monuments %s in the United Arab Emirates' % (year), 
    u'unitedkingdom': u'Images from Wiki Loves Monuments %s in the United Kingdom' % (year), 
    u'unitedstates': u'Images from Wiki Loves Monuments %s in the United States' % (year), 
    #u'uruguay': u'Images from Wiki Loves Monuments %s in Uruguay' % (year), 
    #u'venezuela': u'Images from Wiki Loves Monuments %s in Venezuela' % (year), 
}

countrynames = { 
    u'albania': u'Albania', 
    u'algeria': u'Algeria', 
    u'andorra': u'Andorra', 
    u'antarctica': u'Antarctica', 
    u'argentina': u'Argentina', 
    u'armenia': u'Armenia', 
    u'armenia-nagorno': u'Armenia &<br/>Nagorno-Karabakh', 
    u'aruba': u'Aruba', 
    u'austria': u'Austria', 
    u'australia': u'Australia', 
    u'azerbaijan': u'Azerbaijan', 
    u'bangladesh': u'Bangladesh', 
    u'belarus': u'Belarus', 
    u'belgium': u'Belgium', 
    u'bolivia': u'Bolivia', 
    u'brazil': u'Brazil', 
    u'bulgaria': u'Bulgaria', 
    u'cambodia': u'Cambodia', 
    u'cameroon': u'Cameroon', 
    u'canada': u'Canada', 
    u'chile': u'Chile', 
    u'china': u'China', 
    u'colombia': u'Colombia', 
    u'croatia': u'Croatia', 
    u'czechrepublic': u'Czech Republic', 
    u'denmark': u'Denmark', 
    u'dutch-caribbean': u'Dutch Caribbean', 
    u'egypt': u'Egypt', 
    u'elsalvador': u'El Salvador', 
    u'estonia': u'Estonia', 
    u'finland': u'Finland', 
    u'france': u'France', 
    u'georgia': u'Georgia', 
    u'germany': u'Germany', 
    u'ghana': u'Ghana', 
    u'greece': u'Greece', 
    u'hongkong': u'Hong Kong', 
    u'hungary': u'Hungary', 
    u'india': u'India', 
    u'iran': u'Iran', 
    u'iraq': u'Iraq', 
    u'ireland': u'Ireland', 
    u'israel': u'Israel', 
    u'italy': u'Italy', 
    u'jordan': u'Jordan', 
    u'kenya': u'Kenya', 
    u'kosovo': u'Kosovo', 
    u'latvia': u'Latvia', 
    u'lebanon': u'Lebanon', 
    u'liechtenstein': u'Liechtenstein', 
    u'luxembourg': u'Luxembourg', 
    u'macedonia': u'Macedonia', 
    u'madagascar': u'Madagascar', 
    u'malaysia': u'Malaysia', 
    u'malta': u'Malta', 
    u'mexico': u'Mexico', 
    u'morocco': u'Morocco', 
    u'nepal': u'Nepal', 
    u'netherlands': u'Netherlands', 
    u'nigeria': u'Nigeria', 
    u'norway': u'Norway', 
    u'pakistan': u'Pakistan', 
    u'palestine': u'Palestine', 
    u'panama': u'Panama', 
    u'peru': u'Peru', 
    u'philippines': u'Philippines', 
    u'poland': u'Poland', 
    u'portugal': u'Portugal', 
    u'qatar': u'Qatar', 
    u'romania': u'Romania', 
    u'russia': u'Russia', 
    u'saudiarabia': u'Saudi Arabia', 
    u'serbia': u'Serbia', 
    u'slovakia': u'Slovakia', 
    u'southafrica': u'South Africa', 
    u'southkorea': u'South Korea', 
    u'southtyrol': u'South Tyrol', 
    u'spain': u'Spain', 
    u'sweden': u'Sweden', 
    u'switzerland': u'Switzerland', 
    u'syria': u'Syria', 
    u'taiwan': u'Taiwan', 
    u'thailand': u'Thailand', 
    u'tunisia': u'Tunisia', 
    u'turkey': u'Turkey', 
    u'uganda': u'Uganda', 
    u'ukraine': u'Ukraine', 
    u'unitedarabemirates': u'United Arab Emirates', 
    u'unitedkingdom': u'United Kingdom', 
    u'unitedstates': u'United States', 
    u'uruguay': u'Uruguay', 
    u'venezuela': u'Venezuela', 
}

def convert2unix(mwtimestamp):
    #from wmchart0000.py
    #2010-12-25T12:12:12Z
    [year, month, day] = [int(mwtimestamp[0:4]), int(mwtimestamp[5:7]), int(mwtimestamp[8:10])]
    [hour, minute, second] = [int(mwtimestamp[11:13]), int(mwtimestamp[14:16]), int(mwtimestamp[17:19])]
    d = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return int((time.mktime(d.timetuple())+1e-6*d.microsecond)*1000)

def main():
    #loading files metadata
    conn = oursql.connect(db='commonswiki_p', host='s4.labsdb', read_default_file="~/replica.my.cnf", charset="utf8", use_unicode=True)
    curs = conn.cursor(oursql.DictCursor)
    filename = 'files-%s.txt' % (year)
    files = []
    filesdict = {}
    for country in uploadcats.keys():
        #continue
        print country
        curs.execute(u"""SELECT page_title, 
        (SELECT rev_user_text FROM revision WHERE rev_page=page_id ORDER BY rev_timestamp LIMIT 1) AS username,
        (SELECT rev_timestamp FROM revision WHERE rev_page=page_id ORDER BY rev_timestamp LIMIT 1) AS timestamp,
        (SELECT img_size FROM image WHERE img_name=page_title) AS size,
        (SELECT img_width FROM image WHERE img_name=page_title) AS width,
        (SELECT img_height FROM image WHERE img_name=page_title) AS height
        FROM categorylinks JOIN page ON cl_from=page_id JOIN revision ON page_latest=rev_id JOIN image ON img_name=page_title WHERE cl_to=? AND page_namespace=6;""", (re.sub(u' ', u'_', uploadcats[country]), ))
        row = curs.fetchone()
        while row:
            try:
                page_title = unicode(row['page_title'], 'utf-8')
                username = unicode(row['username'], 'utf-8')
                date = row['timestamp']
                date = u'%s-%s-%sT%s:%s:%sZ' % (date[0:4], date[4:6], date[6:8], date[8:10], date[10:12], date[12:14])
                resolution = u'%s×%s' % (str(row['width']), str(row['height']))
                size = str(row['size'])
                files.append([page_title, country, date, username, resolution, size])
                filesdict[page_title] = {'page_title': page_title, 'country': country, 'date': date, 'username': username, 'resolution': resolution, 'size': size}
            except:
                try:
                    print row
                except:
                    print 'Error'
            row = curs.fetchone()
    
    conn.close()
    print len(files), 'files'
    f = open("%s/%s" % (path, filename), 'w')
    output = u'%s\n%s' % (u';;;'.join(['filename', 'country', 'date', 'username', 'resolution', 'size']), u'\n'.join([u';;;'.join(i) for i in files]))
    f.write(output.encode('utf-8'))
    f.close()
    with open('%s/files-%s.json' % (path, year), 'w') as jsonfile:
        json.dump(filesdict, jsonfile)

    #stats
    dates = {}
    hours = {}
    users = {}
    countries = {}
    resolutions = {}
    sizes_list = []
    c = 0
    for title, country, date, username, resolution, size in files:
        c += 1
        #print c, title
        if countries.has_key(country):
            countries[country]['files'] += 1
            countries[country]['size'] += int(size)
            if not username in countries[country]['uploaders']:
                countries[country]['uploaders'].append(username)
        else:
            countries[country] = { 'files': 1, 'size': int(size), 'uploaders': [username]}
        d = u'%sT00:00:00Z' % (date.split('T')[0])
        h = date.split('T')[1].split(':')[0]
        if dates.has_key(d):
            dates[d] += 1
        else:
            dates[d] = 1
        if hours.has_key(h):
            hours[h] += 1
        else:
            hours[h] = 1
        if users.has_key(username):
            users[username]['files'] += 1
            users[username]['size'] += int(size)
        else:
            users[username] = {'files': 1, 'size': int(size)}
        if resolutions.has_key(resolution):
            resolutions[resolution]['files'] += 1
            resolutions[resolution]['size'] += int(size)
        else:
            resolutions[resolution] = {'files': 1, 'size': int(size)}
        sizes_list.append([int(size), title, username, country])

    sizes_list.sort(reverse=1)
    countries_list = [[v['files'], k] for k, v in countries.items()]
    countries_list.sort(reverse=1)
    countries_list = [[k, v] for v, k in countries_list]
    dates_list = [[k, v] for k, v in dates.items()]
    dates_list.sort()
    hours_list = [[k, v] for k, v in hours.items()]
    hours_list.sort()
    users_list = [[v, k] for k, v in users.items()]
    users_list.sort(reverse=1)
    users_list = [[k, v] for v, k in users_list]
    resolutions_list = [[v, k] for k, v in resolutions.items()]
    resolutions_list.sort(reverse=1)
    resolutions_list = [[k, v] for v, k in resolutions_list]

    dates_graph_data = u', '.join([u'["%s", %s]' % (convert2unix(k), v) for k, v in dates_list])
    dates_graph = u"""<div id="dates_graph" style="width: 1000px;height: 500px;"></div>"""
    dates_graph_mini = u"""<div id="dates_graph" style="width: 300px;height: 150px;"></div>"""
    #unix timestamps are the 31 August - 1 October of current year for all (repeat)
    dates_graph_core = u"""
    <script type="text/javascript">
    $(function () {
        var ts = 1535673600000; // 00:00 Aug 31st of present year
        var tsday = 86400*1000; // do not change
        
        var dates_graph_data_2018 = [%s];
        
        var dates_graph_data_2017 = [[(ts+tsday*0).toString(), 320], [(ts+tsday*1).toString(), 7997], [(ts+tsday*2).toString(), 7311], [(ts+tsday*3).toString(), 9812], [(ts+tsday*4).toString(), 6567], [(ts+tsday*5).toString(), 5309], [(ts+tsday*6).toString(), 4490], [(ts+tsday*7).toString(), 5072], [(ts+tsday*8).toString(), 5333], [(ts+tsday*9).toString(), 4374], [(ts+tsday*10).toString(), 4704], [(ts+tsday*11).toString(), 6496], [(ts+tsday*12).toString(), 6707], [(ts+tsday*13).toString(), 5188], [(ts+tsday*14).toString(), 5003], [(ts+tsday*15).toString(), 3321], [(ts+tsday*16).toString(), 4301], [(ts+tsday*17).toString(), 6150], [(ts+tsday*18).toString(), 5646], [(ts+tsday*19).toString(), 5107], [(ts+tsday*20).toString(), 6426], [(ts+tsday*21).toString(), 6173], [(ts+tsday*22).toString(), 6701], [(ts+tsday*23).toString(), 7583], [(ts+tsday*24).toString(), 8528], [(ts+tsday*25).toString(), 10456], [(ts+tsday*26).toString(), 8301], [(ts+tsday*27).toString(), 10505], [(ts+tsday*28).toString(), 14117], [(ts+tsday*29).toString(), 20442], [(ts+tsday*30).toString(), 27511], [(ts+tsday*31).toString(), 1619]];
        
        var dates_graph_data_2016 = [[(ts+tsday*0).toString(), 366], [(ts+tsday*1).toString(), 5179], [(ts+tsday*2).toString(), 8836], [(ts+tsday*3).toString(), 8759], [(ts+tsday*4).toString(), 8689], [(ts+tsday*5).toString(), 5316], [(ts+tsday*6).toString(), 5562], [(ts+tsday*7).toString(), 5160], [(ts+tsday*8).toString(), 6187], [(ts+tsday*9).toString(), 6455], [(ts+tsday*10).toString(), 6645], [(ts+tsday*11).toString(), 5753], [(ts+tsday*12).toString(), 5503], [(ts+tsday*13).toString(), 4613], [(ts+tsday*14).toString(), 4643], [(ts+tsday*15).toString(), 6142], [(ts+tsday*16).toString(), 6058], [(ts+tsday*17).toString(), 5742], [(ts+tsday*18).toString(), 8285], [(ts+tsday*19).toString(), 6186], [(ts+tsday*20).toString(), 7978], [(ts+tsday*21).toString(), 6818], [(ts+tsday*22).toString(), 6751], [(ts+tsday*23).toString(), 7343], [(ts+tsday*24).toString(), 7475], [(ts+tsday*25).toString(), 9397], [(ts+tsday*26).toString(), 11575], [(ts+tsday*27).toString(), 12276], [(ts+tsday*28).toString(), 13934], [(ts+tsday*29).toString(), 23664], [(ts+tsday*30).toString(), 32493], [(ts+tsday*31).toString(), 2613]];
        
        var dates_graph_data_2015 = [[(ts+tsday*0).toString(), 852], [(ts+tsday*1).toString(), 6981], [(ts+tsday*2).toString(), 6028], [(ts+tsday*3).toString(), 6519], [(ts+tsday*4).toString(), 7189], [(ts+tsday*5).toString(), 5689], [(ts+tsday*6).toString(), 6726], [(ts+tsday*7).toString(), 4823], [(ts+tsday*8).toString(), 3824], [(ts+tsday*9).toString(), 4276], [(ts+tsday*10).toString(), 3521], [(ts+tsday*11).toString(), 4177], [(ts+tsday*12).toString(), 5003], [(ts+tsday*13).toString(), 6793], [(ts+tsday*14).toString(), 4989], [(ts+tsday*15).toString(), 5869], [(ts+tsday*16).toString(), 4800], [(ts+tsday*17).toString(), 4802], [(ts+tsday*18).toString(), 4393], [(ts+tsday*19).toString(), 5661], [(ts+tsday*20).toString(), 7025], [(ts+tsday*21).toString(), 8293], [(ts+tsday*22).toString(), 7860], [(ts+tsday*23).toString(), 6899], [(ts+tsday*24).toString(), 7749], [(ts+tsday*25).toString(), 6534], [(ts+tsday*26).toString(), 7894], [(ts+tsday*27).toString(), 10949], [(ts+tsday*28).toString(), 14017], [(ts+tsday*29).toString(), 15320], [(ts+tsday*30).toString(), 22803], [(ts+tsday*31).toString(), 825]];
        
        var dates_graph_data_2014 = [[(ts+tsday*0).toString(), 837], [(ts+tsday*1).toString(), 10066], [(ts+tsday*2).toString(), 6531], [(ts+tsday*3).toString(), 6595], [(ts+tsday*4).toString(), 5285], [(ts+tsday*5).toString(), 5430], [(ts+tsday*6).toString(), 6534], [(ts+tsday*7).toString(), 6925], [(ts+tsday*8).toString(), 5187], [(ts+tsday*9).toString(), 4659], [(ts+tsday*10).toString(), 5070], [(ts+tsday*11).toString(), 4157], [(ts+tsday*12).toString(), 5416], [(ts+tsday*13).toString(), 5198], [(ts+tsday*14).toString(), 6586], [(ts+tsday*15).toString(), 6604], [(ts+tsday*16).toString(), 7280], [(ts+tsday*17).toString(), 7816], [(ts+tsday*18).toString(), 5855], [(ts+tsday*19).toString(), 5128], [(ts+tsday*20).toString(), 6786], [(ts+tsday*21).toString(), 7939], [(ts+tsday*22).toString(), 7570], [(ts+tsday*23).toString(), 7779], [(ts+tsday*24).toString(), 6979], [(ts+tsday*25).toString(), 8705], [(ts+tsday*26).toString(), 9844], [(ts+tsday*27).toString(), 10181], [(ts+tsday*28).toString(), 12936], [(ts+tsday*29).toString(), 16419], [(ts+tsday*30).toString(), 24490], [(ts+tsday*31).toString(), 2690]];
        
        var dates_graph_data_2013 = [[(ts+tsday*0).toString(), 409], [(ts+tsday*1).toString(), 14345], [(ts+tsday*2).toString(), 8265], [(ts+tsday*3).toString(), 9208], [(ts+tsday*4).toString(), 8663], [(ts+tsday*5).toString(), 7886], [(ts+tsday*6).toString(), 8220], [(ts+tsday*7).toString(), 8453], [(ts+tsday*8).toString(), 9373], [(ts+tsday*9).toString(), 9606], [(ts+tsday*10).toString(), 8279], [(ts+tsday*11).toString(), 9629], [(ts+tsday*12).toString(), 7791], [(ts+tsday*13).toString(), 8388], [(ts+tsday*14).toString(), 8160], [(ts+tsday*15).toString(), 9568], [(ts+tsday*16).toString(), 8790], [(ts+tsday*17).toString(), 9468], [(ts+tsday*18).toString(), 8790], [(ts+tsday*19).toString(), 8381], [(ts+tsday*20).toString(), 8992], [(ts+tsday*21).toString(), 10009], [(ts+tsday*22).toString(), 12367], [(ts+tsday*23).toString(), 9869], [(ts+tsday*24).toString(), 13156], [(ts+tsday*25).toString(), 14209], [(ts+tsday*26).toString(), 15964], [(ts+tsday*27).toString(), 15085], [(ts+tsday*28).toString(), 19514], [(ts+tsday*29).toString(), 33069], [(ts+tsday*30).toString(), 41951], [(ts+tsday*31).toString(), 3711]];

        var dates_graph_data_2012 = [[(ts+tsday*0).toString(), 525], [(ts+tsday*1).toString(), 7641], [(ts+tsday*2).toString(), 8638], [(ts+tsday*3).toString(), 6954], [(ts+tsday*4).toString(), 7276], [(ts+tsday*5).toString(), 7946], [(ts+tsday*6).toString(), 6513], [(ts+tsday*7).toString(), 7268], [(ts+tsday*8).toString(), 8386], [(ts+tsday*9).toString(), 10372], [(ts+tsday*10).toString(), 10613], [(ts+tsday*11).toString(), 8214], [(ts+tsday*12).toString(), 8694], [(ts+tsday*13).toString(), 9046], [(ts+tsday*14).toString(), 8725], [(ts+tsday*15).toString(), 8627], [(ts+tsday*16).toString(), 11119], [(ts+tsday*17).toString(), 9520], [(ts+tsday*18).toString(), 8408], [(ts+tsday*19).toString(), 7387], [(ts+tsday*20).toString(), 8284], [(ts+tsday*21).toString(), 10391], [(ts+tsday*22).toString(), 10656], [(ts+tsday*23).toString(), 14308], [(ts+tsday*24).toString(), 11642], [(ts+tsday*25).toString(), 12848], [(ts+tsday*26).toString(), 13158], [(ts+tsday*27).toString(), 17252], [(ts+tsday*28).toString(), 20409], [(ts+tsday*29).toString(), 26966], [(ts+tsday*30).toString(), 47387], [(ts+tsday*31).toString(), 5554]];

        var dates_graph_data_2011 = [[(ts+tsday*0).toString(), 222], [(ts+tsday*1).toString(), 2373], [(ts+tsday*2).toString(), 1560], [(ts+tsday*3).toString(), 2211], [(ts+tsday*4).toString(), 3473], [(ts+tsday*5).toString(), 3333], [(ts+tsday*6).toString(), 2968], [(ts+tsday*7).toString(), 3050], [(ts+tsday*8).toString(), 2850], [(ts+tsday*9).toString(), 3146], [(ts+tsday*10).toString(), 3546], [(ts+tsday*11).toString(), 4306], [(ts+tsday*12).toString(), 4069], [(ts+tsday*13).toString(), 3755], [(ts+tsday*14).toString(), 3378], [(ts+tsday*15).toString(), 4762], [(ts+tsday*16).toString(), 3596], [(ts+tsday*17).toString(), 4648], [(ts+tsday*18).toString(), 7038], [(ts+tsday*19).toString(), 5095], [(ts+tsday*20).toString(), 4185], [(ts+tsday*21).toString(), 4669], [(ts+tsday*22).toString(), 4390], [(ts+tsday*23).toString(), 4807], [(ts+tsday*24).toString(), 6123], [(ts+tsday*25).toString(), 8159], [(ts+tsday*26).toString(), 6691], [(ts+tsday*27).toString(), 9158], [(ts+tsday*28).toString(), 10408], [(ts+tsday*29).toString(), 13188], [(ts+tsday*30).toString(), 21971], [(ts+tsday*31).toString(), 927]];
       
        var dates_graph = $("#dates_graph");
        var dates_graph_data = [{ data: dates_graph_data_2011, label: "2011"}, { data: dates_graph_data_2012, label: "2012"}, { data: dates_graph_data_2013, label: "2013"}, { data: dates_graph_data_2014, label: "2014"}, { data: dates_graph_data_2015, label: "2015"}, { data: dates_graph_data_2016, label: "2016"}, { data: dates_graph_data_2017, label: "2017"}, { data: dates_graph_data_2018, label: "2018"}];
        var dates_graph_options = { xaxis: { mode: "time", min: (new Date("2018/08/31")).getTime(), max: (new Date("2018/10/01")).getTime() }, lines: { show: true }, points: { show: true }, legend: { noColumns: 8, position: "nw" }, grid: { hoverable: true }, clickable: true, hoverable: true };
        $.plot(dates_graph, dates_graph_data, dates_graph_options);
    });
    
    //from http://people.iola.dk/olau/flot/examples/interacting.html
    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 12,
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#dates_graph").bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));
        
        if (item) {
            if (previousPoint != item.datapoint) {
                previousPoint = item.datapoint;
                
                $("#tooltip").remove();
                var x = item.datapoint[0].toFixed(2),
                    y = item.datapoint[1].toFixed(2);
                
                showTooltip(item.pageX, item.pageY,
                            "y = "+Math.round(y));
            }
        } else {
            $("#tooltip").remove();
            previousPoint = null;            
        }
    });

    </script>""" % (dates_graph_data)
    dates_graph += dates_graph_core
    dates_graph_mini += dates_graph_core

    hours_graph_data = u', '.join([u'["%s", %s]' % (k, v) for k, v in hours_list])
    hours_graph = u"""<div id="hours_graph" style="width: 1000px;height: 250px;"></div>
    <script type="text/javascript">
    $(function () {
        var hours_graph_data = [%s];
       
        var hours_graph = $("#hours_graph");
        var hours_graph_data = [ hours_graph_data, ];
        var hours_graph_options = { xaxis: { mode: null, tickSize: 1, tickDecimals: 0, min: 1, max: 23}, bars: { show: true, barWidth: 0.6 }, points: { show: false }, legend: { noColumns: 1 }, grid: { hoverable: true }, };
        $.plot(hours_graph, hours_graph_data, hours_graph_options);
    });
    </script>""" % (hours_graph_data)
    
    countries_rank = u''
    c = 0
    for k, v in countries_list:
        c += 1
        countries_rank += u'<tr><td>%s</td><td>%s</td><td><a href="//commons.wikimedia.org/wiki/Category:%s">%s</a></td><td>%d</td><td>%.1f</td><td><a href="http://stats.wikilovesmonuments.cl/?pais=%s">Details</a></td></tr>\n' % (c, countrynames[k], re.sub(' ', '_', uploadcats[k]), countries[k]['files'], len(countries[k]['uploaders']), countries[k]['size']/1024.0/1024, k)
    countries_rank += u'<tr><td></td><td><b>Total</b></td><td><b><a href="//commons.wikimedia.org/wiki/Category:Images_from_Wiki_Loves_Monuments_%s">%s</a></b></td><td><b>%d</b></td><td><b>%.1f</b></td><td></td></tr>\n' % (year, sum([countries[k]['files'] for k in countries.keys()]), len(users.keys()), sum([countries[k]['size'] for k in countries.keys()])/1024.0/1024)
    countries_rank = u"""<table id="countries" class="wikitable" style="text-align: center;">
    <tr><th>#</th><th>Country</th><th>Files</th><th>Uploaders</th><th>MBytes</th><th>Details</th></tr>
    %s
    </table>""" % (countries_rank)
    
    users_rank = u''
    c = 0
    for k, v in users_list[:100]:
        c += 1
        users_rank += u'<tr><td>%s</td><td><a href="//commons.wikimedia.org/wiki/User:%s">%s</a></td><td><a href="//commons.wikimedia.org/wiki/Special:ListFiles/%s">%s</a></td><td>%.1f</td></tr>' % (c, re.sub(' ', '_', k), k, re.sub(' ', '_', k), users[k]['files'], users[k]['size']/1024.0/1024)
    users_rank += u'<tr><td></td><td><b>Total</b></td><td><b><a href="//commons.wikimedia.org/wiki/Category:Images_from_Wiki_Loves_Monuments_%s">%s</a></b></td><td><b>%.1f</b></td></tr>' % (year, sum([users[k]['files'] for k in users.keys()]), sum([users[k]['size'] for k in users.keys()])/1024.0/1024)
    users_rank = u"""<table id="uploaders" class="wikitable" style="text-align: center;">
    <tr><th>#</th><th>Uploader</th><th>Files</th><th>MBytes</th></tr>
    %s
    </table>""" % (users_rank)
    
    resolutions_rank = u''
    c = 0
    for k, v in resolutions_list[:15]:
        c += 1
        resolutions_rank += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%.1f</td></tr>' % (c, k, resolutions[k]['files'], resolutions[k]['size']/1024.0/1024)
    resolutions_rank += u'<tr><td></td><td><b>Total</b></td><td><b><a href="//commons.wikimedia.org/wiki/Category:Images_from_Wiki_Loves_Monuments_%s">%s</a></b></td><td><b>%.1f</b></td></tr>' % (year, sum([resolutions[k]['files'] for k in resolutions.keys()]), sum([resolutions[k]['size'] for k in resolutions.keys()])/1024.0/1024)
    resolutions_rank = u"""<table id="resolutions" class="wikitable" style="text-align: center;">
    <tr><th>#</th><th>Resolution</th><th>Files</th><th>MBytes</th></tr>
    %s
    </table>""" % (resolutions_rank)
    
    sizes_rank = u''
    c = 0
    for size, title, username, country in sizes_list[:15]: 
        c += 1
        sizes_rank += u'<tr><td>%s</td><td><a href="//commons.wikimedia.org/wiki/File:%s">%s</a></td><td>%.1f</td><td><a href="//commons.wikimedia.org/wiki/User:%s">%s</a></td><td>%s</td></tr>' % (c, title, len(title)>10 and (u'%s...' % title[:10]) or title, size/1024.0/1024, re.sub(' ', '_', username), username, countrynames[country])
    sizes_rank += u'<tr><td></td><td><b>Total</b></td><td><b>%.1f</b></td><td></td><td></td></tr>' % (sum([resolutions[k]['size'] for k in resolutions.keys()])/1024.0/1024)
    sizes_rank = u"""<table id="sizes" class="wikitable" style="text-align: center;">
    <tr><th>#</th><th>File</th><th>MBytes</th><th>Uploader</th><th>Country</th></tr>
    %s
    </table>""" % (sizes_rank)
    
    intro = u"<b>%s files</b> by <b>%s uploaders</b> from <b>%s countries</b> so far" % (sum([countries[k]['files'] for k in countries.keys()]), len(users.keys()), len(countries.keys()))
    output = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en" dir="ltr" xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Wiki Loves Monuments statistics</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rel="stylesheet" type="text/css" href="wlm.css" />
<script language="javascript" type="text/javascript" src="modules/jquery.js"></script>
<script language="javascript" type="text/javascript" src="modules/jquery.flot.js"></script>
</head>

<body style="background-color: white;">

<center>
<table border=0 cellpadding=0px width=1000px style="text-align: center;">
<tr>
<td valign=middle ><img src="//upload.wikimedia.org/wikipedia/commons/thumb/f/f3/LUSITANA_WLM_2011_d.svg/120px-LUSITANA_WLM_2011_d.svg.png" /></td>
<td valign=top width=99%%>
<br/><big><big><big><b><a href="//commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_%s">Wiki <i>Loves</i> Monuments</a></b></big></big></big>
<br/><b>September %s</b>
<br/><br/>%s
<br/><br/>Uploads <a href="#day">per day</a> and <a href="#hour">per hour</a> - Rankings for <a href="#countries">countries</a>, <a href="#uploaders">uploaders</a>, <a href="#sizes">sizes</a> and <a href="#resolutions">resolutions</a>
</td>
<td valign=middle><img src="//upload.wikimedia.org/wikipedia/commons/thumb/f/f3/LUSITANA_WLM_2011_d.svg/120px-LUSITANA_WLM_2011_d.svg.png" /></td>
</tr>
</table>

<h2 id="day">Uploads per day</h2>
%s

<h2 id="hour">Uploads per hour</h2>
%s

<h2 id="detailed">Detailed statistics</h2>
<table border=0>
<tr>
<td valign=top>
<center>
<!-- countries rank -->%s
<!-- resolutions rank -->%s
<!-- sizes rank -->%s
</center>
</td>
<td valign=top>
<center>
<!-- users rank -->%s
</center>
</td>
</tr>
</table>

Download 2018 metadata and make your own statistics: <a href="files-2018.txt">CSV</a> and <a href="files-2018.json">JSON</a><br/><br/>

<b>See also:</b> <a href="stats-2017.php">2017 stats</a> (<a href="files-2017.txt">csv</a>, <a href="files-2017.json">json</a>), <a href="stats-2016.php">2016 stats</a> (<a href="files-2016.txt">csv</a>, <a href="files-2016.json">json</a>), <a href="stats-2015.php">2015 stats</a> (<a href="files-2015.txt">csv</a>, <a href="files-2015.json">json</a>), <a href="stats-2014.php">2014 stats</a> (<a href="files-2014.txt">csv</a>, <a href="files-2014.json">json</a>), <a href="stats-2013.php">2013 stats</a> (<a href="files-2013.txt">csv</a>), <a href="stats-2012.php">2012 stats</a> (<a href="files-2012.txt">csv</a>) and <a href="stats-2011.php">2011 stats</a> (<a href="files-2011.txt">csv</a>)<br/><br/>

<b>Other statistics:</b> <a href="http://stats.wikilovesmonuments.cl/?pais=">country details</a> (Superzerocool), <a href="http://www.geobib.fr/mh/stats/">cumulative</a> (Sylvain), <a href="http://wikizabytki.pl/stats/">country race</a> (Yarl) and <a href="//commons.wikimedia.org/wiki/Commons:Wiki_Loves_Monuments_%s/Tools">many more</a>!
<br/><br/>

<i><b>Last update:</b> %s (UTC). Developed by <a href="https://en.wikipedia.org/wiki/User:Emijrp">emijrp</a> using <a href="http://www.flotcharts.org">flot</a>. <a href="https://github.com/emijrp/wlm-stats">Source code</a> is GPL.</i><br/><br/>

<a href="//tools.wmflabs.org/wlm-maps/"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/9/93/Wiki_Loves_Monuments_2015_-_2015-09-01.png/640px-Wiki_Loves_Monuments_2015_-_2015-09-01.png" title="Check the map!" /></a>

<br/><br/>

</center>

</body>
</html>""" % (year, year, intro, dates_graph, hours_graph, countries_rank, resolutions_rank, sizes_rank, users_rank, year, datetime.datetime.now())
    with open('%s/stats-%s.php' % (path, year), 'w') as f:
        f.write(output.encode('utf-8'))
    
    output = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en" dir="ltr" xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Wiki Loves Monuments statistics</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<link rel="stylesheet" type="text/css" href="wlm.css" />
<script language="javascript" type="text/javascript" src="modules/jquery.js"></script>
<script language="javascript" type="text/javascript" src="modules/jquery.flot.js"></script>
</head>

<body style="background-color: white;">
%s
</body>
</html>""" % (dates_graph_mini)
    with open('%s/stats-%s-mini.php' % (path, year), 'w') as f:
        f.write(output.encode('utf-8'))

if __name__ == '__main__':
    main()
