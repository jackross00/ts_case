import utility.db as db
import utility.chars as chars
import logging
import pandas

def std_website_visits():
    global frame
    tbl = 'website_visits'
    try:
        
        frame = db.read_sql(
        """
        
        SELECT b.web_seq,
               a.date as entry_date,
               a.website,
               a.visits
        FROM STG_{} a
        left join hub_website b
        on a.website = b.website
        
        WHERE a.date IS NOT NULL
        and a.website IS NOT NULL
        
        """.format(tbl,tbl))
        
        # Datatype standardization
        # Doesn't appear to be a need to set strict character limits.
        frame['entry_date'] = frame['entry_date'].astype('datetime64[ns]').dt.normalize()
        frame['visits'] = chars.convert_to_int(frame['visits'])             
        
        # Add our additional columns
        frame['load_time'] = pandas.Timestamp.now()
        
        # Clear standard table and load
        db.exec_sql(schema='public',cmd="truncate std_{}; commit;".format(tbl))
        frame.to_sql('std_{}'.format(tbl),db.open_conn(),if_exists='append', index=False)
    except Exception as Argument:
        logging.exception('{} failed to load.'.format(tbl))
        return False
    else:
        return True