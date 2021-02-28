import os_android_strings_extractor.modules.strings_extractor_boilerplate as bp


####################################################################################
# this module meant to turn the strings.xml file in an android project to a human  #
# readable xls file, ready to be translated to a specific language or bunch of     #
# languages                                                                        #
####################################################################################

def extract_to_xlsx(project_path, output_path, src_language, languages_list):
    strings_dict = bp.build_strings_dict(project_path)
    bp.dict_to_xlsx(project_path, strings_dict, output_path, src_language, languages_list)
