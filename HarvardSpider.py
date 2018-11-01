from Spider import *

class HarvardSpider(Spider):

    def __init__(self, baseURL, delay, fileName):
        super().__init__(baseURL, delay, fileName)

    def crawl(self, maxDatasets):

        # setting up tracking variables
        rows = 10
        curCount = 0
        start = 0
        
        # Loading already scaped dataset dictonary from json file
        self.loadDataFromFile()

        while curCount < maxDatasets:

            url = self.baseURL + '/api/search?q=*&fq=metadataSource:"Harvard Dataverse"' + '&type=dataset' + "&start="  + str(start) 
            response = requests.get(url)
            data = response.json()
            pp.pprint(data)
           
            # Reading in all datasets from one response(MAX : 10 )
            for row in data['data']['items']:

                print("In Inner Loop"+ "\n\n")

                dataset_url = row['url']

                if(row['type'] == 'dataset'):
                    meta_data = super().extract_metadata(dataset_url)
                   
                    #adding dataset to hashMap
                    if(self.cacheDataset(meta_data)):
                        curCount += 1
                        pp.pprint(meta_data)
                    else:
                        print("Skipping Dataset due to json format error/ No metadata present")

                    if(curCount == maxDatasets):
                        break

                    # Crawler delay
                    time.sleep(self.delay)

            # Page offset
            start += rows
            print(start)

         # Write to File
        self.writeCacheToFile()