# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class SourceMessage(Document):
	def autoname(self):
		self.name = dataent.generate_hash()
