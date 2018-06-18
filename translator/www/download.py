import datetime
import os
import dataent.utils

def get_context(context):
	context['files'] = get_files()

def get_files():
	ret = []
	langs = dataent.db.sql_list("select name from tabLanguage")
	apps = dataent.db.sql_list("select name from `tabTranslator App`")
	for lang in langs:
		for app in apps:
			file_name = "{0}-{1}.csv".format(app, lang)
			file_path = dataent.utils.get_files_path(file_name)
			if not os.path.exists(file_path):
				continue
			dt=os.path.getmtime(file_path)
			ret.append((lang,
						"/files/"+ file_name,
						file_name,
						datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')))
	return ret
