def parse_function_path_string(string):
    """
    takes in the function string and splits it into the module path and function path.
    :param string:
    :return:
    """

    list_ = string.split('.')
    module_path = '.'.join(list_[:-1])
    function_path = list_[-1]

    return module_path, function_path
