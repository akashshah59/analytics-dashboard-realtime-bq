import dash
import dash_html_components as html
import dash_core_components as dcc
from google.cloud import bigquery
from dash.dependencies import Output, State, Input


object_list = ["involved_party","financial_market_instrument","transaction","exchange_rate","positions","portfolio"]
plot_type_list = ['multi-line','multi-bar','cigar-bar','stacked-bar','pie','bubble']
color_list = ['Green','Magenta','Blue','Brown','Purple','Yellow','Red','Orange']
#html.Br(),
#        html.Div([
#            html.Label("CREATE INSIGHTS"
#                )],
#            style = {'width':'120%','textAlign':'center','font-size':'x-large','color':'white'}
#        ),

dataObjects = []
for obj in object_list:
    obj_dict = {}
    obj_dict['label'] = obj
    obj_dict['value'] = obj
    dataObjects.append(obj_dict)

plot_type = []
for obj in plot_type_list:
    obj_dict = {}
    obj_dict['label'] = obj
    obj_dict['value'] = obj
    plot_type.append(obj_dict) 

color = []
for obj in color_list:
    obj_dict = {}
    obj_dict['label'] = obj
    obj_dict['value'] = obj
    color.append(obj_dict)

def SQL():
    sqlDiv =  html.Div([
		html.Br(),
                dcc.Textarea(		
			id='sql-query',
			placeholder='Enter SQL Query',
                        style={'width':'132%'}

		),
		html.Div([
        		dcc.Link(id = 'query-visual',children = [html.Button('NEXT >>',id='button-visual',style = {'background-color':'#FEBD69','color':'#232F3E','text-align':'center','margin-left':'100px'})],href='/visualmenu') 
   		])],style = {'padding-left':'25px','padding-right':'105px'})
    return sqlDiv




def createMenu():
    menuDiv = html.Div([
        
        html.Br(),
        html.Div([
        dcc.Dropdown(
            id='object-dropdown',
            options=dataObjects,
            placeholder="SELECT OBJECT"
        )],
        style = {'width':'140%'}
        ),
                 html.Div([
        dcc.Textarea(
        id = 'formula',
        placeholder='ENTER FORMULA',
        style={'width':'140%'}
        )],

        style = {'marginTop':20,'marginBottom':20}
        
        ),

        html.Div([

        dcc.Dropdown(
            id='condition-dropdown',
            options=[],
            placeholder="SELECT CONDITION",
            style = {'border-color':'#232F3E'}
        ),

        dcc.Dropdown(
            id='comparison-dropdown',
            options=[
                {'label': '<', 'value': '<'},
                {'label': '<=', 'value': '<='},
                {'label': '>', 'value': '>'},
                {'label': '>=', 'value': '>='},
                {'label': '=', 'value': '='},
                {'label': '!=', 'value': '!='},
                {'label':'in','value':'in'},
                {'label':'not in','value':'not in'}
            ],
            value='==',
            style = {'border-color':'#232F3E'}
        ),

        dcc.Textarea(
            id='value-textarea',
            placeholder='ENTER VALUE:',
        style= {'width':'100%','border-color':'#232F3E'}
        )
        ],
        style = {'display':'inline-block','width':'140%'}
        ),
        
        html.Div([
        dcc.Dropdown(
            id='groupby-dropdown',
            options=[],
            placeholder='GROUP BY?',
            multi=True
        )],
        style = {'marginTop':20,'marginBottom':20,'vertical-align':'top','width':'140%'}
        ),

        html.Div([
        dcc.Dropdown(
            id='orderby-dropdown',
            options=[],
            placeholder="ORDER BY?"
        )],
        style = {'marginTop':20,'marginBottom':20,'vertical-align':'top','width':'140%'}
        ),
        
        html.Div([
        dcc.RadioItems(
            id = 'radio',
        options=[
            {'label': 'ASC', 'value': 'ASC'},
            {'label': 'DESC', 'value': 'DESC'},
            ],
        labelStyle = {'display' :'inline-block','color':'white'}),
        ],
        style = {'marginTop':20,'marginBottom':20,'vertical-align':'top','width':'140%'}
        ),

    html.Div([
        dcc.Link(id = 'next',children = [html.Button('NEXT >>',id='button',style = {'background-color':'#FEBD69','color':'#232F3E','text-align':'center','margin-left':'70px'})],href='/visualmenu')
    ])],
  style = {'padding-left':'25px','padding-right':'105px'})
    return menuDiv

def createVisual():
    visualDiv = html.Div([
    
   	html.Br(),
    	html.Div([
    	dcc.Dropdown(
        	id='plot-type-dropdown',
         	options=plot_type,
       	 	placeholder="Select plot type"
    	)],
    	style = {'width':'100%'}
    	),
    
    	html.Div([
    	html.Div(dcc.Dropdown(
        	id = 'x-axis',
                options = [],
       	 	placeholder='X-AXIS',
                style={'border-color':'#232F3E'}
    
    	)),
    	html.Div(dcc.Dropdown(
        	id = 'y-axis',
       	 	placeholder='Y-AXIS',
                options = [],
                style={'border-color':'#232F3E'}
    
    	)),
	html.Div(dcc.Dropdown(
        	id = 'z-axis',
        	placeholder='Z-AXIS',
                options = [],
                style={'border-color':'#232F3E'}
 
    	))],
        style = {'marginTop':20,'className':'three columns','width':'30%'}
    	),

  
    	html.Div([
    	dcc.Dropdown(
        	id='groupby-textarea',
        	placeholder='GROUP BY?',
                options = [],
                style={'width':'100%'}
    	)],
        style = {'marginTop':20,'marginBottom':20}
    	),

    	html.Div([
    	dcc.Dropdown(
        	id='color-dropdown',
        	options=color,
        	placeholder="COLOR?"
    	)],
    	style = {'marginTop':20,'marginBottom':20,'vertical-align':'top'}
    	),


    	html.Div([
    	dcc.Textarea(
        	id = 'title',
        	placeholder='Enter title...',
        	style={'width':'100%'}
    
    	)],
	style = {'marginTop':20,'marginBottom':20,'vertical-align':'top'}
    	),

    	html.Div([
    	dcc.Textarea(
        	id = 'legend',
        	placeholder='LEGEND TITLE',
        	style={'width':'100%'}
    
    	)],
	style = {'marginTop':20,'marginBottom':20,'vertical-align':'top'}
    	),
    
    	html.Div([
   	dcc.Textarea(
        	id = 'x-label',
        	placeholder='X-LABEL',
        	style={'width':'100%'}
    
    	)],
	style = {'marginTop':20,'marginBottom':20,'vertical-align':'top'}
    	),

    	html.Div([
   	dcc.Textarea(
        	id = 'y-label',
        	placeholder='Y-LABEL',
        	style={'width':'100%'}
    
    	)],
	style = {'marginTop':20,'marginBottom':20,'vertical-align':'top'}
    	),
    html.Div([
           dcc.Dropdown(
               id='tab-dropdown',
               options=[
                   {'label': '1', 'value': '1'},
                   {'label': '2', 'value': '2'}
               ],
               placeholder = "Select Tab Position.",
               style = {'border-color':'#232F3E'}
       ),
       dcc.Dropdown(
           id='thumbnail-dropdown',
           options=[
               {'label': '1', 'value': '1'},
               {'label': '2', 'value': '2'},
               {'label': '3', 'value': '3'},
               {'label': '4', 'value': '4'},
               {'label': '5', 'value': '5'},
               {'label': '6', 'value': '6'},
               {'label': '7', 'value': '7'},
               {'label': '8', 'value': '8'},
           ],
           placeholder = "Select Thumbnail Position"
       )],
       style = {'marginBottom':20,'width':'100%','border-color':'#232F3E'}
       
       ),
        html.Div([
            dcc.Link(html.Button('SUBMIT CHANGE',id='submit-button',style = {'background-color':'#FEBD69','color':'#232F3E','text-align':'center','margin-left':'55px'})
        ,href = '/')])
    
	],
        style = {'padding-left':'25px','width':'85%','padding-right':'15px'})

    return visualDiv





