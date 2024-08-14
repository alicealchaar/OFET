# OFET
#Para o programa atualizado pelo Fred
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
    v_inicial = int(-17)       ##########Lembrar de ajeitar esses valores
    v_final = int(-20)
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
    # # plt.plot(vgs_intervalo, ids_intervalo, 'o', label='Dados experimentais',markersize=5)
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
pasta = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 08 12 (férias)/Disp 2/80um/80um 24 08 08 (-40V) perfeito'
nome_pasta= os.path.basename(pasta)
match = re.search(r'\d+',nome_pasta) #para pegar o comprimento do canal a partir do nome da pasta
L = int(match.group())
W = 1000
Ci = 50
arquivos = glob.glob(os.path.join(pasta,"*.txt")) #para ler cada cada arquivo .txt dentro da pasta
for j,caminho_arquivo in enumerate (arquivos):
    nome_arquivo = os.path.basename(caminho_arquivo) #
    medidas.append(j)
    ler_arquivo_txt(caminho_arquivo,L,W,Ci,j)
    salvar_dados()
    plt.plot(vgs,sqrt_ids)
    plt.xlabel("VGS")
    plt.ylabel("sqrt(IDS)")
plt.show()

plt.plot(medidas,v_limiar_todos,marker = 'o', color = 'blue')
plt.xlabel('Medidas')
plt.ylabel('V_limiar')
plt.show()

def criar_arquivo(diretorio):
    nome = "_DadosTemporais.txt"
    caminho = os.path.join(diretorio, nome)
    with open(caminho, 'w') as file:
        for i in range (len(medidas)):
            file.write("{:.7e}  {:.7e}\n".format(medidas[i],v_limiar_todos[i]))

criar_arquivo(pasta)
print("Os dados foram salvos com sucesso!")