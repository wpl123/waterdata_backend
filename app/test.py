import pandas as pd
import codecs

def check_codecs(filename):
    try:
        f = codecs.open(filename, encoding='utf-8', errors='strict')    #utf-8 NO --> utf-16, ansi, unicode
        for line in f:
            pass
        result = "Valid utf-8"
    except UnicodeDecodeError:
        result = "invalid utf-8"
    return result

def download_csvdata(download_dir):
#    print(download_url)
    print("inside download_csv_data")
    for i in range(2010,2022):
        for j in range(1,12):
            download_dir1 = download_dir.replace('YYYY',str(i))
            download_dir2 = download_dir1.replace('MM', str(j).zfill(2))
            result = check_codecs(download_dir2)
            print(result + ' ' + download_dir2)
            
            
def main():
    download_url = 'http://www.bom.gov.au/watl/eto/tables/nsw/narrabri_airport/narrabri_airport-YYYYMM.csv' 
    download_dir = "/home/admin/dockers/waterdata_backend/data/api/narrabri_airport-YYYYMM.csv"
    

    meter_no = "054038"
    print(download_dir)
    download_csvdata(download_dir)           
    

if __name__ == "__main__":
    main()    