def containsSymbol(value):
    symbolPresent = False
    for i in range(len(value)):
        if value[i].isspace() or not value[i].isalnum() == True:
            symbolPresent = True
            return True

    if symbolPresent == False:
        return False
