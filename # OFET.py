# OFET
#Para o programa atualizado pelo Fred
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit
import glob
import re

tempo,vds,vgs,ids,vgs,potência,v_inicial,v_final,x0_ida,x0_volta,a,coef_saturação = [None]*12
abs_ids,sqrt_ids,vgs_intervalo_ida,ids_intervalo_ida,vgs_intervalo_volta,ids_intervalo_volta, v_limiar_ida,v_limiar_volta, medidas= [],[],[],[],[],[],[],[],[]

def colunas_extras(ids):
    global abs_ids,sqrt_ids
    abs_ids,sqrt_ids =[],[]
    for i in ids:
        abs_ids.append(abs(i))
        sqrt_ids.append(np.sqrt(abs(i)))
    # plt.plot(vgs,sqrt_ids)
    # plt.plot(vds,sqrt_ids, label = 'VDS')
    # plt.xlabel('VGS')
    # plt.ylabel('sqrt(IDS)')
    # plt.show(block=False)

def reta(x,a,b):
    return a * x + b

def ler_arquivo_txt(caminho_arquivo,L,W,Ci,j):
    global tempo,vds,vgs,ids,igs,vgs,potência, v_inicial,v_final, vgs_intervalo_ida,ids_intervalo_ida, vgs_intervalo_volta,ids_intervalo_volta,x0_ida,x0_volta,a, coef_saturação, v_limiar_ida, v_limiar_volta
    vgs_intervalo_volta=[]
    ids_intervalo_volta=[]
    vgs_intervalo_ida = []
    ids_intervalo_ida = []
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        tempo = []
        vds = []
        vgs = []
        ids = []
        igs = []
        potência = []
        armazenar = False 

        for linha in linhas:
            if not armazenar: 
                if  linha[0].isnumeric() or linha[0] == '-':
                    armazenar = True
            if armazenar:
                if linha[0].isalpha() or linha[0].isspace():
                    break  
                colunas = linha.split()
                tempo.append(float(colunas[0]))
                vds.append (float(colunas[1]))
                vgs.append(float(colunas[2]))
                ids.append(float(colunas[3]))
                igs.append(float(colunas[4]))
                potência.append(float(colunas[5]))
    colunas_extras(ids)
    # v_inicial=float(input("Digite o valor inicial da tensão da parte da curva onde começa a reta: "))
    # v_final = float(input("Agora, o valor final: "))
    v_inicial = int(-17)       ##########Lembrar de ajeitar esses valores
    v_final = int(-20)
    depois_da_curva = None
    for pos,i in enumerate(vgs): #pos = index
        if pos>0:
            if i>vgs[pos-1]:
                depois_da_curva = 'ok'
            if depois_da_curva == None:
                if i<=v_inicial and i>=v_final:
                    vgs_intervalo_ida.append(i)
                    ids_intervalo_ida.append(sqrt_ids[pos])
            else:
                if i<=v_inicial and i>=v_final:
                    vgs_intervalo_volta.append(i)
                    ids_intervalo_volta.append(sqrt_ids[pos])    
    #ida           
    vgs_intervalo_ida = np.array(vgs_intervalo_ida)
    ids_intervalo_ida = np.array(ids_intervalo_ida)
    coef_ida, incerteza_ida = curve_fit(reta, vgs_intervalo_ida, ids_intervalo_ida)
    a_ida, b_ida = coef_ida
    x0_ida = -b_ida/a_ida
    # coef_saturação = (2*L*a*a)/(W*Ci)
    v_limiar_ida.append(x0_ida) 

    #volta
    vgs_intervalo_volta = np.array(vgs_intervalo_volta)
    ids_intervalo_volta = np.array(ids_intervalo_volta)
    coef_volta, incerteza_volta = curve_fit(reta, vgs_intervalo_volta, ids_intervalo_volta)
    a_volta, b_volta = coef_volta
    x0_volta = -b_volta/a_volta
    # coef_saturação = (2*L*a*a)/(W*Ci)
    v_limiar_volta.append(x0_volta) 

pasta = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 08 12 (férias)/Disp 2/80um/80um 24 08 08 (-40V) perfeito'
nome_pasta= os.path.basename(pasta)
match = re.search(r'\d+',nome_pasta) #para pegar o comprimento do canal a partir do nome da pasta
L = int(match.group())
W = 1000
Ci = 50
arquivos = glob.glob(os.path.join(pasta,"*.txt")) #para ler cada cada arquivo .txt dentro da pasta
for j,caminho_arquivo in enumerate (arquivos):
    nome_arquivo = os.path.basename(caminho_arquivo) 
    medidas.append(j)
    ler_arquivo_txt(caminho_arquivo,L,W,Ci,j)
    plt.plot(vgs,sqrt_ids)
    plt.xlabel("VGS")
    plt.ylabel("sqrt(IDS)")
plt.show()

plt.plot(medidas,v_limiar_ida,marker = 'o', color = 'blue')
plt.plot(medidas,v_limiar_volta,marker = 'o', color = 'red')
plt.xlabel('Medidas')
plt.ylabel('V_limiar')
plt.show()

# plt.plot(medidas,v_limiar_todos,marker = 'o', color = 'blue')
# plt.xlabel('Medidas')
# plt.ylabel('V_limiar')
# plt.show()

# # def criar_arquivo(diretorio):
# #     nome = "_DadosTemporais.txt"
# #     caminho = os.path.join(diretorio, nome)
# #     with open(caminho, 'w') as file:
# #         for i in range (len(medidas)):
# #             file.write("{:.7e}  {:.7e}\n".format(medidas[i],v_limiar_todos[i]))

# # criar_arquivo(pasta)
# # print("Os dados foram salvos com sucesso!")
