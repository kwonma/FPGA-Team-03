import csv

# NOTE:
# in order for this program to run properly, remove headers from
# oscilliscope csv file leaving only the data

# Signal Tracking Variables
low  = False    # is the signal low?
high = False    # is the signal high?
h_count = False # has the signal been high?
l_count = False # has the signal been low?
s = 0           # sum of time spent high AND low

# Signal thresholds
sig_width_threshold = 2 # ignore any signals over 2.5 ms
low_threshold = 0.5       # low logic is below 0.5V
high_threshold = 2.8    # high logic is above 2.5V

zero_bit_threshold = 1.5
one_bit_threshold = 2

#row[0] = time
#row[1] = voltage

file_name = '1zoomed.csv'

# Open CSV file
with open(file_name, newline='') as csvfile:
    print("running\n")
    file = csv.reader(csvfile, delimiter=',')

    # go through the file row by row
    for row in file:

        # if the signal has been HIGH and LOW recently
        # we are interested in the combined length of
        # their signals. 
        if h_count and l_count:

            # if the combined HIGH & LOW signal width is
            # less than zero_bit_threshold, recieve logic 0
            if s < zero_bit_threshold:
                print('0')

            # if the combined HIGH & LOW signal width is
            # less than 1_bit_threshold, recieve logic 0
            elif s > one_bit_threshold:
                print('1')

            # reset HIGH & LOW sum and reset signal tracking
            print(s)
            h_count = False
            l_count = False
            s = 0

        # reset signal widths (stops from printing old values
        # when there is not a new signal width)
        delta_low  = 0
        delta_high = 0

        # initial conditions
        if (float(row[1]) < low_threshold) and not low and not high:
            low_start_time = float(row[0])
            low  = True
            high = False
            
        elif (float(row[1]) > high_threshold) and not high and not low:
            high_start_time = float(row[0])
            high = True
            low  = False

        # High to low transition
        if (float(row[1]) < low_threshold) and high:

            # the time the signal spend HIGH will be the current
            # time (right when the signal stops being HIGH) to when
            # it first transitioned HIGH
            delta_high = float(row[0]) - high_start_time

            # the signal is now low, record transition time
            low_start_time = float(row[0])

            # update signal tracking
            low  = True
            high = False

        # Low to high transition
        elif (float(row[1]) > high_threshold) and low:

            # the time the signal spent LOW will be the current
            # time (right when the signal stops being LOW) to when
            # it first transitioned LOW
            delta_low = float(row[0]) - low_start_time

            # the signal is now high, record transition time
            high_start_time = float(row[0])

            # update signal tracking
            high = True
            low  = False

        # check the width of the HIGH signal
        if delta_high:
            # convert delta_high (in seconds) to ms
            d_h = round(delta_high * 1000, 3) #delta_high in ms
            #print("Delta High: " + str(d_h) + ' ms\n')
            
            # if the signal width is within the threshold and
            # has not been HIGH in the last transition, add the
            # signal HIGH width to the HIGH & LOW width sum, s
            if d_h < sig_width_threshold and not h_count:
                s += d_h
                h_count = True 

        # check the width of the LOW signal
        elif delta_low:
            # convert delta_low (in seconds) to ms
            d_l = round(delta_low * 1000, 3) # delta_low in ms
            #print("Delta Low: " + str(d_l) + ' ms\n')

            # if the signal width is within the threshold and
            # has not been LOW in the last transition, add the
            # signal LOW width to the HIGH & LOW width sum, s
            if d_l < sig_width_threshold and not l_count:
                s += d_l
                l_count = True
