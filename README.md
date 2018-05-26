# Taipei Land Use #

In this repository, we collect data from multiple sources regarding renewal areas in Taipei City starting year 2012.

Our data is obtained thanks to 
 * [**Taipei Historical Maps**](https://www.historygis.udd.gov.taipei)
 * [**Taipei Urabn Development Department**](https://english.udd.gov.taipei/Default.aspx) for Illegal Rooftops
 * [**Taipei Urban Regeneration Office**](https://english.uro.gov.taipei/Default.aspx) for Renewal Areas
 * [**Taiwan National Development Council**](https://data.gov.tw/dataset/62206) for Land Prices
 
# Folders #
 
## Data ##
In this folder, we organize our obtained and cleaned data.
The final result concatenating everything is `Final.csv`
 
Particular files of interest:
 * `Land Prices 201X.csv`: Land price data for year 201X
 * `Output.csv`: List of Illegal Rooftops and their coordinates
  
## IPython ##
This folder contains jupyter notebook files where we experimented with different methods.

 * `GreenFinder.ipynb`: This notebook shows how we calculate the vegetation indices
 * `TSNE.ipynb`: This notebook shows how we built our TSNE posters
   
N.B.: The images are not uploaded to github due to their number and size. They can be recovered by using `Scripts\SnapRenewalAreas` in QGIS
   
## Latex Stuff ##
This folder contains **.tex** files we used to generate our report for the course

## OCR ##
This folder contains the scripts used to download and parse renewal areas data. It also contains the data in different subfolders:

 * `GeoJson`: GeoJson data files for each renewal area
 * `LandNumber`: Subdivisions of each renewal area
 * `Text`: Raw uncleaned text obtained after OCR on the scans
 
## Rooftop Address ##
Raw data for the illegal rooftop locations (District/Street Name)

## Scripts ##
Python scripts used in QGIS in order to analyse and generate our `final.csv` file as well as snapshots at different zoom levels for the satellite and infrared imagery:

 * `AddressToLatLon.py`: Transforms the raw illegal rooftop address into usable (lat,lon) coordinates
 * `DrawOnMap.py`: Reads the illegal rooftops and renewal area data and displays them on the map
 * `GenerateRenewalsQGIS.py`: Generates the first part of the information about renewal areas relating to illegal rooftops
 * `GenerateRenewalPython.py`: Generates the second part of the information abotu renewal areas relating to land prices, vegetation and dates
 * `SnapIllegalRooftops.py`: Takes snapshots of all the illegal rooftops and stores them in a specified folder
 * `SnapRenewalAreas.py`: Takes snapshots of all the renewal areas and stores them in a specified folder
 * `Utils.py`: Commonly used functions and variables
 
## Website ##
```diff
- YALAN PLEASE FILL THIS
 ``` 
