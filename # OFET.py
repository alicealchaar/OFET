# OFET
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit
import glob
import re

tempo,vds,vgs,ids,vgs,potência,v_inicial,v_final,x0,a,coef_saturação = [None]*11
abs_ids,sqrt_ids,vgs_intervalo,ids_intervalo,v_limiar_todos, medidas= [],[],[],[],[],[]

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
    global tempo,vds,vgs,ids,igs,vgs,potência, v_inicial,v_final, vgs_intervalo,ids_intervalo,x0,a, coef_saturação
    vgs_intervalo=[]
    ids_intervalo=[]
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
    v_inicial = int(-15)
    v_final = int(-17)
    # plt.close()
    for pos,i in enumerate(vgs):
        if pos>0:
            if i>vgs[pos-1]:
                break
            if i<=v_inicial and i>=v_final:
                vgs_intervalo.append(i)
                ids_intervalo.append(sqrt_ids[pos])
    vgs_intervalo = np.array(vgs_intervalo)
    ids_intervalo = np.array(ids_intervalo)
    coef, incerteza = curve_fit(reta, vgs_intervalo, ids_intervalo)
    a, b = coef
    x0 = -b/a
    coef_saturação = (2*L*a*a)/(W*Ci)
    # plt.plot(vgs,sqrt_ids)
    # #plt.plot(vgs_intervalo, ids_intervalo, 'o', label='Dados experimentais',markersize=5)
    # plt.plot(vgs_intervalo, reta(vgs_intervalo, a, b), 'r-', label=f'Fitting {j}')
    # plt.xlabel('VGS')
    # plt.ylabel('sqrt(IDS)')
    # plt.legend()
    # plt.show()
    # print(f'O coeficiente de saturação é {coef_saturação}')
    # print(f'O valor de x para y=0 é {x0}')
    v_limiar_todos.append(x0)


def salvar_dados():
    with open(caminho_arquivo, 'w') as file:
        file.write("Tempo            VDS              VGS              IDS              IGS         |IDS|         sqrt(|IDS|)    V_limiar    coef_angular  mobilidade\n")
        for i in range(len(tempo)):
            if i == 0:
                file.write("{:.7e}  {:.7e}  {:.7e}  {:.7e}  {:.7e} {:.7e}  {:.7e}    {:.7e}  {:.7e}   {:.7e}\n".format(
                    tempo[i], vds[i], vgs[i], ids[i], igs[i], abs_ids[i], sqrt_ids[i], x0, a, coef_saturação))
            else:
                file.write("{:.7e}  {:.7e}  {:.7e}  {:.7e}  {:.7e} {:.7e}  {:.7e}    \n".format(
                    tempo[i], vds[i], vgs[i], ids[i], igs[i], abs_ids[i], sqrt_ids[i]))
pasta = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 06 05/80um'
nome_pasta= os.path.basename(pasta)
match = re.search(r'\d+',nome_pasta)
L = int(match.group())
W = 1000
Ci = 50
arquivos = glob.glob(os.path.join(pasta,"*.txt"))
for j,caminho_arquivo in enumerate (arquivos):
    medidas.append(j)
    ler_arquivo_txt(caminho_arquivo,L,W,Ci,j)
    salvar_dados()

medidas_par = []
medidas_impar = []
v_par = []
v_impar = []
for k in range(len(medidas)):
    if k % 2 == 0:
        if k !=14 and k!=13: 
            medidas_par.append(k)
            v_par.append(v_limiar_todos[k])
    else:
        if k !=14 and k!=13:
            medidas_impar.append(k)
            v_impar.append(v_limiar_todos[k])
plt.plot(medidas_par,v_par,marker = 'o', color = 'blue')
plt.plot(medidas_impar,v_impar,marker = 'o', color = 'red')
plt.xlabel('Medidas')
plt.ylabel('V_limiar')
plt.show()