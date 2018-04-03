#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:55:08 2017

@author: clebson
"""
import pandas as pd
import numpy as np
import scipy.stats as stat

class Bootstrap():
    
    def __init__(self, tamanhoAmosta):
        self.tamanhoAmostra = tamanhoAmosta
        
    def gev(self, forma, loc, esc):
        amostra = pd.DataFrame()
        
        
    def normal(self, media, desvio):
       pass

class Parametros():
    def __init__(self, dados):
        self.dados = dados['Vazao'].values
        print(self.dados)
        
    def mvs(self, distribuicao):
        if distribuicao == 'GEV':
            parametros = stat.genextreme.fit(self.dados)
        elif distribuicao == 'NOR':
            parametros = stat.norm.fit(self.dados)
        elif distribuicao == 'GP':
            parametros = stat.genpareto.fit(self.dados)

        return parametros
    
    def mml(self):
        if self.distribuicao == 'GEV':
            parametros = stat.genextreme

class Magnitudes():

    def __init__(self, forma, localizacao, escala):
        self.forma = forma
        self.loc = localizacao
        self.escala = escala

    def genepareto(self, probabilidade):
        quantil = stat.genpareto.ppf(probabilidade, self.forma,
                                 loc=self.loc,
                                 scale=self.escala)

        return quantil

    def lista_de_magnitudes(self, tamanho, distribuicao):

        esp = 1/tamanho
        prob = 0
        listaprob = []
        lista = []
        for i in range(tamanho):
            if distribuicao == 'genepareto':
                mag = self.genepareto(prob)
            lista.append(mag)
            listaprob.append(prob)
            prob += esp

        return pd.DataFrame(lista, columns=['Magnitude'], index=listaprob)
