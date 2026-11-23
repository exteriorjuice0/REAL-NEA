def containsNumber(value):
    numberPresent = False
    for i in range(len(value)):
        if value[i].isdigit() == True:
            numberPresent = True
            return True

    if numberPresent == False:
        return False
