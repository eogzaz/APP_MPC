import requests
from bs4 import BeautifulSoup
import pandas as pd
from astroquery.jplhorizons import Horizons
from astroquery.mpc import MPC

def observations_MPC(asteroide):
  # URL base
  url_base = "https://www.minorplanetcenter.net/db_search/show_object"

  # Parámetros de búsqueda
  params = {
      "utf8": "✓",
      "object_id": asteroide
  }

  # Realizar la solicitud GET
  response = requests.get(url_base, params=params)

  # Verificar si la solicitud fue exitosa
  if response.status_code == 200:
      # Obtener el URL final de redirección
      final_url = response.url

      # Get the HTML content from the response
      html_content = response.text

      # Use BeautifulSoup to parse the HTML
      soup = BeautifulSoup(html_content, 'html.parser')

      # Find all the table tags in the HTML
      tables = soup.find_all('table')

  else:
      print(f"Error al acceder a la página del MPC Código de estado: {response.status_code}")

  if len(tables)== 0 or final_url == 'https://www.minorplanetcenter.net/db_search':
    return print("Este no es un objeto en el MPC")
  else:
    df_observations = pd.read_html(final_url)[-1]
    print(f"Obtencion exitosa de las observaciones del objeto: {asteroide}")

  return df_observations

def efemerides(asteroide,fecha_inicial, fecha_final):
  obj = Horizons(id=asteroide,id_type='smallbody',
                 epochs={'start': fecha_inicial, 'stop': fecha_final, 'step': '1d'})
  eph = obj.ephemerides()
  df_efeme = eph['datetime_str', 'datetime_jd','RA', 'DEC', 'delta', 'r', 'alpha'].to_pandas()
  return df_efeme