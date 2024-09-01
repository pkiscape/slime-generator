# Slime Generator

A CLI tool that allows you to create slime with fun attributes! It supports a local SQLite database which stores information about each slime. 

Creates a Slime:
   
1) Creates Attributes of the Slime (UID, Version, Name, Color, Template, and Accessories), in a Slime object
2) Creates Slime Picture, containing Attributes
3) Inserts data(Slime attributes/picture) into Database
4) Optional actions such as read actions / stats and graphs

According to the RNG, accessories will be chosen for the slime (up to two). There are common, uncommon, and rare accessories. 

| Rarity    | Item |
| -------- | ------- |
| Common   | Sunglasses, Sunhat    |
| Uncommon | Top Hat, Wizard Hat, Mustache     |
| Rare     | Robin Hood Hat, Santa Hat, Crown, Golden Top Hat, Golden Sunglasses, Mustache+, Helmet    |

![Example Slime](etc/example_slime.jpg)


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Design](#design)

## Installation

```pip install -r requirements.txt```


## Usage
```
usage: slime_generator.py [-h] -n NUMBER [-g] [-v] [-r] [-ni] [-d] [-s SLEEP]

Slime CLI tool

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Specify the number of slimes you want to create
  -g, --graph           Create graph of slime creation times
  -v, --verbose         Print slime information and creation times
  -r, --rare            Rare Detector: prints information when a rare occurance happens
  -ni, --no-images      Do not save slime images to the img/ directory
  -d, --db-images       Adds the slime image to the sqlite database
  -s SLEEP, --sleep SLEEP
                        Add static backoff (sleep timer) in seconds to wait after creation of each slime
  ```

## Examples

1) Create 10 slime, displaying a graph to show their creation times. Slimes get saved to img/ directory by default.

    `python3 slime_generator.py -n 10 -g`

2) Create 15 slime, being verbose to see them get created.

    `python3 slime_generator.py -n 15 -v`

3) Create 20 slime, printing when there's a rare item,  while showing a graph.

    `python3 slime_generator.py -n 20 -r -g`

4) Create 100 slimes with graphs, verbosity, rare detector, adding the slime image in DB.

    `python3 slime_generator.py -n 100 -g -v -r -d`

5) Create 200 slimes with verbosity, omitting images in the img/ folder, with a 1 second wait time.

    `python3 slime_generator.py -n 200 -v -ni -s 1`

## Design

After image creation, this information gets put into the local SQLite database. 

    +-------------------+      		  
    |       Slime       |       
    +-------------------+    		 
    | Slime ID (PK)     |               
    | Version           |             
    | Name              |               
    | Color             |        	  
    | Template          |        
    | SlimeImage        |       
    +-------------------+        
                                 
             ^                   
             |
    +-------------------+  
    |    Accessories    |
    +-------------------+  
    | SlimeID (FK)      | 
    | AccessoryName     |
    +-------------------+ 

