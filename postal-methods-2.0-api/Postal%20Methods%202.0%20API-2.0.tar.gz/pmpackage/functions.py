import json
import requests


class JSONObject:
  def __init__( self, dict ):
      vars(self).update( dict )

class Response:
    status = 0
    errorMessage = ''
    result = None

class Address:
    def __init__(self, company = None,address1= None,address2= None,city= None
                 ,state= None,zip= None,country= None):
        self.company = company
        self.address1 =  address1
        self.address2 = address2
        self.city = city
        self.zip = zip
        self.state = state
        self.country = country

class PMAPI():
    def __init__(self, apiKey):
        self.ApiKey = apiKey
        self.url = 'https://api.secure.postalmethods.com/v1/'

    def SendLetter(self, myDescription="",
                   perforation=False,
                   replyOnEnvelope=False,
                   returnAddress=None,
                   File=None, fileUrl='',
                   isDoubleSided=False,
                   isColored=False,
                   urlFileExtension='',
                   refId='',
                   returnAddressPosition=1,
                   isReturnAddressAppended=False
                   ):
        if returnAddress is None:
            returnAddress = Address()
        payload = {
            'myDescription': (None, myDescription),
            'perforation': (None, perforation),
            'replyOnEnvelope': (None, replyOnEnvelope),
            'returnAddress.Company': (None, returnAddress.company),
            'returnAddress.AddressLine1': (None, returnAddress.address1),
            'returnAddress.AddressLine2': (None, returnAddress.address2),
            'returnAddress.City': (None, returnAddress.city),
            'returnAddress.State': (None, returnAddress.state),
            'returnAddress.Zipcode': (None, returnAddress.zip),
            'returnAddress.Country': (None, returnAddress.country),
            'File': File, 'fileUrl': (None, fileUrl),
            'isDoubleSided': (None, isDoubleSided),
            'isColored': (None, isColored),
            'urlFileExtension': (None, urlFileExtension),
            'refId': (None, refId),
            'returnAddressPosition': (None, returnAddressPosition),
            'isReturnAddressAppended': (None, isReturnAddressAppended)
        }

        url = self.url + 'Letter/send'
        headers = {'Secret-Key': self.ApiKey}
        req = requests.post(url, files=payload, headers=headers)
        resp = Response()
        resp.status = req.status_code
        jsonobject = json.loads(req.text, object_hook=JSONObject)
        if req.status_code == 200:
            resp.result = jsonobject.result
        else:
            resp.errorMessage = jsonobject.error.message

        return resp

    def SendLetterWithAddress(self, myDescription="",
                              perforation=False,
                              replyOnEnvelope=False,
                              returnAddress=None,
                              sendToAddress=None,
                              File=None, fileUrl='',
                              templateId=0,
                              isDoubleSided=False,
                              isColored=False,
                              urlFileExtension='',
                              refId='',
                              returnAddressPosition=1,
                              isReturnAddressAppended=False
                              ):
        if returnAddress is None:
            returnAddress = Address()
        if sendToAddress is None:
            sendToAddress = Address()
        payload = {'myDescription': (None, myDescription),
                   'perforation': (None, perforation),
                   'replyOnEnvelope': (None, replyOnEnvelope),
                   'returnAddress.Company': (None, returnAddress.company),
                   'returnAddress.AddressLine1': (None, returnAddress.address1),
                   'returnAddress.AddressLine2': (None, returnAddress.address2),
                   'returnAddress.City': (None, returnAddress.city),
                   'returnAddress.State': (None, returnAddress.state),
                   'returnAddress.Zipcode': (None, returnAddress.zip),
                   'returnAddress.Country': (None, returnAddress.country),
                   'sendToAddress.State': (None, sendToAddress.state),
                   'sendToAddress.City': (None, sendToAddress.city),
                   'sendToAddress.Zipcode': (None, sendToAddress.zip),
                   'sendToAddress.AddressLine1': (None, sendToAddress.address1),
                   'sendToAddress.Country': (None, sendToAddress.country),
                   'sendToAddress.Company': (None, sendToAddress.company),
                   'sendToAddress.AddressLine2': (None, sendToAddress.address2),
                   'File': File, 'fileUrl': (None, fileUrl),
                   'templateId': (None, templateId),
                   'isDoubleSided': (None, isDoubleSided),
                   'isColored': (None, isColored),
                   'urlFileExtension': (None, urlFileExtension),
                   'refId': (None, refId),
                   'returnAddressPosition': (None, returnAddressPosition),
                   'isReturnAddressAppended': (None, isReturnAddressAppended)
                   }

        url = self.url + 'Letter/sendWithAddress'
        headers = {'Secret-Key': self.ApiKey}
        req = requests.post(url, files=payload, headers=headers)
        resp = Response()
        resp.status = req.status_code
        jsonobject = json.loads(req.text, object_hook=JSONObject)
        if req.status_code == 200:
            resp.result = jsonobject.result
        else:
            resp.errorMessage = jsonobject.error.message

        return resp

    def GetPDF(self, RequestId):
        url = self.url + 'Letter/' + str(RequestId) + '/pdf'
        headers = {'Secret-Key': self.ApiKey}
        req = requests.get(url, headers=headers)
        resp = Response()
        resp.status = req.status_code
        if req.status_code == 200:
            resp.result = req.text
        else:
            resp.errorMessage = 'Error Getting File'
        return resp

    def GetLetterStatus(self, RequestIds):
        url = self.url + 'Letter/status?Id=' + str(RequestIds[0])
        for Id in range(1, len(RequestIds)):
            url = url + '&Id=' + str(RequestIds[Id])
        headers = {'Secret-Key': self.ApiKey}
        req = requests.get(url, headers=headers)
        resp = Response()
        resp.status = req.status_code
        jsonobject = json.loads(req.text, object_hook=JSONObject)
        if req.status_code == 200:
            resp.result = jsonobject.result
        else:
            resp.errorMessage = jsonobject.error.message

        return resp

    def GetLetterDetails(self, RequestId):
        url = self.url + 'Letter/' + str(RequestId)
        headers = {'Secret-Key': self.ApiKey}
        req = requests.get(url, headers=headers)
        resp = Response()
        resp.status = req.status_code
        jsonobject = json.loads(req.text, object_hook=JSONObject)
        if req.status_code == 200:
            resp.result = jsonobject.result
        else:
            resp.errorMessage = jsonobject.error.message

        return resp

    def CancelDelivery(self, RequestId):
        url = self.url + 'Letter/' + str(RequestId) + '/cancel'
        headers = {'Secret-Key': self.ApiKey}
        req = requests.put(url, headers=headers)
        resp = Response()
        resp.status = req.status_code
        jsonobject = json.loads(req.text, object_hook=JSONObject)
        if req.status_code == 200:
            resp.result = jsonobject.result
        else:
            resp.errorMessage = jsonobject.error.message

        return resp
