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
    dados = pd.read_json('dadosXingo.json')
    print(dados)
    caract = crt.Caracteristicas(dados, 'XINGO')
    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
#    pre = pr.Prepara(dados, '49370000')
#    dadosAno = pre.grupoAnoHidro(mesInicioAnoHidro)
#    imprimi = impr.Arquivo(dados['XINGO'])
#    imprimi.json('dadosXingo')
#    rateRise, rise = caract.rate(tipo='fall', quartilLimiar=0.75, evento='cheia')
#    psf = caract.periodoSemFalhas()
#    picos, eventos = caract.pulsosDuracao(quartilLimiar=0.75, evento='cheia')
#    grafico = impr.Graficos(dados, 'XINGO')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotHidroParcial(picos, quartilLimiar = 0.75, nomeGrafico='cheia')
#    grafico.plotGantt()
#    grafico.plotHidro()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))