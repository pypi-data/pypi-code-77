import requests
from bs4 import BeautifulSoup
import datetime

class beginCheck:
    def __init__(self, from_date=False, to_date= False, from_currency ='EUR', to_currency='KES'):
        URL = 'https://www.currency-converter.org.uk/currency-rates/historical/table/%s-%s.html'%(from_currency, to_currency)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        financialTable = soup.find("table") 
        financialTableRows = str(financialTable).split('</tr>')
        
        self.gotten_currency = {}
        
        for row in financialTableRows:
            tdResults = row.split('\n')
            try:
                day = tdResults[1].replace('<td>','').replace('</td>', '')
                date = tdResults[2].replace('<td>','').replace('</td>', '').replace('/', '-')
                if from_date:
                    if self.returnDateSysFormart(date) < self.returnDateSysFormart(from_date):
                        continue
                if to_date:
                    if self.returnDateSysFormart(date) > self.returnDateSysFormart(to_date):
                        continue
                date_sysformart = self.returnDateString(date)
                fromCurr = tdResults[3].replace('<td>','').replace('</td>', '')
                toCurr = tdResults[4].replace('<td>','').replace('</td>', '')
                self.gotten_currency[date_sysformart]={'value': eval(toCurr.replace(to_currency,'').replace(' ', '')), 'details':[day, date_sysformart, fromCurr+ toCurr]}
            except:
                pass
        
    
    def correctKey(self, tempDate):
        return self.returnDateString(self.returnDateSysFormart(tempDate))
    
    def returnDateString(self, thisDate):
        try:
            day = thisDate.day
            month = thisDate.month
            if(day < 10): day = '0%s'%(day)
            if(month < 10): month = '0%s'%(month)
            custom_date = '%s-%s-%s'%(thisDate.year, month, day)
        except:
            thisDate = self.returnDateSysFormart(thisDate)
            day = thisDate.day
            month = thisDate.month
            if(day < 10): day = '0%s'%(day)
            if(month < 10): month = '0%s'%(month)            
            custom_date = '%s-%s-%s'%(thisDate.year, month, day)  
        return custom_date;    

    def returnDateSysFormart(self, thisDate):
        try:
            custom_date = datetime.datetime.strptime(thisDate, '%Y-%m-%d')
        except:
            custom_date = datetime.datetime.strptime(thisDate, '%d-%m-%Y')
        return custom_date    

    def returnDateHumanFormart(self, thisDate):
        day, month, year = thisDate.day, thisDate.month, thisDate.year
        if day < 10:
            day = '0%s'%(day)
        if month < 10:
            month = '0%s'%(month)
        custom_date = '%s-%s-%s'%(day, month, year)
        return custom_date  
    
    def keysToList(self, dictData):
        testKeys = dictData.keys()
        newlist = list()
        for i in testKeys:
            newlist.append(i)  
        return newlist     
        

    