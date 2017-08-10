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
    caminho = os.getcwd()
#    caminho = ('/home/clebson/Área de Trabalho/Samuellson/NEW/')
#    caminho = ('C:\\Users\\franciely\\Desktop\\Dados_Nasa\\')
#    dados = arq.Arquivos(caminho, fonte='ONS').lerArquivos()
    dados = pd.read_csv("dadosXingo.csv", index_col = 0, names=["Data", "XINGO"], parse_dates=True)
    caract = crt.Caracteristicas(dados, 'XINGO')
#    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
#    pre = pr.Prepara(dados, '49370000')
#    dadosAno = pre.grupoAnoHidro(mesInicioAnoHidro)
#    imprimi = impr.Arquivo(dados['XINGO'])
#    imprimi.csv('dadosXingo')
#    rateA, riseA = caract.rate(tipo='rise', quartilLimiar=0.75, evento='cheia')
#    rateB, fallB = caract.rate(tipo='fall', quartilLimiar=0.75, evento='cheia')
#    psf = caract.periodoSemFalhas()
#    picos, eventos = caract.pulsosDuracao(quartilLimiar=0.75, evento='cheia')
#    grafico = impr.Graficos(dados, 'XINGO')
#    grafico.plotDuraçãoPulso(eventos, 'cheia')
#    grafico.plotNPulsos(eventos, 'estiagem')
#    grafico.plotReversoes(riseA, fallB)
#    grafico.plotRate(riseA, 'Ascensão')
#    grafico.plotRate(fallB, 'Recessão')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotHidroParcial(picos, quartilLimiar = 0.25, nomeGrafico='estiagem')
#    grafico.plotGantt()
#    grafico.plotHidro()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))