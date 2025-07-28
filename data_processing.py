import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_obtention import observaciones_APIMPC, efemerides_API
from data_cleansing import limpieza_obsevaciones, organizacion_df
import asyncio
from concurrent.futures import ThreadPoolExecutor

def obtencion_dataframe1(asteroide, fecha_inicial='1980 01 01', fecha_final='2025 07 12'):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(obtencion_dataframe_async(asteroide, fecha_inicial, fecha_final))

async def obtencion_dataframe_async(asteroide, fecha_inicial, fecha_final):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        # Tareas en paralelo
        obs_future = loop.run_in_executor(executor, lambda: limpieza_obsevaciones(
            asteroide, observaciones_APIMPC(asteroide), fecha_inicial, fecha_final
        ))

        efem_future = loop.run_in_executor(executor, lambda: efemerides_API(
            asteroide, fecha_inicial, fecha_final
        ))

        df_obs, df_efeme = await asyncio.gather(obs_future, efem_future)

    # Fusionar resultados
    df_total = pd.merge(df_obs, df_efeme, left_on='Julian Day N', right_on='Date JD', how='inner')[[
        'obsTime', 'Distancia_Perihelio', 'Delta', 'r', 'fase', 'Magn corregiada a banda V'
    ]]
    df_total = df_total.rename(columns={'Magn corregiada a banda V': 'Magn'})
    df_total['Magn_abs'] = df_total['Magn'].astype(float) - 5*np.log10(df_total['r'] * df_total['Delta'])

    return organizacion_df(df_total)


def obtencion_dataframe(asteroide, fecha_inicial='1980 01 01', fecha_final='2025 07 12'):
  #Obtencion de datos obsrvacionales MPC
  df_obs = limpieza_obsevaciones(asteroide,observaciones_APIMPC(asteroide),fecha_inicial,fecha_final)

  #Obtención efemerides
  df_efeme = efemerides_API(asteroide,fecha_inicial,fecha_final)

  #dataframe total
  df_total=pd.merge(df_obs, df_efeme, left_on='Julian Day N', right_on='Date JD', how='inner')[['obsTime','Distancia_Perihelio','Delta','r','fase','Magn corregiada a banda V']]
  df_total = df_total.rename(columns={'Magn corregiada a banda V': 'Magn'})
  df_total['Magn_abs'] = df_total['Magn'].astype(float) - 5*np.log10(df_total['r']*df_total['Delta'])

  return organizacion_df(df_total)

        # Función de filtrado
def fase_menor_5(data_sin_editar):
  data = data_sin_editar.copy()
  fase = data['fase'].to_numpy()
  data['fase'] = np.where(fase < 5, np.nan, fase)
  return data.dropna().reset_index(drop=True)


def grafica_fase(df, title='none', familia='none'):
  fig, ax = plt.subplots(figsize=(6, 5))

  # First plot (Phase Curve)
  ax.plot(df['fase'], df['Magn_abs'].astype(float), 'o', markerfacecolor='cyan', markeredgecolor='blue', markersize=2)
  ax.set_title(f'{title} - Curva de Fase')
  ax.set_ylim(max(df['Magn_abs'])+1, min(df['Magn_abs'])-1)
  ax.set_xlim(0, max(df['fase'])+1)
  ax.set_xlabel('Fase')
  ax.set_ylabel('Magnitud')
  ax.grid()

  return fig

def grafica_SLC(df, title='none', familia='none'):
  fig, ax = plt.subplots(figsize=(6, 5))

  # Second plot (SLC)
  ax.plot(df['Distancia_Perihelio'], df['Magn_abs'].astype(float), 'o', markerfacecolor='cyan', markeredgecolor='blue', markersize=2)
  ax.set_ylim(max(df['Magn_abs'])+1, min(df['Magn_abs'])-1)
  ax.set_xlim(min(df['Distancia_Perihelio'])-50, max(df['Distancia_Perihelio'])+50)
  ax.set_title(f'{title} - SLC')
  ax.set_xlabel('Distancia al perihelio [días]')
  ax.set_ylabel('Magnitud')
  ax.grid()


  return fig