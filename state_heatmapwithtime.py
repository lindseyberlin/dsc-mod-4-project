def getdata_stateheatmapwithtime(df, state):
    '''
    Expects the original dataframe from our zillow_data.csv

    State must be a string of the state code
    Example: "TX" for Texas
    '''
    from uszipcode import SearchEngine
    from sklearn import preprocessing
    import pandas as pd

    # Instantiating the zipcode search engine
    search = SearchEngine(simple_zipcode=True)

    # Creating the state-level dataframe
    df_state = df.loc[df["State"] == state]

    # Dropping the state column, now that we no longer need it
    df_state = df_state.drop(columns="State")

    # Creating an empty dictionary to hold found zipcode values
    zipcode_dict = {}

    # Using our zipcode search engine to find lat/long data per zipcode
    for zipcode in df_state.index:
        zipc = search.by_zipcode(zipcode)
        zipcode_dict[zipcode] = [zipc.lat, zipc.lng]

    # Creating lists to hold those lat/long values
    lats = []
    longs = []
    
    # Appending lat/long values to those lists
    for zipcode in zipcode_dict.keys():
        lats.append(zipcode_dict[zipcode][0])
        longs.append(zipcode_dict[zipcode][1])  
    
    # Adding those lists to our dataframe
    df_state["Lat"] = lats
    df_state["Long"] = longs

    # Creating a column list
    column_list = list(df_state.columns)
    # Removing the lat/long columns, to only have date columns
    column_list.remove("Lat")
    column_list.remove("Long")

    # Creating a row list
    row_list = list(df_state.index)

    # Creating an empty list to hold our data to visualize in the heatmap
    heat_data = []

    # Iterating column by column, aka month by month
    for col in column_list:
        lat_long_weight = []
        # Within each column, grabbing the lat/long data plus values for weight
        for row in row_list:
            row_data = [df_state.loc[row]["Lat"],
                        df_state.loc[row]["Long"],
                        round(df_state.loc[row, col], 3)]
            lat_long_weight.append(row_data)
        heat_data.append(lat_long_weight)
    return heat_data