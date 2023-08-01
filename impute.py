def imputeCat(df, imputer):
    """
    Recibe un DataFrame categórico df y una string imputer.
    En función de imputer, realiza una estrategia de tratamiendo de numpy.nan sobre una copia de df.
    Retorna la copia.
    """
    df = df.copy()
    
    imputers = {'mode', 'knn', 'forest'}
    
    if imputer == 'mode':
        df = modeImputer(df)
    elif imputer == 'knn':
        raise Exception(f'{imputer} is not implemented')
    elif imputer == 'forest':
        raise Exception(f'{imputer} is not implemented')
    else:
        raise Exception(f'{imputer} is not a valid option. Please chose one from {imputers}')
        
    return df

def imputeNum(df, imputer):
    """
    Recibe un DataFrame numérico df y una string imputer.
    En función de imputer, realiza una estrategia de tratamiendo de numpy.nan sobre una copia de df.
    Retorna la copia.
    """
    df = df.copy()
    
    imputers = {'mean', 'median', 'knn', 'forest'}
    
    if imputer == 'mean':
        df = meanImputer(df)
    elif imputer == 'median':
        df = medianImputer(df)
    elif imputer == 'knn':
        raise Exception(f'{imputer} is not implemented')
    elif imputer == 'forest':
        raise Exception(f'{imputer} is not implemented')
    else:
        raise Exception(f'{imputer} is not a valid option. Please chose one from {imputers}')
        
    return df