import requests, json
nazwa = "PKN Orlen"
jezyk = "pl"
parametr = "numberOfEmployees"
jezyki_do_porownania = ["en","de","ru","pl"]

dbpediapar="http://dbpedia.org/ontology/"+parametr
url = 'https://api.wikirank.net/api.php'
data = {"name": nazwa, "lang":jezyk}
r = requests.post(url, json=data)
js = json.loads(r.text)

quality={}
jezyk_nazwa={}
jezyk_parametr={}

for key,value in js["result"].items():
    if key not in jezyki_do_porownania: continue
    quality[key]=2/((1/(value["quality"]))+1/(value["popularity"]))
    jezyk_nazwa[key]=value["name"]
    
    main_url='http://mappings.dbpedia.org/server/extraction/'
    url=main_url+key+'/extract?title='+value["name"]+'&format=rdf-json&extractors=mappings'

    r = requests.get(url)
    for line in r.text.splitlines():
        js = json.loads(line[:-1])
        if dbpediapar in (js[list(js)[0]]):
            jezyk_parametr[key]=js[list(js)[0]][dbpediapar][0]["value"]
    
najlepszawersja=sorted(quality, key=quality.get, reverse=True)[0]
print (parametr+" ("+najlepszawersja +"): "+str(jezyk_parametr[najlepszawersja]))

