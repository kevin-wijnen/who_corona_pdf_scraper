import PyPDF2
import PDFDownloader
from datetime import date, datetime, timedelta
import pycountry

link = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/{}-sitrep-{}-covid-19.pdf' # Link to the pdf

firstDate = datetime.strptime("21-1-2020", "%d-%m-%Y").date() # Date of first publication

countries=[f.name for f in pycountry.countries] # List of all countries found in pycountry


def prepare_WHO_grabberdata(date): # Takes a date and gives a formatted date en number back to use in the link
    issuenumber = (date-firstDate).days + 1
    if date.month < 10:
        str_month = "0"+str(date.month)
    else:
        str_month = str(date.month)
    strToday = str(date.year)+str_month+str(date.day)
    return strToday, issuenumber


def get_latest_WHO_Data():
    # Date and issue of today
    today = datetime.now().date()
    strToday, issuenumber_today = prepare_WHO_grabberdata(today)

    # Date and issue of yesterday
    yesterday = today - timedelta(1)
    strYesterday, issuenumber_yesterday = prepare_WHO_grabberdata(yesterday)

    data = [] # Empty list of data
    headers = ['country','total confirmed cases','total deaths','total new deaths'] # List of headers

    try: # Looking if there is a PDF file of the issue of today in the folder
        pdfFileObj = open("rawPDFdata/file-{}.pdf".format(issuenumber_today), 'rb')

    except IOError as e: # Issue of today is not in folder doesn't exist in folder so it has to be grabbed from WHO
        print(e)
        searchlink = link.format(strToday,str(issuenumber_today)) # Creating the link and calling the PDFDownloader to grab the issue of today

        if PDFDownloader.download_PDF(searchlink,"rawPDFdata", "file-{}".format(str(issuenumber_today))):
            pdfFileObj = open("rawPDFdata/file-{}.pdf".format(str(issuenumber_today)), 'rb')

        else: # Issue of today doesn't exist so yesterday has to be grabbed
            try:
                pdfFileObj = open("rawPDFdata/file-{}.pdf".format(issuenumber_yesterday), 'rb')
            except IOError as f:
                print(f)
                searchlink = link.format(strToday, issuenumber_yesterday)
                PDFDownloader.download_PDF(searchlink,"rawPDFdata", "file-{}".format(str(issuenumber_yesterday)))
                pdfFileObj = open("rawPDFdata/file-{}.pdf".format(str(issuenumber_yesterday)), 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    #### Convert data from pdf into list of dictionaries ####
    for pageNum in range(0,pdfReader.getNumPages()):
        page = pdfReader.getPage(pageNum)
        splitpage = page.extractText().split("\n")

        # print('Length: ', len(splitpage))
        for x in range(0, len(splitpage)):
            if splitpage[x] in countries:
                datarow = {}
                datarow['country'] = splitpage[x]
                datarow['total confirmed cases'] = int(splitpage[x+2])
                datarow['total confirmed new cases'] = int(splitpage[x+4])
                datarow['total deaths'] = int(splitpage[x+6])
                datarow['total new deaths'] = int(splitpage[x+8])
                data.append(datarow)
    pdfFileObj.close()
    print('Done')
    return data, headers

def sort_WHO_data_high_to_low(data):
    sorted_data = sorted(data, key=lambda i:i['cases'], reverse=True)
    for x in range(1,len(sorted_data)+1):
        sorted_data[x-1]['index'] = x
    return sorted_data

def sort_WHO_data_low_to_high(data):
    sorted_data = sorted(data, key=lambda i:i['cases'])
    for x in range(1, len(sorted_data)+1):
        sorted_data[x]['index'] = x
    return sorted_data