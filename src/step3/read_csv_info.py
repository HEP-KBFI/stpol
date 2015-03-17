import csv

def get_event_count(infile):
    sum_events = 0
    with open(infile, 'rb') as f:
        reader = csv.reader(f)
        first = True  
        for row in reader:
            if first == True:
                header = row
                first = False
            else:
                sum_events += int(row[1])
    return sum_events

if __name__ == "__main__":    
    print get_event_count("/home/andres/single_top/stpol_pdf/src/step3/output/Oct28_reproc/iso/UnclusteredEnUp/T_t_ToLeptons/output0_processed.csv")
