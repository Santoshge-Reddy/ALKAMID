from alkamid import Alkamid


alkamid = Alkamid()

# dictionaries for chemical_details and chemicals_in_plants 
chemical_details = alkamid.chemical_details
chemicals_in_plants = alkamid.chemicals_in_plants





# df_chemical_details = alkamid.df_chemical_details
# df_chemicals_in_plants = alkamid.df_chemicals_in_plants
chemical_dataframe = alkamid.chemical_dataframe

# # statistics for the  data
statistics = alkamid.statistics


# run this command to save data to json files
Alkamid(save_to_json=True)

