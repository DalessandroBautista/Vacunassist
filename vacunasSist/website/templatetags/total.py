from django import template
from website.models import Vacuna, Vacunatorio
register = template.Library()

@register.filter
def total(arr):
    vacunas = Vacuna.objects.all()
    vacunatorios = Vacunatorio.objects.all()
    total = len(vacunas)+len(vacunatorios)+1
    datosGenerales = [0]*total
    datosFinal = []
    datosFinal.append("El total de vacunados en todos los vacunatorios es de ")
    datosFinal.append(0)
    print("")
    datosGenerales[len(datosGenerales)-1]= datosFinal

    #datosGenerales[len(datosGenerales)-1] = 0
    for i,vacunatorio in enumerate(arr):
        datosLocales = []
        datosLocales.append("Total de vacunados en el "+vacunatorio[0])
        datosLocales.append(0)
        #datosGenerales.insert(i,datosLocales)
        datosGenerales[i]=datosLocales
        for j,vacuna in enumerate(vacunatorio[1]):
            if(datosGenerales[j+len(vacunatorios)] == 0):
                datosVacuna = []
                datosVacuna.append("Total de vacunados por "+ vacuna[0])
                datosVacuna.append(vacuna[1])
                #datosGenerales.insert((j+len(vacunatorios)),datosVacuna)
                datosGenerales[j+len(vacunatorios)]=datosVacuna
            else:
                print(datosGenerales[j+len(vacunatorios)][1] + vacuna[1])
                datosGenerales[j+len(vacunatorios)][1] = datosGenerales[j+len(vacunatorios)][1] + vacuna[1]
            datosGenerales[i][1] = datosGenerales[i][1]+vacuna[1]    
        datosGenerales[len(datosGenerales)-1][1]= datosGenerales[len(datosGenerales)-1][1] + datosGenerales[i][1]  
    
    #print(datosGenerales[0])

    print(len(datosGenerales))
    for dato in datosGenerales:
        print(dato)      
    return datosGenerales