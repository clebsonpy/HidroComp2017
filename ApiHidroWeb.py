# -*- coding: utf-8 -*-
 
# ********  DECLARACOES INICIAIS

import requests
import re
import shutil
from bs4 import BeautifulSoup

 
class Hidroweb():
 
    url_estacao = 'http://hidroweb.ana.gov.br/Estacao.asp?Codigo={0}&CriaArq=true&TipoArq={1}'
    url_arquivo = 'http://hidroweb.ana.gov.br/{0}'
    tiposArq = {'Access': 0,  'txt': 1}
    tiposDiscretizacao = {'Vazao': '9'}
    
    def __init__(self, estacao, tipoArq, discretizacao):
        self.estacao = estacao
        self.tipoArq = tipoArq
        self.discretizacao = discretizacao
 
    def montar_url_estacao(self):
        return self.url_estacao.format(self.estacao, self.tiposArq[self.tipoArq])
 
    def montar_url_arquivo(self, caminho):
        return self.url_arquivo.format(caminho)
 
    def montar_nome_arquivo(self, estacao):
        return u'{0}.zip'.format(estacao)
 
    def salvar_arquivo_texto(self, link):
        r = requests.get(self.montar_url_arquivo(link), stream=True)
        print(r.status_code)
        if r.status_code == 200:
            with open(self.montar_nome_arquivo(self.estacao), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print('** %s ** (baixado)' % (self.estacao, ))
        else:
            print('** %s ** (problema)' % (self.estacao, ))
 
    def obter_link_arquivo(self, response):
        soup = BeautifulSoup(response.content)
        print(soup)
        link = soup.find('a', href=re.compile(r"^ARQ/"))
        return link.get('href')
        
        
 
    def baixar(self):
        post_data = {'cboTipoReg': self.tiposDiscretizacao[self.discretizacao]}
        r = requests.post(self.montar_url_estacao(), data=post_data)
        link = self.obter_link_arquivo(r)
        self.salvar_arquivo_texto(link)
        print('** %s ** (concluído)' % (self.estacao, ))
 
if __name__ == '__main__':
    hid = Hidroweb('49370000', 'txt', 'Vazao')
    hid.baixar()