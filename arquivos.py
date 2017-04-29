import os
import pandas as pd
import lerArquivos as la
import multiprocessing as mp

class Arquivos(la.LerTxt, la.LerXls, la.LerHdf, la.LerSam):

    def __init__(self, caminho, fonte, nomeArquivo=None, consistencia=2, tipoDado='fluviométrico'):
        self.caminho = caminho
        self.fonte = fonte.upper()
        self.nomeArquivo = nomeArquivo
        self.consistencia = consistencia
        self.tipoDado = tipoDado.upper()


    def listaArq(self):
        listaDir = os.listdir(self.caminho) #Lista tudo q contêm na pasta
        tipos = {'ONS':'.xls', 'ANA':'.TXT', 'NASA':'.HDF5', 'CEMADEN':'.sam'} #Dic de ext referênte a cada fonte 
        listaArquivo = []
        for arquivo in listaDir:
            if os.path.isfile(os.path.join(self.caminho, arquivo)):
                nome, ext = os.path.splitext(arquivo) # Separa nome e ext do arquivo
                if ext == tipos[self.fonte]: #compara ext do arquivo com a da fonte
                    listaArquivo.append(nome)
        if len(listaArquivo) == 1:
            listaArquivo = listaArquivo[0]
        return listaArquivo
    
    def lerArquivos(self, nome=None):
        self.nomeArquivo = nome
        if self.nomeArquivo == None:
            self.nomeArquivo = self.listaArq()

        if type(self.nomeArquivo) == list:
            p = mp.Pool(mp.cpu_count()*4) # Inicia multiprocessos
            listaDfs = p.map(self.lerArquivos, self.nomeArquivo) #Executa multiprocessos
            p.close() #finaliza multiprocessos
            if self.fonte == 'ANA':
                dadosVazao = pd.DataFrame()
                for df in listaDfs:
                    dadosVazao = dadosVazao.combine_first(df)
                return dadosVazao.sort_index()
            else:
                dadosVazao = pd.DataFrame(listaDfs)
                return dadosVazao.sort_index()

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
            elif self.fonte == 'CEMADEN':
                return self.lerSam()
