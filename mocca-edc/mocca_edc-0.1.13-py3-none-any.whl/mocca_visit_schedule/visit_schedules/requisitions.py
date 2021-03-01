from edc_visit_schedule import FormsCollection, Requisition

from mocca_labs import chemistry_panel, fbc_panel

requisitions_prn = FormsCollection(
    Requisition(show_order=10, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=20, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=10, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=20, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_day1",
)
requisitions_all = FormsCollection(
    Requisition(show_order=10, panel=fbc_panel, required=False, additional=False),
    Requisition(show_order=20, panel=chemistry_panel, required=False, additional=False),
    name="requisitions_all",
)
