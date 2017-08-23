
ZERO = 0
MAX_LONGITUDE = 180
MIN_LONGITUDE = -180
MAX_LATITUDE = 90
MIN_LATITUDE = -90
# MAX_LONGITUDE_IN_AU = 154
# MIN_LONGITUDE_IN_AU = 112.5
# MAX_LATITUDE_IN_AU = -9
# MIN_LATITUDE_IN_AU = -43.5

def get_string(str,valid_input):
    """
    Get a valid string from the input stream

    :param str: message displayed to user
    :param valid_input: list of valid input
    :return: the valid string
    """
    while True:
        try:
            input_str = input(str)
            if input_str in valid_input:
                break
            else:
                print("Please enter a valid string")
        except TypeError as error:
            print("Error:",error)
    return input_str



def get_int(str,lower=None,upper=None):
    """
    Get a valid integer within the interval

    :param str: message displayed to user
    :param lower: lower bound of the interval(endpoint included)
    :param upper: upper bound of the interval(endpoint included)
    :return: the valid input integer
    """
    while True:
        try:
            num = int(input(str))
            if lower!=None and num<lower:
                print("===========================================")
                print("Error:Please enter a number greater than {}".format(lower))
                print("===========================================")
            elif upper!=None and num>upper:
                print("===========================================")
                print("Error:Please enter a number smaller than {}".format(upper))
                print("===========================================")
            else:
                break
        except :
            print("====================================")
            print("Error:Please enter a valid integer. ")
            print("====================================")

    return num



def get_float(str,lower=None,upper=None):
    """
    Get a valid float within the interval

    :param str: message displayed to user
    :param lower: lower bound of the interval(endpoint included)
    :param upper: upper bound of the interval(endpoint included)
    :return: the valid float number
    """
    while True:
        try:
            num = float(input(str))
            if lower!=None and num<lower:
                print("===========================================")
                print("Error:Please enter a number greater than {}".format(lower))
                print("===========================================")
            elif upper!=None and num>upper:
                print("===========================================")
                print("Error:Please enter a number smaller than {}".format(upper))
                print("===========================================")
            else:
                break
        except :
            print("=========================================")
            print("Error:Please enter a valid float number. ")
            print("=========================================")

    return num



def yxz_checker(lst):
    """
    Check if the coordinates is YXZ-formatted in AU

    :param lst: string list storing the coordinates
    :return: True if YXZ formatted, False otherwise
    """
    try:
        coor = [float(i) for i in lst ]

        if len(coor)!= 3:
            return False
        if coor[0]>MAX_LATITUDE or coor[0]< MIN_LATITUDE:
            return False
        if coor[1]>MAX_LONGITUDE or coor[1]<MIN_LONGITUDE:
            return False

        return True
    except:
        return False

