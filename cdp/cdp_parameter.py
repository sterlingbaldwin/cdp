import abc
import importlib
import sys
import os


class CDPParameter(object):
    __metaclass__ = abc.ABCMeta

    def __get__(self):
        self.check_values()

    @abc.abstractmethod
    def check_values(self):
        """ Check that all of the variables in
        this parameter file are valid. """
        raise NotImplementedError()

    def load_parameter_from_py(self, parameter_file_path):
        """ Initialize a parameter object from a Python script. """
        parameter_as_module = \
            self.import_user_parameter_file_as_module(parameter_file_path)
        self.load_parameters_from_module(parameter_as_module)

    def import_user_parameter_file_as_module(self, parameter_file_path):
        if not os.path.isfile(parameter_file_path):
            raise IOError('Parameter file %s not found.' % parameter_file_path)

        path_to_module = os.path.split(parameter_file_path)[0]
        module_name = os.path.split(parameter_file_path)[1]
        if module_name.count('.') > 1:
            raise ValueError("Filename cannot contain '.' outside extension.")
        if '.' in module_name:
            module_name = module_name.split('.')[0]

        sys.path.insert(0, path_to_module)
        return importlib.import_module(module_name)

    def load_parameters_from_module(self, parameter_as_module):
        user_defined_parameters = []
        for user_parameter in dir(parameter_as_module):
            if not user_parameter.startswith('__'):
                user_defined_parameters.append(user_parameter)

        # Initialize the variables in this parameter, so the driver can
        # access them as if they were defined regularly.
        for p in user_defined_parameters:
            exec("self." + p + " = parameter_as_module." + p)
