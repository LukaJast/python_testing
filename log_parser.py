def count_errors(log_file):
    """ Function for spotting and counting ERROR in a file"""
    count = 0
    # print (log_file)
    with open(log_file, "r") as file:
        for line in file:
            if "ERROR" in line:
                count += 1
        return count


def has_fatal(log_file):
    """Checks if the log contain a FATAL error"""
    fatal = True
    with open(log_file, "r") as file:
        for line in file:
            if "FATAL" in line:
                fatal = True
        return fatal



def find_errors(log_file):
    """Check line number of first FATAL error"""
    with open(log_file, "r") as file:
        for number, line in enumerate(file, start=1):
            if "ERROR" in line:         
                error_line = number
                print(number)
                return number

# log_file = input("Podaj plik loga: ")
# number = find_errors(log_file)
# print("First ERROR is on line " + str(number))
#
# Testing branch

