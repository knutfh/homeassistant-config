import appdaemon.plugins.hass.hassapi as hass

import datetime
import requests

class DoDns(hass.Hass):


    def initialize(self):
        self.log("DigitalOcean Dynamic DNS initialized")

        self.apikey = self.args['api_key']
        self.domain = self.args['domain']

        self.url = f'https://api.digitalocean.com/v2/domains/{self.domain}/records/'
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': 'Bearer ' + self.apikey
        }

        self.listen_event(self.run_cb, event='update_dns')

        self.run_hourly(self.run_cb, datetime.time(0, 16, 0))


    def run_cb(self, kwargs):
        #self.log(f"Updating DNS at {self.now()}")
        self.select_and_update_records(self.get_domain_records())

    def get_current_ip(self):
        return requests.get('https://api.ipify.org').text.rstrip()


    def get_domain_records(self):
        records = self.session.get(self.url).json()
        return records['domain_records']


    def update_dns(self, record_id, new_ip):
        """
        Update a given record ID with a new IP address
        :param record_id: Which DNS record to update
        :param new_ip: Give DNS record this IP address
        """
        response = self.session.put(self.url + str(record_id), json={'data': new_ip})
        if response.ok:
            self.log('IP address updated successfully to ' + new_ip)
        else:
            self.log('IP address update failed with message: ' + response.text)


    def select_and_update_records(self, records):
        current_ip = self.get_current_ip()
        self.log(f'Current IP is {current_ip}')

        for record in records:
            if record['type'] == 'A':
                self.log(f'Processing id {record["id"]} with name {record["name"]} and IP {record["data"]}')
                if not record['data'] == current_ip:
                    self.log(f'IP is not equal to new IP. Update it.')
                    self.update_dns(record['id'], current_ip)
                else:
                    self.log(f'IP equal to new IP. Skip.')