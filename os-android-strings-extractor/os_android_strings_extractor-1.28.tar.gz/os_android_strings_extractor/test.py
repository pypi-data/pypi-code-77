
import os_android_strings_extractor.strings_extractor as se

se.extract_to_xlsx(strings_file_path='/Users/home/Programming/android/Remotes/Projects/GeneralRemoteAndroid/app/src/main/res/values/strings.xml',
                   output_path='/Users/home/Desktop/translations/remotes_translations.xlsx',
                   src_language='English',
                   languages_list=['French', 'German', 'Hindi', 'Spanish', 'Arabic', 'Russian', 'Lahnda', 'Japanese', 'Portuguese'])
