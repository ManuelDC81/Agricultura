import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta del archivo
file_path = r'C:\Users\Usuario\Documents\FAO_stat_cultivos.xlsx'

# Verificar si el archivo existe
if not os.path.exists(file_path):
    st.error("El archivo no se encontró en la ruta especificada: {}".format(file_path))
    st.stop()

# Cargar los datos
data = pd.read_excel(file_path, sheet_name='Hoja1')

# Mostrar los primeros registros para ver si se cargaron correctamente
st.write("Primeros registros de los datos cargados:", data.head())

# Filtrar los datos
data = data[['Área', 'Producto', 'Año', 'Valor']]

# Crear una lista de productos únicos
productos = data['Producto'].unique()

# Sidebar para seleccionar productos
st.sidebar.title('Seleccione un producto')
selected_producto = st.sidebar.selectbox('Producto', productos)

# Filtrar los datos según el producto seleccionado
filtered_data = data[data['Producto'] == selected_producto]

# Mostrar los datos filtrados para ver si la selección funciona
st.write(f"Datos filtrados para el producto {selected_producto}:", filtered_data.head())

# Generar el gráfico comparativo
st.title('Comparación de Producción Agrícola')

st.subheader(selected_producto)
producto_data = filtered_data[filtered_data['Producto'] == selected_producto]
fig, ax = plt.subplots()

for pais in producto_data['Área'].unique():
    pais_data = producto_data[producto_data['Área'] == pais]
    # Eliminar duplicados promediando los valores numéricos
    pais_data = pais_data.groupby('Año').agg({'Valor': 'mean'}).reset_index()
    # Rellenar años faltantes con NaN
    pais_data = pais_data.set_index('Año').reindex(range(pais_data['Año'].min(), pais_data['Año'].max() + 1)).reset_index()
    pais_data['Área'] = pais
    # Mostrar datos procesados para cada país
    st.write(f"Datos procesados para el país {pais}:", pais_data.head())
    ax.plot(pais_data['Año'], pais_data['Valor'], marker='o', label=pais)

ax.set_xlabel('Año')
ax.set_ylabel('Índice de Producción Bruto')
ax.legend()
st.pyplot(fig)
plt.close(fig)  # Cierra la figura después de mostrarla




