import pandas as pd
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os


class Alkamid():
	"""docstring for Alkamid"""
	def __init__(self, save_to_json=False):
		self.save_to_json = save_to_json
		self.url ='http://alkamid.ugent.be/alkamidresults.php'

		# dictionaries for chemical_details and chemicals_in_plants
		self.chemical_details = {}
		self.chemicals_in_plants = {}
		self.details = []
		

		# dataframes for chemical_details and chemicals_in_plants
		self.chemical_dataframe = pd.DataFrame()

		self.df_chemical_details = pd.DataFrame()
		self.df_chemicals_in_plants = pd.DataFrame()


		# statistics of the crawl
		# of unique plants
		# of unique chemicals
		# of unique (plant, chemical) pairs
		# mean & standard deviation of chemicals per plant
		# the longest chemical name

		self.statistics = {}
		self.stat_unique_plants = 0
		self.stat_unique_chemicals = 0
		self.stat_unique_pairs = 0
		self.mean_standard_deviation = []
		self.longest_chemical_name = ''

		self.crawl()


		self.details = [self.chemical_details, self.chemicals_in_plants]

		if(self.save_to_json == True):
			print('saved data to json files')
			file_name = str(int(time.time()))
			# detect the current working directory and print it
			path = os.getcwd()
			# print ("The current working directory is %s" % path)

			
			details_file = self.df_chemical_details.to_json(orient='table')
			with open(path+'/'+file_name+'_chemical_details.json', 'w+') as out_file:
				out_file.write(details_file)

			plants_details_file = self.df_chemicals_in_plants.to_json(orient='table')
			with open(path+'/'+file_name+'_chemicals_in_plants.json', 'w+') as out_file:
				out_file.write(plants_details_file)


	def crawl(self, query=''):
		
		html = urlopen(self.url + query)
		soup = BeautifulSoup(html, 'lxml')

		next_page = soup.select('.pagenumber.unselected a')

		if next_page and next_page[0]:
			next_page = soup.select('.pagenumber.unselected a')[0]['href']


		list_tr = soup.find_all('tr')
		del list_tr[0]
		for x in list_tr:
			S_chemical_name  = x.select_one('td:nth-of-type(3)').text
			S_trivial_name  = x.select_one('td:nth-of-type(4)').text
			S_formula  = x.select_one('td:nth-of-type(5)').text
			S_origin  = x.select_one('td:nth-of-type(6)').text
			S_mw  = x.select_one('td:nth-of-type(7)').text



			trivial_name = S_trivial_name

			if trivial_name == '-' :
				trivial_name = None


			plant_origin = S_origin
			chemical_name = S_chemical_name

			if plant_origin == '-':
				plant_origin = None

			if chemical_name == '-':
				chemical_name = None


			self.chemical_details[chemical_name] = {
				'trivial_name' : {trivial_name},
				'formula' : S_formula,
				'molecular_weight' : S_mw
			}

			if chemical_name:
				if len(self.longest_chemical_name) < len(chemical_name):
					self.longest_chemical_name = chemical_name


			cip = self.chemicals_in_plants.get(plant_origin)
			if cip:
				plant_origin_value = cip
				plant_origin_value.add(chemical_name)

			else:
				plant_origin_value = {chemical_name}


			self.chemicals_in_plants[plant_origin] = {plant for plant in plant_origin_value if plant} 


		if next_page:
			self.crawl(next_page)
		else:


			unique_plants =  {pl for pl in self.chemicals_in_plants if pl}
			self.stat_unique_plants =  len(unique_plants)




			unique_chemicals =  {cd for cd in self.chemical_details if cd}
			self.stat_unique_chemicals =  len(unique_chemicals)



			# processing dataframe
			# processing chemical details dataframe
			self.df_chemical_details = pd.DataFrame(self.chemical_details)
			self.df_chemical_details = self.df_chemical_details.transpose()

			self.df_chemical_details['trivial_name'] = self.df_chemical_details['trivial_name'].apply(list)
			self.df_chemical_details.index.name = 'chemical'

			self.df_chemical_details = self.df_chemical_details.reset_index()
			self.df_chemical_details = self.df_chemical_details.dropna() 
			


			# processing chemicals in plants dataframe
			self.df_chemicals_in_plants = pd.DataFrame(self.chemicals_in_plants.items(), columns = [ 'origin', 'chemical'])
			self.df_chemicals_in_plants['chemical'] = self.df_chemicals_in_plants['chemical'].apply(list)
			self.df_chemicals_in_plants = self.df_chemicals_in_plants.explode('chemical')
			self.df_chemicals_in_plants = self.df_chemicals_in_plants.dropna(subset=['chemical']) 

			#joining two data frames on chemical details field
			self.chemical_dataframe = pd.merge(self.df_chemicals_in_plants, self.df_chemical_details, on='chemical', how='inner')


			# unique pairs ('plants' and chemical names)
			self.stat_unique_pairs = len(self.df_chemicals_in_plants)


			# calculating mean and std of chemicals_in_plants
			value_counts  =  self.df_chemicals_in_plants['origin'].value_counts()
			mean = value_counts.mean()
			std = value_counts.std()

			self.mean_standard_deviation = [mean, std]

			# statistics of the data
			self.statistics = {
				'unique_plants' : self.stat_unique_plants,
				'unique_chemicals' : self.stat_unique_chemicals,
				'unique_pairs' : self.stat_unique_pairs,
				'mean_and_std' : self.mean_standard_deviation,
				'longest_chemical_name' : self.longest_chemical_name,
			}





if __name__ == '__main__':
	result = Alkamid(save_to_json=True)
	print(result)