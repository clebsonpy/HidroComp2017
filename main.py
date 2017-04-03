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
import graficos as gfc

if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
    dados = arq.Arquivos(caminho, fonte='ANA', consistencia=2).lerArquivos()
    caract = crt.Caracteristicas(dados, '49370000')
    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
    cheias = caract.cheias()
    periodo = caract.periodoSemFalhas()
    grafico = gfc.Graficos()
    grafico.plotHidro(dados, 'Cle')
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))