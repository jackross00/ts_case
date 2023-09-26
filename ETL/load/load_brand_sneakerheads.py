import utility.db as db
import utility.chars as chars
import logging
import pandas

def load_brand_sneakerheads():
    global wh_frame, sat_frame, sat_frame_chg, sat_frame_add
    tbl = 'brand_sneakerheads'
    try:
        # Load Website Hub
        wh_frame = db.read_sql(
            """
            
            SELECT distinct website as web_bk,
                            website
            FROM std_{}
            
            WHERE web_seq is null
            AND website not in (SELECT web_bk
                                FROM hub_website)
            
            """.format(tbl)
        )        
        
        wh_frame['load_time'] = pandas.Timestamp.now()
        wh_frame.to_sql('hub_website',db.open_conn(),if_exists='append', index=False)
        
        # Load brand Hub
        wh_frame = db.read_sql(
            """
            
            SELECT distinct brand as brand_bk,
                            brand
            FROM std_{}
            
            WHERE brand_seq is null
            AND brand not in (SELECT brand_bk
                                FROM hub_brand)
            
            """.format(tbl)
        )        
        
        wh_frame['load_time'] = pandas.Timestamp.now()
        wh_frame.to_sql('hub_brand',db.open_conn(),if_exists='append', index=False)   
          
        # Load Metrics Satellite
        sat_frame = db.read_sql(
            """
            
            SELECT  b.web_seq,
                    d.brand_seq,
                    a.load_time,
                    a.entry_date,
                    a.impressions,
                    a.clicks,
                    a.conversions,
                    a.revenue,
                    CASE
                        WHEN a.impressions = c.impressions AND a.clicks = c.clicks AND a.conversions = c.conversions AND a.revenue = c.revenue  THEN 'UNCHANGED'
                        WHEN c.entry_date IS NOT NULL THEN 'CHANGED'
                        ELSE 'ADDED'
                    END AS change_status
            FROM std_{} a
            LEFT JOIN hub_website b 
            on a.website = b.web_bk
            LEFT JOIN hub_brand d
            on a.brand = d.brand_bk
            LEFT JOIN sat_metrics c
            on a.entry_date = c.entry_date
            and b.web_seq = c.web_seq
            and d.brand_seq = c.brand_seq
            
            """.format(tbl)
        )
        
        # Delete Old Modified Records in Sat, Add New
        sat_frame_chg = sat_frame[sat_frame['change_status'] == 'CHANGED']
        sat_frame_chg.to_sql('sat_metrics_chg'.format(tbl),db.open_conn(),if_exists='replace', index=False)
        db.exec_sql(schema='public',cmd=
            """
                DELETE FROM sat_metrics
                WHERE web_seq::text||brand_seq::text||entry_date in (SELECT web_seq::text||brand_seq::text||entry_date
                                                                     FROM sat_metrics_chg);
                                            
                commit;
                
            """
        )
        sat_frame_chg = sat_frame_chg.drop('change_status',axis=1)
        sat_frame_chg.to_sql('sat_metrics'.format(tbl),db.open_conn(),if_exists='append', index=False)
        
        # Add New Records
        sat_frame_add = sat_frame[sat_frame['change_status'] == 'ADDED']
        sat_frame_add = sat_frame_add.drop('change_status',axis=1)
        sat_frame_add.to_sql('sat_metrics'.format(tbl),db.open_conn(),if_exists='append', index=False)
    except Exception as Argument:
        logging.exception('{} failed to load.'.format(tbl))
        return False
    else:
        return True