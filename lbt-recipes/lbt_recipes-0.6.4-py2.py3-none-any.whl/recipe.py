# coding: utf-8
"""Classes to handle recipe inputs and outputs."""
from __future__ import division

import os
import json
import importlib
import shutil

from honeybee.config import folders
from ladybug.futil import preparedir, copy_file_tree


class Recipe(object):
    """Recipe class to be used as a base for all Ladybug Tools recipes.

    Note that this class is only intended for recipes that have a single output
    called "results", which is typically a folder containing all of the
    result files of the recipe.

    Args:
        recipe_name: Text for the name of the recipe folder within this python
            package (eg. daylight_factor). This can also be the full path to a
            recipe folder (the folder containing the package.json and run.py file).
            If the input does not correspond to an installed package or a valid
            recipe folder, an exception will be raised.

    Properties:
        * name
        * tag
        * path
        * default_project_folder
        * simulation_id
        * inputs
        * outputs
    """

    def __init__(self, recipe_name):
        # check to be sure that the requested recipe is installed
        install_folder = os.path.dirname(__file__)
        recipe_folder = os.path.join(install_folder, recipe_name)
        if os.path.isdir(recipe_folder):  # it's a recipe in this package
            self._name = recipe_name
            self._path = recipe_folder
        elif os.path.isdir(recipe_name):  # it's an externally-installed recipe
            self._name = os.path.basename(recipe_name)
            self._path = recipe_name
        else:
            raise ValueError('Recipe "{}" is not installed.'.format(recipe_name))

        # load the package.json file to extract the recipe attributes
        package_json = os.path.join(self._path, 'package.json')
        assert os.path.isfile(package_json), \
            'Recipe "{}" lacks a package.json.'.format(self._name)
        with open(package_json) as json_file:
            package_data = json.load(json_file)

        # set the recipe attributes
        self._tag = package_data['metadata']['tag']
        self._default_project_folder = None
        self._simulation_id = None
        self._inputs = [RecipeInput(inp) for inp in package_data['inputs']]
        self._outputs = [RecipeOutput(outp) for outp in package_data['outputs']]

    @property
    def name(self):
        """Get text for recipe name."""
        return self._name

    @property
    def tag(self):
        """Get text for recipe tag (aka. its version number)."""
        return self._tag

    @property
    def path(self):
        """Get the path to the recipe's folder.

        This folder contains a package.json with metadata about the recipe as well
        as a run.py, which is used to execute the recipe.
        """
        return self._path

    @property
    def default_project_folder(self):
        """Get or set the directory in which the recipe's results will be written.

        If unset, this will be a folder called unnamed_project within the user's
        default simulation folder
        """
        return self._default_project_folder if self._default_project_folder is not None \
            else os.path.join(folders.default_simulation_folder, 'unnamed_project')

    @default_project_folder.setter
    def default_project_folder(self, path):
        self._default_project_folder = path

    @property
    def simulation_id(self):
        """Get or set text for the simulation ID to use within the project folder.

        If unset, this will be the same as the name of the recipe.
        """
        return self._simulation_id if self._simulation_id is not None else self._name

    @simulation_id.setter
    def simulation_id(self, value):
        self._simulation_id = value

    @property
    def inputs(self):
        """Get a tuple of RecipeInput objects for the recipe's inputs."""
        return tuple(self._inputs)

    @property
    def outputs(self):
        """Get a tuple of RecipeOutput objects for the recipe's outputs."""
        return tuple(self._outputs)

    def input_value_by_name(self, input_name, input_value):
        """Set the value of an input given the input name.
        
        Args:
            input_name: Text for the name of the input to be set. For example,
                'radiance-parameters'.
            input_value: The value to which the input will be set. Note that
                setting a value will ensure it is passed through any of the
                input's handlers and cast to an appropriate data type.
        """
        for inp in self._inputs:
            if inp.name == input_name:
                inp.value = input_value
                break
        else:
            raise ValueError(
                'Input "{}" was not found for recipe "{}".'.format(
                    input_name, self.name))

    def handle_inputs(self):
        """Run the handlers of all inputs to ensure they are ready for simulation."""
        for inp in self._inputs:
            inp.handle_value()

    def write_inputs_json(self, project_folder=None, indent=4):
        """Write the inputs.json file that gets passed to queenbee luigi.

        Note that running this method will automatically handle all of the inputs.

        Args:
            project_folder: The full path to where the inputs json file will be
                written. If None, the default_project_folder on this recipe
                will be used.
            indent: The indent at which the JSON will be written (Default: 4).
        """
        # create setup the project folder in which the inputs json will be written
        p_fold = project_folder if project_folder else self.default_project_folder
        if not os.path.isdir(p_fold):
            preparedir(p_fold)
        file_path = os.path.join(p_fold, '{}_inputs.json'.format(self.simulation_id))
        # create the inputs dictionary, ensuring all inputs are handled in the process
        inp_dict = {}
        for inp in self.inputs:
            inp.handle_value()
            if inp.is_path:  # we need to copy the path to the project folder
                path_basename = os.path.basename(inp.value)
                dest = os.path.join(project_folder, path_basename)
                if os.path.isfile(inp.value):
                    shutil.copyfile(inp.value, dest)
                elif os.path.isdir(inp.value):
                    copy_file_tree(inp.value, dest, overwrite=True)
                inp_dict[inp.name] = path_basename
            else:
                inp_dict[inp.name] = inp.value
        # write the inputs dictionary to a file
        with open(file_path, 'w') as fp:
            json.dump(inp_dict, fp, indent=indent)
        return file_path

    def output_value_by_name(self, output_name, project_folder=None):
        """Set the value of an input given the input name.
        
        Args:
            input_name: Text for the name of the input to be set. For example, 'results'.
            project_folder: The full path to the project folder containing
                completed recipe results. If None, the default_project_folder on
                this recipe will be assumed. (Default: None).
        """
        proj = self.default_project_folder if project_folder is None else project_folder
        sim_path = os.path.join(proj, self.simulation_id)
        for outp in self._outputs:
            if outp.name == output_name:
                return outp.value(sim_path)
        else:
            raise ValueError(
                'Output "{}" was not found for recipe "{}".'.format(
                    output_name, self.name))

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        """Represent recipe."""
        return '{}:\n {}'.format(
            self.name, '\n '.join([str(inp) for inp in self.inputs]))


class _RecipeParameter(object):
    """Base class for managing recipe inputs and outputs.

    Args:
        spec_dict: Dictionary representation of an input or output, taken from the
            package.json and following the RecipeInterface schema.

    Properties:
        * name
        * description
        * handlers
    """

    def __init__(self, spec_dict):
        # set the properties based on the output specification
        self._name = spec_dict['name']
        self._description = spec_dict['description']

        # load any of the handlers if they are specified
        handlers = []
        if 'alias' in spec_dict:
            for alias in spec_dict['alias']:
                if 'grasshopper' in alias['platform'] and 'handler' in alias:
                    for hand_dict in alias['handler']:
                        if hand_dict['language'] == 'python':
                            module = importlib.import_module(hand_dict['module'])
                            hand_func = getattr(module, hand_dict['function'])
                            handlers.append(hand_func)
        self._handlers = None if len(handlers) == 0 else tuple(handlers)

    @property
    def name(self):
        """Get text for the name."""
        return self._name

    @property
    def description(self):
        """Get text for the description."""
        return self._description

    @property
    def handlers(self):
        """Get an array of handler functions for this object.

        This will be None if the object has no alias or Grasshopper handler.
        """
        return self._handlers

    def __repr__(self):
        return 'RecipeParameter: {}'.format(self.name)


class RecipeInput(_RecipeParameter):
    """Object to represent and manage recipe inputs.

    Args:
        input_dict: Dictionary representation of an input, taken from the
            package.json and following the RecipeInterface schema.

    Properties:
        * name
        * description
        * value
        * default_value
        * is_required
        * is_handled
        * handlers
        * is_path
    """
    INPUT_TYPES = {
        'DAGStringInput': str,
        'DAGIntegerInput': int,
        'DAGNumberInput': float,
        'DAGBooleanInput': bool,
        'DAGFolderInput': str,
        'DAGFileInput': str,
        'DAGPathInput': str,
        'DAGArrayInput': tuple,
        'DAGJSONObjectInput': dict
    }
    PATH_TYPES = ('DAGFileInput', 'DAGFolderInput', 'DAGPathInput')

    def __init__(self, input_dict):
        # check to be sure that we have the right object and initialize basic properties
        _RecipeParameter.__init__(self, input_dict)
        assert input_dict['type'] in self.INPUT_TYPES, 'Input specification "{}" is ' \
            'not valid. Must be one of the following:\n{}'.format(
                input_dict['type'], '\n'.join(self.INPUT_TYPES.keys()))
        self._type = self.INPUT_TYPES[input_dict['type']]
        self._is_path = True if input_dict['type'] in self.PATH_TYPES else False

        # set the value to None by default and import any default values
        self._value, self._default_value = None, None
        if 'default' in input_dict and input_dict['default'] is not None:
            self._default_value = input_dict['default']
        self._is_required = input_dict['required']
        self._is_handled = True  # will be set to false if a user specifies a value

    @property
    def value(self):
        """Get or set a value for this input.

        This will be the default_value if it has not been specified. Note that
        setting a value will ensure it is passed through any of the handlers
        and cast to an appropriate data type.
        """
        return self._value if self._value is not None else self._default_value

    @value.setter
    def value(self, value):
        if value is not None:
            if self._handlers is not None:
                self._is_handled = False  # set to false so we can handle it later
            else:
                value = self._type(value)
            self._value = value
        else:
            self._value = None

    @property
    def default_value(self):
        """Get the default value for this input."""
        return self._default_value

    @property
    def is_required(self):
        """Get a boolean for whether this input is required to run the recipe."""
        return self._is_required

    @property
    def is_handled(self):
        """Get a boolean for whether this input is handled and is ready for simulation.
        """
        return self._is_handled

    @property
    def is_path(self):
        """Get a boolean noting whether this input is a file or folder path."""
        return self._is_path

    def handle_value(self):
        """Run the handlers of this input to yield a correct input for simulation."""
        if not self._is_handled:
            for handler in self._handlers:
                self._value = handler(self._value)
            self._value = self._type(self._value)

    def __repr__(self):
        """Represent recipe input."""
        return '{}: {}'.format(self.name, self.value)


class RecipeOutput(_RecipeParameter):
    """Object to represent and manage recipe outputs.

    Args:
        output_dict: Dictionary representation of an output, taken from the
            package.json and following the RecipeInterface schema.

    Properties:
        * name
        * description
        * handlers
    """

    def __init__(self, output_dict):
        _RecipeParameter.__init__(self, output_dict)

        # process properties related to the output type
        self._type = output_dict['from']['type']
        try:
            self._path = output_dict['from']['path']
        except:  # not a file or a folder; this type of output is not yet supported
            self._path = None

    def value(self, simulation_folder):
        """Get the value of this output given the path to a simulation folder.
        
        Args:
            simulation_folder: The path to a simulation folder that has finished
                running. This is the path of a project folder joined with
                the simulation ID.
        """
        assert self._type in ('FileReference', 'FolderReference'), \
            'Parsing output type "{}" is not yet supported.'.format(self._type)
        result = os.path.join(simulation_folder, self._path)
        if self._handlers is not None:
            for handler in self._handlers:
                result = handler(result)
        return result

    def __repr__(self):
        """Represent recipe output."""
        return 'Output: {}'.format(self.name)
