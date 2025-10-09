import pandas as pd
import os
from sqlalchemy import create_engine
import logging


logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s -%(levelname)s -%(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
    '''This function will ingest the dataframe into database table'''
    df.to_sql(table_name,con = engine,if_exists = 'replace',index = 'False')
    
def load_raw_data():
    '''This function will load CSV into dataframe and ingest them into db'''
    start = time.time()
    for file in os.listdir('C:\\Users\\admin\\Documents\\study\\data anlytics\\end to end\\data'):
        if'.csv' in file:
            # print('---',file,'---')
            df = pd.read_csv('C:\\Users\\admin\\Documents\\study\\data anlytics\\end to end\\data\\'+file)
            logging.info(f'Ingesting {file} in db' )
            ingest_db(df,file[:-4],engine)
    end = time.time()
    total_time = (end -start)/60
    logging.info('--------Ingestion complete---------')
    logging.info(f'Total Time Taken: {total_time} ,minutes')

if __name__=='__main__':
    load_raw_data()