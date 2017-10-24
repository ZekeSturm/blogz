def checker(bname,bbody):
    error = False
    nameerror = ""
    blogerror = ""

    if len(bname) <= 0:
        nameerror = 'Please do not leave this field blank!'
        error = True
    
    if len(bbody) <= 0:
        blogerror = 'Please do not leave this field blank!'
        error = True

    return {'error':error, 'nameerror':nameerror, 'blogerror':blogerror}