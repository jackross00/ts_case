import utility.db as db
import utility.chars as chars
import logging
import pandas

def load_website_visits():
    global wh_frame, sat_frame, sat_frame_chg, sat_frame_add
    tbl = 'website_visits'
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
        
        # Load Website Visits Satellite
        sat_frame = db.read_sql(
            """
            
            SELECT b.web_seq,
                a.load_time,
                a.entry_date,
                a.visits,
                CASE
                    WHEN a.visits = c.visits THEN 'UNCHANGED'
                    WHEN c.entry_date IS NOT NULL THEN 'CHANGED'
                    -- We wont handle deleted because we assume web traffic not going away --
                    ELSE 'ADDED'
                END AS change_status
            FROM std_{} a
            LEFT JOIN hub_website b 
            on a.website = b.web_bk
            LEFT JOIN sat_website_visits c
            on a.entry_date = c.entry_date
            and b.web_seq = c.web_seq
            
            """.format(tbl,tbl)
        )
        
        # Delete Old Modified Records in Sat, Add New
        sat_frame_chg = sat_frame[sat_frame['change_status'] == 'CHANGED']
        sat_frame_chg.to_sql('sat_{}_chg'.format(tbl),db.open_conn(),if_exists='replace', index=False)
        db.exec_sql(schema='public',cmd=
            """
                DELETE FROM sat_{}
                WHERE web_seq::text||entry_date in (SELECT web_seq::text||entry_date
                                            FROM sat_{}_chg);
                                            
                commit;
                
            """.format(tbl,tbl)
        )
        sat_frame_chg = sat_frame_chg.drop('change_status',axis=1)
        sat_frame_chg.to_sql('sat_{}'.format(tbl),db.open_conn(),if_exists='append', index=False)
        
        # Add New Records
        sat_frame_add = sat_frame[sat_frame['change_status'] == 'ADDED']
        sat_frame_add = sat_frame_add.drop('change_status',axis=1)
        sat_frame_add.to_sql('sat_{}'.format(tbl),db.open_conn(),if_exists='append', index=False)
        
    except Exception as Argument:
        logging.exception('{} failed to load.'.format(tbl))
        return False
    else:
        return True