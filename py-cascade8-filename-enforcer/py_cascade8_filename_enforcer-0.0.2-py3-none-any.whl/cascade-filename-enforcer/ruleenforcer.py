#!/usr/bin/env python
""" Module to enforce file naming rules for all sites. """
import time, requests, json,os 
from requests.utils import quote  

class CascadeCMSFileNameRuleEnforcer: 
    def __init__(self, cpass=None, cuser=None,restapi=None): 
        """ Use environment variables to populate base REST API URL and 
        authentication variables """ 
        self.cpass = cpass
        self.cuser = cuser
        self.restapi = restapi
        if self.validate_obj(): 
            self.auth = f"u={self.cuser}&p={self.cpass}"

    def validate_obj(self): 
        if not self.cpass : 
            raise Exception(
                "Please pass cpass=<Cascade account password> to the "
                "CascadeCMSFileNameRuleEnforcer() invocation"
                )
        if not self.cuser : 
            raise Exception(
                "Please pass cuser=<Cascade account username> to the "
                "CascadeCMSFileNameRuleEnforcer() invocation"
                )
        if not self.restapi : 
            raise Exception(
                "Please pass restapi=<Cascade REST API Base URL> to the "
                "CascadeCMSFileNameRuleEnforcer() invocation"
                )
        return True 

    def rename(self, identifier=None, filetype=None, new_name=None,  destination_container_id=None): 
        """ Method to rename an existing CMS resource via POST request to /move endpoint 
        Args: 
        identifier (string) - identifier of resource being renamed
        filetype (string) - file type of the resource being renamed, generally 'page' or 'file'
        new_name (string) - the desired new name of the resource 
        destination_container_id - the ID of the new folder in which the file will live
        if  you are just renaming, the destination_container_id can be pulled from the 
        existing parent folder id of the resource
        Returns: POST request response 
        """
        response = None
        if identifier and new_name and destination_container_id and filetype:
            # Renaming a file is like moving a file to the same destination container, but giving
            # it a different name
            url = f'{self.restapi}/move/{identifier}?{self.auth}'
            # first thing you need to do is get its current container identifier
            # now you can make a POST request using that container 
            data = {
                "identifier": {
                    "id": identifier,
                    "type": filetype
                },
                "moveParameters": {
                    "destinationContainerIdentifier": {
                        "id": destination_container_id,
                        "type": "folder"
                    }, 
                    "newName": new_name
                }    
            } 
            response = requests.post(url, data=json.dumps(data))
        return response


    def get_all_sites(self):
        """ Method to get list of all sites
        Args: none
        Returns: list of sites as JSON objects 
        """ 
        url = f'{self.restapi}/listSites?{self.auth}'
        response = requests.get(url)
        sites = response.json()['sites']
        return sites


    def get_site_resources(self,site_name):
        """ Method to get all the resources within a site's content folder
            Args: site name
            Returns: list of all resources in a site's content folder
            Assumption: your Cascade CMS sites are structured as <sitename>/content/*
            If you don't have a root /content/ folder, change this. 
            """
        url = f'{self.restapi}/read/folder/{site_name}/content?{self.auth}'
        response = requests.get(url)
        return response.json()

    def valid_filename(self,name):
        """ Method to determine if a file follows the Cascade CMS filename
            rules 
            Args: file name
            Returns: boolean 
        """
        return name.islower() and " " not in name


    def is_image_file(self,name):
        """ simple utility method to determine if file is an image file
        Args: filename to check (string)
        Returns: boolean
        """ 
        return ".png" in name.lower() or ".jpg" in name.lower()
 

    def has_children(self, data):
        """ Method to determine if a JSON object contains "children"
        (i.e. for recursion, are there children objects to recursively traverse?)
        Args: data (json/dictionary)
        Returns: boolean (true if there are children to traverse) """
        return "asset" in data and "folder" in data['asset'] and "children" in data['asset']['folder']

    def enforce_proper_name(self, current_name): 
        """ Method to translate an incorrectly formatted file name to
        a properly formatted file name
        Args: existing/current file name (string)
        Returns: new, fixed file name (string)
        """
        # Remove spaces, replace with hyphen. Convert upper to lower.
        return current_name.strip().replace(" ","-").lower()

    def get_filename_from_fullpath(self, filepath): 
        """ Method to get JUST the file name from a full filepath
        Args: full filepath (string)
        Returns: file name (string)
        """
        # If there are no / characters, this will just return the filepath as is.
        return filepath.split('/')[-1]

    def skip_current_site(self, skip_sites=[], current_parent_folder={}): 
        """ utility method to determine if current folder should be skipped.
        if any of the skip_sites elements are in the current_parent_folder JSON
        then return True, otherwise false
        Args: 
        skip_sites (list) - list of sites that should be skipped
        current_parent_folder - JSON dictionary 
        """ 
        return any([site in current_parent_folder for site in skip_sites])

    def traverse(self, current_parent_folder={}, site_full_assets_list=[], skip_sites=[]):
        """ Recursive method to return a full list of all full paths to files within a site
            args: 
            current_parent_folder (JSON object/dictionary) the current folder being traversed
            site_full_assets_list (list) - a list of all site assets that grows with each recursive call
            skip_sites (list) - list of site names that you want to skip - i.e.
            do not enforce rules for these sites
            Returns: site_full_assets_list (list of full paths)
            """  
        # Determine if current folder / site should be skipped
        if self.skip_current_site(
            skip_sites=skip_sites,
            current_parent_folder=current_parent_folder
            ):
            # if so, immediately return full assets list 
            return site_full_assets_list 

        url = f'{self.restapi}/read/folder/{current_parent_folder}?{self.auth}'
        response = requests.get(url).json()

        if self.has_children(response):
            children = response['asset']['folder']['children']
            # get the current folder id, this needs to be used as the destinationContainerIdentifier if you have to rename one of its children
            current_folder_id = response['asset']['folder']['id']

            for child in children:
                # Create full path to be used for "Move" operation. cannot
                # be relative to parent folder..  
                # Remove the extra intermediate 'content' or whatever name it may be
                # by removing last element after slash of parent
                full_child_path = ''.join(current_parent_folder.split(
                    '/')[:1]) + '/' + child['path']['path']
                # Get current name
                current_name = self.get_filename_from_fullpath(full_child_path)
                # If child has an invalid name
                if not self.valid_filename(current_name): 
                    # Get new name after rule enforcement
                    new_name = self.enforce_proper_name(current_name)
                    response = self.rename(
                        identifier=child['id'], 
                        filetype=child['type'],
                        new_name=new_name,
                        destination_container_id=current_folder_id
                        )
                    file_changed = {
                        'old': current_name,
                        'new': new_name
                    }
                    # Also append it to the list of bad assets
                    site_full_assets_list.append(file_changed)
                # Check if this is a folder.
                if child['type'] == 'folder':
                    # self.traverse() recursive on this folder.
                    # The full child path is now the parent.
                    site_full_assets_list = self.traverse(
                        full_child_path,
                        site_full_assets_list
                        )
        return site_full_assets_list

    def publish_site(self, site_id): 
        """ method to publish a site; should be called after modifying filenames;
        recommended to publish from root folder 
        args: publish_folder (string); the folder to publish  """
        response = None 
        try:
            url = f'{self.restapi}/publish/folder/{site_id}?{self.auth}'
            response = requests.post(url).json()
        except Exception as e: 
            response = "error: {e}"
        return response 
        
def test(site_name="redesign.cofc.edu",site_id="fca49d0aac1e00090ad4228845233487"):
    """ Test call - only on one site passed as argument """  
    print(f"Beginning scan for invalid filenames in site {site_name}")
    cpass = quote(os.environ.get('CASCADE_CMS_PASS',''))
    cuser = os.environ.get('CASCADE_CMS_USER','')
    restapi= os.environ.get('CASCADE_CMS_REST_API_BASE','')
    rule_enforcer = CascadeCMSFileNameRuleEnforcer(
        cpass=cpass, cuser=cuser, restapi=restapi
    ) 
    site_dicts = []
    site_dictionary = {
        f'{site_name}': {
            'bad_assets': rule_enforcer.traverse(
                current_parent_folder=f'{site_name}/media',
                site_full_assets_list=[],
                skip_sites=["_Auto-Migrated Global_", "_skeleton.cofc.edu"]
            ),
            'publish_result': rule_enforcer.publish_site(site_id)
        } 
    }
    site_dicts.append(site_dictionary)
    with open('test_site_read_redesign.json', 'w') as f:
        json.dump(site_dicts, f)
    print(f"Completed scan of site {site_name}")

def main(): 
    """ Production call - loop through all Cascade CMS sites and 
    fix improper filenames, keeping a record of the resources changed in 
    a local JSON file """ 
    # Create rule enforcer
    cpass = quote(os.environ.get('CASCADE_CMS_PASS',''))
    cuser = os.environ.get('CASCADE_CMS_USER','')
    restapi= os.environ.get('CASCADE_CMS_REST_API_BASE','')
    rule_enforcer = CascadeCMSFileNameRuleEnforcer(
        cpass=cpass, cuser=cuser, restapi=restapi
    ) 
    site_dicts = []
    for s in rule_enforcer.get_all_sites():
        site_name = s['path']['path']
        site_id = s['id'] 
        # Start with the base of site_name/content. initialize a
        print(f"Beginning scan for invalid filenames in site {site_name}")
        site_dictionary = {
            f'{site_name}': {
                'bad_assets': rule_enforcer.traverse(
                    current_parent_folder=f'{site_name}/content',
                    site_full_assets_list=[],
                    skip_sites=["_Auto-Migrated Global_", "_skeleton.cofc.edu"]
                ),
                'publish_result': rule_enforcer.publish_site(site_id)
            } 
        }
        site_dicts.append(site_dictionary)
        with open('site_read.json', 'w') as f:
            json.dump(site_dicts, f)
        print(f"Completed scan of site {site_name}")


if __name__ == "__main__":
    # One site: redesign.cofc.edu 
    test()
    # All sites!
    # main()