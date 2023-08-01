import pandas as pd

def splitNumCat(df):
    """
    Recibe un DataFrame df.
    Retorna dos DataFrame, uno con valores numéricos y el otro opuesto, con valores categóricos.
    """
    df_num = df._get_numeric_data().copy()
    df_cat = df.drop(df_num.columns, axis = 1)
    return df_num, df_cat

def mergeNumCat(df_num, df_cat):
    """
    Recibe dos DataFrame df_num y df_cat, uno numérico y otro categórico.
    Retorna el resultado de un pandas.merge de ambos dataframes en función de su índice.
    No elimina ningún numpy.nan.
    """
    df_cat_idx = df_cat.reset_index()
    df_num_idx = df_num.reset_index()
    
    df = pd.merge(df_cat_idx, df_num_idx, on = 'index').drop('index', axis = 1)
    return df