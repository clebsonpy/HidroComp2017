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
    def __init__(self, dados, distribuicao):
        self.dados = dados
        self.distribuicao = distribuicao
        
    def mvs(self):
        if self.distribuicao == 'GEV':
            parametros = stat.genextreme.fit(self.dados)
        elif self.distribuicao == 'NOR':
            parametros = stat.norm.fit(self.dados)
        
        return parametros
    
    def mml(self):
        if self.distribuicao == 'GEV':
            parametros = stat.genextreme