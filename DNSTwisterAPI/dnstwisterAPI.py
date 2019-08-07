import requests
import csv
import datetime

url_data = {} #all data to cycle through from specific domain
bad_ips = [] #placeholder for bad ips
bad_domains = [] #placeholder for bad domains
test_domains = [] #placeholder for test domains
                     

def cycle_domains():
  read_csv_bad_items()
  read_csv_test_domains()
  for domain in test_domains:
   fuzz_url(domain)
   url_data = {} #clear old list for specific domain
    
def fuzz_url(url):
  get_urls(url)
  response_fuzz = requests.get(fuzz_urls)
  todos_fuzz = response_fuzz.json()
  global fuzzy_domains
  fuzzy_domains = todos_fuzz['fuzzy_domains']
  global iffyurls
  for iffyurls in fuzzy_domains:
    ip_url(iffyurls['resolve_ip_url'])
  #print (url_data)
  #print (bad_ips)
  #print (bad_domains)
    
def get_urls(url):
  response = requests.get("https://dnstwister.report/api/to_hex/"+url)
  todos = response.json()
  global domain_name
  global domain_hex
  global fuzz_urls
  global parked_score_url
  global resolve_ip_url
  global complete_url
  domain_name = todos['domain']
  domain_hex = todos['domain_as_hexadecimal']
  fuzz_urls = todos['fuzz_url']
  parked_score_url = todos['parked_score_url']
  resolve_ip_url = todos['resolve_ip_url']
  complete_url = todos['url']

  
def ip_url(hex_url):
  #print(hex_url)
  response = requests.get(hex_url)
  todos_ip = response.json()
  received_ip = todos_ip['ip']
  if received_ip == False:
    print ('1')
  elif iffyurls['domain'] == domain_name:
    print ('2')
    #return None
  else:
    url_data[iffyurls['domain']] = received_ip
    incident_creation(received_ip,iffyurls['domain'])
    print ('3')

    
def incident_creation(ip,domain):
  if ip not in bad_ips and domain not in bad_domains:
    write_csv_incident(ip, domain, "new ip and domain parked")
    write_csv_bad_items(ip,domain)
  elif ip not in bad_ips:
    write_csv_bad_items(ip,domain)
    write_csv_incident(ip, domain, "ip change, domain no-change")
  elif domain not in bad_domains:
    write_csv_bad_items(ip,domain)
    write_csv_incident(ip, domain, "ip no-change, domain change")#MIGHT NEED TO MAKE A CSV EACH TIME 
  else:
    return None
  
def write_csv_incident(ip, domain, cause):
  with open(r'C:\Users\David\Documents\DNSTwisterAPI\incident_list.csv', mode='a', newline = '\n') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    currentDT = datetime.datetime.now()
    time = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    writer.writerow([ip, domain, cause, time])


def write_csv_bad_items(ip, domain):
  with open(r'C:\Users\David\Documents\DNSTwisterAPI\bad_items.csv', mode='a', newline='\n') as file:
    currentDT = datetime.datetime.now()
    time = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([ip, domain, time])

def read_csv_bad_items():
  with open(r'C:\Users\David\Documents\DNSTwisterAPI\bad_items.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        bad_ips.append(row[0])
        bad_domains.append(row[1])
  
def read_csv_test_domains():
  with open(r'C:\Users\David\Documents\DNSTwisterAPI\test_domains.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        test_domains.append(row[0])
        

cycle_domains()