#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 03:42:07 2017

@author: clebson
"""
import pandas as pd
import arquivoTxt as arq
import caracteristica as crt
import prepara as pre
import os

def plotlyCredenciais(username, apiKey):
    import plotly.tools as tls
    tls.set_credentials_file(username=username, api_key= apiKey)
    tls.set_config_file(world_readable=True, sharing='public')

def plotGantt(dfGantt, filename):
    import plotly.figure_factory as FF
    import plotly.offline as off
    fig = FF.create_gantt(dfGantt, index_col='IndexCol', colors = ['#000000', '#858585'], group_tasks=True, bar_width=0.475)
    off.plot(fig, filename=filename)

if __name__ == "__main__":
    
    caminho = os.getcwd()
    dadosVazao = arq.separaDadosConsisBruto(arq.trabaLinhas(caminho, '49370000'), tipo=2)
    nFalhas, ganttBool, ganttMes = crt.falhas(dadosVazao)
    periodos = crt.periodoSemFalhas(ganttBool)
    dfGantt = pre.gantt(periodos, '49370000')
    plotGantt(dfGantt, filename='ganttChart')
   