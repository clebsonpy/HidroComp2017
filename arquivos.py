import os
import timeit
import pandas as pd
import prepara
import lerTxt as lt
import lerXls as lx

class Arquivos(lt.LerTxt, lx.LerXls):
    
    def __init__(self, caminho, fonte):
        self.caminho = caminho
        self.fonte = fonte
        self.tipos = {'ONS':'xls', 'ANA':'TXT'}
        
    def listaArq(self):
        listaDir = os.listdir(self.caminho)
        listaArquivo = []
        for arquivo in listaDir:
            if os.path.isfile(os.path.join(self.caminho, arquivo)):
                nome, ext = arquivo.split('.')
                if ext == self.tipos[self.fonte]:
                    listaArquivo.append(nome)
        if len(listaArquivo) == 1:
            return listaArquivo[0]
        else:
            return listaArquivo
    
    def lerArquivos(self, nomeArquivo=None, consistencia=None):
        if nomeArquivo == None:
            nomeArquivo = self.listaArq()
                
        if type(nomeArquivo) == list:
            dadosVazao = pd.DataFrame()
            pp = prepara.Prepara()
            for nome in nomeArquivo:
                dadosVazao = pp.combinaDateFrame(dadosVazao, self.lerArquivos(nome))
            if consistencia != None:
                dadosVazao = pp.separaDadosConsisBruto(dadosVazao, consistencia)
            return dadosVazao
        else:
            self.nomeArquivo = nomeArquivo
            if self.fonte == 'ANA':
                return self.lerTxt()
            elif self.fonte == 'ONS':
                return self.lerXls()
            
if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
    arq = Arquivos(caminho, fonte='ONS')
    dados = arq.lerArquivos()
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))
#    dadox = pd.DataFrame.add(dados)
#    print(dados)