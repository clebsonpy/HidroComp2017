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

if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
    dados = arq.Arquivos(caminho, fonte='ANA').lerArquivos()
    caract = crt.Caracteristicas(dados, '39980000')
    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
    prep = pr.Prepara('39980000')
    x = prep.grupoAnoHidro(dados, mesInicioAnoHidro)
#    picos, eventos = caract.pulsosDuracao(vazaoLimiar=0.25, evento='estiagem')
#    periodo = caract.periodoSemFalhas()
#    grafico = gfc.Graficos()
#    grafico.plotHidro(dados, 'Cle')
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))