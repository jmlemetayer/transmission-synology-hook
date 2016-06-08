#!/usr/bin/env python

import json
import os
import requests
import urlparse

class synology:

    def __init__(self, base_url):
        self.base_url = base_url
        self.sid = None
        self.info = self.getinfo('all')

    def basereq(self, api, method, path, version, data={}):
        url = urlparse.urljoin(urlparse.urljoin(self.base_url, 'webapi/'), path)
        cookies = dict()
        data['api'] = api
        data['method'] = method
        data['version'] = version
        if self.sid != None:
            cookies['id'] = self.sid
        result = requests.post(url, data, cookies=cookies, timeout=10)
        response = json.loads(result.text)
        assert response, "Empty response"
        assert response['success'], "Invalid response"
        assert response['success'] == True, "Failed response"
        if 'data' in response:
            return response['data']
        return

    def getinfo(self, query):
        data = dict()
        data['query'] = query
        return self.basereq('SYNO.API.Info', 'query', 'query.cgi', 1, data)

    def request(self, api, method, data={}):
        info = self.info[api]
        assert info, "Unknown API"
        return self.basereq(api, method, info['path'], info['maxVersion'], data)

    def login(self, account, passwd):
        data = dict()
        data['session'] = 'DownloadStation'
        data['account'] = account
        data['passwd'] = passwd
        response = self.request('SYNO.API.Auth', 'login', data)
        assert response['sid'], "No SID in login response"
        self.sid = response['sid']

    def logout(self):
        data = dict()
        data['session'] = 'DownloadStation'
        self.request('SYNO.API.Auth', 'logout', data)
        self.sid = None

    def mkdir(self, folder_path, name):
        data = dict()
        data['force_parent'] = 'true'
        data['folder_path'] = os.path.join('/', folder_path.strip('/'))
        data['name'] = name.strip('/')
        self.request('SYNO.FileStation.CreateFolder', 'create', data)

    def download(self, urls, destination, username=None, password=None):
        data = dict()
        data['create_list'] = 'true'
        data['type'] = 'url'
        data['destination'] = '"' + destination.strip('/') + '"'
        data['url'] = json.dumps(urls)
        if username != None:
            data['username'] = '"' + username + '"'
        if password != None:
            data['password'] = '"' + password + '"'
        self.request('SYNO.DownloadStation2.Task', 'create', data)
