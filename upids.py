import base64
import requests
import re

# A simple Python script that retrieves published (and unpublished) media IDs
# for CBC Radio audio that lives in MPX. Logs in to MPX using supplied credentials
# and retrieves items with recent publish dates.

# Config
mpx_user = "firstname.lastname@cbc.ca"
mpx_password = "enter_password_here"
show = "Spark"
number_of_results = 10

# Authenticate
auth_endpoint = "https://identity.auth.theplatform.com/idm/web/Authentication/signIn?schema=1.0&form=json&_duration=3600000"
headers = { "Authorization": "Basic %s" % base64.b64encode("mps/" + mpx_user + ":" + mpx_password) }

s = requests.Session()
r = s.get(auth_endpoint, headers=headers)
auth_token = r.json().get('signInResponse').get('token')

params = { 'token': auth_token,
		   'range': '1-%s' % number_of_results,
		   'sort': 'pubDate|desc',
		   'byCustomValue': "{show}{%s}" % show,
		   'account': 'http://access.auth.theplatform.com/data/Account/1186324321',
		   'schema': '1.6.0',
		   'form': 'json',
		   'pretty': 'true' }

base = 'http://mps.theplatform.com/data/Media'
r = s.get(base, params=params)

entries = r.json().get('entries')

for entry in entries:
	entry_id_url = entry.get('id')
	entry_id = re.search(r'\d{10}', entry_id_url).group()

	desktop_id_url = entry.get('media$content')[0].get('plfile$releases')[0].get('id')
	desktop_id = re.search(r'\d{10}', desktop_id_url).group()

	print '''%s\nDesktop ID: %s\nMobile ID: %s\n''' % (entry.get('title'), desktop_id, entry_id)