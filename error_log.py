import datetime

def eprint(text):
    print("ERROR -> " + str(text))
    with open("error_log.txt", 'a') as errlog:
        current_time = datetime.datetime.now()
        errlog.write(f"{str(current_time): <28}ERROR -> " + str(text) + "\n")
