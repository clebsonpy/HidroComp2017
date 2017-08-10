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
    
    def plotDuraçãoPulso(self, eventos, tipo):
        rateQ = go.Scatter(x=eventos.Ano,
                y=eventos.Duracao,
                mode='markers+lines',
                marker=dict(color='red',
                             size = 3),
                opacity = 1)
        data = [rateQ]
        bandxaxis = go.XAxis(
                title = "Anos",
                )
        bandyaxis = go.YAxis(
                title = "Duração Média",
                )
        layout = dict(
            title = "Duração Média de Eventos de %s" % tipo.title(),
            xaxis = bandxaxis,
            yaxis = bandyaxis)
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos//Duracao' + tipo + '.html')
    
    def plotNPulsos(self, eventos, tipo):
        rateQ = go.Scatter(x=eventos.Ano,
                y=eventos.nPulsos,
                mode='markers+lines',
                marker=dict(color='red',
                             size = 3),
                opacity = 1)
        data = [rateQ]
        bandxaxis = go.XAxis(
                title = "Anos",
                )
        bandyaxis = go.YAxis(
                title = "N° de Pulsos",
                )
        layout = dict(
            title = "Número de Pulsos de %s" % tipo,
            xaxis = bandxaxis,
            yaxis = bandyaxis)
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos//NPulsos' + tipo + '.html')
    
    def plotReversoes(self, dfRise, dfFall):
        rateQ = go.Scatter(x=dfRise.Ano,
                y=dfRise["rise"] + dfFall["fall"],
                mode='markers+lines',
                marker=dict(color='red',
                             size = 3),
                opacity = 1)
        data = [rateQ]
        bandxaxis = go.XAxis(
                title = "Anos",
                )
        bandyaxis = go.YAxis(
                title = "N° Reversões",
                )
        layout = dict(
            title = "Número de reversões anuais de vazões",
            xaxis = bandxaxis,
            yaxis = bandyaxis)
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos//reversões' + '.html')
    
    def plotRate(self, dfRate, typeRate):
        
        rateQ = go.Scatter(x=dfRate.Ano,
                y=dfRate["Media"],
                mode='markers+lines',
                marker=dict(color='red',
                             size = 3),
                opacity = 1)
        data = [rateQ]
        bandxaxis = go.XAxis(
                title = "Anos",
                )
        bandyaxis = go.YAxis(
                title = "Taxa Média (m³/s)",
                )
        layout = dict(
            title = "Taxa de %s de vazão" % typeRate.title(),
            xaxis = bandxaxis,
            yaxis = bandyaxis)
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos//%s' % typeRate + '.html')
        
    def plotHidroParcial(self, dfPicos, quartilLimiar, nomeGrafico):
        limiar = self.dados[self.nPosto].quantile(quartilLimiar)
        median = self.dados[self.nPosto].median()
        
        print(limiar)
        if self.nPosto == None:
            return 'Erro! forneça o n° do Posto'
        else:
            traceHidro = go.Scatter(x=self.dados.index,
                y=self.dados[self.nPosto],
                name = self.nPosto,
                line = dict(color = '#17BECF',
                            width = 1),
                opacity = 1)
            traceLimiar = go.Scatter(x=self.dados.index,
                y=[limiar]*len(self.dados),
                name = "Limiar",
                line = dict(color = '#858585',
                             width = 1),
                opacity = 1)
            traceMedian = go.Scatter(x=self.dados.index,
                y=[median]*len(self.dados),
                name = "Mediana",
                line = dict(color = 'yellow',
                             width = 1),
                opacity = 1)
            pointInicio = go.Scatter(x=dfPicos.Inicio,
                y=self.dados[self.nPosto].loc[dfPicos.Inicio],
                name = "Inicio do Evento",
                mode='markers',
                marker=dict(color='blue',
                             size = 5),
                opacity = 1)
            pointFim = go.Scatter(x=dfPicos.Fim,
                y=self.dados[self.nPosto].loc[dfPicos.Fim],
                name = "Fim do Evento",
                mode='markers',
                marker=dict(color='red',
                             size = 5),
                opacity = 1)
            data = [traceHidro, traceLimiar, traceMedian, pointInicio, pointFim]
            layout = dict(
                title = "Hidrograma Início e Fim de Eventos (%s)" % nomeGrafico.title())
            fig = dict(data=data, layout=layout)        
        py.offline.plot(fig, filename='gráficos\%s' % nomeGrafico + '.html')
    
        
    def plotHidroPorAno(self, mesIniAno = (1, 'JAN')):
        df = self.grupoAnoHidro(mesIniAno)
        
        z = []
        y = []
        x = []
        for i in df:
            for j in df[i].index:
                y.append(df[i][j])
                z.append(int(i))
                x.append(j)
                    
        trace1 = go.Scatter(
            x = x,
            y = y,
            mode='markers',
            marker=dict(
                size='3',
                color = z, #set color equal to a variable
                colorscale='Jet',
                showscale=True,
            ),
            
        )
        data = [trace1]
        bandxaxis = go.XAxis(
            title = "Mês",
            tickformat = "%b",
            )
        
        bandyaxis = go.YAxis(
            title = "Vazão(m³/s)",
            )
        
        layout = dict(
                title = "Hidrograma",
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                width=800, height=640,
                autosize = False)
        
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos\Hidrograma_Ano_%s' % self.nPosto + ".html")
    
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