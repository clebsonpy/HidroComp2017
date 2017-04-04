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
        grupoCheias = cheias.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxEvento = {'Ano': [], 'Data':[], 'Vazao':[], 'Inicio':[], 'Fim':[], 'Duracao':[]}
        for key, serie in grupoCheias:
            dados = {'Data':[], 'Vazao':[]}
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(self.dadosVazao[self.nPosto].loc[i])
                    dados['Data'].append(i)
                elif len(dados['Vazao']) > 0:
                    maxEvento['Ano'].append(key.year)
                    maxEvento['Data'].append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    maxEvento['Vazao'].append(max(dados['Vazao']))
                    maxEvento['Inicio'].append(dados['Data'][0])
                    maxEvento['Fim'].append(dados['Data'][-1])
                    maxEvento['Duracao'].append(len(dados['Data']))
                    dados = {'Data':[], 'Vazao':[]}
        eventoCheia = pd.DataFrame(maxEvento)
        dic = {'Ano':[], 'Duracao':[], 'nPulsos':[]}
        
        for i, serie in grupoCheias:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(eventoCheia['Duracao'].loc[eventoCheia['Ano'] == i.year].mean())
            dic['nPulsos'].append(len(eventoCheia.loc[eventoCheia['Ano'] == i.year]))
        evento = pd.DataFrame(dic)
        return eventoCheia, evento
    
    def estiagem(self, vazaoLimiar=0.25):
        limiar = self.dadosVazao[self.nPosto].quantile(vazaoLimiar)
        cheias = self.dadosVazao[self.nPosto].isin(self.dadosVazao[self.nPosto].loc[self.dadosVazao[self.nPosto] <= limiar])
        grupoCheias = cheias.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        minEvento = {'Ano': [], 'Data':[], 'Vazao':[], 'Inicio':[], 'Fim':[], 'Duracao':[]}
        for key, serie in grupoCheias:
            dados = {'Data':[], 'Vazao':[]}
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(self.dadosVazao[self.nPosto].loc[i])
                    dados['Data'].append(i)
                elif len(dados['Vazao']) > 0:
                    minEvento['Ano'].append(key.year)
                    minEvento['Data'].append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    minEvento['Vazao'].append(max(dados['Vazao']))
                    minEvento['Inicio'].append(dados['Data'][0])
                    minEvento['Fim'].append(dados['Data'][-1])
                    minEvento['Duracao'].append(len(dados['Data']))
                    dados = {'Data':[], 'Vazao':[]}
        eventoEstiagem = pd.DataFrame(minEvento)
        dic = {'Ano':[], 'Duracao':[], 'nPulsos':[]}
        
        for i, serie in grupoCheias:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(eventoEstiagem['Duracao'].loc[eventoEstiagem['Ano'] == i.year].mean())
            dic['nPulsos'].append(len(eventoEstiagem.loc[eventoEstiagem['Ano'] == i.year]))
        evento = pd.DataFrame(dic)
        return eventoEstiagem, evento
    
    
    
#    def maximaAnual(self, grupos):
#        vazaoMax = []
#        dataMax = []
#        for data, dado in grupos:
#            vazaoMax.append(dado.values.max())
#            dataMax.append(dado.idxmax()[0])
#        maxAnualSerie = pd.Series(vazaoMax, dataMax)
#        return maxAnualSerie