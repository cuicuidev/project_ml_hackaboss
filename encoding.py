def encode(df, target_series, encoding, custom_encodings):
    df = df.copy()
    
    encodings = {'best', 'brute_force', 'custom'}
    
    if encoding == 'best':
        df, encodings_map = encodeBest(df, target_series)
    elif encoding == 'brute':
        df, encodings_map = encodeBrute(df, target_series)
    elif encoding == 'custom':
        df, encodings_map = encodeCustom(df, target_series, custom_encodings)
    else:
        raise Exception(f'{encoding} is not a valid option. Please chose one from {encodings}')
        
    return df, encodings_map

def encodeBrute():
    raise Exception('brute encoding not implemented')

def encodeBest(df, target):
    return encodeCustom(df, target, getBestEncodings(df, target))

def targetEncoding(df, target, condition):
    """
    Recibe un DataFrame categórico df, una Serie target y una string condition.
    Retorna df con las categorías cambiadas a la mediana o el promedio de la serie target, dependiendo de condition.
    """
    df_target = df.copy()
    df = pd.concat([df_target, pd.DataFrame(target)], axis = 1)
    encodings_map = {}

    for column in df_target.columns:
        if condition == 'target_mean':
            encode = df.groupby(column).mean()[target.name]
            df_target[column] = df_target[column].replace(encode)
            encodings_map[column] = encode
        if condition == 'target_median':
            encode = df.groupby(column).median()[target.name]
            df_target[column] = df_target[column].replace(encode)
            encodings_map[column] = encode
            
    return df_target, encodings_map

def frequencyEncoding(df):
    """
    Recibe un DataFrame categórico df.
    Retorna df con las categorías cambiadas a la frecuencia con la que aparecen.
    """
    df_frequency = df.copy()
    
    encodings_map = {}

    for column in df_frequency.columns:
        encode = df_frequency[column].value_counts()
        df_frequency[column] = df_frequency[column].replace(encode)
        encodings_map[column] = encode
    return df_frequency, encodings_map

def oneHotEncoding(df):
    """
    Recibe un DataFrame categórico df.
    Retorna get_dummies de pandas con drop_first = True.
    """
    return pd.get_dummies(df.dropna(), drop_first = True)

def getBestEncoding(series, target):
    scaler = MinMaxScaler()
    
    frequency_encoding = series.map(series.value_counts(normalize = True))
    frequency_encoding = pd.Series(scaler.fit_transform(frequency_encoding.values.reshape(-1, 1)).flatten(), index=frequency_encoding.index)
    
    target_mean_encoding = series.map(target.groupby(series).mean())
    target_mean_encoding = pd.Series(scaler.fit_transform(target_mean_encoding.values.reshape(-1, 1)).flatten(), index=target_mean_encoding.index)

    target_median_encoding = series.map(target.groupby(series).median())
    target_median_encoding = pd.Series(scaler.fit_transform(target_median_encoding.values.reshape(-1, 1)).flatten(), index=target_median_encoding.index)

    encodings = [frequency_encoding, target_mean_encoding, target_median_encoding]
    names = ['frequency', 'target_mean', 'target_median']

    std_devs = {}
    
    for encoding, name in zip(encodings, names):
        std_dev = encoding.std()
        std_devs[name] = std_dev
    
    higher = 0
    best = None
    for key, value in std_devs.items():
        if value > higher:
            higher = value
            best = key
    return best, higher

def getBestEncodings(df, target):
    encodings = {}
    std_devs = {}
    for column in df.columns:
        encodings[column], std_devs[column] = getBestEncoding(df[column], target)
    return encodings

def encodeCustom(df_cat, target, encoders):
    df = df_cat.copy()
    
    frequency = []
    target_mean = []
    target_median = []
    one_hot = []
    
    for column, encoder in encoders.items():
        if encoder == 'frequency':
            frequency.append(column)
        if encoder == 'target_mean':
            target_mean.append(column)
        if encoder == 'target_median':
            target_median.append(column)
        if encoder == 'one_hot':
            one_hot.append(column)
            
    df_freq = pd.DataFrame()
    df_targ_mean = pd.DataFrame()
    df_targ_med = pd.DataFrame()
    df_one_hot = pd.DataFrame()
    
    map_freq = {}
    map_targ_mean = {}
    map_targ_med = {}
    
    try:
        df_freq, map_freq = frequencyEncoding(df[frequency])
    except:
        pass
    
    try:
        df_targ_mean, map_targ_mean = targetEncoding(df[target_mean], target, 'target_mean')
    except:
        pass
    
    try:
        df_targ_med, map_targ_med = targetEncoding(df[target_median], target, 'target_median')
    except:
        pass
    
    try:
        df_one_hot = oneHotEncoding(df[one_hot])
    except:
        pass
    
    df = pd.concat([df_freq, df_targ_mean, df_targ_med, df_one_hot], axis = 1)
    encodings_map = {}
    encodings_map.update(map_freq)
    encodings_map.update(map_targ_mean)
    encodings_map.update(map_targ_med)
    
    return df, encodings_map