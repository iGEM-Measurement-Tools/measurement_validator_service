import tempfile

################################
# This is where I'm not quite sure how to handle it
# We can get the contents, but then we need to send it to the backend for processing
# For now, let's kludge this with putting the contents into a tempfile
def upload_file(contents: bytes):
    f = tempfile.NamedTemporaryFile(delete=False,suffix='.xlsx')
    f.write(contents)
    f.close()
    return f.name
