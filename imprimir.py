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
import matplotlib
from matplotlib import pyplot as plt

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

class Graficos(pp.Prepara):
    def __init__(self, dados, nPosto=None):
        self.dados = dados
        self.nPosto = nPosto

    def plotlyCredenciais(self, username = 'clebsonpy', apiKey = 'qBKNP6BAO2mmPsaOTGq8'):
        py.tools.set_credentials_file(username=username, api_key= apiKey)
        py.tools.set_config_file(world_readable=True, sharing='public')

    def plotPolar(self, dfPolar):
        dicMes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set",
                  "Out", "Nov", "Dez"]
        dicNone = [None, None, None, None, None, None, None, None, None, None, None, None]

        print(dfPolar)
        trace = go.Scatter(
            r=dfPolar[self.nPosto], #Vazao
            t=dfPolar.index, #Data
            mode='markers',
            name='Trial 1',
            marker=dict(
                color='rgb(27,158,119)',
                size=110,
                line=dict(
                    color='white'
                ),
                opacity=0.7
            )
        )
        data = [trace]
        angularX = go.AngularAxis(
                tickformat = '%b'
                )
        layout = go.Layout(
            angularaxis = angularX,
            title='',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            orientation=270,

        )

        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig, filename='polar-area-chart')

    def plotGantt(self, dfGantt, tipo=None):
        fig = FF.create_gantt(dfGantt, colors = '#000000', group_tasks=True, title= "Eventos de Cheias")
        if tipo == 'spells':
            fig['layout']['xaxis']['tickformat'] = '%b'
            fig['layout']['xaxis']['type'] =  "date"
            fig['layout']['xaxis']['showgrid'] = True
            fig['layout']['xaxis']['range'] = ['9/1/1999', '8/31/2000']
            fig['layout']['xaxis']['tick0'] = pd.to_datetime('9/1/1999')
            fig['layout']['xaxis']['ticklen'] = pd.to_datetime('8/31/2000')
            fig['layout']['xaxis']['autorange'] = False
            fig['layout']['xaxis']['autotick'] = False
            fig['layout']['xaxis']['dtick'] = "M1"
            fig['layout']['xaxis']['title'] = 'Mês'
            fig['layout']['yaxis']['title'] = 'Anos'
            return py.offline.plot(fig, filename='gráficos/floodSpells.html')

        return py.offline.plot(fig, filename='gráficos/gantt.html')

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
            yaxis = bandyaxis,
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/Duracao' + tipo + '.html')

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
            yaxis = bandyaxis,
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/NPulsos' + tipo + '.html')

    def plotReversoes(self, dfRise, dfFall):
        r = dfRise["Soma"] + dfFall["Soma"]
        rMed = r.mean()
        rCv = r.std()/rMed
        print(r)
        rateQ = go.Scatter(x=dfRise.Ano,
                y=dfRise["Soma"] + dfFall["Soma"],
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
            yaxis = bandyaxis,
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/reversões' + '.html')
        return r, rMed, rCv

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
            yaxis = bandyaxis,
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/%s' % typeRate + '.html')

    def plotHidroParcial(self, dfPicos, limiar, nomeGrafico):
        #limiar = self.dados[self.nPosto].quantile(limiar)
        median = self.dados[self.nPosto].median()
        #mean = self.dados[self.nPosto].mean()

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
            """traceMedian = go.Scatter(x=self.dados.index,
                y=[median]*len(self.dados),
                name = "Mediana",
                line = dict(color = 'red',
                             width = 1),
                opacity = 1)"""
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
            pointVazao = go.Scatter(x=dfPicos.index,
                y=self.dados[self.nPosto].loc[dfPicos.index],
                name = "Pico",
                mode='markers',
                marker=dict(color='green',
                             size = 5),
                opacity = 1)

            data = [traceHidro, traceLimiar, pointInicio,
                    pointFim, pointVazao]
            bandxaxis = go.XAxis(
                    title = "Anos",
            )

            bandyaxis = go.YAxis(
                    title = "Vazão(m³/s)",
            )
            layout = dict(
                title = "Hidrograma Série Duração Parcial (%s)" % nomeGrafico.title(),
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                font=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
            )
            fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/%s' % nomeGrafico + '.html')

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
            mode = "markers",
            marker=dict(
                size = 3,
                color = z,
                colorscale='Jet',
                showscale=True,
                colorbar=dict(
                title=""
            )
        ),)

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
            width=1050, height=840,
            autosize = False,
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))

        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/Hidrograma_Ano_%s' % self.nPosto + ".html")

    def plotHidro(self):
        bandxaxis = go.XAxis(
            title="Data",
        )

        bandyaxis = go.YAxis(
            title="Vazão(m³/s)",
        )

        layout = dict(
            title="Hidrograma",
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            font=dict(family='Courier New, monospace', size=22, color='#7f7f7f'))

        if self.nPosto == None:
            fig = self.dados.iplot(kind='scatter', asFigure=True, layout=layout)
        else:
            fig = self.dados[self.nPosto].iplot(kind='scatter', asFigure=True,
                                                layout=layout, color='#17BECF')

        py.offline.plot(fig, filename='gráficos/hidrograma'+'.html')

    def plot_distr(self, dados):
        
        data = []
        for i in dados:
            line = go.Scatter(
                x = dados[i],
                y = dados.index,
                name = i
            )
            data.append(line)
            
        bandxaxis = go.XAxis(
            title="Vazão(m³/s)",
        )

        bandyaxis = go.YAxis(
            title="Probabilidade",
        )

        layout = dict(
            title="Generalizada de Pareto",
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            width=840,
            height=672,
            font=dict(family='Courier New, monospace', size=12, color='#7f7f7f'))


        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/genparetoacumulada' + '.html')

    def plot_point(self, dados, coluna, nome_grafico):

        trace1 = go.Scatter(
            x=dados[coluna],
            y=dados.index,
            mode="markers",
            marker=dict(
                size=5,),
        )

        data = [trace1]

        bandxaxis = go.XAxis(
            title="Vazão",
        )

        bandyaxis = go.YAxis(
            title="Autocorrelação",
        )
        layout = dict(
            title="Autocorrelação",
            xaxis=bandxaxis,
            yaxis=bandyaxis,
            font=dict(family='Courier New, monospace', size=16, color='#7f7f7f'))

        fig = dict(data=data, layout=layout)
        py.offline.plot(fig, filename='gráficos/%s' % nome_grafico + '.html')


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
