#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 02:05:38 2017

@author: clebson
"""
import pandas as pd
import numpy as np
import calendar
import datetime
import caracteristica as crct

class Prepara():
    def __init__(self, dados, nPosto = None):
        self.dados = dados
        self.nPosto = nPosto
    
    def gantt(self):
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        cont = 0
        for i in self.dados:
            color = 0
            n = 1
            psf = crct.Caracteristicas(self.dados, i).periodoSemFalhas()
            for j in psf.index:
                df.set_value(index = cont, col = 'Task', value = i)
                df.set_value(index = cont, col = 'Description', value = i + ' - %s' % j)
                df.set_value(index = cont, col = 'IndexCol', value = color)
                df.set_value(index = cont, col = 'Start', value = psf['Inicio'].loc[j])
                df.set_value(index = cont, col = 'Finish', value = psf['Fim'].loc[j])
                cont += 1
                color += (100*n)
                n *= -1
        return df
    
    def julin(self, ano, dayJ):
        diasMes = calendar.monthrange(ano, 2)[1]
        if diasMes == 29:
            data = datetime.datetime.strptime('2000%s' % dayJ, '%Y%j')
        elif diasMes == 28:
            if dayJ > 59:
                data = datetime.datetime.strptime('2000%s' %(dayJ+1), '%Y%j')
            else:
                data = datetime.datetime.strptime('2000%s' % dayJ, '%Y%j')
        return data
        
    def anualMaxPolar(self, dfMaxAnual):
        dataJulian = list(map(int, pd.DatetimeIndex(dfMaxAnual.index.values).strftime("%j")))
        dataJulInt = [i for i in dataJulian]
        dfMaxAnual['DataJ'] = dataJulInt
        data = []
        for i in dfMaxAnual.index:
            data.append(self.julin(i.year, dfMaxAnual.DataJ.loc[i]))
        dfMaxAnual['Data'] = data
        index = pd.date_range('2000-1-1', '2000-12-31')
        df = pd.DataFrame(index = index)
        df['XINGO'] = None
        for i in dfMaxAnual.index:
            df['XINGO'][dfMaxAnual.Data.loc[i]] = dfMaxAnual.XINGO.loc[i]
        return df
    
    def periodsSpells(self, picos, mesHidro):
        df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
        cont = 0
        for i in picos.index:
            df.set_value(index = cont, col = 'Task', value = picos['Ano'].loc[i])
            df.set_value(index = cont, col = 'Description', value = '%s - %s' % (picos['Ano'].loc[i], cont))
            df.set_value(index = cont, col = 'IndexCol', value = 0)
            inicio = picos['Inicio'].loc[i]
            fim = picos['Fim'].loc[i]
            dataInicio =  pd.to_datetime('%s/%s/%s' % (inicio.month, inicio.day, 1999)) if inicio.month >= mesHidro[0] else pd.to_datetime('%s/%s/%s' % (inicio.month, inicio.day, 2000))
            dataFim = pd.to_datetime('%s/%s/%s' % (fim.month, fim.day, 1999)) if fim.month >= mesHidro[0] else pd.to_datetime('%s/%s/%s' % (fim.month, fim.day, 2000))
            df.set_value(index = cont, col = 'Start', value = dataInicio)
            df.set_value(index = cont, col = 'Finish', value = dataFim)
            cont += 1
        return df
    
    def grupoAnoHidro(self, mesHidro):
        grupos = self.dados[self.nPosto].groupby(pd.Grouper(freq='AS-%s' % mesHidro[1]))
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
    
    def mapaPrecipitacao(self):
        df = self.dados.groupby(pd.Grouper(freq='A')).sum().to_period().T
        dics = {'Lon':[], 'Lat':[]}
        for i in df.index:
            dics['Lat'].append(float(i[0]))
            dics['Lon'].append(float(i[1]))
        
        df2 = pd.DataFrame(dics)
        df2 = df2.combine_first(pd.DataFrame(pd.Series(df['2016'].values, name='2016')))
        
        return df2