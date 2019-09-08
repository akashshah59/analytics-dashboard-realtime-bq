from google.cloud import bigquery
import google.cloud
import urllib
import re


#Configuration File kept somewhere.
event = {
        'projectId':'root-furnace-225703',
        'dataset_id_from' : 'gpb_ds_ukk_transformation'
        }

client = bigquery.Client(event['projectId'])
dataset_id_from = event['dataset_id_from']


def formSelectQuery(row,coreObject):
    #createView = "CREATE VIEW `" +projectId +'.analyticsdataset.'+str(row['object']) +"_kpi_"+str(row['kpi_id']) + "` AS "
    if re.search('select', str(row['formula']), re.IGNORECASE):
        Query = str(row['formula'])
    else :    
        createView = ""
        select = "SELECT " + str(row['formula'])
        grouping = 'GROUP BY ' + str(row['grouping'])
        table_from = " FROM `" +event['projectId'] + ".{}.".format(event['dataset_id_from']) + coreObject +"`"
        orderBy ='ORDER BY ' +  ' '.join(str(row['orderBy']).split(':')) 
        condition = 'WHERE ' + str(row['condition'])
    
        if condition == 'WHERE None':
            condition = ''
        if grouping == 'GROUP BY None':
            grouping = ''
        if orderBy == 'ORDER BY None':
            orderBy = ''
        if select == "SELECT None":
            print("KPI must contain some select columns")

        Query =  createView + select + " " + table_from + " " + condition + " " + grouping +  " " + orderBy
    print(Query) 
    try:
        query_job = client.query(Query)
        df = query_job.result().to_dataframe()
        return df
        print("Successfully calculated KPI...Now visualizing.")
    except google.cloud.exceptions.GoogleCloudError as e:
        if e.code == 409:
            print("KPI Exists")
    except Exception as e :
        print(e)


