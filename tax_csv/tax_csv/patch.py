from __future__ import unicode_literals
import frappe
from frappe.desk.reportview import get_match_cond
from frappe.model.db_query import DatabaseQuery
from frappe.utils import nowdate
import json
import socket
from frappe.model.document import Document


def patch():
	prepatch_pe()
	patch_sinv()
	after_patch_pe()

def patch_sinv():
	sinv_list = frappe.db.sql("""
			SELECT si.name
			FROM `tabSales Invoice Item` sii
			left join `tabSales Invoice` si on si.name = sii.parent and si.docstatus = 1 and si.is_return = 0
			where (sii.target_warehouse is not null or sii.target_warehouse <> "")
			group by si.name
		""", as_dict = 1)

	for sinv in sinv_list:

		si = frappe.get_doc("Sales Invoice",sinv.name)

		# reposting Invoice cancel semua
		si.cancel()
		
		# docstatus 0
		si.docstatus = 0

		# sales invoice item target warehouse di null where parent not return
		for item in si.items:
			item.target_warehouse = ""

		si.save()

		# submit ulang
		si.submit()

		frappe.db.commit()

def prepatch_pe():
	pe_list = frappe.db.sql("""
			SELECT si.name, pe.name `pe_name`, pe.docstatus
			from `tabSales Invoice Item` sii
			left join `tabSales Invoice` si on si.name = sii.parent and si.docstatus = 1
			join `tabPayment Entry Reference` per on per.reference_name = si.name 
			join `tabPayment Entry` pe on pe.name = per.parent and pe.docstatus = 1
			where (sii.target_warehouse is not null or sii.target_warehouse <> "")
			group by si.name
		""", as_dict = 1)

	# buat field temporary menyimpan nilai docstatus skrg
	# update semua docstatus jadi 0

	for _pe in pe_list:

		frappe.db.sql("""UPDATE `tabPayment Entry` set old_docstatus = docstatus where name = "{}" """.format(_pe.pe_name))		
		frappe.db.sql("""UPDATE `tabPayment Entry` set docstatus = 0 where name = "{}" """.format(_pe.pe_name))		
		frappe.db.commit()

def after_patch_pe():
	pe_list = frappe.db.sql("""
			SELECT si.name, pe.name `pe_name`, pe.docstatus
			from `tabSales Invoice Item` sii
			left join `tabSales Invoice` si on si.name = sii.parent and si.docstatus = 1
			join `tabPayment Entry Reference` per on per.reference_name = si.name 
			join `tabPayment Entry` pe on pe.name = per.parent and pe.docstatus = 1
			where (sii.target_warehouse is not null or sii.target_warehouse <> "")
			group by si.name
		""", as_dict = 1)

	for _pe in pe_list:
		frappe.db.sql("""UPDATE `tabPayment Entry` set docstatus = old_docstatus where name = "{}" """.format(_pe.pe_name))		
		frappe.db.commit()
