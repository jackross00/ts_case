from stage import *
from standardize import *
from load import *

###### Staging ######

stg_website_visits(file='website-visits')
stg_brand_healthyfeet(file='brand-performance-healthyfeet')
stg_brand_runnation(file='brand-performance-runnation')
stg_brand_sneakerheads(file='brand-performance-sneakerheads')


###### Standardize ######

std_website_visits()
std_brand_sneakerheads()
std_brand_healthyfeet()
std_brand_runnation()

###### Load ######

load_website_visits()
load_brand_sneakerheads()
load_brand_healthyfeet()
load_brand_runnation()