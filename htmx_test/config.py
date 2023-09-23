import inspect
import base64
import builtins
import datetime
import decimal
from decimal import Decimal
from logging import getLogger

# from Crypto import Random
from django.conf import settings
from django.core.cache import cache
#check table exist or not
from django.db import connections
from django.utils.translation import gettext as _

from  importlib import import_module
from pprint import pprint
import os
from os.path import join
import traceback
from django.contrib.humanize.templatetags.humanize import intcomma
import re
import os
from django.utils.http import urlencode
from django.urls import reverse
from django.core.files.storage import default_storage
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
import base64
import functools
import threading
def pp(*args):
	if settings.DEBUG:
		for arg in args:
			pprint(arg)
			pass

builtins.pp = pp

def trace_exception():
	if settings.DEBUG:
		traceback.print_exc()
		# Get traceback as a string and do something with it
		error = traceback.format_exc()

builtins.trace_exception = trace_exception


def _is_class_method(func):
	""" Check the given function object is a simple function or class method """
	spec = inspect.getfullargspec(func)
	return spec.args and spec.args[0] == 'self'

def sanitize(str):
	import cgi
	transform = cgi.escape(str)
	return transform


def encode_decimal(obj):
	if isinstance(obj, decimal.Decimal):
		return str(obj)
	return obj


def db_table_exist(connection,tb):
	db_cursor = connections[connection].cursor()
	check_exists_query = "SELECT relname FROM pg_class WHERE relname=%s;"
	db_cursor.execute(check_exists_query, [tb])
	result = db_cursor.fetchone()
	if result:
		return True
	return False



# Template Related
def remove_invisible_characters(text):
	for c in ('\a', '\b', '\f', '\v','\n','\r',"\\n","&nbsp;",'\xa0','<br>','<br/>','<br />'):
		text = text.replace(c, '')
	return text

def get_defualt_private_file_storage():
	if hasattr(settings,'PRIVATE_FILE_STORAGE') and settings.PRIVATE_FILE_STORAGE:
		try:
			# Nod to tastypie's use of importlib.
			parts = settings.PRIVATE_FILE_STORAGE.split('.')
			module_path, class_name = '.'.join(parts[:-1]), parts[-1]
			module = import_module(module_path)
			return getattr(module, class_name)()
		except ImportError as e:
			msg = "Could not import '%s' for setting. %s: %s." % (val, e.__class__.__name__, e)
			pass

	return default_storage


class form_media(object):
	def get_css(forms):
		files_css = []
		if forms:

			for key, values in forms.items():
				
				for css in values.media._css: # for all the scripts used by the form
					if css:
						files_css.append(values.media.absolute_path(css)) # we retrieve their url	
		
		if files_css:
			files_css = list(set(files_css))
		
		return files_css
	def get_js(forms):
		files_js = []
		if forms:

			for key, values in forms.items():
				
				for js in values.media._js: # for all the scripts used by the form
					if js:
						files_js.append(values.media.absolute_path(js)) # we retrieve their url	
		
		if files_js:
			files_js = list(set(files_js))
		
		return files_js
	def get_ajax_css(forms):
		files_css = []
		if forms:

			for key, values in forms.items():
				
				for css in values.media._css: # for all the scripts used by the form
					if css:
						files_css.append(values.media.absolute_path(css)) # we retrieve their url	
		
		if files_css:
			files_css = list(set(files_css))
		
		return files_css
	def get_ajax_js(forms):
		files_js = []
		if forms:

			for key, values in forms.items():
				
				for js in values.media._js: # for all the scripts used by the form
					if js:
						files_js.append(values.media.absolute_path(js)) # we retrieve their url	
		
		if files_js:
			files_js = list(set(files_js))
		return files_js




'''
Dynamically import class or function

'''
def import_from(module, name):
	module = __import__(module, fromlist=[name])
	return getattr(module, name)


'''
check the key is exist
'''
def keys_exists(element, *keys):
	'''
	Check if *keys (nested) exists in `element` (dict).
	'''
	if type(element) is not dict:
		raise AttributeError('keys_exists() expects dict as first argument.')
	if len(keys) == 0:
		raise AttributeError('keys_exists() expects at least two arguments, one given.')

	_element = element
	for key in keys:
		try:
			_element = _element[key]
		except KeyError:
			return False
	return True

def dictDiffByKey(dict1,dict2):
	return_dict = {}
	if dict1 and dict1:
		set1 = set(dict1)
		set2 = set(dict2)
		return_dict =  set2 - set1
	return return_dict


def stringToBase64(s):
	b = base64.b64encode(s.encode('utf-8'))
	d = b.decode('utf-8')
	return d

def base64ToString(b):
	return base64.b64decode(b).decode('utf-8')

def urlStringToBase64(s):
	return stringToBase64(s)

def urlBase64ToString(b):
	return base64ToString(b)

	





def afl_round(val,digits = None):
	return_val = val
	if digits:
		digit_decimal = pow(10, digits)
		int_val = int(Decimal(str(val)) * digit_decimal)
		return_val = int_val / digit_decimal
	return return_val


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def isNum(data):
	try:
		int(data)
		return True
	except ValueError:
		return False

def date_string_validate(date_text,format ='%Y-%m-%d'):
	try:
		datetime.datetime.strptime(date_text, format)
		return True
	except ValueError:
		return False



def str2bool(v):
    if(type(v) == bool):
        return v
    return v.lower() in ("yes", "true", "t", "1","on")

def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



# Define a lock for synchronizing access to the cache
cache_lock = threading.Lock()

# Decorator to make the lru_cache thread-safe and allow cache clearing
def thread_safe_lru_cache(maxsize=128, clear_on_call=False):
    def decorator(func):
        cached_func = functools.lru_cache(maxsize=maxsize)(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if clear_on_call:
                wrapper.clear_cache()
            with cache_lock:
                return cached_func(*args, **kwargs)

        def clear_cache():
            with cache_lock:
                cached_func.cache_clear()

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator