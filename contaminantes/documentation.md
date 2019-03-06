# botaminantes

Botaminantes is a python webscraper that can be used to show the last data about pollution in Madrid in the very last hour. A user can filter the information gather by:
- Name of the station
- Name of the contaminant available
- Both

## Dependencies

The only imports in python are:  
- urllib.request  
- urllib.parse  
- re  

Python 3 is needed for running the program. A calling example:
```python
python3 agente.py
```
Any other input is handled by the program.

## Implementation

The architecture of the program is divided in functions, keeping the idea of making something scalable in mind. Thus, every filter is separated in functions in order to iterate between them if the user wants to.

### The main method:
```python
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


def switch(n):
    if n == 3:
        station_contaminant()
    elif n ==1:
        stations_()
    elif n ==2:
	cont_()
```
It is very clear that the main interaction lives in the switch function. Here we the 3 different options that our user can follow.

But before the interaction with the user, the program has already the data needed and structured in a dictionary called *pollution*.

### The data gathering

- First, we declare the containers for further use:  
```python
#fields of interest
contaminants = []
stations = []
pollution = {}
```

- As we use regex, we will need some strings which I have encapsulated in a few variables (we only use 1 regex and we could have compiled it but we did not). The following are strings for search the data of interest in the web page.
```python
# regex utils
preStat ="<td class=\"primertd\" headers=\"Estación\">"
postStat= "</td>"
preRow = "<td headers=\""
postRow = "</td>"
preCont ="<th style=\"width:45px\" id=\""
postCont ="\">"
```
- The url to wich make the request. There is one commented because that was the first attempt, the second is final and contains less bloated information.
```python
# urls
# url_madrid = "http://www.mambiente.madrid.es/opencms/opencms/calaire/consulta/Gases_y_particulas/informegaseshorarios.html?__locale=es"
url_madrid2 = "http://www.mambiente.madrid.es/opencms/opencms/calaire/consulta/Gases_y_particulas/informegaseshorarios_antiguo.html?__locale=es"
```

- Next thing we do is to open the url in a file.
``` python
# open url in file
opener = urllib.request.FancyURLopener({})
with opener.open(url_madrid2) as f:
    # print(f.read().decode('utf-8'))
    lines = f.read().decode('utf8').splitlines()
f.close()
```
At this point we won't need more url requests.

- Now we search the stations and contaminants available in order to create at every execution the data vacant dynamically. This means that if in a recent future, new stations with sensors or new sensors to identify new contaminants are included, our program will identify it as well without any change in the code.
```python
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
```

- Finally we only need to fill the **pollution** dictionary so we can acces to the information more efficiently.
```python
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
```
The final if is because we do not need to cover all the lines to gather the information. If we would want to prepare this program for the future updates we should include a function (depending on the lines and the parameters previously identified) instead of a constant number (600).

The regex used simply obtains every string between two given.

### Very narrow modular filters

Corresponding with the three main interactions:

1. By stations:
```python
def stations_():    
    print("\n")
    print("Datos por estación")
    a = input_station()
    pol = pollution[stations[a]]
    begining()
    for k in pol:
        print(k + " " + pol[k] + uds(k))
ending()
```

2. By contaminant:
```python
def cont_():
    print("\n")
    print("Datos un contaminante para todas las estaciones disponibles")
    b = input_cont()
    begining()
    print("Los sensores de " + contaminants[b] + " indican:")
    for k in pollution:
        print (k + ": " + pollution[k][contaminants[b]] + uds(contaminants[b]))
ending()
```

3. Both:
```python
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
```
## Usage
The program is endowed with a simple command line interface to guide the user. If any problem is identified, please consider contact with the developer.
