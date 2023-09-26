import utility.db as db
import utility.chars as chars
import logging
import pandas

def stg_brand_runnation(file=''):
    tbl = 'stg_brand_runnation'
    try:
        # Read csv to pandas frame, all as strings
        frame = pandas.read_csv("./data/{}.csv".format(file), dtype=object, index_col=False)
        
        for i in chars.chars.special_chars: 
            frame.columns = frame.columns.str.replace(' ','')
            frame.columns = frame.columns.str.replace('{}'.format(i),'_',regex=False)
        
        # Clear stage table
        db.exec_sql(schema='public',cmd="truncate {}; commit;".format(tbl))
        
        #Load stage table with frame
        frame.to_sql('{}'.format(tbl),db.open_conn(),if_exists='append', index=False)
    except Exception as Argument:
        logging.exception('{} failed to load.'.format(tbl))
        return False
    else:
        return True