def cleaner(dataframe):
    return dataframe.dropna().astype(str).tolist()