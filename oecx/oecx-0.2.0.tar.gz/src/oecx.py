import requests
import networkx as nx
import json
import csv
import os


stop=0
for r, d, f in os.walk(os.path.expanduser('~')):
    if stop == 1:
            break
    for files in d:
        if 'anaconda3' in os.path.join(r,files):
                path_=os.path.join(r,files)
                stop=1
                break
path_ += '/oecx_contry_names/country_names.tsv'

with open(path_) as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    next(tsvreader)
    countries=[]
    for line in tsvreader:
        country={}
        country['id']= line[0]
        country['id_3char']= line[1]
        country['name']= line[2]
        countries.append(country)

def net(hs4,year,traide_flow):
    # select impor or export
    if traide_flow == 'export':
        url_b= 'https://oec.world/olap-proxy/data?cube=trade_i_baci_a_92&drilldowns=Year,Importer%20Country&measures=Trade%20Value&parents=true&Year={}&Exporter%20Country={}&HS4={}&properties=Importer%20Country%20ISO%203'
    if traide_flow == 'import':
        url_b= 'https://oec.world/olap-proxy/data?cube=trade_i_baci_a_92&drilldowns=Year,Exporter%20Country&measures=Trade%20Value&parents=true&Year={}&Importer%20Country={}&HS4={}&properties=Exporter%20Country%20ISO%203'

    dates=[]
    for country in countries:
        ID=country['id']
        url=url_b.format(year,ID,hs4)
        cont=requests.get(url).content.decode("utf-8")
        dic = json.loads(cont)['data']
        for md in dic:
            md.update(country)
        dates += dic

    #networkx
    edges=[[key['name'],key['Country'] ] for key in dates ]
    G = nx.DiGraph()
    G.add_edges_from(edges)


    return G
