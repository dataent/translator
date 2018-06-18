from __future__ import unicode_literals
import dataent

def get_info(lang, this_month = False):
	def _get():
		condition = ""
		if this_month:
			condition = " and modified > DATE_SUB(NOW(), INTERVAL 1 MONTH)"

		return {
			"total": dataent.db.sql("""select count(*) from `tabSource Message`
				where disabled != 1""")[0][0],
			"verified": dataent.db.sql("""select count(*) from `tabTranslated Message`
				where language=%s and verified > 0 {0}""".format(condition), lang)[0][0],
			"edited": dataent.db.sql("""select count(*) from `tabTranslated Message`
				where language=%s and modified_by != 'Administrator' {0}""".format(condition),
					lang)[0][0]
		}

	if this_month:
		return _get()
	else:
		return dataent.cache().get_value("lang-data:" + lang, _get)

@dataent.whitelist()
def verify(message):
	dataent.get_doc({
		"doctype": "Translated Message Validation",
		"message": message
	}).insert(ignore_permissions=1)

@dataent.whitelist()
def update(message, source, translated, language):
	updated = False
	if message:
		message = dataent.get_doc("Translated Message", message)
		if message.language == language:
			message.translated = translated
			message.save(ignore_permissions=1)
			updated = True

	if not updated:
		message = dataent.new_doc("Translated Message")
		message.translated = translated
		message.language = language
		message.source = source
		message.save(ignore_permissions=1)

@dataent.whitelist()
def report(message, value):
	message = dataent.get_doc("Source Message", message)
	message.flagged = value
	message.save(ignore_permissions=1)

def monthly_updates():
	translators = dataent.db.sql_list("""select distinct modified_by from
		`tabTranslated Message`""")

	message = dataent.get_template("/templates/emails/translator_update.md").render({
		"dataent": dataent
	})

	# refer unsubscribe against the administrator
	# document for test
	dataent.sendmail(translators, "EPAAS Translator <hello@epaas.com>",
		"Montly Update", message, bulk=True, reference_doctype="User",
		reference_name="Administrator")

def clear_cache():
	for lang in dataent.db.sql_list("select name from tabLanguage"):
		dataent.cache().delete_value("lang-data:" + lang)

def get_home_page(user):
	""" website user should be redirected to /index after login"""
	return "/index"
