import dataent
import click
from translator.data import import_source_messages
from dataent.core.page.data_import_tool.data_import_tool import import_file_by_path
from translator.data import import_translated_from_text_files

def execute():
	dataent.db.auto_commit_on_many_writes = False
	# reload doc Source message
	dataent.reload_doc("translator", "doctype", "source_message")
	dataent.reload_doc("translator", "doctype", "translator_app")

	dataent.delete_doc('Page', 'website-home')
	dataent.delete_doc('Page', 'user-properties')
	dataent.delete_doc('Page', 'Setup')
	dataent.get_doc({'doctype': 'Translator App', 'app_name': 'dataent'}).save()
	dataent.get_doc({'doctype': 'Translator App', 'app_name': 'epaas'}).save()
	# import_source_messages()
	import_file_by_path('source_messages.csv')
	dataent.db.commit()

	count = dataent.db.count("Translated Message")

	source_messages = dict(dataent.db.sql("select message, name from `tabSource Message`"))
	for name, source, modified, modified_by in dataent.db.sql("select name, source, modified, modified_by from `tabTranslated Message`"):
		if source in source_messages:
			dataent.db.set_value("Translated Message", name, "source", source_messages[source], modified_by=modified_by, modified=modified)
		else:
			d = dataent.new_doc("Source Message")
			d.disabled = 1
			d.message = source
			d.save()
			source_messages[source] = d.name
			dataent.db.set_value("Translated Message", name, "source", d.name, modified_by=modified_by, modified=modified)
		count -= 1
		click.clear()
		print(count, 'remaining')

	dataent.db.commit()

	import_translated_from_text_files('../uts', '../ts')
	dataent.db.commit()

	# reload doc Translated Message
	dataent.db.auto_commit_on_many_writes = True

