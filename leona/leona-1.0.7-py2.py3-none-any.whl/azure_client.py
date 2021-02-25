from src.imports import os
from src.imports import environ
from src.imports import requests
from src.imports import json
from src.utils import get_config
import azurerm

config = get_config()
client_secret = config["azure"]["secret"]
client_id = config["azure"]["client"]
tenant_id = config["azure"]["tenant"]
subscription_id = config["azure"]["subscription"]
resource = config["azure"]["resource"]

# client_id = "1e29a510-f542-40b1-ac65-c12315e0c689"
# client_secret = "7npFT-V5bo_.Rc-slNYFbM7JOsW9LITk4K"
# tenant_id = "47e31edf-3674-44b6-b3fd-758b52669dd9"
# subscription_id = "e995aa90-9440-4208-90b4-87fd3d3312a3"
# resource = "https://management.azure.com/"


def get_healthcheck():
  res_id, summary = ([] for i in range(2))
  access_token = azurerm.get_access_token(tenant_id, client_id, client_secret)
  headers = {'Authorization': 'Bearer ' + access_token}
  url = "https://management.azure.com/subscriptions/%s/providers/Microsoft.ResourceHealth/availabilityStatuses?api-version=2018-07-01" % (subscription_id)
  response = requests.get(url,headers=headers)
  response = json.loads(response.text)
  for item in response['value']:
    res_id.append(item['id'])
    summary.append(item['properties']['summary'])
  log = "\n".join("{}".format(x) for x in zip(summary))
  formated_log = str(log).replace('("',"").replace('.",)', "")
  formated_log = str(formated_log).replace("('","").replace(".',)", "")
  print(formated_log)
  
   



