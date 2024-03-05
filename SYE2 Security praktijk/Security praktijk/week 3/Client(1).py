import socket, sys, asyncio, websockets, json, time, string, operator, statistics
from string import ascii_lowercase, digits
import os



async def client_stub(username, password):
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
    #server_address = "ws://127.0.0.1:3840"
    server_address = "ws://192.168.1.10:3840"
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

# Basic function for calling server
def call_server(username, password):
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
            run_until_complete(client_stub(username,password))
    #save_output_to_txt(reply+str(time_delta)+ enter)
    
    if reply[-15:] == 'Access Granted!':
        print('Correct password found: {}'.format(password))
    time.sleep(0.001) # Make sure to wait so as to not overload the server!
    
    return reply, time_delta

def length_password(username, passwordlength):
    resultaat = "" 
    call_server("","")
    for i in range(passwordlength):
        resultaat += "o"
        
        if len(resultaat) > 1:
            reply,time_delta =call_server(username, resultaat)
            
            save_output_to_txt('Sending login attempt for username: {} and password: {}'.format(username, resultaat)+ (" "*(passwordlength- len(resultaat)))+ ' response time = '+str(time_delta)+ '\n')
            print(f'{resultaat}')
        
     


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
    Purely for visual purposes.
    """
    
    with open('output.txt', 'a') as f:
        f.write(output)
    return

# make a function that takes all the resut times from output.txt and makes a histogram of it
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
    print_stats(response_times)
    return

#print(call_server('000000','hunter2'))

def main():
    """Main function. Loops through all possible passwords
    and sends them to the server.
    """

    username = '000000'
   # password = 'hunter2'
    passwordlength = int(input("Geef de lengte van de string: "))
    length_password(username, passwordlength)
    
    #call_server(username, password)
    print ('done')


if __name__ == '__main__':
    main()



