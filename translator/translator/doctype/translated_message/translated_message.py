# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils import strip
from dataent.model.document import Document

import re

class TranslatedMessage(Document):
	def autoname(self):
		self.name = dataent.generate_hash()

	def before_insert(self):
		if dataent.db.count("Translated Message", {"source": self.source, "language":self.language}):
			raise dataent.ValidationError("Translated Message for this source message already exists")

	def validate(self):
		if self.verified > 0:
			if dataent.db.get_value("User", dataent.session.user, "karma") < 100:
				dataent.throw(_("Only user with more than 100 karma can edit verified translations"))

			self.verified = 0

		source_msg = dataent.db.get_value("Source Message", self.source, "message")
		if get_placeholders_count(source_msg) != get_placeholders_count(self.translated):
			dataent.throw(_("Number of placehodlers (eg, {0}) do not match the source message"))

		# strip whitespace and whitespace like characters
		self.translated = strip(self.translated)

def on_doctype_update():
	dataent.db.add_index("Translated Message", ["language", "source(10)"])

def get_placeholders_count(message):
	return len(re.findall("{\d}", message))
