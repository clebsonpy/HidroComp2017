#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import calendar as cal
import arquivoTxt as arq
import os

#Ano hidrlogico
def mesInicioAnoHidrologico(dados):
    grupoMesAno = dados.groupby(pd.Grouper(freq='M')).mean().to_period()
    indexMult = list(zip(*[grupoMesAno.index.month, grupoMesAno.index.year]))
    indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Ano"])
    grupoMesAno.set_index(indexN, inplace=True)
    grupoMesMedia = grupoMesAno.groupby(level='Mes').mean()
    mesHidro = grupoMesMedia.idxmin().values
    mesHidroAbr = cal.month_abbr[mesHidro[0]].upper()
    return mesHidro[0], mesHidroAbr

#Periodos sem falhas
def periodoSemFalhas(ganttBool):
    aux = []
    listaInicio = []
    listaFim = []
    for i in ganttBool.index:
        if ~ganttBool.loc[i].values:
            aux.append(i)
        elif len(aux) > 2 and ganttBool.loc[i].values:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
            aux = []
            
    if len(aux) > 0:
        listaInicio.append(aux[0])
        listaFim.append(aux[-1])
    dic = {'Inicio': listaInicio, 'Fim': listaFim}
    return pd.DataFrame(dic)

def falhas(dadosVazao):
    dadosVazao.sort_index(inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    ganttMes = dadosVazao.isnull().groupby(pd.Grouper(freq = 'M')).sum()
    ganttBool = dadosVazao.isnull()
    #ganttBool.drop_duplicates(keep='last', inplace=True)
    for i in ganttMes.index:
        if ganttMes.loc[i].isnull().all():
            ganttMes.set_value(index = i, col = ganttMes.axes[1], value = i.day)
    return nFalhas, ganttBool, ganttMes.to_period()

if __name__ == "__main__":
    caminho = os.getcwd()
    dados = arq.separaDadosConsisBruto(arq.trabaLinhas(caminho, '49370000'), tipo=2)
    nfalhas, ganttBool, ganttMes = falhas(dados)
    periodos = periodoSemFalhas(ganttBool)