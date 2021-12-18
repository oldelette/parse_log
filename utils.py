from time import localtime
from time import timezone
from time import altzone

def get_local_tzone():
    """Get the current time zone on the local host"""
    if localtime().tm_isdst:
        if altzone < 0:
            tzone = '+' + \
                    str(int(float(altzone) / 60 // 60)).rjust(2,
                            '0') + \
                            str(int(float(
                                altzone) / 60 % 60)).ljust(2, '0')
        else:
            tzone = '-' + \
                    str(int(float(altzone) / 60 // 60)).rjust(2,
                            '0') + \
                            str(int(float(
                                altzone) / 60 % 60)).ljust(2, '0')
    else:
        if altzone < 0:
            tzone = \
                    '+' + str(int(float(timezone) / 60 // 60)).rjust(2,
                            '0') + \
                            str(int(float(
                                timezone) / 60 % 60)).ljust(2, '0')
        else:
            tzone = \
                    '-' + str(int(float(timezone) / 60 // 60)).rjust(2,
                            '0') + \
                            str(int(float(
                                timezone) / 60 % 60)).ljust(2, '0')

    return tzone
