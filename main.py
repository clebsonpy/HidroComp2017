#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:00:55 2017

@author: clebson
"""
import os
import timeit
import arquivos as arq
import caracteristica as crt
import prepara as pr
import imprimir as impr

if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
#    caminho = ('/home/clebson/Área de Trabalho/Samuellson/NEW/')
#    caminho = ('C:\\Users\\franciely\\Desktop\\Dados_Nasa\\')
    dados = arq.Arquivos(caminho, fonte='ANA').lerArquivos('49370000')
#    imprimi = impr.Arquivo(dados)
#    imprimi.excel('outNEW')
    caract = crt.Caracteristicas(dados, '49370000')
    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
    rateRise, rise = caract.rate(tipo='fall', quartilLimiar=0.75, evento='cheia')
#    psf = caract.periodoSemFalhas()
    picos, eventos = caract.pulsosDuracao(quartilLimiar=0.75, evento='cheia')
#    grafico = gfc.Graficos(dados, '49370000')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotGantt()
#    grafico.plotHidro()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))