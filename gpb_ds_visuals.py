import dash 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go
from plotly import plotly as py
from google.cloud import bigquery
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output
from colour import Color
import dash_table


def makeGradient(mappingList,color,dataStructure):
    mappingList = mappingList + ['dummy']
    if dataStructure == 'dict':
        return dict(zip(mappingList,[c.hex_l for c in list(Color(color).range_to(Color("white"),len(mappingList)*2))[:len(mappingList)]])) 
    elif dataStructure == 'list':
        return [c.hex_l for c in list(Color(color).range_to(Color("white"),len(mappingList)*2))[:len(mappingList)]]


def scatterMarkers(valList):
    sumList = sum(valList)
    return [each/sumList*200 for each in valList]

def plotMultiBar(df,x,y,groupBy,color,title,xlabel,ylabel,legend,typeConv):
    if typeConv:
        df = df[df[x].notnull()]
        df[x] = df[x].apply(lambda x: dt.datetime.strptime(x,'%b %Y'))
        xtick = dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True,
                                     ticks ='outside',
                                 tickformat='%b %Y',
                dtick='M1'
            )
    else:
        xtick = dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True,
                                     ticks ='outside'
            )
    try:
        code_type=df[groupBy].unique().tolist()
        colors = makeGradient(code_type,color,'dict')
        data = []
        newdf = pd.DataFrame()
        for t in code_type:
            newdf = df[df[groupBy] == t]
            newdf = newdf.sort_values(by=[x])
            trace = go.Bar(
                x=newdf[x],
                y=newdf[y],
                name= t,
                textfont = dict(size=10),
                marker={'color': colors[t]} )
            data.append(trace)
            layout = go.Layout(
                    title = title,
                    xaxis=xtick,yaxis=dict(title = ylabel ),#'AMOUNT (SUM)'),
            legend = dict(x = 1 , y = 1),
            annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))],
            barmode='group'
            )
        fig = go.Figure(data = data, layout= layout)
        return fig
    except UnboundLocalError:
        print("Error while loading graph. Error in Data frame.")
        return None

def plotMultiLine(df,x,y,groupBy,color,title,xlabel,ylabel,legend,typeConv):
    if typeConv:
        df = df[df[x].notnull()]
        df[x] = df[x].apply(lambda x: dt.datetime.strptime(x,'%b %Y'))
        xtick = dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True,
                                     ticks ='outside',
                                 tickformat='%b %Y',
                dtick='M1'
            )
    else:
        xtick = dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True,
                                     ticks ='outside'
            )
    try:
        code_type=df[groupBy].unique().tolist()
        colors = makeGradient(code_type,color,'dict')
        data = []
        newdf = pd.DataFrame()
        for t in code_type:
            newdf = df[df[groupBy] == t]
            newdf = newdf.sort_values(by=[x])
            trace = go.Scatter(
                x=newdf[x],
                y=newdf[y],
                name= t,
                textfont = dict(size=10),
                marker = {'color': colors[t]},
                line={} )
            data.append(trace)
            layout = go.Layout(
                    title = title,
                    xaxis=xtick,
            yaxis=dict(title = ylabel ),#'AMOUNT (SUM)'),
            legend = dict(x = 1 , y = 1),
            annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))]
            )
        fig = go.Figure(data = data, layout= layout)
        return fig
    except UnboundLocalError:
        print("Please restart the server.")
        return None

def plotCigarBar(df,x,y,groupBy,color,title,xlabel,ylabel,legend,typeConv):
    df = df[df[x].notnull()]
    if typeConv:
        df[x] = df[x].apply(lambda x: dt.datetime.strptime(x,'%b %Y'))
    try:
        code_type=df[groupBy].unique().tolist()
        colors = makeGradient(code_type,color,'dict')
        data = []
        newdf = pd.DataFrame()
        for t in code_type:
            newdf = df[df[groupBy] == t]
            newdf = newdf.sort_values(by=[x])
            trace = go.Bar(
                #Made x as y and y as x.
                x=newdf[x],
                y=newdf[y],
                name= t,
                orientation = 'h',
                marker={'color': colors[t]} )
            data.append(trace)
            layout = go.Layout(
                    title = title,
                    xaxis=dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True
            ),yaxis=dict(title = ylabel ),#'AMOUNT (SUM)'),
            legend = dict(x = 1 , y = 1),
            annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))],
            barmode='stack'
            )
        fig = go.Figure(data = data, layout= layout)
        return fig
    except UnboundLocalError:
        print("Error while plotting graph.")
        return None

def plotStackedBar(df,x,y,groupBy,color,title,xlabel,ylabel,legend,typeConv):
    df = df[df[x].notnull()]
    if typeConv:
        df[x] = df[x].apply(lambda x: dt.datetime.strptime(x,'%b %Y'))
    try:
        code_type=df[groupBy].unique().tolist()
        colors = makeGradient(code_type,color,'dict')
        data = []
        newdf = pd.DataFrame()
        for t in code_type:
            newdf = df[df[groupBy] == t]
            newdf = newdf.sort_values(by=[x])
            trace = go.Bar(
                x=newdf[x],
                y=newdf[y],
                name= t,
                textfont = dict(size=10),
                marker={'color': colors[t]} )
            data.append(trace)
            layout = go.Layout(
                    title = title,
                    xaxis=dict( title = xlabel,#'DATE (BY MONTH)',
                                autorange = True,
                                     ticks ='outside',
                                 tickformat='%b %Y',
            dtick='M1'
            ),yaxis=dict(title = ylabel ),#'AMOUNT (SUM)'),
            legend = dict(x = 1 , y = 1),
            annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))],
            barmode='stack'
            )
        fig = go.Figure(data = data, layout= layout)
        return fig
    except UnboundLocalError:
        print("Error while plotting graph.")
        return None


def plotPie(df,x,groupBy,color,title,legend):
    #Add varargs while coding this.
    #Add to another visualization code file .
    #HardCoding.
    if type(color) == type(None):
        color = 'magenta'
    try:
        x = x.lower()
        groupBy = groupBy.lower()
        color = color.lower()
        textSize=10 
        lbls = df[groupBy].tolist()
        vls = df[x].tolist()
        if vls == []:
            return None
        trace = go.Pie(labels=lbls, values=vls,
                   hoverinfo='label+percent', textinfo='value', 
                   textfont=dict(size=textSize,color = Color("white").hex_l),
                   marker=dict(
                       #colors=makeGradient(df[x].unique().tolist(),color,'list')
                       )                  
                   
                   )
        layout = go.Layout(title = title,
             annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))])
        fig = go.Figure(data=[trace],layout=layout) 
        return fig
    except UnboundLocalError:
        print("Error while plotting graph. Issue in your data frame.")
        return None

def plotBubble(df,x,y,z,groupBy,color,title,xlabel,ylabel,legend,typeConv):
    df = df[df[x].notnull()]
    if typeConv:
        df[x] = df[x].apply(lambda x: dt.datetime.strptime(x,'%b %Y'))
    try:
        code_type=df[groupBy].unique().tolist()
        colors = makeGradient(code_type,color,'list')
        data = []
        newdf = pd.DataFrame()
        text = []
        for i,j,k,m in zip(df[x].tolist(),df[y].tolist(),df[z].tolist(),df[groupBy].tolist()) :
            text.append('Position Credit Accrual Amount   '+str(round(i,2))+'<br>Position Debit Accrual Amount   '+str(round(j,2))+'<br>Position Amount   '+str(round(k,2)) + '<br>Type: ' + str(m))
        trace = go.Scatter(
 	  	 x=df[x].tolist(),
   		 y=df[y].tolist(),
                 text = text,
                 hoverinfo = 'text',
    		 mode='markers',
   		 marker=dict(
                     color = colors,
       		 size=scatterMarkers(df[z].tolist())
                 )
        )
        layout = go.Layout(
                 title = title,
                 xaxis=dict( title = xlabel,#'DATE (BY MONTH)',
                             autorange = True,
                             ticks ='outside'
            ),yaxis=dict(title = ylabel ),#'AMOUNT (SUM)'),
        legend = dict(x = 1 , y = 1),
        annotations=[dict( x=1.15,
                               y=1.15,
                               opacity =1,
                               xref='paper',
                               yref='paper',
                               showarrow = False,
                               text=legend,
                               font = dict(
                               color = "black"))]
            )
        data = [trace]
        fig = go.Figure(data = data,layout=layout)
        return fig
    except UnboundLocalError:
        print("Error while plotting graph.")
        return None

def plotTable(df):

    try:
        trace = go.Table(
        header=dict(values=list(df.columns),
        fill = dict(color='#C2D4FF'),
	align = ['left'] * df.shape[1]),
	cells=dict(values=[df[df.columns[i]] for i in range(0,df.shape[1])],
	fill = dict(color='#F5F8FF'),
	align = ['left'] * df.shape[1]))

        data = [trace]
        fig = go.Figure(data = data)
        return fig
    except UnboundLocalError:
        print("Please restart the server.")
        return None

def plotDashTable(df,identifier,filterBool):
    fixed_rows = 1
    if filterBool == True :
        fixed_rows = 2
    return html.Div(dash_table.DataTable(
    id = identifier,
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
    filtering = filterBool,
    editable = False,
    #row_selectable = 'multi',
    selected_rows = [],
    #pagination_mode="fe",
    #pagination_settings={
    #            "displayed_pages": 1,
    #            "current_page": 0,
    #            "page_size":10} ,                                                            
    #navigation="page",
    n_fixed_rows=fixed_rows,
        css=[{
                    'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
            style_cell={
                        'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                                'maxWidth': 0,
                                                    },
            style_table={'overflowX':'scroll','overflowY':'scroll','height':250}
       ))


def plotDonut(value_dict):
    try:
        fig = {
        "data": [
            {
                "values": value_dict['values'] ,
                "labels": value_dict['labels'],
                "domain": {"column": 0},
                "hoverinfo":"label+percent",
                "hole": .4,
                "type": "pie",
                "marker":{"colors":['green','red']}
        }
        ],
        "layout": {
                
                "annotations": [
                {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text":value_dict['title'], 
                "x": 0.50,
                "y": 0.5
                }
		
        ]
         }
        }
        return fig
    except UnboundLocalError:
        print("Please restart the server.")
        return None



