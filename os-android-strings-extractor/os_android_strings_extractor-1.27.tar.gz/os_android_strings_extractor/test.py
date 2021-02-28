
import os_android_strings_extractor.strings_extractor as se

se.extract_to_xlsx(project_path='/Users/home/Programming/android/Remotes/Projects/GeneralRemoteAndroid',
                   output_path='/Users/home/Desktop/translations/remotes_translations.xlsx',
                   src_language='English',
                   languages_list=['French', 'German', 'Hindi', 'Spanish', 'Arabic', 'Russian', 'Lahnda', 'Japanese', 'Portuguese'])
