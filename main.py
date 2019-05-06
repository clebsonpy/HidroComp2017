#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:00:55 2017

@author: clebson
"""
import os
import timeit

import pandas as pd

import arquivos as arq
import caracteristica as crt
import imprimir as impr
import prepara as pr
import estatistica as stat

if __name__ == "__main__":
    ini = timeit.default_timer()
#    caminho = os.path.join(os.getcwd(), 'Dados_Chuva')
    caminho = "/home/clebsonpy/Vazões"
    dados = arq.Arquivos(caminho, fonte='ANA',
                         tipoDado='fluviométrico').lerArquivos()
#    dados = pd.read_csv("dadosXingo.csv", index_col=0, names=[
#                        "Data", "XINGO"], parse_dates=True)
#    dados = crt.Caracteristicas(dados)
#    autocorr = dados.autocorrelacao_por_vazao(tipoEvento='cheia')
    #maxAnual = dados.maxAnual()
    #print(maxAnual)
#    mesInicioAnoHidro = dados.mesInicioAnoHidrologico()
#    print(mesInicioAnoHidro)
    print(dados)
    pre = pr.Prepara(dados)
    dfgantt = pre.gantt()
#    x = pre.anualMaxPolar(maxAnual)
#    dadosAno = pre.grupoAnoHidro(mesInicioAnoHidro)
#    dfDayJ, dayJ = caract.daysJulian(reducao="Maxima")
#    rateA, riseA = caract.rate(tipo='rise', quartilLimiar=0.75, evento='cheia')
#    rateB, fallB = caract.rate(tipo='fall', quartilLimiar=0.75, evento='cheia')
#    psf = caract.periodoSemFalhas()

#    picos, eventos_por_ano, dM, dCv, pM, pCv, limiar = dados.pulsosDuracao(tipoEvento='cheia')
#    estat = stat.Parametros(picos)
#    print(len(picos))
#    para = estat.mvs('GP')
#    paras = {"Referência":[0.0236, 2769.993, 1944,4188],
#             "Percentil 75° - Mediana":[-0.352, 2839.954, 4125.727],
#             "Percentil 75° - Média":[-0.146, 2769.999, 2791.191],
#             "1.65 picos por ano - Mediana":[-0.525, 1440.999, 6155.358],
#             "1.65 picos por ano - Média":[0.214, 2806.999, 2337.735],
#             "2.3 picos por ano - Mediana":[0.929, 1332.999, 958.874],
#             "2.3 picos por ano - Média":[-0.023, 2099.022, 2445.033],}

#    paras = {"Referência":[0.0236, 2769.993, 1944,4188],
#             "2.3 picos por ano - Mediana":[0.929, 1332.999, 958.874],
#             "2.3 picos por ano - Média":[-0.023, 2099.022, 2445.033],}
#    mag = stat.Magnitudes()
#    lista_mag = mag.lista_de_magnitudes(1000, 'genepareto', paras)
#    print(lista_mag)
    #para = stat.Parametros(maxAnual)
    #print(para.mvs('GEV'))
#    imprimi = impr.Arquivo(picos)
#    imprimi.excel('SDP_Referência')
#    spells = pre.periodsSpells(picos, mesInicioAnoHidro)
    grafico = impr.Graficos(dados)
#    grafico.plotPolar(x)
#    grafico.plotDuraçãoPulso(eventos, 'cheia')
#    grafico.plotNPulsos(eventos, 'estiagem')
#    re, nRe, rCv = grafico.plotReversoes(riseA, fallB)
#    grafico.plotRate(riseA, 'Ascensão')
#    grafico.plotRate(fallB, 'Recessão')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotHidroParcial(picos, limiar, nomeGrafico='cheia')
    grafico.plotGantt(dfgantt)
#    grafico.plotHidro()
#    grafico.plot_distr(lista_mag)
#    grafico.plot_point(lista_mag, 'Magnitude', 'prob_acumulada')
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))
