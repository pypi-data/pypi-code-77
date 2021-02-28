import os
from os_xml_handler import xml_handler as xh
from os_file_handler import file_handler as fh


#################################################
# just the StringsExtractor boiler plate script #
#################################################


# will return a dictionary containing all of the strings in the xml file by "id": "value"
def build_strings_dict(strings_file_path):
    strings_xml = xh.read_xml_file(strings_file_path)
    strings_node = xh.find_all_nodes(xh.get_root_node(strings_xml), 'string')

    nodes_to_translate = []
    for node in strings_node:
        translatable_val = xh.get_node_att(node, 'translatable')
        if translatable_val is None or translatable_val == "true":
            nodes_to_translate.append(node)
    return nodes_to_translate


# will turn the strings dictionary to a good looking xlsx file
def dict_to_xlsx(string_nodes, output_path, src_language, languages_arr):
    import xlsxwriter

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(output_path)

    big_red_format = workbook.add_format()
    title_format = workbook.add_format()
    content_format = workbook.add_format()
    border_format = workbook.add_format()

    big_red_format.set_font_color('red')
    big_red_format.set_font_size(16)

    title_format.set_font_size(22)

    content_format.set_font_size(12)
    content_format.set_font('Arial')
    big_red_format.set_align('center')

    border_format.set_top()

    # set the border

    for language in languages_arr:
        worksheet = workbook.add_worksheet(language)

        # widen all of the columns used
        worksheet.set_column('A:A', 50, cell_format=content_format)
        worksheet.set_column('B:B', 50, cell_format=content_format)
        worksheet.set_column('C:C', 50, cell_format=content_format)
        worksheet.set_column('F:F', 50, cell_format=content_format)

        # set headers
        worksheet.write('A1', 'Translation Project', title_format)
        worksheet.write('A3', src_language, big_red_format)
        worksheet.write('B3', language, big_red_format)
        worksheet.write('F3', 'Code (DO NOT CHANGE)', big_red_format)

        # set strings
        for i in range(len(string_nodes)):
            node = string_nodes[i]
            node_id = xh.get_node_att(node, 'name')
            node_value = xh.get_text_from_node(node)
            worksheet.write('A' + str(i + 4), node_value)
            worksheet.write('F' + str(i + 4), node_id)

    workbook.close()
