import utility.db as db
import utility.chars as chars
import logging
import pandas

def std_brand_sneakerheads():
    global frame
    tbl = 'brand_sneakerheads'
    try:
        
        frame = db.read_sql(
        """
        
        SELECT NULL as web_seq,
               c.brand_seq,
               a.date as entry_date,
               'sneakerheads.com' as website,
               a.brand,
               a.imp as impressions,
               a.clicks,
               a.conv as conversions,
               a.rev as revenue
        FROM STG_{} a
        left join hub_brand c
        on a.brand = c.brand_bk
        
        WHERE a.brand IS NOT NULL
        AND a.date IS NOT NULL
        
        """.format(tbl))
        
        # Datatype standardization
        # Doesn't appear to be a need to set strict character limits.
        frame['entry_date'] = frame['entry_date'].astype('datetime64[ns]').dt.normalize()
        frame['impressions'] = chars.convert_to_int(frame['impressions'])
        frame['clicks'] = chars.convert_to_int(frame['clicks'])
        frame['conversions'] = chars.convert_to_int(frame['conversions'])
        frame['revenue'] = chars.convert_to_int(frame['revenue'])    
        
        # Add our additional columns
        frame['load_time'] = pandas.Timestamp.now()
        
        # Clear standard table and load
        db.exec_sql(schema='public',cmd="truncate std_{};commit;".format(tbl))
        frame.to_sql('std_{}'.format(tbl),db.open_conn(),if_exists='append', index=False)
    except Exception as Argument:
        logging.exception('{} failed to load.'.format(tbl))
        return False
    else:
        return True