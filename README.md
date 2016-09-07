hdtorrentsit-cp-provider
=======================

A CouchPotatoServer module to add the private tracker HDTorrents.it as a torrent provider for Italian torrents.

####SETUP INSTRUCTIONS (TL;DR)

Download the master branch *https://github.com/neothematrix/hdtorrentsit-cp-provider/archive/master.zip* and extract it
inside a "hdtorrentsit-cp-provider" folder into your CouchPotato "custom_plugins" folder (it's under CouchPotato data dir folder).
If you don't know where your CouchPotato data dir folder is, open CouchPotato web interface, then go to: Settings -> About -> Directories.
Make sure to enable it inside the "Searcher" section of CouchPotato configuration, and make sure to add your username and password (mandatory)

####SETUP INSTRUCTIONS

```
# Download the HDTorrents.it search provider (Italian torrents only, see https://hdtorrents.it)
https://github.com/neothematrix/hdtorrentsit-cp-provider/archive/master.zip

# Shut down CouchPotatoServer, either by opening it up in a browser 
# and going to "Settings" -> "Shutdown", or by terminating the process

# Open your CouchPotato data dir folder and go to the "custom_plugins" folder
# If you don't know where your CouchPotato data dir folder is, open CouchPotato web interface,
# go to: Settings -> About -> Directories.
cd ~/CouchPotatoServer # or wherever you have it stored
cd ./custom_plugins

# Extract the downloaded master.zip into a folder named corsaronero
unzip master.zip -d hdtorrentsit-cp-provider # note, your master.zip might be located somewhere else

# Startup CouchPotatoServer
cd ~/CouchPotatoServer # or wherever you have it stored
python CouchPotato.py

# Now you should see *HDTorrents.it* as one of the prodivers for Torrents. Enable it!
# It's suggested to add *ita, italian, sub ita* etc. as "preferred keywords" and also "required keywords"
# in "Setting" -> "Searcher" -> "Preferred Words"if you use other providers that may contain sources in
# different languages. This will give Italian releases a higher score.
# Also make sure you don't have the "italian" string among the "ignored keywords"!

# IMPORTANT: in order to retrieve all the results of a search, you need to login to HDTorrents.it, then go
# to "Modifica profilo" and set the value of "Torrents per pagina" to a very high value, i.e.: 9999
```
