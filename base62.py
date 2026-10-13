def convert(count):
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_code = ""
    while count != 0 :
        short_code = short_code + str[count %  62]
        count = count / 62
    
    return short_code
