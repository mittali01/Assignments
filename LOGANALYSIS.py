import datetime
import re

with open('Sample.log', 'r') as f:
    f_contents = f.readlines()
    data = {}
    time_difference = {}
    count_errors = 0
    count_success = 0
    maximum = datetime.timedelta(0)
    minimum = datetime.timedelta(days=100)
    regex1 = r"((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))"
    regex2 = r"[0-3]{1}[0-9]{1}"
    regex3 = r"[1-2]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}"
    regex4 = r"\d{4}"
    regexList = [regex1, regex2, regex3, regex4]

    for lines in f_contents:
        dev = re.compile(r'[A-Z]{3}[0-1]{4}', re.MULTILINE)
        con = re.search(r'Connected', lines)
        err = re.search(r'ERROR', lines)
        success = re.search(r'SUCCSESS',lines)
        disconn = re.search(r'Disconnected', lines)
        match = re.findall(dev, lines)

        li = []
        index = 0
        for regex in regexList:
            s = re.search(regex, lines)
            if s:
                li.insert(index, s.group(0))
                index += 1
        dtstr = " ".join(li)
        dtobj = datetime.datetime.strptime(dtstr, "%b %d %H:%M:%S %Y")

        for i in match:
            if not i in data:
                data[i] = [0, 0, 0]
            if con:
                data[i][0] += 1

            if err:
                data[i][1] += 1

            if success:
                data[i][2] +=1

            if not i in time_difference:
                time_difference[i] = ""
            if con:
                time_difference[i] = dtobj

            if disconn:
                processdatatime = dtobj - time_difference[i]
                maximum = max(maximum, processdatatime)
                minimum = min(minimum, processdatatime)

    for j in data:
        print("{} is connected {} times".format(j, data[j][0]))
        if data[j][1] > 0:
            count_errors += 1
        if data[j][2] > 0:
            count_success += 1

    print("The number of devices that encountered error are:", count_errors)
    print("The number of devices that successfully sent data are:", count_success)
    maxdays, maxhrs, maxmins, maxseconds = maximum.days, maximum.seconds // 3600, maximum.seconds // 60 % 60, maximum.seconds % 60
    mindays, minhrs, minmins, minseconds = minimum.days, minimum.seconds // 3600, minimum.seconds // 60 % 60, minimum.seconds % 60

    print("Maximum time process data is: {} days, {} hours, {} minutes, {} seconds".format(maxdays, maxhrs, maxmins,
                                                                                           maxseconds))
    print("Minimum time process data is: {} days, {} hours, {} minutes, {} seconds".format(mindays, minhrs, minmins,
                                                                                           minseconds))
