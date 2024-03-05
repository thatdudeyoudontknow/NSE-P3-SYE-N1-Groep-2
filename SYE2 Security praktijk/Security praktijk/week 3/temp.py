# make a function that takes all the resut times from output.txt and makes a histogram of it
from traceback import print_stack


def make_histogram():
    """Makes a histogram of the response times from the output.txt file.
    """
    
    with open('output.txt', 'r') as f:
        lines = f.readlines()
        response_times = []
        for line in lines:
            if 'Access Granted!' in line:
                response_times.append(float(line.split(' ')[-1]))
    response_times.sort()
    print(response_times)  # Use print instead of print_stack
    return

print(make_histogram())

