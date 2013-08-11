from unittest import TestCase

import yaml
import os
import urllib


def config():
    configpath = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(configpath) as f:
        return yaml.load(f.read())


def construct_api_url(config, endpoint):
    c = config
    return c['api_protocol'] + '://' + c['api_host'] + ':' + \
        str(c['api_port']) + '/' + str(c['api_version']) + '/' + \
        endpoint


def api_call(url, method, data):
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    if method == 'GET':
        u = urllib.request.urlopen(url + '?' + encoded_data.decode('utf-8'))
    elif method == 'POST':
        u = urllib.request.urlopen(url, encoded_data)
    else:
        raise ValueError('Unsupported Method Type')

    return u.read()


class TestHelpers(TestCase):
    def test_config(self):
        c = config()
        self.assertTrue('api_version' in c.keys())
        self.assertIsInstance(c['api_version'], int)
        self.assertTrue('api_protocol' in c)
        self.assertTrue(c['api_protocol'] in ['http', 'https'])
        self.assertTrue('api_host' in c)
        self.assertIsInstance(c['api_port'], int)
        self.assertTrue('api_port' in c)
        self.assertIsInstance(c['api_port'], int)

    def test_construct_api_url(self):
        config = {'api_version': 0,
                  'api_protocol': 'http',
                  'api_host': 'localhost',
                  'api_port': 5000}
        self.assertEquals(construct_api_url(config, 'foo'),
                          'http://localhost:5000/0/foo')

    def test_api_call(self):
        self.assertIsNotNone(api_call(url="http://posttestserver.com/post.php", data={}, method='POST'))
        self.assertIsNotNone(api_call(url="http://www.google.de", data={}, method='GET'))
