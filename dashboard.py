import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import plotly as py
from google.cloud import bigquery
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output, State
import gpb_ds_visuals as visuals
import gpb_ds_analytics_load as analytics
import gpb_ds_kpi_menu as menu
import google.cloud
import dash_bootstrap_components as dbc
import re
import  gpb_ds_evaluate as nnm
import nnm as netNew

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
client = bigquery.Client()


event = {
        'projectId':'root-furnace-225703',
        'dataset_id_from' : 'gpb_ds_ukk_transformation',
        'interval':12*50000,
        'theme':'#232F3E'
        }

app.config.suppress_callback_exceptions = True



nnmDict = netNew.models()
training = nnmDict['trainSet']
test = nnmDict['testSet']

dashboard = html.Div([
dcc.Interval(id='interval-component-main', interval = event['interval'], n_intervals = 0)
    ,html.H1('GPB DATA SERVICES ANALYTICS DASHBOARD',style = {'color':event['theme'],'font-weight':'bold','text-align':'center'}),
    #html.Div(dcc.Link(dcc.RadioItems(id='radio-choose', options=[
    #    {'label': 'Enter SQL', 'value': 'sql','href' : '/kpimenu'},
    #                    {'label': 'KPI manager', 'value': 'kpi_managaer'}
    #]))),
    html.Div(id='option_div'),
    html.Div(dcc.Link(html.Button('Enter SQL query',style = {'background-color':'#FEBD69','color':'#232F3E','font-weight':'bold'}),href='/sqlquery'),style = {'text-align':'center','justify-content':'center'}),
    html.Br(),
    html.Div(dcc.Link(html.Button('Navigate to KPI manager',style = {'background-color':'#FEBD69','color':'#232F3E','font-weight':'bold'}),href='/kpimenu'),style = {'text-align':'center','justify-content':'center'}),
    html.Br(),
    dcc.Tabs(id="tabs", value='Tab1', children=[
        dcc.Tab(label='TRANSACTIONS', id='tab1', value='Tab1', children =[]),
        dcc.Tab(label='POSITIONS AND INVOLVED PARTIES', id='tab2', value= 'Tab2',
            children=[]),
        dcc.Tab(label='NET NEW MONEY', id='tab3', value= 'Tab3',
            children=[dcc.Markdown('''
> ### Training Data
                '''),html.Div(visuals.plotDashTable(training,'training',False)),dcc.Markdown('''
> ### Predictions                   
                    '''),html.Div(visuals.plotDashTable(test,'test',True)),dcc.Markdown('''
> ### Accuracy
                    '''),html.Div(html.Table(id='table-3',
                    children=[html.Tr(children = [html.Td(html.Div(children=[dcc.Graph(id='graph-3-3')])),html.Td(html.Div(children=[dcc.Graph(id='graph-3-4')]))])]))])
        ],style= {'border-radius':'25px'})#,colors={'primary':event['theme'],'background':event['theme'],'border':'white'},vertical = False)
    ],style = {'padding-left':'0px','vertical-align':'top','display':'inline-block','width':'100%'})

app.layout = html.Div([html.Div(id='output_div'),html.Div(id='output_div2'),html.Div(id='visual_div'),dcc.Store(id='memory-data'),
html.Div(
    [dcc.Location('url'),html.Div([html.Div(id='page-content',children = [])])])])
 

@app.callback(
    dash.dependencies.Output('option_div','value'),
    [dash.dependencies.Input('radio-choose','value')])
def navigate_SQL_KPI(selected_option):
    if selected_option == 'sql':
        print('sql')
    
    else :
        print('kpi')
        html.Div(dcc.Link('here',href='/kpimenu'))

thumbnails = {}

def getThumbnailCount():
    Query = '''select CASE WHEN tab_id = 1 THEN 'one' WHEN tab_id = 2 THEN 'two' WHEN tab_id = 3 THEN 'three' WHEN tab_id = 4 THEN 'four' END as tabNo,count(visual_id) as thumbnailCount
   from `root-furnace-225703.gpb_ds_ukk_analytics.gpb_ds_ukk_thumbnail_definition` group by tab_id;'''
    try :
        query_job = client.query(Query)
        kpilist = query_job.result().to_dataframe()
        for index, row in kpilist.iterrows():
            thumbnails[row.tabNo] = row.thumbnailCount
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("Google Cloud Error. (BigQuery)")
    except Exception as e :
        print(e)

def getKPI(kpi_id): 
    table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_kpi_definition'
    Query = "select * from `" + table + "` where kpi_id = " + str(kpi_id)
    try :
        query_job = client.query(Query)
        kpilist = query_job.result().to_dataframe()
        for index, row in kpilist.iterrows():
            return row
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("Google Cloud Error. (BigQuery)")
    except Exception as e :
        print(e)


def getVisualDef(visual_id):
    table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_visual_definition'
    Query = "select * from `" + table + "` where visual_id = " + str(visual_id)
    try :
        query_job = client.query(Query)
        kpilist = query_job.result().to_dataframe()
        for index, row in kpilist.iterrows():
            return row
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("Google Cloud Error. (BigQuery)")
    except Exception as e :
        print(e)


def getThumbnailDef(tab_id,thumbnail_id):
    table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_thumbnail_definition'
    Query = "select * from `" + table + "` where thumbnail_id = " + str(thumbnail_id) + " and tab_id = " + str(tab_id)
    try :
        query_job = client.query(Query)
        kpilist = query_job.result().to_dataframe()
        for index, row in kpilist.iterrows():
            return row
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("Google Cloud Error. (BigQuery)")
    except Exception as e :
        print(e)  

def getFigure(tab_id,thumbnailId):
    thumbnail = getThumbnailDef(tab_id,thumbnailId)
    print(thumbnail)
    if type(thumbnail) == type(None):
        print("Thumbnail Definition not present for thumbnail number " + str(thumbnailId)+ " in tab number " + str(tab_id))
    else:
        kpi = getKPI(thumbnail.kpi_id)
        if type(kpi) == type(None):
            #Ideally Return No Data Found Chart.
            print("KPI not present in definition table for thumbnail number " + str(thumbnailId))
            return None
        
        df = None
        typeConv = None
        if kpi.object != None :
            df = analytics.formSelectQuery(kpi,'gpb_ds_ukk_'+kpi.object+'_clean')
            print('Inside Analytics definition for object {}'.format(str(kpi.object)))  
            if kpi.object == 'transaction':
                typeConv = True
            else:
                typeConv = False
            print(typeConv)
        else :
            df = analytics.formSelectQuery(kpi,'object')
        
        if type(df) == type(None):
            #Ideally return No Data Found Chart.
            #No Data was found, do not go to visualization definition.
            return None
        visual = getVisualDef(thumbnail.visual_id)
        print("Inside visual definition for object {}".format(str(kpi.object)))
        if type(visual) == type(None):
            print("Visual Definition not present for thumbnail number " + str(thumbnailId))
        else:
            if visual.plot_type == "multi-bar":
                return visuals.plotMultiBar(df,visual.x,visual.y,visual.groupBy,visual.color,visual.title,visual.xlabel,visual.ylabel,visual.legend,typeConv)
            elif visual.plot_type == "cigar-bar": 
                return visuals.plotCigarBar(df,visual.x,visual.y,visual.groupBy,visual.color,visual.title,visual.xlabel,visual.ylabel,visual.legend,typeConv)
            elif visual.plot_type == "stacked-bar": 
                return visuals.plotStackedBar(df,visual.x,visual.y,visual.groupBy,visual.color,visual.title,visual.xlabel,visual.ylabel,visual.legend,typeConv)
            elif visual.plot_type == "multi-line": 
                return visuals.plotMultiLine(df,visual.x,visual.y,visual.groupBy,visual.color,visual.title,visual.xlabel,visual.ylabel,visual.legend,typeConv)
            elif visual.plot_type == "pie": 
                return visuals.plotPie(df,visual.x,visual.groupBy,visual.color,visual.title,visual.legend)
            elif visual.plot_type == "bubble":
                print(df)
                return visuals.plotBubble(df,visual.x,visual.y,visual.z,visual.groupBy,visual.color,visual.title,visual.xlabel,visual.ylabel,visual.legend,typeConv)


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kpimenu':
        return html.Div([
        html.Div(
            html.H2("KPI DATA WIZARD"
                ),
            style = {'color':event['theme'],'font-weight':'bold','margin-left':'550px'}
        ),
        html.Div(menu.createMenu(),style = {'visibility':'visible','background-color':event['theme'],'position':'fixed','height':'70%','border-radius':'25px','margin-left':'535px'}) 
])
    elif pathname == '/visualmenu':
        return html.Div([
        html.Div(
            html.H2("VISUAL DATA WIZARD"
                ),
            style = {'color':event['theme'],'font-weight':'bold','margin-left':'550px'}
        ),
        html.Div(menu.createVisual(),style = {'visibility':'visible','background-color':event['theme'],'position':'relative','height':'100%','border-radius':'25px','margin-left':'540px','margin-right':'550px'}) 
])
    elif pathname == '/sqlquery':
        print('sqlQuery!')
        return html.Div([
            html.Div(
                html.H2('SQL Query'),
                style = {'color':event['theme'],'font-weight':'bold','margin-left':'640px'}
                ),
        html.Div(menu.SQL(),style = {'visibility':'visible','background-color':event['theme'],'position':'relative','height':'100%','border-radius':'25px','margin-left':'540px','margin-right':'550px'})
            
        ])        
    else :
        return dashboard


def fetchMaxID(which,**kwargs):
    if which == 'kpi':
        table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_kpi_definition'
        Query = "select max(kpi_id) as maximum from `" + table + "`"
        try :
            query_job = client.query(Query)
            kpilist = query_job.result().to_dataframe()
            for index, row in kpilist.iterrows():
                return row.maximum
        except google.cloud.exceptions.GoogleCloudError as e:
            if e.code == 409:
                print("Google Cloud Error. (BigQuery)")
        except Exception as e :
            print(e)
    elif which == 'visual':
        table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_visual_definition'
        Query = "select max(visual_id) as maximum from `" + table + "`"
        try :
            query_job = client.query(Query)
            kpilist = query_job.result().to_dataframe()
            for index, row in kpilist.iterrows():
                return row.maximum
        except google.cloud.exceptions.GoogleCloudError as e:
            if e.code == 409:
                print("Google Cloud Error. (BigQuery)")
        except Exception as e :
            print(e)
    elif which == 'thumbnail':
        table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_thumbnail_definition'
        Query = "select max(thumbnail_id) as maximum from `" + table + "` where tab_id = " + str(kwargs['tab_id'])
        try :
            query_job = client.query(Query)
            kpilist = query_job.result().to_dataframe()
            for index, row in kpilist.iterrows():
                return row.maximum
        except google.cloud.exceptions.GoogleCloudError as e:
            if e.code == 409:
                print("Google Cloud Error. (BigQuery)")
        except Exception as e :
            print(e)

@app.callback(Output('memory-data', 'data'),[Input('button-visual','n_clicks')],[State('sql-query','value')])
def update_temp(n_clicks,sqlQuery):

    print('inside temp:::::::::::::::::::::::')
    print('here::::',sqlQuery)
    formula = ''
    if sqlQuery != None :
        print("inside if:::::::::::::::::::::::::::")
        sqlQuery.strip('\n')
        sqlQuery = sqlQuery.replace('\n'," ")
        print('.... ',sqlQuery)
        result = re.search('SELECT(.*)FROM',sqlQuery)
        print('here:::::::::::::::::::@@@@@@@@@@@@@@@@@@@              ',result.group(1))
        formula = str(result.group(1))
    print("Formula Entered is: " + formula)
    columnNames = list()
    formula = formula.lower().split(',')
    for each in formula:
        if ' as ' in each:
            columnNames.append(each.rsplit(' as ', 1)[1].strip())
    cNames = columnNames
    print(cNames)
    options = []
    for obj in cNames:
        obj_dict = {}
        obj_dict['label'] = obj
        obj_dict['value'] = obj
        options.append(obj_dict)   
    return {'options':options}

@app.callback(Output('groupby-textarea', 'options'),[Input('plot-type-dropdown', 'value')],[State('memory-data', 'data')])
def update_groupby(value,data):
    return data['options']

@app.callback(Output('x-axis', 'options'),[Input('plot-type-dropdown', 'value')],[State('memory-data', 'data')])
def update_x(value,data):
    return data['options']

@app.callback(Output('y-axis', 'options'),[Input('plot-type-dropdown', 'value')],[State('memory-data', 'data')])
def update_y(value,data):
    return data['options']

@app.callback(Output('z-axis', 'options'),[Input('plot-type-dropdown', 'value')],[State('memory-data', 'data')])
def update_z(value,data):
    return data['options']


#This is a HACK . Come back to this portion of the code.
@app.callback(Output('groupby-dropdown', 'options'),[Input('condition-dropdown', 'value')],[State('memory-data', 'data')])
def update_groupbydrop(value,data):
    return data['options']

@app.callback(Output('orderby-dropdown', 'options'),[Input('condition-dropdown', 'value')],[State('memory-data', 'data')])
def update_orderbydrop(value,data):
    return data['options']

@app.callback(Output('output_div', 'children'),[Input('button', 'n_clicks')],[State('object-dropdown', 'value'),State('formula', 'value'),State('condition-dropdown','value'),State('comparison-dropdown','value'),State('value-textarea','value'),State('groupby-dropdown','value'),State('orderby-dropdown','value'),State('radio','value')])
def update_output(n_clicks,object_dropdown,formula,conditionDropDown,comparisonDropDown,valueTextarea,groupby,orderby,value):
    kpi_id = int(fetchMaxID('kpi')) + 1
    job_config = bigquery.QueryJobConfig()
    table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_kpi_definition'
    columns = ','.join(('kpi_id','object','formula','condition','`grouping`','orderBy'))
   
    l = [str(kpi_id),object_dropdown,formula,str(conditionDropDown) + ' ' + str(comparisonDropDown) + ' '+ str(valueTextarea),str(','.join(groupby)),str(orderby) + ' ' + str(value)] 
    l[1:] = list(map(lambda x: "'" + x + "'",l[1:]))
    print(','.join(l))
    print(','.join(l).strip("\n"))
    Query = "insert into  `" + table + "` (" + str(columns) + ") values (" + ','.join(l) + ")"
    print(Query)
    #try :
    print('try')
    query_job = client.query(Query,job_config = job_config,location='europe-west2')
    print(query_job.result())
    kpilist = query_job.result().to_dataframe()
    for index, row in kpilist.iterrows():
        return row
    print('inserted')
    '''except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("Google Cloud Error. (BigQuery)")
    except Exception as e :
        print(e)'''
    print("Updating KPI Definition Table.")

@app.callback(Output('output_div2','children'),[Input('button-visual','n_clicks')],[State('sql-query','value')])
def update_query(n_clicks,query):
    kpi_id = int(fetchMaxID('kpi')) + 1
    job_config =  bigquery.QueryJobConfig()
    table = event['projectId'] + '.gpb_ds_ukk_analytics.gpb_ds_ukk_kpi_definition'
    columns = ','.join(('kpi_id','object','formula','condition','`grouping`','orderBy'))
    formula = r"'" + query + r"'"
    q = ','.join((str(kpi_id),'null',formula,'null','null','null')) 
    Query = 'Insert into `'+ table + '` (' + str(columns) + ') values (' + q + ')'
    Query.strip('\n')
    Query = Query.replace('\n'," ")
    print('Query::::  '+Query)
    try :
        print('inside try:::::::')
        query_job = client.query(Query,job_config = job_config, location = 'europe-west2')
    
        kpilist = query_job.result().to_dataframe()
        for index, row in kpilist.iterrows():
            return row
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409 :
            print('Google Cloud Error. (BigQuery)')
    except Exception as e :
        print(e)

@app.callback(Output('visual_div','children'),[Input('submit-button','n_clicks')],[State('plot-type-dropdown','value'),State('x-axis','value'),State('y-axis','value'),State('z-axis','value'),State('groupby-textarea','value'),State('color-dropdown','value'),State('title','value'),State('legend','value'),State('x-label','value'),State('y-label','value'),State('tab-dropdown','value'),State('thumbnail-dropdown','value'),State('memory-data','data')])
def update_menu(n_clicks,plot_type_dropdown,x_axis,y_axis,z_axis,groupby_dropdown,color_dropdown,title,legend,x_label,y_label,tab_dropdown,thumbnail_dropdown,columnData):
    print("Column Data is as follows"+ str(columnData))
    visual_id = int(fetchMaxID('visual')) + 1
    table = client.get_table(client.dataset('gpb_ds_ukk_analytics').table('gpb_ds_ukk_visual_definition'))
    visual_row = list()
    kpi_id = str(fetchMaxID('kpi'))
    a = (x_label,kpi_id,plot_type_dropdown,x_axis,y_axis,y_label,groupby_dropdown,color_dropdown,legend,z_axis,None,title,int(visual_id))
    print(a)
    visual_row.append(a)
    errors = client.insert_rows(table,visual_row)
    print("Errors:" , str(errors))
    print("Visual Definition Updated.")

    table  = client.get_table(client.dataset('gpb_ds_ukk_analytics').table('gpb_ds_ukk_thumbnail_definition'))
    thumbnail_row = list()
    if thumbnail_dropdown != None and kpi_id != None and visual_id !=None and tab_dropdown!= None:
        currentThumbnail = int(fetchMaxID('thumbnail',tab_id=tab_dropdown)) + 1
        if currentThumbnail >= int(thumbnail_dropdown):
            thumbnail_dropdown = currentThumbnail
        else:
            print("Already existing KPI what should we do ?")
        a = (int(tab_dropdown),visual_id,kpi_id,int(thumbnail_dropdown))
        print(a)
        thumbnail_row.append(a)
    errors = client.insert_rows(table,thumbnail_row)
    print("Errors:",str(errors))
    print("Updated Thumbnail Definition Table.")

@app.callback(Output('tab1','children'),[Input('interval-component-main','n_intervals')])
def updateEntireTab(n_intervals):
    getThumbnailCount()
    def createTabs(n):
        rows = []
        for i in range(0,n):
            if i%2 == 0:
                row =  html.Tr(children = [html.Td(html.Div(children=[dcc.Graph(id='graph-1-'+str(i+1),figure = getFigure(1,i+1)),
                dcc.Interval(id='interval-component-1-'+str(i+1), interval = event['interval'], n_intervals = 0)])
                ),html.Td(html.Div(children=[dcc.Graph(id='graph-1-'+str(i+2),figure = getFigure(1,i+2)),
                dcc.Interval(id='interval-component-1-'+str(i+2), interval = event['interval'], n_intervals = 0)]))])
                rows = rows + [row]
        return rows

    table  = html.Table(
    id='table-1')
    try:
        nTabs = thumbnails['one']
    except:
        #No KPIs definined for entire tab.
        print("1st Tab does not have any thumbnails defined.")
        return None
    if nTabs == 1:
        return [dcc.Graph(id='graph-1-'+str(nTabs),figure = getFigure(1,nTabs)),dcc.Interval(id='interval-component-1-'+str(nTabs), interval = event['interval'], n_intervals = 0)]
    if nTabs%2 == 0:
        n = nTabs
        rows = createTabs(n)
    else:
        n = nTabs - 1
        rows = createTabs(n)
        rows = rows + [html.Tr(children = [html.Td(html.Div(children=[dcc.Graph(id='graph-1-'+str(nTabs),figure = getFigure(1,nTabs)),dcc.Interval(id='interval-component-1-'+str(nTabs), interval = event['interval'], n_intervals = 0)]),colSpan = '2')])]
    table.children = rows 
    return [html.Div(table)]


@app.callback(Output('tab2','children'),[Input('interval-component-main','n_intervals')])
def updateEntireTab(n_intervals):
    getThumbnailCount()   
    def createTabs(n):
        rows = []
        for i in range(0,n):
            if i%2 == 0:
                row =  html.Tr(children = [html.Td(html.Div(children=[dcc.Graph(id='graph-2-'+str(i+1),figure = getFigure(2,i+1)),
                dcc.Interval(id='interval-component-2-'+str(i+1), interval = event['interval'], n_intervals = 0)])
                ),html.Td(html.Div(children=[dcc.Graph(id='graph-2-'+str(i+2),figure = getFigure(2,i+2)),
                dcc.Interval(id='interval-component-2-'+str(i+2), interval = event['interval'], n_intervals = 0)]))])
                rows = rows + [row]
        return rows

    table  = html.Table(
    id='table-2')
    try:
        nTabs = thumbnails['two']
    except:
        #No thumbnails defined for entiretab.
        print("2nd Tab does not have any thumbnails defined.")
        return None   
    if nTabs == 1:
        print("Only one KPI defined for Tab2")
        return [dcc.Graph(id='graph-2-'+str(nTabs),figure = getFigure(2,nTabs)),dcc.Interval(id='interval-component-2-'+str(nTabs), interval = event['interval'], n_intervals = 0)]
    if nTabs%2 == 0:
        n = nTabs
        rows = createTabs(n)
    else:
        n = nTabs - 1
        rows = createTabs(n)
        rows = rows + [html.Tr(children = [html.Td(html.Div(children=[dcc.Graph(id='graph-2-'+str(nTabs),figure = getFigure(2,nTabs)),dcc.Interval(id='interval-component-2-'+str(nTabs), interval = event['interval'], n_intervals = 0)]),colSpan = '2')])]
    table.children = rows 
    return [html.Div(table)]


@app.callback(Output('graph-3-3', 'figure'),[Input('training', 'derived_virtual_data')])
def input_test(derived_virtual_data):
    if derived_virtual_data is not None:
        currentData = pd.DataFrame(derived_virtual_data)
        correct = currentData['Match'].sum()*100/currentData.shape[0]
        error = 100- correct
    return visuals.plotDonut({'values':[correct,error],'labels':['correct','error'],'title':'Train'})

@app.callback(Output('graph-3-4', 'figure'),[Input('test', 'derived_virtual_data')])
def input_test(derived_virtual_data):
    if derived_virtual_data is not None:
        currentData = pd.DataFrame(derived_virtual_data)
        correct = currentData['Match'].sum()*100/currentData.shape[0]
        error = 100- correct
    return visuals.plotDonut({'values':[correct,error],'labels':['correct','error'],'title':'Test'})



@app.callback(Output('condition-dropdown', 'options'),[Input('object-dropdown', 'value')])
def update_condition(value):
    columnList =[]
    print('The object selected was {}.'.format(str(value).lower()))
    Query = '''SELECT
     column_name 
    FROM
     {}.INFORMATION_SCHEMA.COLUMNS
    WHERE
     table_name="gpb_ds_ukk_{}_clean"'''.format(event['dataset_id_from'].lower(),str(value).lower())
    query_job = client.query(Query)
    results = query_job.result()
    for res in results :
        temp = {}
        temp['label'] = res.values()[0]
        temp['value'] = res.values()[0] 
        columnList.append(temp)
    return columnList





if __name__ == '__main__': app.run_server(host='0.0.0.0',port=8050,debug=True)


