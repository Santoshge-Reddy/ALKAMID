# ALKAMID-module
ALKAMID-test module, scraping the site with plant chemical details


Install the dependencies using requirements.txt
pip install -r requirements.txt

## To run the code
python main.py


main.py
from alkamid import Alkamid
alkamid = Alkamid()

## Dictionaries for chemical_details and chemicals_in_plants 
chemical_details = alkamid.chemical_details
chemicals_in_plants = alkamid.chemicals_in_plants

## Dataframe of the chemical details
chemical_dataframe = alkamid.chemical_dataframe

## Statistics for the  data
statistics = alkamid.statistics


## Run this command to save data to json files
Alkamid(save_to_json=True)

