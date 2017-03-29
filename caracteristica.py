#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import calendar as cal

class Caracteristicas():
    def __init__(self, dadosVazao, nPosto):
        self.dadosVazao = dadosVazao
        self.nPosto = nPosto
    #Ano hidrlogico
    def mesInicioAnoHidrologico(self):
        grupoMesAno = self.dadosVazao.groupby(pd.Grouper(freq='M')).mean().to_period()
        indexMult = list(zip(*[grupoMesAno.index.month, grupoMesAno.index.year]))
        indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Ano"])
        grupoMesAno.set_index(indexN, inplace=True)
        grupoMesMedia = grupoMesAno[self.nPosto].groupby(level='Mes').mean()
        mesHidro = grupoMesMedia.idxmin()
        mesHidroAbr = cal.month_abbr[mesHidro]
        return mesHidro, mesHidroAbr.upper()
    
    #Periodos sem falhas
    def periodoSemFalhas(self):
        aux = []
        listaInicio = []
        listaFim = []
        ganttBool = self.falhas()[1][self.nPosto]
        for i in ganttBool.index:
            if ~ganttBool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and ganttBool.loc[i]:
                listaInicio.append(aux[0])
                listaFim.append(aux[-1])
                aux = []
                
        if len(aux) > 0:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
        dic = {'Inicio': listaInicio, 'Fim': listaFim}
        return pd.DataFrame(dic)
    
    def falhas(self):
        self.dadosVazao.sort_index(inplace=True)
        nFalhas = self.dadosVazao.isnull().sum()
        ganttMes = self.dadosVazao.isnull().groupby(pd.Grouper(freq = 'M')).sum()
        ganttBool = self.dadosVazao.isnull()
        #ganttBool.drop_duplicates(keep='last', inplace=True)
        for i in ganttMes.index:
            if ganttMes.loc[i].isnull().all():
                ganttMes.set_value(index = i, col = ganttMes.axes[1], value = i.day)
        return nFalhas, ganttBool, ganttMes.to_period()