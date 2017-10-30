def postChecker(bname,bbody):
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

def logSignChecker(uname,pword,confirm):
    error = False
    nameerror = ""
    passerror = ""
    confirmerror = ""

    if len(uname) < 3:
        if len(uname) <= 0:
            nameerror = 'Please do not leave this field blank!'
        else:
            nameerror = 'Your username must be at least 3 characters in length!'
        error = True

    if len(pword) < 3:
        if len(pword) <= 0:
            passerror = 'Please do not leave this field blank!'
        else:
            passerror = 'Your password must be at least 3 characters in length!'
        error = True

    if len(confirm) <= 0:
        confirmerror = 'Please do not leave this field blank!'
        error = True

    return {'error':error, 'nameerror':nameerror, 'passerror':passerror, 'confirmerror':confirmerror}