# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document

class TranslatedMessageValidation(Document):
	def before_insert(self):
		if dataent.db.get_value("Translated Message Validation",
			{"owner": self.owner, "message": self.message}):
			dataent.throw(_("You have already verifed"))

	def after_insert(self):
		dataent.db.sql("""update `tabTranslated Message`
			set verified = verified + 1 where name=%s""", self.message)

		user = dataent.db.get_value("Translated Message", self.message, "modified_by")
		if user==dataent.session.user:
			dataent.throw("You can't verify your own edits!")
		if user != "Administrator":
			dataent.db.sql("""update `tabUser`
				set karma = karma + 1 where name=%s""", user)

		dataent.cache().delete_value("lang-data:" + dataent.db.get_value("Translated Message",
			self.message, "language"))

