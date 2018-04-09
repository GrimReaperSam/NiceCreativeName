## Crawler

Crawl raw renew docs from http://uro.gov.taipei/ .
* Save pdf to _Crawler_

## Extracter

Takes only the 3rd-5th page from the original pdf. 
* Requires **pdfextract**
* Takes pdf from _Crawler_
* Saves pdf to _Pdf_

## OCR

Converts pdf to txt using Google Drive API. 
* Takes pdf from _Pdf_
* Saves txt to _Text_

## Parser

Parses raw text into csv of location + landnumber. 
* Takes txt from _Text_
* Saves csv to _LandNumber_
* BUGGY RESULT!

## GeoJson

Gets GeoJson of renew cases using  https://twland.ronny.tw .
* Takes csv to _LandNumber_
* Saves json to _GeoJson_