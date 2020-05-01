import http.client
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import pandas as pd

extracted_data=[]

class BikeScraper():
    feature_list=['Body Type', 'Fuel Type', 'Engine Description', 'Fuel System', 'Cooling', 'Displacement', 'Maximum Power', 'Maximum Torque', 'Number of Cylinders', 'Bore', 'Stroke', 'Number of Gears', 'Clutch', 'Gearbox Type', 'Front Brake', 'Rear Brake', 'Front Suspension', 'Rear Suspension', '0-100 kmph', 'Overall Length', 'Overall Width', 'Overall Height', 'Seat Height', 'Ground Clearance', 'Wheelbase', 'Kerb/Wet Weight', 'Fuel Tank Capacity', 'Speedometer', 'Tachometer', 'Trip Meter', 'Clock', 'Electric Start']
    i=1

    def fetch_specs(self, company_name, status, model, price, spec_link):
        print(self.i)
        self.i+=1
        single_data={}
        single_data['company_name']=company_name
        single_data['status']=status
        single_data['model']=model
        single_data['price']=price
        page3 = requests.get(spec_link)
        soup3 = BeautifulSoup(page3.text, 'html.parser')
        try:
            specs_sheet = soup3.find("div", {"id": "veh-details"})
            for specs in specs_sheet.find_all('tr'):
                if(len(list(specs))==5):
                    # print(specs)
                    feature= specs.find(class_='specs-label col-md-7 col-xs-6').text
                    value= specs.find(class_='specs-value col-md-5 col-xs-6').text
                    if value=="":
                        if(specs.find(class_='specs-value col-md-5 col-xs-6').find(class_='icon icon-check-mark')):
                            value=1
                        else: value=0
                    if(feature in self.feature_list):
                        single_data[feature]=value

            for x in self.feature_list:
                if x not in single_data.keys():
                    single_data[x]="NaN"
            extracted_data.append(single_data)
            # pprint(single_data)
        except:
            pass



    def fetch_bike_details(self, company_name, status, data):
        for i in data.find_all(class_='col-sm-4 col-md-3 col-xs-6 comp-models'):
            spec_link= i.find('a', href=True)['href']
            price=list(i.find(class_='price text-info'))[2]
            print(company_name, "---", status, "---", i.b.text, "---", price, "---", spec_link)
            self.fetch_specs(company_name, status, i.b.text, price, spec_link)


    def company_bikes(self, link, company_name):
        page2 = requests.get(link)
        soup2 = BeautifulSoup(page2.text, 'html.parser')

        available_data= soup2.find("div", {"id": "available"})
        if(available_data!=None):
            status="available"
            self.fetch_bike_details(company_name, status, available_data)

        expected_data= soup2.find("div", {"id": "expected"})
        if(expected_data!=None):
            status="expected"
            self.fetch_bike_details(company_name, status, expected_data)

        discontinued_data= soup2.find("div", {"id": "discontinued"})
        if(discontinued_data!=None):
            status="discontinued"
            self.fetch_bike_details(company_name, status, discontinued_data)

        no_launch_data= soup2.find("div", {"id": "no-launch-plans"})
        if(no_launch_data!=None):
            status="no-launch-plans"
            self.fetch_bike_details(company_name, status, no_launch_data)


    def company_list(self):
        single_data={}
        page = requests.get('https://autos.maxabout.com/bikes/companies')
        soup = BeautifulSoup(page.text, 'html.parser')
        for company in soup.find_all(class_='col-sm-3 col-md-2 col-xs-6 companies'):
            company_name= company.find(class_='info').text
            link= company.find('a', href=True)['href']
            single_data['company_name']= company_name
            # print(company_name, link)
            self.company_bikes(link, company_name)



obj= BikeScraper()
obj.company_list()
df= pd.DataFrame.from_dict(extracted_data)

df=df[['company_name','model','price','status','Body Type','Fuel Type','Engine Description','Fuel System','Cooling','Displacement','Maximum Power','Maximum Torque','Number of Cylinders','Overall Length','Overall Width','Overall Height','Seat Height','Ground Clearance','Wheelbase','Kerb/Wet Weight','Fuel Tank Capacity','Bore','Stroke','Number of Gears','Clutch','Gearbox Type','Front Brake','Rear Brake','Front Suspension','Rear Suspension','0-100 kmph','Speedometer','Tachometer','Trip Meter','Clock','Electric Start']]

df.to_excel('Bike_data.xlsx')






