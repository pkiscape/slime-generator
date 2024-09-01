#!/usr/bin/env python3

"""
=====================================================
Slime
Create Slime with fun attributes
=====================================================

@version	4
@link		https://github.com/pkiscape
@authors	pkiscape.com
"""

import argparse
import random
import string
import uuid
import timeit
import time
from src import slime_db, slime_image_creator, slime_stats


def main():
    """
    Main function using argparse for a CLI
    """
    argparse_main = argparse.ArgumentParser(description="Slime CLI tool")
    argparse_main.add_argument(
    	"-n", "--number", type=int, help="Specify the number of slimes you want to create", required=True)
    argparse_main.add_argument(
    	"-g", "--graph", action="store_true", help="Create graph of slime creation times", required=False)
    argparse_main.add_argument(
    	"-v", "--verbose", action="store_true", help="Print slime information and creation times", required=False)
    argparse_main.add_argument(
        "-r", "--rare", action="store_true", help="Rare Detector: prints information when a rare occurance happens", required=False)
    argparse_main.add_argument(
    	"-ni", "--no-images", action="store_true", help="Do not save slime images to the img/ directory", required=False)
    argparse_main.add_argument(
    	"-d", "--db-images", action="store_true", help="Adds the slime image to the sqlite database", required=False)
    argparse_main.add_argument(
        "-s", "--sleep", type=float, help="Add static backoff (sleep timer) in seconds to wait after creation of each slime", required=False)
    args = argparse_main.parse_args()

    graph = args.graph if args.graph is not None else False
    verbose = args.verbose if args.verbose is not None else False
    rare = args.rare if args.rare is not None else False
    no_images = args.no_images if args.no_images is not None else False
    db_images = args.db_images if args.db_images is not None else False
    sleep = args.sleep if args.sleep is not None else False

    loop_number = range(args.number)

    # Start total timer
    slime_time_list = []
    total_rt = timeit.default_timer()

    for index, slime in enumerate(loop_number, start=1):
        slime_time = create_slime(
            graph=graph,
            verbose=verbose,
            rare=rare,
            no_images=no_images,
            db_images=db_images,
            index=index,
            loop_number=loop_number
        )

        # End timer for total create time
        slime_time_list.append(slime_time)

        # Add backoff if argument was passed
        if sleep:
            time.sleep(sleep)

    # End timer for total
    create_time = timeit.default_timer() - total_rt

    if graph:
        # -----------Graphs/Stats-----------#
        slime_stats.slime_creation_graph(
        	create_time,
        	args.number,
        	slime_time_list)
    if verbose:
        print("All Slime Creation Time: ", create_time)


class Slime:
    """Slime Object - Creates Attributes of the Slime (ID, KeyID, Version, Name, Color, Template, and Accessories)"""

    def __init__(self):
        self.uid = self.get_uid()
        self.version = self.get_slime_version()
        self.name = self.get_slime_name()
        self.color = self.get_slime_color()
        self.template = self.get_slime_template()
        self.accessories = self.get_slime_accessories()

    def get_uid(self):
        """Unique ID for each slime!"""
        return uuid.uuid4()

    def get_slime_version(self):
        """Static for each version. Can be used to version your slimes!"""
        version = 2
        return version

    def get_slime_name(self):
        """Randomly generated name. I try to make it "namelike" by making the 2nd letter in the first and last name a vowel."""
        vowels = "a", "e", "i", "o", "u"

        # First Name
        fn_rand_num = random.randint(0, 9)
        fn_firstletter = random.choice(string.ascii_uppercase)
        fn_secondletter = random.choice(vowels)
        fn_rest = "".join(random.choices(string.ascii_lowercase, k=fn_rand_num))
        fn = fn_firstletter + fn_secondletter + fn_rest

        # Last Name
        ln_rand_num = random.randint(0, 10)
        ln_firstletter = random.choice(string.ascii_uppercase)
        ln_secondletter = random.choice(vowels)
        ln_rest = "".join(random.choices(string.ascii_lowercase, k=ln_rand_num))
        ln = ln_firstletter + ln_secondletter + ln_rest

        return fn + " " + ln

    def get_slime_color(self):
        """Chooses a color code from random"""
        r, g, b = random.choices(range(256), k=3)

        return f"#{r:02X}{g:02X}{b:02X}"

    def get_slime_template(self) -> int:
        """Chooses a template which will point to a png file"""
        return random.randint(1, 4)

    def get_slime_accessories(self) -> list:
        """
        Slime will have two slots for accessories:

        Hat slot
        Other slot

        There will be two random rolls, one for each accessory.
        Ex. If common is chosen, it chooses a random common.
        """
        # Common
        common_other = ["Sunglasses"]
        common_hat = ["Sunhat"]

        # Uncommon
        uncommon_other = ["Mustache"]
        uncommon_hat = ["Top Hat", "Wizard Hat"]

        # Rare
        rare_other = ["Golden Sunglasses", "Mustache+"]
        rare_hat = ["Robin Hood Hat", "Santa Hat", "Crown", "Golden Top Hat", "Helmet"]

        slime_accessories = []

        # Other slot roll
        roll_other = random.randint(1, 26)

        if roll_other in (1, 2, 3, 4, 5):
            slime_accessories.append(random.choice(common_other))

        if roll_other in (9, 10, 11):
            slime_accessories.append(random.choice(uncommon_other))

        if roll_other == 25:
            slime_accessories.append(random.choice(rare_other))

        # Hat slot roll
        roll_hat = random.randint(1, 26)

        if roll_hat in (1, 2, 3, 4, 5):
            slime_accessories.append(random.choice(common_hat))

        if roll_hat in (9, 10, 11):
            slime_accessories.append(random.choice(uncommon_hat))

        if roll_hat == 25:
            slime_accessories.append(random.choice(rare_hat))

        return slime_accessories


def create_slime(graph, verbose, rare, no_images,  db_images, index, loop_number):
    """
    Creates a Slime:
    1) Creates Attributes of the Slime (UID, Version, Name, Color, Template, and Accessories)
    2) Creates Slime Picture, containing Attributes
    3) Inserts data(Slime attributes/picture) into Database
    4) Optional actions such as read actions / stats and graphs / rare detector
    """
    # Start timer
    slime_start = timeit.default_timer()

    # Create DB and Tables if not already created
    found = slime_db.check_tables()

    if found is False:
        slime_db.create_tables()

    # -----------Create Slime Object-----------#
    slime = Slime()
    # -----------Create Slime Picture-----------#

    slime_uid_str = str(slime.uid)

    slime_image = slime_image_creator.draw_slime(
        uid=slime_uid_str,
        version=slime.version,
        name=slime.name,
        color=slime.color,
        template=slime.template,
        accessories=slime.accessories,
        no_images=no_images
    )
    # -----------Insert data into Database-----------#

    # Store Slime and Accessories in DB
    slime_list = [slime_uid_str, slime.version, slime.name, slime.color, slime.template, slime_image]
    slime_db.insert_into_slime_table(slime_list, db_images)

    accessory_list = []

    for accessory in slime.accessories:
        accessory_list = [slime_uid_str, accessory]
        slime_db.insert_into_accessories_table(accessory_list)

    if rare:
        slime_stats.slime_rare_detector(
            slime_rare_list = slime_list[0:4],
            accessories = slime.accessories
            )

    # DB Read Actions -> slimedb.read_all_slime()

    slime_time = timeit.default_timer() - slime_start

    if verbose:
        print(f"{index}/{loop_number.stop} Slime Created. ID:{slime_uid_str}, Name: {slime_list[2]} in {slime_time} seconds")

    return slime_time


if __name__ == "__main__":
    main()
