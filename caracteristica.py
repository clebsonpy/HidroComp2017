#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import calendar as cal

class Caracteristicas():
    def __init__(self, dadosVazao, nPosto):
        self.dadosVazao = dadosVazao
        self.nPosto = nPosto.upper()
    #Ano hidrologico
    def mesInicioAnoHidrologico(self):
        mediaMes = [self.dadosVazao[self.nPosto].loc[self.dadosVazao.index.month==i].mean() for i in range(1,13)]
        mesHidro = 1 + mediaMes.index(min(mediaMes))
        """
        grupoMesAno = self.dadosVazao.groupby(pd.Grouper(freq='M')).mean().to_period()
        indexMult = list(zip(*[grupoMesAno.index.month, grupoMesAno.index.year]))
        indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Ano"])
        grupoMesAno.set_index(indexN, inplace=True)
        grupoMesMedia = grupoMesAno[self.nPosto].groupby(level='Mes').mean()
        mesHidro = grupoMesMedia.idxmin()
        """
        mesHidroAbr = cal.month_abbr[mesHidro]
        return mesHidro, mesHidroAbr.upper()

    #Periodos sem falhas
    def periodoSemFalhas(self):
        aux = []
        listaInicio = []
        listaFim = []
        ganttBool = self.dadosVazao.isnull()[self.nPosto]
        for i in ganttBool.index:
            if ~ganttBool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and ganttBool.loc[i]:
                listaInicio.append(aux[0])
                listaFim.append(aux[-1])
                aux = []
        if len(aux) > 0:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
        dic = {'Inicio': listaInicio, 'Fim': listaFim}
        return pd.DataFrame(dic)

    def cheias(self, vazaoLimiar=0.75):
        limiar = self.dadosVazao[self.nPosto].quantile(vazaoLimiar)
        cheias = self.dadosVazao[self.nPosto].isin(self.dadosVazao[self.nPosto].loc[self.dadosVazao[self.nPosto] >= limiar])
        che = []
        da = []
        dic = {'index':[], 'Vazao':[]}
        for i in cheias.index:
            if cheias.loc[i]:
                che.append(self.dadosVazao[self.nPosto].loc[i])
                da.append(i)
            elif len(che) > 0:
                dic['index'].append(da[che.index(max(che))])
                dic['Vazao'].append(max(che))
                che = []
                da = []
        return pd.DataFrame(pd.Series(dic['Vazao'], index=dic['index'], name=self.nPosto))
        
        """
        maxp = []
        aux = []
        data = []
        for i in self.dadosVazao[self.nPosto].index:
            if self.dadosVazao[self.nPosto].loc[i] > limiar:
                
                aux.append(self.dadosVazao[self.nPosto].loc[i])
                data.append(i)
            elif float(i[1]) < limiar and len(aux) > 0:
                indx = aux.index(max(aux))
                maxp.append([data[indx], max(aux)])
                data = []
                aux = []
        return maxp
        """ 
    
    