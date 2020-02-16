import oct2py

"""
This module is used to link a web frontend to the Excel Process Validator 
https://github.com/iGEM-Measurement-Tools/Excel_Process_Validator

Note that it is important to run each validation in a fresh session of Octave,
in order to avoid potential cross-contamination between runs
"""

op = oct2py.Oct2Py()

def protocol_catalog():
    """
    Return an array of all of the protocols that this EPV knows about, in Dash dropdown dictionary format:
    Each entry in the array is a dictionary {'label': 'protocol name', 'value': 'octave invocation'}
    """
    catalog = op.eval('ValidationCatalog.list();')
    return [{'label':entry[0], 'value':'ValidationCatalog.'+entry[1]+"('{}')"} for entry in catalog]

def autodetect_protocol(filename):
    """ Look at file and see if we can associated it with a protocol; if not, return None"""
    for entry in protocol_catalog():
        result = validate(filename,entry['value'])
        if result['succeed'] is True:
            return entry['value']

    return None # not yet implemented

def validate(filename, protocol_call=None):
    """ Run validation on a file, returning a """
    try:
        op = oct2py.Oct2Py()
        # hard-wired call for the moment, but should be using protocol_call format instead
        op.eval('pkg load io')
        op.eval(protocol_call.format(filename))
        report = op.eval('EPVSession.to_xml();')
        value = None # should actually be materials extracted from the run
        succeed = True
    except:
        # need to figure out how to properly handle exceptions
        value = None
        report = 'Excel Process Validator:\n execution failed\n\n'
        succeed = False

    return {'value':value, 'report':report, 'succeed':succeed}
