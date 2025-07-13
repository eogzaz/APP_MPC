import pandas as pd
import numpy as np

from utils import Date_to_julian, Date_to_julian_N
from data_obtention import observations_MPC, efemerides
from data_cleansing import Correccion_Banda, Distancia_Perihelio, organizacion_df


def limpieza_obsevaciones(asteroide,df_obs_sin_limpiar, fecha_inicial, fecha_final):
  #Eliminar filas con almenos un NaN en la columna Magn y seleccion de las columnas que se van a usar
  df_obs_sin_nan= df_obs_sin_limpiar.dropna()[['Date (UT)', 'Magn']].reset_index(drop=True)

  #Seleccion de solo las observaciones en Filtro V y R, y cambio de formato de fecha
  df_obs = Correccion_Banda(df_obs_sin_nan)

  #Agrego columna con dia juliano
  df_obs['Julian Day']=df_obs['Date (UT)'].apply(Date_to_julian)
  df_obs['Julian Day N']=df_obs['Date (UT)'].apply(Date_to_julian_N)



  #Rango de fechas
  df_obs=df_obs[(df_obs['Julian Day']>=Date_to_julian(fecha_inicial)) & (df_obs['Julian Day']<=Date_to_julian(fecha_final))]

  df_obs=df_obs.reset_index(drop=True)
  df_obs=Distancia_Perihelio(asteroide, df_obs)

  return df_obs

def obtencion_dataframe(asteroide, fecha_inicial='1980 01 01', fecha_final='2025 07 09'):
  #Obtencion de datos obsrvacionales MPC
  df_obs = limpieza_obsevaciones(asteroide,observations_MPC(asteroide),fecha_inicial,fecha_final)

  #Obtención efemerides
  df_efeme = efemerides(asteroide,fecha_inicial,fecha_final)

  #dataframe total
  df_total=pd.merge(df_obs, df_efeme, left_on='Julian Day N', right_on='datetime_jd', how='inner')[['Date (UT)','Distancia_Perihelio','delta','r','alpha','Magn corregiada a banda V']]
  df_total = df_total.rename(columns={'Magn corregiada a banda V': 'Magn'})
  df_total['Magn_abs'] = df_total['Magn'].astype(float) - 5*np.log10(df_total['r']*df_total['delta'])

  return organizacion_df(df_total)

