def cleaner(dataframe):
    return [' '.join(dataframe.dropna().astype(str).tolist())]