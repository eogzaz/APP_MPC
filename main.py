from data_cleansing import Periodo_y_Perihelio
from data_processing import obtencion_dataframe
import streamlit as st
import datetime

st.set_page_config(layout="wide")
#st.title('Obtención de datos del MPC')
st.markdown("<h1 style='text-align: center'>Obtención de datos del MPC</h2>", unsafe_allow_html=True)
st.write('''
         Este programa se conecta con la base de datos de observaciones del MPC 
         y con la base datos de efemerides del JPL para obtener los datos de necesarios 
         para hacer la curva de luz secular (SLC) y la curva de fase de algun asteroide.
         ''')
col1,col2 =st.columns(2)

with col1:
    asteroide = st.text_input('Ingrese el número de algún asteroide que desea estudiar: ', value=None, 
                              placeholder='Ej: 1036') #probar con st.number_input
    
    st.write('''
             _**Nota:** La cantidad de asteroides que tienen designado un
             número designado es *811552*, esto a la fecha 2025/07/11 
             (ultima actualizacion de esta app)_
             ''')
with col2:
    fecha_inicial = str(st.date_input('Ingrese fecha de inicio', 
                                  value=datetime.date(1980, 1, 1),
                                  min_value=datetime.date(1800, 1, 1),
                                  max_value="today",
                                  help='''Desde esta fecha se tomaran las observaciones 
                                  del asteroide registradas en el MPC''')).replace('-',' ')

    fecha_final = str(st.date_input('Ingrese fecha final',
                                        value="today",
                                        min_value=datetime.date(1800, 1, 1),
                                        max_value="today",
                                        help='''Hasta esta fecha se tomaran las observaciones
                                          del asteroide registradas en el MPC''')).replace('-',' ')

if asteroide == None :
   a=0
else:
    try:
        
        num = int(asteroide)
        
        if num<1 or num>811552:
           
           st.error("Por favor, ingresa un número entre 1 y 811552") 
        
        else:
            
            periodo, fecha_perihelio = Periodo_y_Perihelio(str(num))

            col3, col4 = st.columns(2)
            with col3:
                col5, col6, col7 = st.columns(3)
                with col5:
                    st.success(f"El asteroide escogido es: {num}")  #agregar de alguna manera el nombre del asteroide
                with col6:
                    st.write(f'Periodo: {periodo/365.25}')
                with col7:
                    st.write(f'fecha del perihelio JD: {fecha_perihelio}')

    except ValueError:
        st.error("Por favor, ingresa un número válido.")
    
    else:
        asteroide=str(asteroide)
    

        with col4:
            col8, col9 = st.columns(2)
            with col8:
                col10, col11= st.columns(2)
                with col10:
                    a=0
                    if st.button("Obtener datos"):
                        a=1
                        with st.spinner("_Procesando..._"):
                            df_ast = obtencion_dataframe(asteroide, fecha_inicial, fecha_final)
                with col11:
                    st.button("Reset", type="primary")
            with col9:
                if a==1:
                    @st.cache_data
                    def convert_for_download(df):
                        return df.to_csv(sep='\t', index=False, header=False).encode("utf-8")

                    txt = convert_for_download(df_ast)

                    st.download_button(
                                        label="Descargar datos (.txt)",
                                        data=txt,
                                        file_name=asteroide + ".txt",
                                        mime="text/csv",
                                        icon=":material/download:",
                                        on_click="ignore"
                                       )
        if a==1:    
            st.dataframe(df_ast) 
