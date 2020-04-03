frappe.ui.form.on("Sales Invoice", {
	refresh:function(frm){
		frm.set_value("tax_date",frm.doc.posting_date)
	},
	posting_date: function(frm){
		frm.set_value("tax_date",frm.doc.posting_date)
	}
})