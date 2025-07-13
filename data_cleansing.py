import pandas as pd
import numpy as np
from astroquery.mpc import MPC

def Correccion_Banda(df):
  '''
  La lista actual de bandas de magnitud aceptables por el MPC es: B, V, R, I, J, W, U, C, L, H, K, Y, G, g, r, i, w, y, z, o, c, v, u.
  La conversión a la banda V utilizada por MPC se encuentra en la página: https://www.minorplanetcenter.net/iau/info/BandConversion.txt
  '''
  Correcciones={'U':-1.3,
                'B':-0.8,
                'g':-0.35,
                'V':0,
                'r':0.14,
                'R':0.4,
                'C':0.4,
                'W':0.4,
                'i':0.32,
                'z':0.26,
                'I':0.8,
                'J':1.2,
                'w':-0.13,
                'y':0.32,
                'L':0.2,
                'H':1.4,
                'K':1.7,
                'Y':0.7,
                'G':0.28,
                'v':0,
                'c':-0.05,
                'o':0.33,
                'u':2.5,
                'N':np.nan,
                'T':np.nan}

  magn_sin_Banda = np.zeros(len(df))
  magn_con_Banda = df['Magn']

  #Corrección estándar para convertir una magnitud en cualquier banda a banda V
  for i in range(len(magn_con_Banda)):
    for j in range(len(Correcciones)):
      if magn_con_Banda[i][-1]==list(Correcciones.keys())[j]:
        magn_sin_Banda[i]=float(magn_con_Banda[i].replace(list(Correcciones.keys())[j],''))+list(Correcciones.values())[j]



  #Correción estandar para magnitudes sin banda explicita a banda V es de 0.8 (https://www.minorplanetcenter.net/iau/info/BandConversion.txt)
  for k in range(len(magn_sin_Banda)):
    if magn_sin_Banda[k]==0:
      magn_sin_Banda[k]=float(magn_con_Banda[k])-0.8

  df['Magn corregiada a banda V'] = magn_sin_Banda
  df=df.dropna().reset_index(drop=True)

  return df

def Periodo_y_Perihelio(asteroide):
  datos = MPC.query_object('asteroid',number=asteroide,return_fields='period,perihelion_date,perihelion_date_jd')[0]
  periodo = float(datos['period'])*365.25
  fecha_perihelio = float(datos['perihelion_date_jd'])
  return periodo, fecha_perihelio

def Distancia_Perihelio(asteroide, df_obs):
  periodo,fecha_perihelio = Periodo_y_Perihelio(asteroide)
  def condicion(fecha,period=periodo):
    if (fecha_perihelio-fecha)%period >= period/2:
        distacia_al_perihelio=period-((fecha_perihelio-fecha)%period)
    else:
        distacia_al_perihelio=-((fecha_perihelio-fecha)%period)
    return round(distacia_al_perihelio)

  df_obs['Distancia_Perihelio'] = df_obs['Julian Day'].apply(condicion)
  return df_obs

def organizacion_df(df):
  df.insert(1, 'Año', df['Date (UT)'].apply(lambda x: x.split()[0].split('-')[0]))
  df.insert(2, 'Mes', df['Date (UT)'].apply(lambda x: x.split()[1].split('-')[0]))
  df.insert(3, 'Dia',df['Date (UT)'].apply(lambda x: int(float(x.split()[2].split('-')[0]))))

  df.drop(columns=['Date (UT)'], inplace=True)

  df['delta'] = df['delta'].apply(lambda x: round(x,2))
  df['r'] = df['r'].apply(lambda x: round(x,2))
  df['alpha'] = df['alpha'].apply(lambda x: round(x,2))
  df['Magn'] = df['Magn'].apply(lambda x: round(x,2))
  df['Magn_abs'] = df['Magn_abs'].apply(lambda x: round(x,2))

  return df


