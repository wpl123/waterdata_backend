import pandas as pd
import urllib.request
import requests
import json



# {"error_num":0,"return":
#    {"traces":[
#        {"error_num":0,"compressed":"0","site_details":
#            {"timezone":"10.0","short_name":"RICHMOND @ LAVELLES","longitude":"152.891551000","name":"RICHMOND RIVER AT LAVELLES ROAD","latitude":"-28.450382000","org_name":"WaterNSW"},
#            "quality_codes":{"255":"Data Unavailable","100":"Quality unknown"},
#            "trace":[
#                {"v":"0","t":20101027000000,"q":255},{"v":"0","t":20101027000100,"q":255},{"v":"0","t":20101027000200,"q":255},{"v":"0","t":20101027000300,"q":255},{"v":"0","t":20101027000400,"q":255},{"v":"0","t":20101027000500,"q":255},


def getResponseFromURL(url):  
    response = requests.get(url)
    jsonData = response.json() 
    if response and response.status_code == 200:
        return jsonData
    else:
        print("Error receiving data ", response.status_code)    


def getResponseFromFile(fname):
    
    with open(fname) as jsonData:
        data = json.load(jsonData)
        return jsonData
           

def displayResponse(_data):
    tracelist = []
    waterdata = _data['return']['traces']
    for tracesdict in waterdata:    #traces
        tracedata = tracesdict['trace']
        for tracedict in tracedata:
            tracelist.append(tracedict)
            df = pd.DataFrame(tracelist)
    print(df)     


def main():

    url = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":"203056","start_time":"20101027000000","interval":"minute","var_list":"100.00,140.01,232","datasource":"A","end_time":"20101114000000","data_type":"mean","rounding":[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],"multiplier":"1"}}'
    shorturl = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":"203056","start_time":"20101027000000","interval":"minute","var_list":"100.00,140.01,232","datasource":"A","end_time":"20101028000000","data_type":"mean","rounding":[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],"multiplier":"1"}}'

    #data = getResponseFromFile('./app/gibbo_code/downloads/test3.json') 
    data = getResponseFromURL(shorturl) 
    status = displayResponse(data)

if __name__ == "__main__":
    main()        