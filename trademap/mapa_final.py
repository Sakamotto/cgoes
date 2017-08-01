# -*- coding: utf-8 -*-
"""

PROJETO: "Uma Estratégia De Antecipação Dos Impactos Regionais E Setoriais
Da Abertura Comercial Brasileira Sobre O Emprego E Requalificação Da População Afetada"

EQUIPE DO PROJETO: Carlos Góes (SAE), Eduardo Leoni (SAE),
Luís Montes (SAE) e Alexandre Messa (Núcleo Econômico da CAMEX).

AUTOR DESTE CÓDIGO: Carlos Góes, SAE/Presidência da República

DATA: 24/07/2017

"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

#####################################
# 1. Retrieve Databases 
#####################################

data_mun = "K:\\Notas Técnicas\\Abertura\\data\\Econometria\\results\\modelresult_mun.json"
shp_mun = "K:/Notas Técnicas/Abertura/data/mapas/BR/BRMUE250GC_SIR.shp"
data_micro = "K:\\Notas Técnicas\\Abertura\\data\\Econometria\\results\\modelresult_micro.json"
shp_micro= "K:/Notas Técnicas/Abertura/data/mapas/BR/BRMIE250GC_SIR.shp"

# Importar dados

modelresult_mun = pd.read_json(path_or_buf=data_mun)
modelresult_micro = pd.read_json(path_or_buf=data_micro)

# Importar SHPs

sf_mun = gpd.read_file(shp_mun)
sf_micro = gpd.read_file(shp_micro)

#####################################
# 2. Adjust and merge databases 
#####################################

# Ajustar código do município ou microregião

sf_mun['CD_GEOCMU'] = [int(item[:-1]) for item in sf_mun['CD_GEOCMU']]
sf_micro['CD_GEOCMI'] = [int(item) for item in sf_micro['CD_GEOCMI']]

# Mesclar bases de dado

sf_mun = sf_mun.set_index("CD_GEOCMU").join(modelresult_mun.set_index("municipio"), how="left").reset_index(drop=False)
sf_micro = sf_micro.set_index("CD_GEOCMI").join(modelresult_micro.set_index("microrregiao"), how="left").reset_index(drop=False)

#####################################
# 3. Plot Maps
#####################################

groups = ["","_pos","_neg"]

for group in groups:
    fig, axes = plt.subplots(figsize=(10, 10))
    
    mymap = sf_micro.plot(ax=axes,
                     column="pop_change_mun_final" + group,
                     linewidth=0.02,
                     cmap="seismic_r",
                     vmin = -2,
                     vmax = 2)
    
    plt.axis('off')
    plt.title('Brasil: Variação Esperada no Emprego 10 anos após liberalização comercial, por microrregião')
    plt.tight_layout()
    
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    sm = plt.cm.ScalarMappable(cmap="seismic_r", norm=plt.Normalize(vmin = -2, vmax = 2))
    sm._A = []
    fig.colorbar(sm, cax=cax)
    
    plt.show()
    
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas/pdf/mapa_micro" + group + ".pdf")
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas/svg/mapa_micro" + group + ".svg")
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas/png/mapa_micro" + group + ".png", dpi=600, transparent=False)

#####################################
# 4. Loop for State Maps
#####################################

estados = sf_micro['UFSigla'].unique()

for estado in estados:
    sf_mini = sf_micro[ sf_micro['UFSigla'] == estado ]
    
    fig, axes = plt.subplots(figsize=(10, 10))
    
    mymap = sf_mini.plot(ax=axes,
                 column="pop_change_mun_final",
                 linewidth=0.02,
                 cmap="seismic_r",
                 vmin = -2,
                 vmax = 2)
    
    plt.axis('off')
    plt.title(str(estado) + ': Variação Esperada no Emprego 10 anos após liberalização comercial, por microrregião')  
    plt.tight_layout()
    
    cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    sm = plt.cm.ScalarMappable(cmap="seismic_r", norm=plt.Normalize(vmin = -3, vmax = 3))
    sm._A = []
    fig.colorbar(sm, cax=cax)
    
    plt.show()
    
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas/pdf/mapa_" + estado + ".pdf")
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas/svg/mapa_" + estado + ".svg")
    fig.savefig("K:/Notas Técnicas/Abertura/data/mapas//png//mapa_" + estado + ".png", dpi=600, transparent=False)

