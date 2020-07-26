from alkamid import Alkamid


alkamid = Alkamid()

# dictionaries for chemical_details and chemicals_in_plants 
chemical_details = alkamid.chemical_details
chemicals_in_plants = alkamid.chemicals_in_plants
print('====================Start======================')
print('dictionaries for chemical_details')
print(chemical_details)
print('=====================End=================')

print('====================Start======================')
print('dictionaries for chemicals_in_plants')
print(chemicals_in_plants)
print('=====================End=================')





# df_chemical_details = alkamid.df_chemical_details
# df_chemicals_in_plants = alkamid.df_chemicals_in_plants
chemical_dataframe = alkamid.chemical_dataframe
print('====================Start======================')
print('dataframe for chemical details')
print(chemical_dataframe)
print('=====================End=================')


# # statistics for the  data
statistics = alkamid.statistics
print('====================Start======================')
print('statics for the data')
print(statistics)
print('=====================End=================')


# run this command to save data to json files
Alkamid(save_to_json=True)

