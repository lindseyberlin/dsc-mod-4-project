def prep_state_data(df, state):
    '''
    A specific script, written for pre-processed data read in from zillow_data.csv
    This function will prepare and return a state-level set of nested lists, where
    the outer list corresponds to the time steps, and the inner list is the
    latitude/longitude/weight data that will be plotted by folium's HeatMapWithTime

    Expected Inputs:
    df: pandas dataframe, read in from zillow_data.csv, with whatever necessary
        pre-processing already completed (drop metadata columns except state, 
        grab dates to examine, remove of all nulls, normalize/scale prices)
    state: string of the state code, ie: "TX" for Texas

    Outputs:
    heat_data: nested lists to be read into a folium HeatMapWithTime

    Note! The pandas dataframe, df, must not have any null values!

    Example:
    from state_heatmapwithtime import *
    tx_data = prep_state_data(df, "TX")
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

def create_index_heatmapwithtime(df, state):
    '''
    A specific script just to return a list to be read into folium's
    HeatMapWithTime to act as the index

    Expected Inputs:
    df: pandas dataframe, read in from zillow_data.csv, with whatever necessary
        pre-processing already completed (drop metadata columns except state, 
        grab dates to examine, remove of all nulls, normalize/scale prices)
    state: string of the state code, ie: "TX" for Texas

    Note! The pandas dataframe, df, must not have any null values!

    Example:
    from state_heatmapwithtime import *
    tx_index = create_index_heatmapwithtime(df, "TX")
    '''
    # Creating the state-level dataframe
    df_state = df.loc[df["State"] == state]

    # Dropping the state column, now that we no longer need it
    df_state = df_state.drop(columns="State")

    # Creating a column list
    column_list = list(df_state.columns)

    return column_list