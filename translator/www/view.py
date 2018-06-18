import dataent

def get_context(context):
	context.no_cache = True
	lang = dataent.form_dict.lang

	# make dict of parent
	parent, parent_dict = None, {}
	if '-' in lang:
		parent = lang.split('-')[0]
		for t in get_messages(parent):
			parent_dict[t.source_name] = t

	context.messages = get_messages(lang)

	if parent:
		for m in context.messages:
			if not m.translated:
				# replace the record
				m.update(parent_dict.get(m.source_name))

	context.title = 'Translate {0}'.format(lang)

	context.parents = [
		{"title": "Community", "name":"community"},
		{"title": "Languages", "name":"translator"}
	]

def get_messages(lang):
	query = """select
		source.name as source_name, source.message,
		translated.name as translated_name,
		translated.translated,
		translated.verified, source.flagged,
		translated.modified, translated.modified_by,
		user.first_name, user.last_name
	from `tabSource Message` source
		left join `tabTranslated Message` translated on
			(source.name=translated.source and translated.language = %s)
		left join tabUser user on (translated.modified_by=user.name)
	where
		{condition}
		and source.disabled !=1
	order by translated.verified, source.message"""


	if dataent.form_dict.search:
		condition = "(source.message like %s or translated.translated like %s)"
		condition_values = ['%' + dataent.db.escape(dataent.form_dict.search) + '%', '%' + dataent.db.escape(dataent.form_dict.search) + '%']

	else:
		if dataent.form_dict.c:
			c = dataent.db.escape(dataent.form_dict.c)
		else:
			c = "*"

		if c == "*":
			condition = "source.message REGEXP '^[^a-zA-Z]'"
			condition_values = None

		else:
			condition = "source.message like %s"
			condition_values = [c + '%']

	cond_tuple = tuple([lang] + condition_values) if condition_values else (lang,)

	return dataent.db.sql(query.format(condition=condition), cond_tuple, as_dict=True)
