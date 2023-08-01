def preprocessData(df,
                   target_column,
                   drop = None,
                   outliers_data_loss = 0.05,
                   drop_outliers_first = True,
                   impute_num = 'drop',
                   impute_cat = 'drop',
                   encoding = 'best',
                   custom_encodings = None,
                  ):
    # ERROR HANDLING
    ###############################################################################################
    numeric_imputers = {'drop', 'mean', 'median', 'knn', 'forest'}
    categoric_imputers = {'drop', 'mode', 'knn', 'forest'}
    encodings = {'best', 'brute_force', 'custom'}
    
    if impute_num not in numeric_imputers:
        raise Exception(f"impute_num debe ser alguno de los siguientes: {numeric_imputers}")
    
    if impute_cat not in categoric_imputers:
        raise Exception(f"impute_cat debe ser alguno de los siguientes: {categoric_imputers}")
        
    if encoding not in encodings:
        raise Exception(f"encoding debe ser alguno de los siguientes: {encodings}")
    ###############################################################################################
    
    df = df.copy()
    
    # drops columns
    try:
        df.drop(drop, axis = 1, inplace = True)
    except:
        pass
    
    # splits dataframe into numeric and categoric variables
    df_num, df_cat = splitNumCat(df)
    
    # drops outliers from the numeric columns
    df_num = dropOutliers(df_num, threshold = getBestOutliersThreshold(df_num, data_loss = outliers_data_loss))
    
    if drop_outliers_first:
        # merges numeric and categoric columns back together to ensure target encodings do not take outliers into account
        df = mergeNumCat(df_num, df_cat)
        df_num, df_cat = splitNumCat(df)
    
    # encodes categoric variables
    df_cat, encodings_map = encode(df_cat, df[target_column], encoding, custom_encodings)
    
    # imputes categoric missing values
    if impute_cat != 'drop':
        df_cat = imputeCat(df_cat, impute_cat)
    
    # imputes numeric missing values
    if impute_num != 'drop':
        df_num = imputeNum(df_num, impute_num)
    
    # merges numeric and categoric columns back together
    df = mergeNumCat(df_num, df_cat)
    
    return df, encodings_map


