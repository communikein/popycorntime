# popycorntime
An automated tool to look for TV Shows episodes and download them via torrent files

## INSTALL
To be able to use this script we will have to go through 4 steps:
1. Download and install both Python 2.7 and qBittorrent
  Here are the links to both the programs you will need to install:
    * Python 2.7 - [link to download](https://www.python.org/download/releases/2.7/)
    * qBittorrent - [link to download](https://www.qbittorrent.org/)

2. Install the required python libraries
  Once both the program are installed, we now need to install the python libraries used by the script.
  We are going to use four different libraries:
    * urllib2
    * json
    * BautifulSoup
    * qbittorrent
  
  To install them, simply open the command line, type the following commands and hit enter after every single one of them:
  ```
  pip install urllib2
  pip install BeautifulSoup
  pip install qbittorrent
  ```

3. Setup qBittorrent for remote use
    * Open the *preferences* menu
    * Go to the *Web UI* subsection
    * Enable *Web User Interface (Remote control)* by ticking the box next to it
    * In the *IP address* field insert *127.0.0.1*
    * In the *Port* field insert *8080*
    * In the *authentication* section:
      * In the *Username* field insert *admin*
      * In the *Password* field insert *administrator*
    * Click *OK*

4. Configure the script to use qBittorrent
  If you did all the steps in the previous step (Step 3.), then you are good to go.
  
