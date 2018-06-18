from __future__ import unicode_literals
import dataent
from dataent.utils import get_fullname

def get_context(context):
	context.no_cache=True
	data = dataent.db.sql("""select count(*) as translated, modified_by
		from `tabTranslated Message`
		where modified_by != "Administrator"
		group by modified_by order by translated desc limit 20""", as_dict=1)

	for d in data:
		d.fullname = get_fullname(d.modified_by)

	context.users = data
