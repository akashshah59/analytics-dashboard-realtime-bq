from google.cloud import bigquery
import google.cloud




def retNnm():
        print("Inside return NNM")
        Query = 'SELECT * FROM `root-furnace-225703.gpb_ds_ukk_kubernetes.nnm_data`'
        event = {
        'projectId':'root-furnace-225703',
        'dataset_id_from' : 'gpb_ds_ukk_transformation'
        }
        client = bigquery.Client(event['projectId'])
        try:
                query_job = client.query(Query)
                df = query_job.result().to_dataframe()
                return df
        except google.cloud.exceptions.GoogleCloudError as e:
                if e.code == 409:
                        print('It exists')
        except Exception as e :
                 print(e)

def retDonut():
        value = {'title':'Donut Chart','values':[[80,20],[90,10]],'labels':[['correct','error'],['correct','error']]}
        return value

