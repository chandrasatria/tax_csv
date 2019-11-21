// Copyright (c) 2016, Bobby and contributors
// For license information, please see license.txt

frappe.ui.form.on('EFilling Tool', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.print_to_excel= function(doc, cdt, cdn) {
	
        $c_obj_csv(doc, 'print_to_excel', '', '');
  
}

frappe.query_reports["EFilling Tool"] = {
	"filters": [
		{
			"fieldname": "tanggal_faktur",
			"label": __("Tanggal"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		},

		]
}