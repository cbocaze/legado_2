import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash(__name__,
                external_scripts=["https://platform.linkedin.com/in.js"],
                #external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

app.title = "Legado de Gobierno - Pandemia y recuperación económica"
server = app.server

#bases utilizadas para trabajar
df_imacec_interanual = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Imacec (% interanual) 1997-2021")
df_imacec_desestacionalizado = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Imacec des. índice 1996-2021")
df_recuperacion_economica = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="OECD Recuperación PIB")
df_red_proteccion_social = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="RPS y Población en cuarentena")
df_cobertura_rps = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Cobertura RPS por países")
df_saldos_cuentas_bancarias = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Saldos Cuentas")
df_saldos_morosidad = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Mora Crediticia")
df_caida_y_cobertura_ingresos = pd.read_excel("recuperacion_economica_pandemia.xlsx", sheet_name="Caida y transferencia recursos")

#gráficos
fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Scatter(y=df_imacec_interanual["1.Imacec"], x=df_imacec_interanual["Periodo"], mode="lines"), row=1, col=1)
fig.add_trace(go.Scatter(y=df_imacec_desestacionalizado["1.Imacec"], x=df_imacec_desestacionalizado["Periodo"], mode="lines"), row=1, col=2)

figura_imacec_interanual = px.line(df_imacec_interanual, x="Periodo", y="1.Imacec", title="Variación interanual del Imacec (%). 1997 - 2021" )
figura_imacec_desestacionalizado = px.line(df_imacec_desestacionalizado, x="Periodo", y="1.Imacec", title="Variación interanual del Imacec (%). 1997 - 2021" )
figura_recuperacion = px.bar(df_recuperacion_economica, x="Pais", y="Years to recover", title="Recuperación del PIB (años)", orientation=("v"))




#figura_ingresos_laborales = px.line(df_ingresos_laborales, x="Periodo", y="Ingreso Laboral", title="Ingreso laboral del hogar promedio (moneda 2020). 2010 - 2021" )
#figura_esfuerzo_fiscal = px.bar(df_esfuerzo_fiscal, x="Paises", y="Subtotal (% PIB)", title="Esfuerzo fiscal para enfremtar la pandemia sobre la línea (% del PIB)" )
#figura_rps = px.bar(df_rps, x="Periodo", y=["Préstamo Solidario", "prestaciones del SC", "Bono Covid-19", "IFE", "Bono Clase Media", "Bono a los transportistas", "Bono de $200 mil AFP" ], title="Monto total de transferencias directas a nivel país. 1980 - 2021" )
#figura_poblacion_cuarentena = px.line(df_rps, x="Periodo", y="% de la población en cuarentena", title="Población en cuarentena (%). 2020 - 2021" )
#figura_cobertura = px.bar(df_cobertura, y="Paises", x="Cobertura promedio (% de la población)", title="Cobertura promedio (% de la población*)", orientation="h")


app.layout = html.Div(
    children=[
        dcc.Graph(
            id='example-graph-1',
            figure=figura_imacec_interanual
            ),
        dcc.Graph(
            id='example-graph-2',
            figure=figura_imacec_desestacionalizado
            ),
           dcc.Graph(
            id='example-graph-3',
            figure=fig
            ),
           dcc.Graph(
            id='example-graph-4',
            figure=figura_recuperacion
            ) 
        ]
    )

@app.callback(
    Output("download-pdf", "data"),
    Input("btn_pdf", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "210702 Cinco claves de las ayudas a los hogares del Gobierno durante la Pandemia.pdf"
    )

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')





"""
#gráficos
figura_ocupados = px.line(df_ocupados, x="Periodo", y="Ocupados (miles)", title="Número de ocupados (miles). 2010 - 2021" )
figura_ingresos_laborales = px.line(df_ingresos_laborales, x="Periodo", y="Ingreso Laboral", title="Ingreso laboral del hogar promedio (moneda 2020). 2010 - 2021" )
figura_esfuerzo_fiscal = px.bar(df_esfuerzo_fiscal, x="Paises", y="Subtotal (% PIB)", title="Esfuerzo fiscal para enfremtar la pandemia sobre la línea (% del PIB)" )
figura_rps = px.bar(df_rps, x="Periodo", y=["Préstamo Solidario", "prestaciones del SC", "Bono Covid-19", "IFE", "Bono Clase Media", "Bono a los transportistas", "Bono de $200 mil AFP" ], title="Monto total de transferencias directas a nivel país. 1980 - 2021" )
figura_poblacion_cuarentena = px.line(df_rps, x="Periodo", y="% de la población en cuarentena", title="Población en cuarentena (%). 2020 - 2021" )
figura_cobertura = px.bar(df_cobertura, y="Paises", x="Cobertura promedio (% de la población)", title="Cobertura promedio (% de la población*)", orientation="h")


#-----------------------------------------------------------------------------------------------------#
#código para creación de página
colors = {
    'background': '#111111',
    'text': '#000000'
}

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Pandemia: La peor caída económica en 40 años seguida de la recuperación más rápida", 
                    className="header-title"
                ),
                html.P(
                    children="Después de la peor caída en 40 años se recuperó el nivel de crecimiento previo a la pandemia",
                    className="header-description",
                ),
            ],
            className="header",
        ),
  
        html.Div(
            children='''El Covid-19 llegó a Chile en marzo 2020 afectando directamente los trabajos debido a las medidas
                    sanitarias que tuvieron como consecuencias la paralización total o parcial de las actividades
                    económicas. Según la Encuesta Nacional de Empleo (ENE) entre el trimestre antes de la llegada de
                    la pandemia a Chile (dic-feb 2020) y el punto más bajo (may-jul 2020) se perdieron 1.990.181
                    empleos, equivalente al 22% de los empleos pre-pandemia.''',
            className="texto-central"),
       
        html.Div(children='''
             La única encuesta que mide ingresos durante la pandemia a nivel de hogar es la Encuesta de Ocupación y Desocupación 
de la U. de Chile (EOD), representativa para el Gran Santiago. Según la EOD, el ingreso laboral promedio de los hogares 
llegó a su punto más bajo en junio 2020, con una caída del 32% respecto al nivel pre-pandemia. De esta forma, la ENE y la EOD muestran que en sólo 4 meses el número de ocupados e ingreso laboral de los hogares 
retrocedió al nivel de hace 10 años, dando cuenta del fuerte impacto de la pandemia sobre el mercado laboral.
 
    '''),

        dcc.Graph(
            id='example-graph-1',
            figure=figura_ocupados,
    ),

        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
      
        dcc.Graph(
            id='example-graph-2',
            figure=figura_ingresos_laborales,
    ),
    
        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
    
        dcc.Graph(
            id='example-graph-3',
            figure=figura_esfuerzo_fiscal,
    ),

        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
    
        dcc.Graph(
            id='example-graph-4',
            figure=figura_rps,
    ),
    
        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
    
        dcc.Graph(
            id='example-graph-5',
            figure=figura_poblacion_cuarentena,
    ),
    
        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
    
        dcc.Graph(
            id='example-graph-6',
            figure=figura_cobertura,
    ),
    
        html.Div([html.Script(**{"data-url": "https://platform.linkedin.com/in.js"}, type="IN/Share")]
    ),
    
    html.Button("Descargar estudio completo", id="btn_pdf"), dcc.Download(id="download-pdf"),
        
])


             
@app.callback(
    Output("download-pdf", "data"),
    Input("btn_pdf", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "210702 Cinco claves de las ayudas a los hogares del Gobierno durante la Pandemia.pdf"
    )

if __name__ == '__main__':
    app.run_server(debug=True)
"""