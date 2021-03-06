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

st.title("??Por qu?? Amazon deber??a preocuparse por las tasas de inter??s?")
st.header("Efectos de la tasa de inter??s interbancaria sobre el comercio al por menor en M??xico")
st.altair_chart((z), use_container_width=True)

st.subheader('El dinero y el desempe??o economico')
st.caption('"El sistema de precios es un instrumento registrador que autom??ticamente recoge todos los efectos relevantes de las acciones individuales. Sus indicaciones son la resultante de todas estas decisiones individuales y, al mismo tiempo, su gu??a." -Friedrick August Von Hayek')


st.markdown("""Siendo el dinero un medio econ??mico de intermediaci??n para el intercambio indirecto de otros bienes y servicios, este se ve sujeto a las mismas leyes de oferta y demanda que todos los dem??s bienes y servicios. A medida que una econom??a se desarrolla y su sociedad, el nivel de complejidad y cantidad de las transacciones en dicha econom??a incrementa. Se terminan desarrollando mecanismos e instituciones para la coordinaci??n espacial y temporal de los agentes econ??micos siendo los bancos, las tasas de inter??s y los mercados financieros ejemplos paradigm??ticos. Los bancos que funcionan para coordinar el esfuerzo de ahorradores, inversores y emprendedores median y canalizan los flujos de efectivo de un lugar a otro junto con la tasa de inter??s como mecanismo para coordinar a los agentes a trav??s del tiempo, indicando cu??ndo ahorrar y disminuir el consumo, cuando invertir lo ahorrado o cuando gastar y consumir. 

De esta forma la tasa de inter??s interbancaria controlada por BANXICO es la batuta que instrumenta a todo el sistema financiero para funcionar a un ritmo u otro. Luego del sistema financiero los flujos de cr??dito permean a las dem??s industrias y rincones de los mercados teniendo un efecto en cascada y paulatino que termina por afectar las actividades de cualquier persona. El ecommerce y el comercio al por menor no es la excepci??n y la manipulaci??n de la tasa de inter??s puede tener efectos adversos o positivos en estos sectores como veremos a continuaci??n.
""")
st.altair_chart(c, use_container_width=True)
with st.expander("Pie de grafica"):
    st.markdown("""
            *La grafica de arriba muestra la tasa de interes - que representa la relaci??n de valor entre bienes persentes contra bienes futuros - de todo el a??o 2020. Datos obtenidos del API del Sistema de informaion economica de **BANXICO** [(ver c??digo)](https://github.com/SantiagoSF/BANXICO-Indicators)*
    """)


st.markdown("""La tasa de inter??s interbancaria representa la relaci??n de preferencias temporales de los agentes econ??micos entre la oferta de bienes y servicios presentes contra la oferta de bienes y servicios futuros. Una baja tasa de inter??s representa una menor aversi??n al riesgo y una disposici??n al sacrificio del consumo presente a cambio de un consumo mayor en el futuro. En otras palabras: una baja tasa de inter??s indica a los actores econ??micos que pueden incrementar el gasto corriente e invertir en proyectos empresariales a futuro para obtener beneficios. Por contraparte una alta tasa de inter??s indica una mayor aversi??n al riesgo y una mayor tasa de preferencia temporal por bienes presentes que futuros, indicando a los agentes que deben dejar de invertir o consumir, o hacerlo con mayor cautela. Esto hace que los bancos centrales instrumenten como medida para paliar shocks econ??micos la manipulaci??n forzada de las tasas de inter??s y el a??o 2020 no fue contrario a esta tradici??n. La crisis sanitaria provocada por el SARS-COVID-2 provoc?? una contracci??n en la actividad econ??mica y la demanda general de forma sostenida lo que llev?? a los Bancos centrales a disminuir las tasas de inter??s lo que provocar??a un abaratamiento del cr??dito y del apalancamiento financiero, haciendo correr flujos de dinero y capital por la econom??a, fomentando as?? la inversi??n y el consumo. No obstante, un riesgo primordial en este tipo de medidas es la inflaci??n: esta se dispara cuando la cantidad de bienes y servicios se mantiene igual en relaci??n a la cantidad de masa monetaria en circulaci??n. De forma tal que si existen 100 onzas de oro en una econom??a y el precio de 1 kg de huevo es de 1 onza de oro, si inyectamos de la noche a la ma??ana otras 100 onzas de oro sin incrementar la oferta el precio del huevo se duplicar?? de 1 onza de oro por kilo a 2 onzas de oro por kilo. Este efecto provocado por la expansi??n crediticia no es instant??neo y puede variar el tiempo en el que se ve reflejado. 
""")
st.altair_chart(d, use_container_width=True)

st.markdown("""En la imagen superior podemos observar la tasa de inflaci??n en la econom??a mexicana en todo el a??o 2020, a??o de la pandemia. La cuarentena y las medidas sanitarias comenzaron de manera s??lida y coordinada en el pa??s a finales de Marzo y principios de Mayo, lo cual coincide con una bajada en la inflaci??n. Esto se debe a que exist??a una gran cantidad de oferta en el mercado cuando de pronto la cantidad de demanda se contrajo y los actores desarrollaron una mayor aversi??n al riesgo atesorando las cantidades de dinero de las que dispon??an y as??, con este ahorro retirando una gran cantidad de masa monetaria de la circulaci??n en el mercado. Esto provoc?? que la inflaci??n bajar?? al haber un punto en el tiempo donde la cantidad de oferta no vari?? en misma proporci??n que la cantidad de moneda para efectuar los intercambios, existiendo mayor oferta que dinero, abaratando los precios. Es aqu?? donde entra en juego el banco de m??xico bajando las tasas de inter??s para incentivar el consumo.
""")
st.altair_chart(one, use_container_width=True)

st.markdown("""El banco de m??xico observando la situaci??n en China desde diciembre y la evoluci??n de la pandemia en Italia y Europa empez?? a anticiparse a un posible shock por lo cual empez?? a disminuir la tasa de inter??s interbancaria t??midamente pero con tendencia clara desde Enero. Con esto buscaba generar un margen de liquidez y apalancamiento financiero a los mercados ante una eventual contracci??n econ??mica. El problema es que el impacto de la pandemia y las medidas sanitarias fueron desbordantes haciendo que el impacto fuera muy fuerte. Esto hizo que el banco de m??xico empezar?? a bajar las tasas de inter??s de manera agresiva mes con mes. El efecto inflacionario no espero dada la r??pida expansi??n crediticia y la imperante necesidad de liquidez por parte de los agentes sumado a una contracci??n en la capacidad productiva por la cuarentena y por tanto, en la oferta general bienes y servicios. Sumado a la a??n m??s agresiva expansi??n crediticia de la reserva federal de Estados unidos y la fuerte integraci??n de las econom??as mexicana y americana lo que llev?? a que la inflaci??n respondiera de manera r??pida.
""")

st.subheader("Indicador Proxy del ecommerce: Producto interno bruto, a precios de mercado - Actividades terciarias: Comercio al por menor")
st.altair_chart(e, use_container_width=True)

st.markdown("""Los efectos de la cuarentena y la pandemia tambi??n se ven reflejados en el comercio al por menor. Este sector comprende el ??ltimo eslab??n en la cadena de producci??n y distribuci??n, es la venta directa de bienes y servicios al consumidor final. Los supermercados, tiendas de ropa, almacenes,  tiendas de conveniencia o el ecommerce entran dentro de esta categor??a. Este sector de la econom??a cay?? hasta un 35% en mayo. La tesis que sostiene la relaci??n del valor de las unidades de oferta monetaria en relaci??n a las unidades de demanda y oferta se puede apreciar en la combinaci??n de las siguientes gr??ficas:
""")
st.altair_chart(one, use_container_width=True)

st.markdown("""La inflaci??n cay?? al mismo tiempo que la demanda en el comercio al por menor. En la ca??da de la inflaci??n no solo va la ca??da en demanda en este sector sino en toda la econom??a de manera general m??s la cautelosa reacci??n de Banxico sosteniendo en cierto margen la tasa de inter??s interbancaria. 
""")

st.markdown("""La tesis de la relaci??n de la actividad econ??mica y el gasto se puede apreciar en la siguiente grafica: """)
st.altair_chart(two, use_container_width=True)
st.markdown("""El efecto de la intensa bajada de inter??s provoc?? una inundaci??n de cr??dito y liquidez en los mercados financieros, que r??pidamente perme?? hasta el comercio al por menor tanto por el lado de la oferta y de la demanda haciendo que este recuperara casi su nivel en julio. Las posteriores bajadas porcentuales en la tasa de inter??s que siguieron en el a??o llevaron a superar las ventas del mes de enero en el mes de octubre pasando de 2,225,643 pesos a 2,579,874.2.
""")

st.subheader("Conclusion")
st.altair_chart((z), use_container_width=True)
st.markdown("""1.  El shock econ??mico y la contracci??n repentina de la demanda provoc?? una subida en el valor de las unidades monetarias (baja la inflaci??n) ya que se posterg?? el consumo presente buscando atesorar, osea ahorrar, la mayor cantidad de dinero posible para poseer liquidez y financiaci??n ante la incertidumbre del futuro econ??mico.
    
2.  Reservar liquidez y ahorrar implica para los agentes econ??micos como las familias la restricci??n del consumo, siendo los sectores m??s cercanos a este como el comercio al por menor y el **ecommerce** los m??s afectados.
    
3.  El banco de M??xico buscando mitigar los efectos adversos sobre la econom??a abarat?? el cr??dito buscando generar liquidez e incrementar la oferta monetaria disponible para las transacciones en el mercado. Esto result?? en el efecto deseado de alcanzar a las familias y el consumidor mexicano recuperando y superando posteriormente las ventas en el comercio al por menor pero como efecto adverso trajo una inflaci??n disparada. Dicho de otra forma, se increment?? el nivel de venta en este sector y se elevaron sus precios como mecanismo de ajuste entre la demanda y la oferta.
    
4.  Esto tiene un impacto directo en el **objetivo** y en el **Flying Wheel** de Amazon de bajar los precios. Las presiones inflacionarias sobre Amazon hacen necesario redoblar esfuerzos en bajar los precios identificando nuevas oportunidades de optimizaci??n en el modelo de negocio, en la cadena de producci??n, en la estructura de organizaci??n interna y en el aprovechamiento de la divisi??n del conocimiento y la generaci??n de nueva informaci??n y l??neas de negocio.""")


# 'date': ["01/01/2021","01/02/2021","01/03/2021","01/04/2021","01/05/2021","01/06/2021","01/07/2021","01/08/2021","01/09/2021","01/10/2021","01/11/2021","01/12/2021"],
# 'serie': ['Tasa objetivo','Tasa objetivo', 'Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo','Tasa objetivo', 'Tasa objetivo'],
# 'value': [5, 5.3, 4.5, 5, 10, 2, 1, 10, 5, 8, 3, 6]