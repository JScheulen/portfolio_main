from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

import yfinance as yf
import numpy_financial as npf
import pandas as pd
import plotly.express as px

from .forms import calculoCredito, subirArchivo
from .models import Monedas, ProyectImg


# Create your views here.
def calculadora(request):
    if request.method == 'POST':
        form = calculoCredito(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            plazo = form.cleaned_data['plazo']
            tasa = form.cleaned_data['tasa']
            get_number(request, {'monto': monto, 'plazo': plazo, 'tasa': tasa})
            messages.success(request, 'Se ingresaron todos los datos correctamente')
            return get_number(request, {'monto': monto, 'plazo': plazo, 'tasa': tasa})
        else:
            print('no es validdo')
    else:
        form = calculoCredito()

    return render(request, 'calculador.html', {'form': form})

def get_number(request, lista):

    monto = int(lista['monto'])
    plazo = int(lista['plazo'])
    tasa = float(lista['tasa']) / 100
    tasaMes = tasa/12 * 100

    tabla = {'mes':[],'DeudaInicial':[],'pagomes': [], 'deudames': [], 'interesmes': []}
    deuda = monto
    total_interes = 0
    pago_total = 0
    for n in range(1, plazo + 1):
        pagoMes = float(npf.pmt(tasa / 12, plazo, -monto))
        pago_total = f'{pagoMes * plazo: ,.0f}'
        deudaMes = float(npf.ppmt(tasa / 12, n, plazo, -monto))
        interesMes = npf.ipmt(tasa / 12, n, plazo, -monto)

        tabla['DeudaInicial'].append(f'{deuda: ,.0f}')
        tabla['pagomes'].append(f'${pagoMes: ,.0f}')
        tabla['deudames'].append(f'${deudaMes:,.0f}')
        tabla['interesmes'].append(f'${interesMes:,.0f}')
        tabla['mes'].append(n)
        total_interes += interesMes
        deuda += deudaMes

    context = {
        'monto': f'{monto: ,.0f}',
        'plazo': plazo,
        'tasaMes': round(tasaMes,2),
        'tasa': f'{tasa*100}%',
        'pagaMes': tabla['pagomes'][0],
        'totalduda': pago_total,
        'total_interes': f'{round(total_interes, 2): ,.0f}'
    }


    return render(request,'resultado.html', {'result': context, 'tabla': tabla})

def casa(request):

    portfolio = ProyectImg.objects.all()

    proyecto = {}
    for item in portfolio:
        #proyecto[str(item.proyecto)] = [item.imgList]
        if str(item.proyecto) not in proyecto:
            proyecto[str(item.proyecto)] = []

        proyecto[str(item.proyecto)].append(item)

    return render(request, 'home.html', {'context': portfolio, 'nuevo': proyecto})

def currency_c(request):

    dinero = Monedas.objects.all()

    if request.method == 'POST':
        form = subirArchivo(request.POST, request.FILES)
        if form.is_valid():
            return subir_archivo(request, form)

    form = subirArchivo()

    return render(request, 'exchange.html', {'form': form, 'dinero': dinero})

def subir_archivo(request, archivo):
    if request.method == 'POST':
        form = subirArchivo(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            data = pd.read_excel(file)

            for index, row in data.iterrows():
                Monedas.objects.get_or_create(
                    moneda = row['Código ISO'],
                    descripcion = row['Moneda']

                )
            return HttpResponse("Success")

    pass

def tasa_cambio(request):
    amount1 = request.GET.get('amount1', None)
    amount2 = request.GET.get('monto', None)
    if amount1 == '':
        amount2 = 1 * amount2
    else:
        amount2 = float(amount1) * float(amount2)

    if request.method == 'GET':
        #print(amount2)
        return JsonResponse({'amount2': amount2})


    return JsonResponse({'amount2': amount2})

def actualizaPrecios(request):

    todo = [n[0] for n in Monedas.objects.all().values_list('moneda')]
    if request.method == 'GET':
        numero1 = request.GET.get('pais1', None)
        numero2 = request.GET.get('pais2', None)
        par = numero1[:3] + numero2[:3]+'=X'

        calculo = yf.download(par, period='1mo')

        data = pd.DataFrame(calculo)
        fechas = data.index
        fechas = fechas.tolist()
        fechas = [f.strftime('%Y-%m-%d') for f in fechas]
        rangoPrecio = [round(d, 5) for d in data['Close'].tolist()]

        figura = px.line(x=fechas, y=rangoPrecio, title="Rango de Precios")
        grafico = figura.to_html()

        valor_final = data['Close'][-1]

        return JsonResponse({'valor': round(valor_final, 4), 'Datos': grafico})


    return HttpResponse("¡Actualización de precios exitosa!")