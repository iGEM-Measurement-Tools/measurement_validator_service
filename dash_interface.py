import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent as d

import igem_dataset
import octave_validation
import lxml.etree as etree

# Init app
# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "iGEM Measurement Validator"

################################################
# styles: for right side report component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


def layout():
    return html.Div([
        #########################
        # Storage for the key backing data
        dcc.Store(id='igem-dataset'),
        #########################
        # Title & icon on top
        html.Div(children=[
            html.Div(className="two columns",
                children=[html.Img(src='https://igem.org/wiki/images/c/cf/Igem_icon.svg',height='70px')]),
            html.Div(className="eight columns",
                     children=[html.H1("iGEM Measurement Validator",style={'color':'forestgreen'})])],
            className="row",
            style={'textAlign': 'center'}),
        # Main panels
        html.Div(
            className="row",
            children=[
                #########################
                # Left side panels
                html.Div(
                    className="two columns",
                    children=[
                        dcc.Markdown(d("""
                            **Reference Links**
                            
                            - [Measurement Hub](https://2020.igem.org/Measurement)
                            - Recommended Protocols:
                              * [Plate Reader Fluorescence Calibration (v3)](https://dx.doi.org/10.17504/protocols.io.6zrhf56)
                              * [Plate Reader Abs600 Calibration (v2)](https://dx.doi.org/10.17504/protocols.io.549g8z6)
                              * [Flow Cytometry Fluorescence Calibration (v1)](https://dx.doi.org/10.17504/protocols.io.2pcgdiw)
                            - [Registry of Standard Parts](http://parts.igem.org/)
                            - [iGEM Main Website](https://igem.org/)
                            """),
                            style={'height': '400px', 'border': '1px darkgrey solid'}),
                        dcc.Markdown(d("""
                            *Controls panel to be developed*
                            """),
                            style={'height': '200px', 'border': '1px darkgrey solid'})],
                ),

                #########################
                # Center upload controls and graph
                html.Div(
                    className="seven columns",
                    children=[
                        dcc.Upload(children=html.Div(['Drag and Drop or ',html.A('Select Files')]),
                            id="dataset-upload",
                            style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                   'borderWidth': '1px', 'borderStyle': 'dashed',
                                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
                            multiple=False,  # only one file can be selected, for now
                        ),
                        html.Div([
                             'Protocol: ',
                             dcc.Dropdown(id='protocol-id', options=octave_validation.protocol_catalog(), value=None,
                                          style={'width': '300px', 'vertical-align': 'middle',
                                                 'display': 'inline-block'}),
                             html.P(id='protocol-auto', children='',
                                    style={'width':'200px', 'font-style': 'italic', 'display': 'inline-block', 'textAlign': 'center'})]
                        ),
                        dcc.Markdown(d("""
                            *Graphical panels to be developed*
                            """)),
                            html.Pre(id='values-dummy', style=styles['pre'])]
                ),

                #########################
                # Right side results display
                html.Div(
                    className="three columns",
                    children=[
                        html.Div(
                            children=[
                                dcc.Markdown(d("""
                                **Report object goes below**

                                *Should also have copy, badge materials*
                                """)),
                                html.Pre(id='validation-report', style=styles['pre'])
                            ],
                            style={'height': '600px', 'border': '1px darkgrey solid'}
                        )
                    ]
                )
            ]
        ),

        #########################
        # Bottom matter, for copyright, linking to GitHub issues, etc.
        html.Div([html.A(['Problems? Report an issue on GitHub'],href='https://github.com/iGEM-Measurement-Tools/measurement_validator_service/issues')],
                 className="row",
                 style={'textAlign': "center"}),
    ])

def define_callbacks():
    # Loading triggers creation and storage of the dataset
    @app.callback(
        [dash.dependencies.Output('igem-dataset', 'data'),
         dash.dependencies.Output('dataset-upload', 'children')],
        [dash.dependencies.Input('dataset-upload', 'contents'),
         dash.dependencies.Input('dataset-upload', 'filename')])
    def load_file(contents, filename):
        if contents:
            content_type, content_string = contents.split(',')
            return igem_dataset.upload_file(base64.b64decode(content_string)), filename
        else:
            return None, html.Div(['Drag and Drop or ',html.A('Select Files')])

    # Loading triggers an attempt to autodetect protocol
    @app.callback(
        [dash.dependencies.Output('protocol-id', 'value'),
        dash.dependencies.Output('protocol-auto', 'children')],
        [dash.dependencies.Input('igem-dataset', 'data')],
        [dash.dependencies.State('protocol-id', 'value')])
    def autodetect_protocol(filename, cur_protocol):
        if filename:
            autodetected = octave_validation.autodetect_protocol(filename)
            if autodetected:
                return autodetected, html.P("Automatically detected",style={'color':'darkgreen'})
            else:
                return cur_protocol, html.P("Cannot detect protocol",style={'color':'lightgrey'})
        else:
            return cur_protocol, ''

    # Having a dataset and a protocol selected triggers analysis
    @app.callback(
        [dash.dependencies.Output('validation-report', 'children'),
         dash.dependencies.Output('values-dummy', 'children')],
        [dash.dependencies.Input('igem-dataset', 'data'),
         dash.dependencies.Input('protocol-id', 'value')])
    def process_file(filename, protocol):
        if filename and protocol:
            result = octave_validation.validate(filename, protocol)
            # in the future, will put the values into graphs as well
            return result['report'],result['value']
        else:
            return None, None


def initialize_app():
    app.layout = layout()
    define_callbacks()


def boot():
    initialize_app()
    app.run_server(debug=True,port=5000) # should figure out a proper way to set the port

if __name__ == '__main__':
    boot()


