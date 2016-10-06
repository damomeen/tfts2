import struct

def conv_float(float_value):
    '''Convert string containing float value into byte IEEE 754 format'''
    return struct.pack('!f', float(float_value))


def get_value(params_list, param_name, remove='', cast=None):
    '''search list of dictionaries for specific parameter value 
    and convert it if required (substring removal and casting)
    '''
    for param in params_list:
        if param['name'] == param_name:
            value = param['value'].replace(remove, '')
            return cast(value) if cast else value
    raise Exception("Param not found")
    
    
def get_param_no_ok(params_list, param_name):
    '''find parameter value and convert it to SNMP TrueValue'''
    value = get_value(params_list, param_name)
    return 1 if value=='YES' else 2
 
 
def get_warning_level(params_list, param_name, remove='', cast=None):
    ''' find paramenter value and split for WARNING/OK part and level part
    which could be converted (substring removal and casting)
    '''
    value = get_value(params_list, param_name)
    values = value.split()
    warning = 1 if values[0] == 'OK' else 2
    level = values[1].replace(remove, '')
    level = cast(level) if cast else level
    return warning, level