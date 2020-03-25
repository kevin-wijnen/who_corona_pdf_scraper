# WHO Corona PDF Scraper
My attempt to scrape data from the situation reports published daily by the World Health Organization.

With this project I try to scrape data from the situation reports that are published by the World Health Organization. These reports are in PDF and contain a table with information about:
- Total confirmed cases
- Total new cases
- Total deaths
- Total new deaths

Problems I have to look out for are:
- The fact that I am reading a PDF so reading a PDF in code brings characters with them
- New countries appearing (These are marked red)
- The link build up (Ends with: "20200324-sitrep-64-covid-19.pdf". Important is to look out for the "20200324"(date) and "64"(number of report))

## Version 1.0
The basics are set up. That means downloading and reading the data. I also created to functions to sort the data from low to high and from high to low.

### Setup
To use these scripts you need the following modules installed:
- PyPDF2
- pycountry
- requests (for PDFDownloader)

### How to use
Import WHOCoronaDataScraper into you Python project and call get_latest_WHO_Data(). It returns two lists: data & headers. Data contains a list of dictionaries per country. Headers contains a list with all the header names which is useful for dataframes in pandas for the future.

### Technical information (for other developers or enthousiasts)
I made a seperate script that downloads the PDF. It takes the link, folder you want it to store in and filename. It returns FALSE if it gets a 404 meaning the file does not exist and TRUE if it does. If it's TRUE then it downloads the PDF in your chosen filename and stores it in you chosen folder.

The other script takes the PDF from the folder en opens it. Then it splits the PDF by newline and starts going through the created list. If it finds a country (by compairing it to the list of countries in pycountry) then is creates a dictionary of that country with the corresponding data and adds it to the list. In the end it returns the data and a list of headers to use for pandas if you want.
