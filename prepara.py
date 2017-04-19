#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 02:05:38 2017

@author: clebson
"""
import pandas as pd
import numpy as np

class Prepara():
    def __init__(self, nPosto):
        self.nPosto = nPosto
    
    def gantt(self, psf):
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        cont = 0
        color = 0
        n = 1
        for j in psf.index:
            df.set_value(index = cont, col = 'Task', value = self.nPosto)
            df.set_value(index = cont, col = 'Description', value = self.nPosto + ' - %s' % j)
            df.set_value(index = cont, col = 'IndexCol', value = color)
            df.set_value(index = cont, col = 'Start', value = psf['Inicio'].loc[j])
            df.set_value(index = cont, col = 'Finish', value = psf['Fim'].loc[j])
            cont += 1
            color += (100*n)
            n *= -1
        return df
    
    
    def grupoAnoHidro(self, dados, mesHidro):
        grupos = dados[self.nPosto].groupby(pd.Grouper(freq='AS-%s' % mesHidro[1]))
        #frameGrafico = pd.DataFrame()
        lista = []
        for key, dado in grupos:
            aux = dado.values.T
            index = dado.index
            indexN = [pd.to_datetime('%s/%s/%s' % (i.month, i.day, 1999)) if i.month >= mesHidro[0] else pd.to_datetime('%s/%s/%s' % (i.month, i.day, 2000)) for i in index]
            serie = pd.Series(aux, index=indexN, name=key.year)
            lista.append(serie)
        frameGrafico = pd.DataFrame(lista)
        #frameGrafico.drop_duplicates(keep='last', inplace=True)
        return frameGrafico.T