import json
import sys
from http import client


def connect_to_api(domain, request):
    connection = client.HTTPSConnection(domain)
    connection.request("GET", request)
    response = connection.getresponse().read().decode("utf-8")
    return json.loads(response)


def check_dns(name):
    json_response = connect_to_api("dns.google.com", "/resolve?name=" + name + "&type=A")
    ips_list = []
    for answer in json_response.get('Answer'):
        data = answer.get('data')
        splitted_data = data.split('.')
        if splitted_data[0].isnumeric():
            ips_list.append(data)
    return ips_list


def check_ip(ip_list, api_key):
    list_organization = []
    for ip in ip_list:
        json_response = connect_to_api("www.whoisxmlapi.com", "/whoisserver/WhoisService?apiKey=" + api_key + "&domainName=" + ip + "&outputFormat=JSON")
        for record in json_response.get('WhoisRecord').get('subRecords'):
            list_organization.append(record.get('registrant').get('organization'))

    return list_organization


page = sys.argv[1]
api_key = sys.argv[2]
ip_list = check_dns(page)
organizations = check_ip(ip_list, api_key)
print(organizations)
