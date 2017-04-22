import os
import pandas as pd
import lerArquivos as la

class Arquivos(la.LerTxt, la.LerXls, la.LerHdf):
    
    def __init__(self, caminho, nomeArquivo=None, consistencia=2, fonte=None,  lat=[-50,50], log = [-180,180]):
        self.caminho = caminho
        self.fonte = fonte
        self.nomeArquivo = nomeArquivo
        self.consistencia = consistencia
        self.log = log
        self.lat = lat
        
        
    def listaArq(self):
        listaDir = os.listdir(self.caminho)
        tipos = {'ONS':'xls', 'ANA':'TXT', 'NASA':'HDF'}
        listaArquivo = []
        for arquivo in listaDir:
            if os.path.isfile(os.path.join(self.caminho, arquivo)):
                nome, ext = arquivo.split('.')
                if ext == tipos[self.fonte]:
                    listaArquivo.append(nome)  
        return listaArquivo
    
    def lerArquivos(self):
        if self.nomeArquivo == None:
            self.nomeArquivo = self.listaArq()
            
        if type(self.nomeArquivo) == list:
            dadosVazao = pd.DataFrame()
            for nome in self.nomeArquivo:
                self.nomeArquivo = nome
                if len(dadosVazao) > 0:
                    dadosVazao = dadosVazao.combine_first(self.lerArquivos())
                else:
                    dadosVazao = self.lerArquivos()
            return dadosVazao
        
        else:
            if self.fonte == 'ANA':
                dados = self.lerTxt()
                dados = dados.iloc[dados.index.isin([self.consistencia], level=1)]
                dados.reset_index(level=1, drop=True, inplace=True)
                return dados
            elif self.fonte == 'ONS':
                return self.lerXls()
            elif self.fonte == 'NASA':
                return self.lerHdf()
        