import urllib.request
import urllib.parse
import re

# display
def pintar():
    print("\n")
    print(contaminants)
    print(stations)
    print(pollution)
    
def input_station():
    print("Seleccione la estación: ")
    for i in enumerate(stations):
        print(i)
    a = int(input(">"))
    return a

def input_cont():
    print("Seleccione el contaminante: ")
    for i in enumerate(contaminants):
        print(i)
    
    b = int(input(">"))
    return b

def uds(s):
    if(s=='CO'):
        uds = " mg/m³"
    else:
        uds = " µg/m³"
    return uds
def begining():
    print("\n")
    print("---------------------------------")

def ending():
    print("---------------------------------")
    print("Data may be affected by further validation.")
    print("Last hour data.")
    print("\n")

def switch(n):
    if n == 3:
        station_contaminant()
    elif n ==1:
        stations_()
    elif n ==2:
        cont_()

def station_contaminant():
    print("\n")
    print("Datos por estación y contaminante")
    a = input_station()
    b = input_cont() 
    begining()
    print("Los sensores de " + contaminants[b] + " en " + stations[a] + " indican:")
    uds = uds(contaminants[b])
    pol = pollution[stations[a]][contamintants[b]]
    print(pol + " " + uds)
    ending()

def stations_():    
    print("\n")
    print("Datos por estación")
    a = input_station()
    pol = pollution[stations[a]]
    begining()
    for k in pol:
        print(k + " " + pol[k] + uds(k))
    ending()

def cont_():
    print("\n")
    print("Datos un contaminante para todas las estaciones disponibles")
    b = input_cont()
    begining()
    print("Los sensores de " + contaminants[b] + " indican:")
    for k in pollution:
        print (k + ": " + pollution[k][contaminants[b]] + uds(contaminants[b]))
    ending()
#fields of interest
contaminants = []
stations = []
pollution = {}

# regex utils
preStat ="<td class=\"primertd\" headers=\"Estación\">"
postStat= "</td>"
preRow = "<td headers=\""
postRow = "</td>"
preCont ="<th style=\"width:45px\" id=\""
postCont ="\">"

# urls
# url_madrid = "http://www.mambiente.madrid.es/opencms/opencms/calaire/consulta/Gases_y_particulas/informegaseshorarios.html?__locale=es"
url_madrid2 = "http://www.mambiente.madrid.es/opencms/opencms/calaire/consulta/Gases_y_particulas/informegaseshorarios_antiguo.html?__locale=es"


# open url in file
opener = urllib.request.FancyURLopener({})
with opener.open(url_madrid2) as f:
    # print(f.read().decode('utf-8'))
    lines = f.read().decode('utf8').splitlines()
f.close()

# search for stations and contamintants available
for line in lines:
    q = re.findall('(?<=' + preCont + ').*?(?=' + postCont + ')', line)
    if(q != []):
        contaminants.append(q[0])
    q = re.findall('(?<=' + preStat + ').*?(?=' + postStat + ')', line)   
    if(q != [] and q[0] != '&nbsp;' ):
        stations.append(q[0])
        # pollution[q[0]]=[]
        pollution[q[0]]={}

# let's go find the pollution
i=0
j=0
o=True
while(o):
    q = re.findall('(?<=' + preStat + str(stations[i]) + postStat + ').*?(?=' +  ')', lines[j])
    if(q != [] and q[0] != '&nbsp;'):
        j+=2
        l=0
        for k in range(15): # 15
            j+=1
            s = re.findall('(?<=' + preRow + contaminants[l] + '\">' + ').*?(?=' + postRow +  ')', lines[j])
            if(s!=[]):
                #pollution[stations[i]].append({contaminants[l] : s[0]})
                pollution[stations[i]][contaminants[l]] = s[0]
                l+=1
        #o=False
        i+=1
    j+=1
    if(j>600): o = False


#pintar()
# main interaction:
def main():
    o = True
    while(o):
        
        print("Web scraper application for gathering data about pollution in Madrid")
        print("Data by stations[1], contaminant[2], or both [3]")
        print ("Quit[Q]")
        k = input(">")
        if k=='q' or k =='Q':
            o = False
        else:
            switch(int(k))
        print("\n")
main()
