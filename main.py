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
import prepara as pr
import imprimir as impr

if __name__ == "__main__":
    ini = timeit.default_timer()
#    caminho = os.path.join(os.getcwd(), 'Dados_Chuva')
#    dados = arq.Arquivos(caminho, fonte='ANA', tipoDado='pluviométrico').lerArquivos()
    dados = pd.read_csv("dadosXingo.csv", index_col = 0, names=["Data", "XINGO"], parse_dates=True)
    dados = crt.Caracteristicas(dados, 'XINGO')
#    total_ano = caract.precipitacao_anual()
    maxAnual = dados.maxAnual()
    print(maxAnual)
#    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
#    pre = pr.Prepara(dados)
#    dfgantt = pre.gantt()
#    x = pre.anualMaxPolar(maxAnual)
#    dadosAno = pre.grupoAnoHidro(mesInicioAnoHidro)
#    imprimi = impr.Arquivo(total_ano)
#    imprimi.excel('Chuva_Anual_Bruto')
#    dfDayJ, dayJ = caract.daysJulian(reducao="Maxima")
#    rateA, riseA = caract.rate(tipo='rise', quartilLimiar=0.75, evento='cheia')
#    rateB, fallB = caract.rate(tipo='fall', quartilLimiar=0.75, evento='cheia')
#    psf = caract.periodoSemFalhas()
#    picos, eventos, dM, dCv, pM, pCv = caract.pulsosDuracao(quartilLimiar=0.25, evento='estiagem')
#    spells = pre.periodsSpells(picos, mesInicioAnoHidro)
#    grafico = impr.Graficos(dados)
#    grafico.plotPolar(x)
#    grafico.plotDuraçãoPulso(eventos, 'cheia')
#    grafico.plotNPulsos(eventos, 'estiagem')
#    re, nRe, rCv = grafico.plotReversoes(riseA, fallB)
#    grafico.plotRate(riseA, 'Ascensão')
#    grafico.plotRate(fallB, 'Recessão')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotHidroParcial(picos, quartilLimiar = 0.75, nomeGrafico='cheia')
#    grafico.plotGantt(dfgantt)
#    grafico.plotHidro()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))
