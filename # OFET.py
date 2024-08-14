# OFET
#Para o programa atualizado pelo Fred
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit
import glob
import re

v_escrever = []
medidas_escrever = []
v_apagar = []
medidas_apagar = []

def ler_arquivo_txt(caminho_arquivo):
    medidas=[]
    v_limiar=[]
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        armazenar = False
        for linha in linhas:
            if not armazenar:
                if  linha[0].isnumeric() or linha[0] == '-':
                    armazenar = True
            if armazenar:
                if linha[0].isalpha() or linha[0].isspace():
                    break
                colunas = linha.split()
                medidas.append(float(colunas[0]))
                v_limiar.append (float(colunas[1]))
    return medidas, v_limiar

pasta = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 08 12 (férias)/Disp 2/80um'
arquivos = glob.glob(os.path.join(pasta,"*.txt")) #para ler cada cada arquivo .txt dentro da pasta

for j,caminho_arquivo in enumerate (arquivos):
    nome_arquivo = os.path.basename(caminho_arquivo)
    m,v = ler_arquivo_txt(caminho_arquivo)
    if '(-10)' in nome_arquivo:
        v_apagar = v
        medidas_apagar = m
    else:
        v_escrever = v
        medidas_escrever = m

plt.plot(medidas_escrever,v_escrever,marker = 'o', color = 'blue')
plt.plot(medidas_apagar,v_apagar,marker = 'o', color = 'red')
plt.xlabel('Medidas')
plt.ylabel('V_limiar')
plt.show()

