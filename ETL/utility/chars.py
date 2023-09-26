class chars:
    specials_str = ' !@#$%^&*(),./<>?[];'
    special_chars = []
    for i in specials_str:
        special_chars.append(i)
        
    american_currency_str = "$,#"
    american_currency = []
    for i in american_currency_str:
        american_currency.append(i)

def convert_to_int(df=None):
    # Remove any special characters to retain the number if character is found
    df2 = df.str.replace('[^0-9]', '', regex=True).astype('int64')
    return df2

def convert_to_date(df=None):
    df2 = df.astype('datetime64[ns]').dt.normalize()
    return df2

def convert_to_datetime(df=None):
    df2 = df.astype('datetime64[ns]')
    return df2