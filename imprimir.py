#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 03:42:07 2017

@author: clebson
"""
import os
import pandas as pd
import arquivos as arq
import caracteristica as crt
import prepara as pp
import plotly as py
import plotly.figure_factory as FF
import cufflinks as cf

class Graficos(pp.Prepara):
    def __init__(self, dados, nPosto=None):
        self.dados = dados
        self.nPosto = nPosto
        
    def plotlyCredenciais(self, username, apiKey):
        py.tools.set_credentials_file(username=username, api_key= apiKey)
        py.tools.set_config_file(world_readable=True, sharing='public')
    
    def plotGantt(self):
        dfGantt = self.gantt(self.dados)
        fig = FF.create_gantt(dfGantt, index_col='IndexCol', colors = ['#000000', '#858585'], group_tasks=True, bar_width=0.475)
        py.offline.plot(fig, filename='DiagramadeGantt.html')
    
    def plotHidroPorAno(self, mesIniAno = (1, 'JAN')):
        dfg = self.grupoAnoHidro(self.dados, mesIniAno)
        fig = dfg.iplot(kind='scatter', asFigure=True)
        py.offline.plot(fig, filename='GraficoAnual'+self.nPosto+'.html')
    
    def plotHidro(self):
        if self.nPosto == None:
            fig = self.dados.iplot(kind='scatter', asFigure=True)
        else:
            fig = self.dados[self.nPosto].iplot(kind='scatter', asFigure=True)
        
        py.offline.plot(fig, filename='hidrograma'+'.html')

class Arquivo():
    def __init__(self, df):
        self.df = df
        
    def excel(self, nomeArquivo):
        writer = pd.ExcelWriter('%s.xlsx' % nomeArquivo)
        self.df.to_excel(writer)
        writer.save()
    
    def json(self, nomeArquivo):
        self.df.to_json('%s.json' % nomeArquivo)
        
class Mapas(pp.Prepara):
    def __init__(self, df):
        self.dados = df
    
    def precipitacao(self):
        dad = self.mapaPrecipitacao()
        print(dad)