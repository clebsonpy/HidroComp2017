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
    caminho = os.getcwd()
#    caminho = ('/home/clebson/Área de Trabalho/Nasa/')
#    caminho = ('/home/clebson/Área de Trabalho/Kleverton/2015-07-02/')
    dados = arq.Arquivos(caminho, fonte='ANA').lerArquivos()
#    caract = crt.Caracteristicas(dados, '49370000')
#    mesInicioAnoHidro = caract.mesInicioAnoHidrologico()
#    psf = caract.periodoSemFalhas()
#    picos, eventos = caract.pulsosDuracao(vazaoLimiar=0.25, evento='estiagem')
#    prep = pr.Prepara()
#    dfGantt = prep.gantt(dados)    
#    dadosPre = prep.grupoAnoHidro(dados, mesInicioAnoHidro)
    grafico = gfc.Graficos(dados, '49370000')
#    grafico.plotHidroPorAno(mesInicioAnoHidro)
#    grafico.plotGantt()
    grafico.plotHidro()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))