#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 02:05:38 2017

@author: clebson
"""
import pandas as pd

class Prepara():
    
    def gantt(self, psf, nPosto):
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        cont = 0
        color = 0
        n = 1
        for j in psf.index:
            df.set_value(index = cont, col = 'Task', value = nPosto)
            df.set_value(index = cont, col = 'Description', value = nPosto + ' - %s' % j)
            df.set_value(index = cont, col = 'IndexCol', value = color)
            df.set_value(index = cont, col = 'Start', value = psf['Inicio'].loc[j])
            df.set_value(index = cont, col = 'Finish', value = psf['Fim'].loc[j])
            cont += 1
            color += (100*n)
            n *= -1
        return df
    
    def maximaAnual(self, grupos):
        vazaoMax = []
        dataMax = []
        for data, dado in grupos:
            vazaoMax.append(dado.values.max())
            dataMax.append(dado.idxmax()[0])
        maxAnualSerie = pd.Series(vazaoMax, dataMax)
        return maxAnualSerie
    
    def grupoAnoHidro(self, dados, mesHidroAbr):
        grupos = dados.groupby(pd.Grouper(freq='AS-%s' % mesHidroAbr))
        frameGrafico = pd.DataFrame()
        for key, dado in grupos:
            aux = dado.values.T[0]
            index = dado.index
            indexN = ['%s/%02d' % (i.month, i.day) for i in index]
            serie = pd.Series(aux, index=indexN, name=key.year)
            frameAux = pd.DataFrame(serie)
            frameGrafico = self.combinaDateFrame(frameGrafico, frameAux)
        frameGrafico.drop_duplicates(keep='last', inplace=True)
        return grupos, frameGrafico