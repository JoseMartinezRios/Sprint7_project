"""
Creacion de la app principal para streamlit
graficos con plotly express
"""
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

#leer archivo csv
df = pd.read_csv('notebooks/dataset_limpio.csv')

#crear grupos de dataset desde el dataset principal
#PRECIOS POR AÑO DE LANZAMIENTO
precio_lanzamiento = df.groupby('model_year')['price'].mean().reset_index()

# MODELOS Y TRANSMISION PREFERIDA POR LOS CLIENTES
trans_model = df.groupby(['type', 'transmission']).size().reset_index()

# MODELO DE FABRICANTE Y CANTIDAD DE CILINDROS ELEGIDOS
cilindro_modelo = df.groupby(['model', 'cylinders'])['is_4wd'].size().reset_index()

#---- creacion de los plots ESTATICOS
fig1 = px.line(
        precio_lanzamiento,
        x='model_year',
        y='price',
        )
fig1.update_layout(
        title='Variacion en los precios de vehiculos lanzados por año',
        xaxis_title='Año de lanzamiento',
        yaxis_title='Precios'
        )

#figura 2
fig2 = px.bar(
        trans_model,
        x='type',
        y=0,
        color='transmission'
        )
fig2.update_layout(
        title='Transmisión preferida por los clientes.',
        xaxis_title='Tipo de vehiculo',
        yaxis_title='Cantidad'
        )

#figura 3
fig3 = px.scatter(
        cilindro_modelo,
        x='model',
        y='is_4wd',
        color='cylinders'
        )
fig3.update_layout(
        title='Modelos preferidos || Cilindros y modelos 4x4',
        xaxis_title='',
        yaxis_title='Cantidad',
        height=600
        )

#figura 4
fig4 = go.Figure()
fig4.add_trace(go.Histogram(x=df[df['year']==2019]['month'],
                            name='2019',
                            opacity=0.3,
                            marker_color='#EB8985'
                            ))
fig4.add_trace(go.Histogram(x=df[df['year']==2018]['month'],
                            name='2018',
                            opacity=0.4,
                            marker_color='#330C73',
                            ))
fig4.update_layout(
        barmode='overlay',
        title='Distribucion de ventas mensual (histograma)',
        xaxis_title='Meses',
        yaxis_title='Cantidad',
        )

#INICIAR CON LOS CODIGOS DE STREAMLIT
st.header('Mini análisis de ventas por vehículo')
st.subheader('Datos a trabajar')
st.write('A continuación se muestra una pequeña parte del datasets a trabajar.')
st.dataframe(df.head())
st.subheader("Mini plot dinámico")
modelos = st.selectbox("Seleccione un modelo a filtar", df.columns)
filtrado = px.bar(x=df[modelos],
                      y=df['is_4wd'],
                      title=f"Dataframe filtrado por {modelos.title()}",
                      )
filtrado.update_layout(
        xaxis={'title': "Categorías filtradas"},
        yaxis={'title': 'Cantidad de vehículos por categoría seleccionada'},
        )
st.plotly_chart(filtrado, use_container_width=True)
                      

st.header('PLOTS ESTÁTICOS')
st.subheader('Empieza otro pico de ventas---')
st.write('En la siguiente gráfica se aprecia que los precios alcanzan un punto máximo en ciertos modelos. Los más buscados resultan ser también los más caros: esto se observa en los modelos "Clásicos", pues lo coleccionistas más ávidos valoran aquellos con coraza metálica, acabados en cromo pulido o pintura clásica con diseños únicos.')
st.write('Dependiendo del coleccionista y de los propietarios, los precios de venta pueden variar considerablemente de un lugar a otro')
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Más fácil y accesible para todos---')
st.write('Muchas personas aficionadas a lo clásico insisten en que la conducción manual es superior, que el automático no debería existir, que el control del vehículo solo se aprende de cierta manera. Pero el mercado se regula por sí mismo: privilegia lo más cómodo y lo más nuevo. La presente gráfica lo deja en evidencia: los números aplastan a los modelos manuales, tanto que casi ni se distinguen en comparación con los automáticos.')
st.write('Como diría Dui: *"El futuro es hoy"*. Y es claro: siempre se buscará lo más práctico para la mayor cantidad de personas posibles. Mujeres que disfrutan conducir pero no quieren transimisión manual, hombres que no disponen de tiempo para un control tan detallado, o el público en general que busca optimizar tanto su transporte como sus herramientas tecnológicas.')
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Más poder al motor---')
st.write('En este gráfico de distribución se observa que la mayoría de las personas conduce vehículos de 4 a 8 cilindros. Quienes utilizan más cilindros son minoría, pues es lógico: si una persona trabaja todos los días, no querrá encender un superauto solo para llegar a la oficina, dejarlo estacionado todo el día y en total utilizarlo solo un par de horas.')
st.write('La practicidad es ley en la clase trabajadora, que sí emplea motores de varios cilindros, pero no por estatus, potencia o velocidad, sino por las cargas que deben soportar en sus labores cotidianas.')
st.plotly_chart(fig3, use_container_width=True)

st.subheader('Del perro al dragón, con las ventas---')
st.write('El siguiente histograma muestra una gran diferencia entre los dos años analizados.\nMientras que todas las ventas del 2018 ocurrieron en el primer tercio del año, en 2019 las transaccionies crecieron enormemente en los dos tercios finales.')
st.write('Esto sugiere que las ventas pueden mejorar si se ponen en práctica consideraciones relacionadas con marketing, manejo de stock, atención al cliente y ubicación estratégica de las sucursales')
st.plotly_chart(fig4, use_container_width=True)
