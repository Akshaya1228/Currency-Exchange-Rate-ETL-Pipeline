def df_to_mysql_data_type_conversion(df_data_types):
    l = []
    for i in df_data_types:
        dtype = str(i)

        if 'int' in dtype:
            l.append('INT')

        elif 'float' in dtype:
            l.append('FLOAT')

        elif 'datetime' in dtype:
            l.append('DATETIME')

        elif 'bool' in dtype:
            l.append('BOOLEAN')

        else:
            l.append('VARCHAR(255)')
    return l