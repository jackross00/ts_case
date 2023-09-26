# ts_case

This is a very light-weight Data Warehouse using the Datavault methodology utilizing just Postgres, Pandas, and SQLAlchemy.

1. Setup the correct database by using docker compose up in the current directory
2. PIP INSTALL the requirements using python3
3. Execute the init.sql
4. Simple run python3 master_run.py and the data pipeline will run in seconds

If you would like to learn more about the DataVault methodology please read data_warehouse_method.txt.

This database has rerun-ability, as well as updating records should any of them change, with error handling should anything arise during the staging/standardizing steps. 

Directory Tree:

│   data_warehouse_method.txt
│   Dockerfile
│   master_run.py
│   requirements.txt
│
├───data
│       brand-performance-healthyfeet.csv
│       brand-performance-runnation.csv
│       brand-performance-sneakerheads.csv
│       website-visits.csv
│
├───ddl
│       init.sql
│
├───load
│   │   load_brand_healthyfeet.py
│   │   load_brand_runnation.py
│   │   load_brand_sneakerheads.py
│   │   load_website_visits.py
│   │   __init__.py
│
├───logs
│       readme.txt
│
├───stage
│   │   stg_brand_healthyfeet.py
│   │   stg_brand_runnation.py
│   │   stg_brand_sneakerheads.py
│   │   stg_website_visits.py
│   │   __init__.py
│
├───standardize
│   │   std_brand_healthyfeet.py
│   │   std_brand_runnation.py
│   │   std_brand_sneakerheads.py
│   │   std_website_visits.py
│   │   __init__.py
│
└───utility
    │   chars.py
    │   db.py
    │   __init__.py
