#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import calendar as cal

class Caracteristicas():
    def __init__(self, dadosVazao, nPosto, dataInicio = None, dataFim = None):
        self.nPosto = nPosto.upper()
        self.dataInicio = pd.to_datetime(dataInicio, dayfirst=True)
        self.dataFim = pd.to_datetime(dataFim, dayfirst=True)
        if self.dataInicio == None and self.dataFim == None:
            self.dadosVazao = dadosVazao.loc[self.dataInicio:self.dataFim]
        elif self.dataInicio == None:
            self.dadosVazao = dadosVazao.loc[:self.dataFim]
        elif self.dataFim == None:
            self.dadosVazao = dadosVazao.loc[self.dataInicio:]
        else:
            self.dadosVazao = dadosVazao
        
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

    def pulsosDuracao(self, vazaoLimiar=0.75, evento='cheia'):
        limiar = self.dadosVazao[self.nPosto].quantile(vazaoLimiar)
        if evento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
        elif evento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
        else:
            return 'Evento erro!'
        
        grupoEventos = eventos.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxEvento = {'Ano': [], 'Data':[], 'Vazao':[], 'Inicio':[], 'Fim':[], 'Duracao':[]}
        for key, serie in grupoEventos:
            dados = {'Data':[], 'Vazao':[]}
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(self.dadosVazao.loc[i, self.nPosto])
                    dados['Data'].append(i)
                elif len(dados['Vazao']) > 0:
                    maxEvento['Ano'].append(key.year)
                    maxEvento['Data'].append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    maxEvento['Vazao'].append(max(dados['Vazao']))
                    maxEvento['Inicio'].append(dados['Data'][0])
                    maxEvento['Fim'].append(dados['Data'][-1])
                    maxEvento['Duracao'].append(len(dados['Data']))
                    dados = {'Data':[], 'Vazao':[]}
        eventosPicos = pd.DataFrame(maxEvento)
        
        dic = {'Ano':[], 'Duracao':[], 'nPulsos':[]}
        for i, serie in grupoEventos:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(eventosPicos.Duracao.loc[eventosPicos.Ano == i.year].mean())
            dic['nPulsos'].append(len(eventosPicos.loc[eventosPicos.Ano == i.year]))
        evento = pd.DataFrame(dic)
        evento.set_value(evento.loc[evento.Duracao.isnull()].index, 'Duracao', 0)
        
        return eventosPicos, evento
    
    