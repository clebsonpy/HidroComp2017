#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 03:42:07 2017

@author: clebson
"""
import numpy as np
import pandas as pd
import arquivos as arq
import caracteristica as crt
import prepara as pp
import plotly as py
import plotly.graph_objs as go
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
        
    def plotHidroParcial(self, dfPicos, quartilLimiar, nomeGrafico):
        limiar = self.dados[self.nPosto].quantile(quartilLimiar)
        print(limiar)
        if self.nPosto == None:
            return 'Erro! forneça o n° do Posto'
        else:
            traceHidro = go.Scatter(x=self.dados.index,
                y=self.dados[self.nPosto],
                name = self.nPosto,
                line = dict(color = '#17BECF'),
                opacity = 1)
            traceLimiar = go.Scatter(x=self.dados.index,
                y=[limiar]*len(self.dados),
                name = "Limiar",
                line = dict(color = '#858585'),
                opacity = 1)
            pointInicio = go.Scatter(x=dfPicos.Inicio,
                y=self.dados[self.nPosto].loc[dfPicos.Inicio],
                name = "Inicio do Evento",
                mode='markers',
                marker=dict(color='#835AF1'),
                opacity = 0.8)
            pointFim = go.Scatter(x=dfPicos.Fim,
                y=self.dados[self.nPosto].loc[dfPicos.Fim],
                name = "Fim do Evento",
                mode='markers',
                marker=dict(color='#FF0000'),
                opacity = 0.8)
            data = [traceHidro, traceLimiar, pointInicio, pointFim]
            layout = dict(
                title = "Parcial")
            fig = dict(data=data, layout=layout)        
        py.offline.plot(fig, filename='gráficos\%s' % nomeGrafico + '.html')
    
    def plotHidroPorAno(self, mesIniAno = (1, 'JAN')):
        dfg = self.grupoAnoHidro(mesIniAno)
        
        y = []
        for i in dfg:
            y.append(dfg[i].values)
        
        traceHidro = go.Data[go.Scatter(
            y=y,
            name = i,
            opacity = 1,
            marker=go.Marker(
                    color= dfg.columns,
                    colorbar=go.ColorBar(
                        title='Colorbar'
                    ),
                    colorscale='Viridis'
            ))]
        
        bandxaxis = go.XAxis(
            tickformat = "%b",
            )
        
        layout = dict(
                title = "Hidrograma Ano",
                xaxis=bandxaxis)
            
        fig = dict(data=traceHidro, layout=layout)
        py.offline.plot(fig, filename='gráficos\GraficoAnual'+self.nPosto+'.html')
    
    def plotHidro(self):
        if self.nPosto == None:
            fig = self.dados.iplot(kind='scatter', asFigure=True)
        else:
            fig = self.dados[self.nPosto].iplot(kind='scatter', asFigure=True)
        
        py.offline.plot(fig, filename='gráficos\hidrograma'+'.html')

class Arquivo():
    def __init__(self, df):
        self.df = df
        
    def excel(self, nomeArquivo):
        writer = pd.ExcelWriter('%s.xlsx' % nomeArquivo)
        self.df.to_excel(writer)
        writer.save()
        
    def csv(self, nomeArquivo):
        self.df.to_csv('%s.csv' % nomeArquivo)
    
    def json(self, nomeArquivo):
        self.df.to_json('%s.json' % nomeArquivo)
        
class Mapas(pp.Prepara):
    def __init__(self, df):
        self.dados = df
    
    def precipitacao(self):
        data = [dict(
            type='scattergeo',
            lon=[],
            lat=[],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.8,
                reversescale=True,
                autocolorscale=False,
                line=dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
            ),
            stream=stream_id,
            name="Plane")]
        
        layout = dict(
            title = 'Busy Airplane Streaming',
            colorbar = False,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5),)
        
        fig = dict( data=data, layout=layout )
        py.iplot( fig, validate=False, filename='geo-streaming2', auto_open=False, fileopt='extend')