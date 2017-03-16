#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 03:42:07 2017

@author: clebson
"""
import os
import arquivoTxt as arq
import caracteristica as crt
import prepara as pre
import plotly.tools as tls
import plotly.figure_factory as FF
import plotly.offline as off

class Graficos():
    
    def plotlyCredenciais(self, username, apiKey):
        tls.set_credentials_file(username=username, api_key= apiKey)
        tls.set_config_file(world_readable=True, sharing='public')
    
    def plotGantt(self, dfGantt, filename):
        fig = FF.create_gantt(dfGantt, index_col='IndexCol', colors = ['#000000', '#858585'], group_tasks=True, bar_width=0.475)
        off.plot(fig, filename=filename+'.html')
    
    def plotHidro(self, dfg, filename):
        off.plot(dfg, filename=filename+'.html')
    
if __name__ == "__main__":

    caminho = os.getcwd()
    dadosVazao = arq.separaDadosConsisBruto(arq.trabaLinhas(caminho, '49370000'), tipo=2)
    nFalhas, ganttBool, ganttMes = crt.Caracteristicas(dadosVazao).falhas()
    periodos = crt.Caracteristicas(dadosVazao).periodoSemFalhas(ganttBool)
    dfGantt = pre.gantt(periodos, '49370000')
    #plotGantt(dfGantt, filename='ganttChart')
    mesHidro, mesHidroAbr = crt.Caracteristicas(dadosVazao).mesInicioAnoHidrologico()
    grupos, dfg = pre.grupoAnoHidro(dadosVazao, mesHidroAbr)
    Graficos().plotGantt(dfGantt, filename='ganttChart')
