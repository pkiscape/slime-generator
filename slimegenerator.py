#!/usr/bin/env python3


#=====================================================
#
# Slime 
# Create Slime with fun attributes
#=====================================================
#
#
#@version	1
#@link		https://github.com/pkiscape
#@authors	pkiscape.com

import argparse
import random
import string
import uuid
import slimedb, slimeimgcreator, slimestats
import timeit

def main():

	'''
	Main function using argparse for a CLI
	'''
	argparse_main = argparse.ArgumentParser(description="Slime CLI tool")
	argparse_main.add_argument("-n","--number",type=int, help="Define how many slime you would like to create",required=True)
	argparse_main.add_argument("-g","--graph", action="store_true", help="Pass this if you would like to view a graph",required=False)
	argparse_main.add_argument("-v","--verbose", action="store_true", help="Print slime information and creation times",required=False)
	argparse_main.add_argument("-r","--rare", action="store_true", help="Rare Detector: prints information when a rare occurance happens",required=False)
	argparse_main.add_argument("-i","--images", action="store_true", help="Prints the slime image in the img/ directory",required=False)
	argparse_main.add_argument("-ndi","--no-db-images", action="store_true", help="Omits the slime image in the sqlite database",required=False)
	args = argparse_main.parse_args()

	graph = args.graph if args.graph is not None else False
	verbose = args.verbose if args.verbose is not None else False
	rare = args.rare if args.rare is not None else False
	images = args.images if args.images is not None else False
	no_db_images = args.no_db_images if args.no_db_images is not None else False

	loop_number=range(args.number)

	#Start total timer
	slime_time_list = []
	total_rt = timeit.default_timer()
	
	for slime in loop_number:
		slime_time = create_slime(graph=graph, verbose=verbose, rare=rare, images=images, no_db_images=no_db_images)

		#End timer for total create time
		slime_time_list.append(slime_time)
		
	#End timer for total
	create_time = timeit.default_timer() - total_rt

	if graph:
		#-----------Graphs/Stats-----------#
		slimestats.slime_creation_graph(create_time, args.number, slime_time_list)
	if verbose:
		print("All Slime Creation Time: ", create_time)


class Slime():
	"""Slime Object - Creates Attributes of the Slime (ID, KeyID, Version, Name, Color, Template, and Accessories)"""
	def __init__(self):

		self.uid = self.getuid()
		self.version = self.slimeversion()
		self.name = self.slimename()
		self.color = self.slimecolor()
		self.template = self.slimetemplate()
		self.accessories = self.slimeaccessories()

	def getuid(self):
		uid = uuid.uuid4()
		return uid

	def slimeversion(self):
		#Static for each version
		version = 1
		return version

	def slimename(self):

		vowels = "a","e","i","o","u"
		
		#firstname
		fn_rand_num = random.randint(0,9)
		fn_firstletter = random.choice(string.ascii_uppercase)
		fn_secondletter = random.choice(vowels)
		fn_rest = ''.join(random.choices(string.ascii_lowercase, k = fn_rand_num))    
		fn = fn_firstletter + fn_secondletter + fn_rest	
		
		#lastname
		ln_rand_num = random.randint(0,10)
		ln_firstletter = random.choice(string.ascii_uppercase)
		ln_secondletter = random.choice(vowels)
		ln_rest = ''.join(random.choices(string.ascii_lowercase, k = ln_rand_num))
		ln = ln_firstletter + ln_secondletter + ln_rest
		fullname = fn + " " + ln
		return fullname

	def slimecolor(self):
		#Chooses a color code
		r = lambda: random.randint(0,255)
		hexadecimal = '#%02X%02X%02X' % (r(),r(),r())
		return(hexadecimal)
		
	def slimetemplate(self):
		#Chooses a template which will point to a png file
		template = random.randint(1,3)
		return template

	def slimeaccessories(self):

		'''
		Slime will have two slots for accessories:

		Hat slot
		Other slot

		There will be two random rolls, one for each accessory. Ex. If common is chosen, it chooses a random common. 
		'''
		#Common
		common_other = ["sunglasses"]
		common_hat = ["sunhat"]
		
		#Uncommon
		uncommon_other = ["mustache"]
		uncommon_hat = ["top hat", "wizard hat"]

		#Rare
		rare_other = ["golden sunglasses"]
		rare_hat = ["robin hood hat", "santa hat", "crown", "golden top hat"]

		chosen = []

		#Other slot roll
		roll_other = random.randint(1,26)

		if roll_other in (1,2,3,4,5):
			chosen.append(random.choice(common_other))
			
		if roll_other in (9,10,11):
			chosen.append(random.choice(uncommon_other))
	 
		if roll_other == 25:
			chosen.append(random.choice(rare_other))

		#Hat slot roll
		roll_hat = random.randint(1,26)

		if roll_hat in (1,2,3,4,5):
			chosen.append(random.choice(common_hat))

		if roll_hat in (9,10,11):
			chosen.append(random.choice(uncommon_hat))

		if roll_hat == 25:
			chosen.append(random.choice(rare_hat))

		return chosen


def create_slime(graph,verbose,rare,images,no_db_images):
	'''
	Creates a Slime:
	1) Creates Attributes of the Slime (UID, Version, Name, Color, Template, and Accessories)
	2) Creates Slime Picture, containing Attributes
	3) Inserts data(Slime attributes/picture) into Database
	4) Optional actions such as read actions / stats and graphs / rare detector
	'''
	#Start timer
	slime_start = timeit.default_timer()

	#Create DB and Tables if not already created
	found = slimedb.check_tables()

	if found == False:
		slimedb.create_tables()

	#-----------Create Slime Object-----------#
	slime = Slime()
	#-----------Create Slime Picture-----------#
	in_memory_slime_image = slimeimgcreator.drawslime(uid=slime.uid,version=slime.version,name=slime.name,color=slime.color,template=slime.template,
		accessories=slime.accessories, images=images)
	#-----------Insert data into Database-----------#
	# Store Slime and Accessories in DB

	slime_list = [str(slime.uid),slime.version,slime.name,slime.color,slime.template,in_memory_slime_image]
	slimedb.insert_into_slime_table(slime_list,no_db_images)
		
	accessory_list = []

	for accessory in slime.accessories:
		accessory_list = [str(slime.uid),accessory]
		slimedb.insert_into_accessories_table(accessory_list)

	if rare:
		slime_rare_list = slime_list[0:4]
		rare_list = slimestats.slime_rare_detector(slime_rare_list, slime.accessories)

	#DB Read Actions
	#slimedb.read_all_slime()
	slime_time = timeit.default_timer() - slime_start

	if verbose:
			print(f"Slime Created: ID:{slime_list[0]}, Name: {slime_list[2]} in {slime_time} seconds")
	
	return slime_time

if __name__ == '__main__':
	main()