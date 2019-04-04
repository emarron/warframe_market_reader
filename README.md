# Warframe Market Statistics Bulk Reader

Gets bulk statistics from warframe items on the market. When you want to check the current price of all the rivens, or corrupted mods, or primes, ect. Recommend you look at the excel file if there are many queries.

# Install!

  - python 3.7
  - xlsxwriter
  - requests
  - tqdm
```
   pip install git
   pip install xlsxwriter
   pip install requests
   pip install tqdm
   git clone https://github.com/emarron/warframe_market_reader
```
   

# Use!

 - run thing.py
 - will request user input, pick from the keys listed in the terminal
 - automatically poops out the items in the keys and their associated volume, minimum, maximum, average, & median from the last hour.
```
   cd warframe_market_reader
   python thing.py
```
  programs will then list available user inputs. In example type:
```
   corrupted_mods
```
  output:
```
{'blind_rage': {'avg': 20.0, 'max': 25, 'med': 20, 'min': 15, 'volume': 120},
 'fleeting_expertise': {'avg': 28.0, 'max': 40, 'med': 29, 'min': 16, 'volume': 134},
 'narrow_minded': {'avg': 25.5, 'max': 35, 'med': 22.0, 'min': 16, 'volume': 100},
 'overextended': {'avg': 20.0, 'max': 22, 'med': 20.0, 'min': 18, 'volume': 89},
 'transient_fortitude': {'avg': 25.5, 'max': 38, 'med': 25, 'min': 13, 'volume': 71}}
```
  also available is an excel sheet. this is output to ./warframe_market_reader/xlsx/warframe_temp.xlsx
  ![excel](https://i.imgur.com/1kcs8Xm.png "excel")
  
# Things!
 - primed mods!
 - corrupted mods!
 - riven mods!
 - nightmare mods!
 - prime warframes!
 - prime primaries!
 - prime secondaries!
 - prime melees!
 - add your own!
 
 # Modifying the program!
  To add to the dictonary of user input: You must know the name in warframe market.
  
  In example: Cleaving Whirlwind is `https://warframe.market/items/cleaving-whirlwind`, so you have `'cleaving_whirlwind'` for your key.
  
  Format: `"key": ['value1','value2',....'value3'],`
  
  Here is a simple way to add to the dictonary, open the thing.py in your editor. navigate to `riven_mods`.
```
    "nightmare_mods": lst_nightmare_mods,
    # the names for these were weird so I did it manually.
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
```
  Duplicated `riven_mods` entry:
```
    "nightmare_mods": lst_nightmare_mods,
    # the names for these were weird so I did it manually.
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
``` 
  Replace with desired key and values:
```
    "nightmare_mods": lst_nightmare_mods,
    "poe_fish_rare": ['murkray', 'norg', 'cuthol', 'glappid'],
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
```

**Free Software, Hell Yeah!**

# Credit!
 - [[DAVID]](https://github.com/dsluo), lots of help. ten out of tenno.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
