import dataent

def get_context(context):
	context.get_info = dataent.get_attr("translator.helpers.get_info")
	context.parents =  [{"title":"Community", "name":"community"}]
