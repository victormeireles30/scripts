# -*- encoding:utf-8 -*-
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from get_prices import *
import threading

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
	setup_testing_defaults(environ)

	status = '200 OK'
	headers = [('Content-type', 'text/plain; charset=utf-8')]

	start_response(status, headers)

	get_prices_thread = threading.Thread(target=get_prices)
	get_prices_thread.daemon = True
	if threading.active_count() == 1:
		get_prices_thread.start()

	ret = [b'Running...\n',b'Check https://docs.google.com/spreadsheets/d/1veuor_lsPmqPMHhUN_78eV6vuSRKemdalbLMfICun2g/edit#gid=965121549 for results.']
	return ret

with make_server('', 8000, simple_app) as httpd:
	print("Serving on port 8000...")
	httpd.serve_forever()