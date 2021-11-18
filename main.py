from typing import Counter
from altair.vegalite.v4.schema.channels import Tooltip
import streamlit as st
import pandas as pd
import altair as alt
import retrieve_data


st.set_page_config(layout="centered")


def handle_banxico_series(series):
    time = []
    name = []
    values = []

    count = 0
    for row in series:
        time.append(row[1])
        name.append(row[0])
        values.append(float(row[2].replace(",", "")))

    return time, name, values





inflation = retrieve_data.ask_series_banxico('SP30577')
tiie = retrieve_data.ask_series_banxico('SF283')
#Producto interno bruto, a precios de mercado Actividades terciarias Comercio al por menor
comercio_menor = retrieve_data.ask_series_banxico('SR16676')



tiie_time, tiie_name, tiie_value = handle_banxico_series(tiie)
inf_time, inf_name, inf_values = handle_banxico_series(inflation)
comercio_menor_time, comercio_menor_name, comercio_menor_values = handle_banxico_series(comercio_menor)

tiie = pd.DataFrame({
    'dates': tiie_time,
    'serie': tiie_name,
    'Interest Rate': tiie_value, 
})

inflation = pd.DataFrame({
    'inflation dates': inf_time,
    'inf serie': inf_name,
    'inf rate': inf_values,
})

comercio_menor = pd.DataFrame({
    'comercio menor dates': comercio_menor_time,
    'comercio menor serie': comercio_menor_name,
    'comercio menor rates': comercio_menor_values,
})


c = alt.Chart(tiie).mark_line().encode(
    x='dates',
    y='Interest Rate',
    text='serie',
    tooltip=['Interest Rate', 'serie'],
)

d = alt.Chart(inflation).mark_line().encode(
    x='inflation dates',
    y='inf rate',
    text='inf serie',
    tooltip=['inf rate', 'inf serie']
)

e = alt.Chart(comercio_menor).mark_bar().encode(
    x='comercio menor dates',
    y='comercio menor rates',
    text='comercio menor serie',
    tooltip=['comercio menor rates', 'comercio menor serie']
)

(c + d + e).properties(
    width="container",
    height=16000
)

z = (c + d + e).resolve_scale(
    y = 'independent'
)

one = (d+e).resolve_scale(
    y='independent'
)
two = (c+e).resolve_scale(
    y='independent'
)



#Estructura de la pagina

st.title("¿Por qué Amazon debería preocuparse por las tasas de interés?")
st.header("Efectos de la tasa de interés interbancaria sobre el comercio al por menor en México")
st.altair_chart((z), use_container_width=True)

st.subheader('El dinero y el desempeño economico')
st.caption('"El sistema de precios es un instrumento registrador que automáticamente recoge todos los efectos relevantes de las acciones individuales. Sus indicaciones son la resultante de todas estas decisiones individuales y, al mismo tiempo, su guía." -Friedrick August Von Hayek')


st.markdown("""Siendo el dinero un medio económico de intermediación para el intercambio indirecto de otros bienes y servicios, este se ve sujeto a las mismas leyes de oferta y demanda que todos los demás bienes y servicios. A medida que una economía se desarrolla y su sociedad, el nivel de complejidad y cantidad de las transacciones en dicha economía incrementa. Se terminan desarrollando mecanismos e instituciones para la coordinación espacial y temporal de los agentes económicos siendo los bancos, las tasas de interés y los mercados financieros ejemplos paradigmáticos. Los bancos que funcionan para coordinar el esfuerzo de ahorradores, inversores y emprendedores median y canalizan los flujos de efectivo de un lugar a otro junto con la tasa de interés como mecanismo para coordinar a los agentes a través del tiempo, indicando cuándo ahorrar y disminuir el consumo, cuando invertir lo ahorrado o cuando gastar y consumir. 

De esta forma la tasa de interés interbancaria controlada por BANXICO es la batuta que instrumenta a todo el sistema financiero para funcionar a un ritmo u otro. Luego del sistema financiero los flujos de crédito permean a las demás industrias y rincones de los mercados teniendo un efecto en cascada y paulatino que termina por afectar las actividades de cualquier persona. El ecommerce y el comercio al por menor no es la excepción y la manipulación de la tasa de interés puede tener efectos adversos o positivos en estos sectores como veremos a continuación.
""")
st.altair_chart(c, use_container_width=True)
with st.expander("Pie de grafica"):
    st.markdown("""
            *La grafica de arriba muestra la tasa de interes - que representa la relación de valor entre bienes persentes contra bienes futuros - de todo el año 2020. Datos obtenidos del API del Sistema de informaion economica de **BANXICO** [(ver código)](https://github.com/SantiagoSF/BANXICO-Indicators)*
    """)


st.markdown("""La tasa de interés interbancaria representa la relación de preferencias temporales de los agentes económicos entre la oferta de bienes y servicios presentes contra la oferta de bienes y servicios futuros. Una baja tasa de interés representa una menor aversión al riesgo y una disposición al sacrificio del consumo presente a cambio de un consumo mayor en el futuro. En otras palabras: una baja tasa de interés indica a los actores económicos que pueden incrementar el gasto corriente e invertir en proyectos empresariales a futuro para obtener beneficios. Por contraparte una alta tasa de interés indica una mayor aversión al riesgo y una mayor tasa de preferencia temporal por bienes presentes que futuros, indicando a los agentes que deben dejar de invertir o consumir, o hacerlo con mayor cautela. Esto hace que los bancos centrales instrumenten como medida para paliar shocks económicos la manipulación forzada de las tasas de interés y el año 2020 no fue contrario a esta tradición. La crisis sanitaria provocada por el SARS-COVID-2 provocó una contracción en la actividad económica y la demanda general de forma sostenida lo que llevó a los Bancos centrales a disminuir las tasas de interés lo que provocaría un abaratamiento del crédito y del apalancamiento financiero, haciendo correr flujos de dinero y capital por la economía, fomentando así la inversión y el consumo. No obstante, un riesgo primordial en este tipo de medidas es la inflación: esta se dispara cuando la cantidad de bienes y servicios se mantiene igual en relación a la cantidad de masa monetaria en circulación. De forma tal que si existen 100 onzas de oro en una economía y el precio de 1 kg de huevo es de 1 onza de oro, si inyectamos de la noche a la mañana otras 100 onzas de oro sin incrementar la oferta el precio del huevo se duplicará de 1 onza de oro por kilo a 2 onzas de oro por kilo. Este efecto provocado por la expansión crediticia no es instantáneo y puede variar el tiempo en el que se ve reflejado. 
""")
st.altair_chart(d, use_container_width=True)

st.markdown("""En la imagen superior podemos observar la tasa de inflación en la economía mexicana en todo el año 2020, año de la pandemia. La cuarentena y las medidas sanitarias comenzaron de manera sólida y coordinada en el país a finales de Marzo y principios de Mayo, lo cual coincide con una bajada en la inflación. Esto se debe a que existía una gran cantidad de oferta en el mercado cuando de pronto la cantidad de demanda se contrajo y los actores desarrollaron una mayor aversión al riesgo atesorando las cantidades de dinero de las que disponían y así, con este ahorro retirando una gran cantidad de masa monetaria de la circulación en el mercado. Esto provocó que la inflación bajará al haber un punto en el tiempo donde la cantidad de oferta no varió en misma proporción que la cantidad de moneda para efectuar los intercambios, existiendo mayor oferta que dinero, abaratando los precios. Es aquí donde entra en juego el banco de méxico bajando las tasas de interés para incentivar el consumo.
""")
st.altair_chart(one, use_container_width=True)

st.markdown("""El banco de méxico observando la situación en China desde diciembre y la evolución de la pandemia en Italia y Europa empezó a anticiparse a un posible shock por lo cual empezó a disminuir la tasa de interés interbancaria tímidamente pero con tendencia clara desde Enero. Con esto buscaba generar un margen de liquidez y apalancamiento financiero a los mercados ante una eventual contracción económica. El problema es que el impacto de la pandemia y las medidas sanitarias fueron desbordantes haciendo que el impacto fuera muy fuerte. Esto hizo que el banco de méxico empezará a bajar las tasas de interés de manera agresiva mes con mes. El efecto inflacionario no espero dada la rápida expansión crediticia y la imperante necesidad de liquidez por parte de los agentes sumado a una contracción en la capacidad productiva por la cuarentena y por tanto, en la oferta general bienes y servicios. Sumado a la aún más agresiva expansión crediticia de la reserva federal de Estados unidos y la fuerte integración de las economías mexicana y americana lo que llevó a que la inflación respondiera de manera rápida.
""")

st.subheader("Indicador Proxy del ecommerce: Producto interno bruto, a precios de mercado - Actividades terciarias: Comercio al por menor")
st.altair_chart(e, use_container_width=True)

st.markdown("""Los efectos de la cuarentena y la pandemia también se ven reflejados en el comercio al por menor. Este sector comprende el último eslabón en la cadena de producción y distribución, es la venta directa de bienes y servicios al consumidor final. Los supermercados, tiendas de ropa, almacenes,  tiendas de conveniencia o el ecommerce entran dentro de esta categoría. Este sector de la economía cayó hasta un 35% en mayo. La tesis que sostiene la relación del valor de las unidades de oferta monetaria en relación a las unidades de demanda y oferta se puede apreciar en la combinación de las siguientes gráficas:
""")
st.altair_chart(one, use_container_width=True)

st.markdown("""La inflación cayó al mismo tiempo que la demanda en el comercio al por menor. En la caída de la inflación no solo va la caída en demanda en este sector sino en toda la economía de manera general más la cautelosa reacción de Banxico sosteniendo en cierto margen la tasa de interés interbancaria. 
""")

st.markdown("""La tesis de la relación de la actividad económica y el gasto se puede apreciar en la siguiente grafica: """)
st.altair_chart(two, use_container_width=True)
st.markdown("""El efecto de la intensa bajada de interés provocó una inundación de crédito y liquidez en los mercados financieros, que rápidamente permeó hasta el comercio al por menor tanto por el lado de la oferta y de la demanda haciendo que este recuperara casi su nivel en julio. Las posteriores bajadas porcentuales en la tasa de interés que siguieron en el año llevaron a superar las ventas del mes de enero en el mes de octubre pasando de 2,225,643 pesos a 2,579,874.2.
""")

st.subheader("Conclusion")
st.altair_chart((z), use_container_width=True)
st.markdown("""1.  El shock económico y la contracción repentina de la demanda provocó una subida en el valor de las unidades monetarias (baja la inflación) ya que se postergó el consumo presente buscando atesorar, osea ahorrar, la mayor cantidad de dinero posible para poseer liquidez y financiación ante la incertidumbre del futuro económico.
    
2.  Reservar liquidez y ahorrar implica para los agentes económicos como las familias la restricción del consumo, siendo los sectores más cercanos a este como el comercio al por menor y el **ecommerce** los más afectados.
    
3.  El banco de México buscando mitigar los efectos adversos sobre la economía abarató el crédito buscando generar liquidez e incrementar la oferta monetaria disponible para las transacciones en el mercado. Esto resultó en el efecto deseado de alcanzar a las familias y el consumidor mexicano recuperando y superando posteriormente las ventas en el comercio al por menor pero como efecto adverso trajo una inflación disparada. Dicho de otra forma, se incrementó el nivel de venta en este sector y se elevaron sus precios como mecanismo de ajuste entre la demanda y la oferta.
    
4.  Esto tiene un impacto directo en el **objetivo** y en el **Flying Wheel** de Amazon de bajar los precios. Las presiones inflacionarias sobre Amazon hacen necesario redoblar esfuerzos en bajar los precios identificando nuevas oportunidades de optimización en el modelo de negocio, en la cadena de producción, en la estructura de organización interna y en el aprovechamiento de la división del conocimiento y la generación de nueva información y líneas de negocio.""")


# 'date': ["01/01/2021","01/02/2021","01/03/2021","01/04/2021","01/05/2021","01/06/2021","01/07/2021","01/08/2021","01/09/2021","01/10/2021","01/11/2021","01/12/2021"],
# 'serie': ['Tasa objetivo','Tasa objetivo', 'Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo', 'Tasa objetivo'],
# 'value': [5, 5.3, 4.5, 5, 10, 2, 1, 10, 5, 8, 3, 6]