from urllib.request import urlopen
import re

# display function
def pintar():
    for e in cont:
        print(e + "\n")
    print("\n")
    print(len(cont) )

def final_display():
    for i, elem in enumerate(motivos):
        print (str(elem) + " en " + carretera +  " a la altura de los kilómetros " + str(kms[i]) + " en el sentido " + str(sentido[i]))

# fields of interest
motivos =[]
kms = []
sentido = []
cont = []

# regex utils
preString = "<span style=\"margin-top:10px; float:left; clear:both\"> <b>"
postString ="</b></span>"
spanStart = "<span style=\"margin-top:10px; float:left; clear:both\"> <b>"
spanEnd = "</b>"
regx_start = '(?<='
regex_mid = ').*?(?='



# urls
url_madrid = "http://infocar.dgt.es/etraffic/Incidencias?filtroHoraIni=null&filtroHoraFin=null&caracter=acontecimiento&orden=carr_nombre%20ASC&provIci=28&ca=13&IncidenciasRETENCION=IncidenciasRETENCION&IncidenciasPUERTOS=IncidenciasPUERTOS&IncidenciasMETEOROLOGICA=IncidenciasMETEOROLOGICA&IncidenciasOBRAS=IncidenciasOBRAS&IncidenciasOTROS=IncidenciasOTROS&IncidenciasEVENTOS=IncidenciasEVENTOS&IncidenciasRESTRICCIONES=IncidenciasRESTRICCIONES"

url_esp = "http://infocar.dgt.es/etraffic/Incidencias?ca=&provIci=&caracter=acontecimiento&accion_consultar=Consultar&IncidenciasRETENCION=IncidenciasRETENCION&IncidenciasOBRAS=IncidenciasOBRAS&IncidenciasPUERTOS=IncidenciasPUERTOS&IncidenciasMETEOROLOGICA=IncidenciasMETEOROLOGICA&IncidenciasEVENTOS=IncidenciasEVENTOS&IncidenciasOTROS=IncidenciasOTROS&IncidenciasRESTRICCIONES=IncidenciasRESTRICCIONES&ordenacion=fechahora_ini-DESC"

# prompt
carretera = input("Inserte carretera en mayúsculas: ")
x = input ("¿En Madrid [1] o España [2]?")
# abrimos url en fichero f
if(x==1):
    f = urlopen(url_madrid)
else:
    f = urlopen(url_esp)

# leemos la pagina y la decodificamos en utf-8 dentro de string y lo separamos por lineas
# s = f.read().decode('utf-8')
# lines = s.splitlines()
lines = f.read().decode('utf-8').splitlines()

# cerramos fichero
f.close()

# comienzo del procesamiento, extraer lineas con M-40
for line in lines:
    if(re.findall(carretera, line)!=[]):
        cont.append(line)


# eliminar contenido superfluo (lineas superfluas)
for i, elem in enumerate(cont):
    c = re.findall('(?<=' + preString + ').*?(?=' + postString + ')', elem)
    if(c == []):
        cont.pop(i)

# rellenamos los campos de interes en orden
for i, elem in enumerate(cont):
    c = re.findall('(?<='+ spanStart +').*?(?=' + spanEnd + ')', elem)
    motivos.append(c)
   #  print(c) 
    d = re.findall(regx_start + "<b> km" + regex_mid + "</b>" + ')', elem)
    kms.append(d)
    e = re.findall(regx_start + "sentido <b>" + regex_mid + "</b>" + ')', elem)
    sentido.append(e)

final_display()


# s = f.read().decode('utf-8')

# c = re.findall('- La AUTOPISTA / AUTOVÍA <b> <span style="color:#ab3000">M-40 </span> </b>(?s)(.*)</b></span>', s)
# c = re.findall('(?<=- La AUTOPISTA / AUTOVÍA <b> <span style="color:#ab3000">M-40 </span> </b>).*?(CIRCULACIÓN</b></span)',s) # </b></span>)', s)
# for i in c:
#    print(i + "\n\n\n")

    # for i in range(len(elements)):
    #    elem = elements[i]
    # better do this:
    # for i, elem in enumerate(elements) ::: con indices
    # for i, elem in enumerate(elements, 10)
