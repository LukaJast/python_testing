def log_creation(file_name):
        """Helper for creating log file"""
        with open(file_name, 'w') as file:
            file.write("WARNING\nWARNING\nWARNING\n")
            print(repr(file_name))
        return file_name


def find_errors(log_file):
    """Check line number of first FATAL error"""
    with open(log_file, "r") as file:
        for number, line in enumerate(file, start=1):
            if "ERROR" in line:         
                error_line = number
                # print(number)
                return number


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
    fatal = False
    with open(log_file, "r") as file:
        for line in file:
            if "FATAL" in line:
                fatal = True
        return fatal
    

def has_warning(log_file):
    """Checks if the log contains a WARNING"""
    warning = False
    with open(log_file, "r") as file:
        for line in file:
            if "WARNING" in line:
                warning = True
        return warning


def find_warning(log_file):
    """Find line number with first WARNING"""
    # breakpoint()
    with open(log_file, "r") as file:
        for number, line in enumerate(file, start=1):
            print(repr(line))
            if "WARNING" in line:
                print (number)
                return number
        

def count_warning(log_file):
    """Counts how many Warnings are in the file"""
    count = 0
    # log_file = log_creation("test.log")
    with open(log_file, "r") as file:
        for line in file:
            if "WARNING" in line:
                count += 1
        return count



# log_file = input("Podaj plik loga: ")
# number = find_errors(log_file)
# print("First ERROR is on line " + str(number))
#
# Testing branch
#

