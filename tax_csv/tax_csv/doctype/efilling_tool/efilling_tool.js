// Copyright (c) 2016, Bobby and contributors
// For license information, please see license.txt

frappe.ui.form.on('EFilling Tool', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.print_to_excel= function(doc, cdt, cdn) {
	
	// $c_obj_csv(doc,"print_to_excel",'','')
	// let get_template_url = '/api/method/frappe.core.doctype.data_export.exporter.export_data';
	let get_template_url = frappe.request.url;
	// var export_params = () => {
	// 	let columns = {};
	// 	Object.keys(frm.fields_multicheck).forEach(dt => {
	// 		const options = frm.fields_multicheck[dt].get_checked_options();
	// 		columns[dt] = options;
	// 	});
	// 	return {
	// 		doctype: frm.doc.reference_doctype,
	// 		select_columns: JSON.stringify(columns),
	// 		filters: frm.filter_list.get_filters().map(filter => filter.slice(1, 4)),
	// 		file_type: frm.doc.file_type,
	// 		template: true,
	// 		with_data: 1
	// 	};
	// };

	var args = {}
	args.cmd = 'runserverobj';
	args.as_csv = 1;
	args.method = "print_to_excel";
	args.arg = "";

	if(doc.substr)
		args.doctype = doc;
	else
		args.docs = doc;

	open_url_post(get_template_url, args);  
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