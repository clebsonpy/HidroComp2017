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
import graficos as gfc
if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd() #'/home/clebson/Área de Trabalho/Nasa/' 
    dados = arq.Arquivos(caminho, fonte='NASA', lon=[-60,-30], lat=[-30,0]).lerArquivos()
#    caract = crt.Caracteristicas(dados, '49370000')
#    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
#    prep = pr.Prepara('49370000')    
#    dadosPre = prep.grupoAnoHidro(dados, mesInicioAnoHidro)
#    picos, eventos = caract.pulsosDuracao(vazaoLimiar=0.25, evento='estiagem')
#    periodo = caract.periodoSemFalhas()
#    grafico = gfc.Graficos()
#    grafico.plotHidroPorAno(dadosPre, 'Hidrograma_por_ano')
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))