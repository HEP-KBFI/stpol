import os

def read_cross_sections():
    lines = [line.strip() for line in open("/".join([os.environ["STPOL_DIR"], "src", "headers", "cross_sections.txt"]))]
    cross_sections = {}
    for line in lines:
        if len(line) == 0 or "#" in line or "sample" in line:
            continue
        (name, xs) = line.split(",")
        cross_sections[name.replace("\"", "")] = float(xs)
    return cross_sections

def scale_to_lumi(lumi, xs, total_events):
      expected_events = xs * lumi
      scale_factor = float(expected_events)/total_events
      #print lumi, "xs", xs, "exp", expected_events, "total", total_events
      return scale_factor

def replace_name(name):
    x = name.replace("Mu1", "Mu")    
    x = x.replace("Mu2", "Mu")
    x = x.replace("Mu3", "Mu")
    x = x.replace("Mu_miss", "Mu")
    x = x.replace("Ele1", "Ele")
    x = x.replace("Ele2", "Ele")
    x = x.replace("Ele_miss", "Ele")
    return x

def list_to_string(mylist):
    conc = ""    
    for a in mylist:
        conc += a + " "
    return conc

def get_file_list(file_list_file, isHdfsCms = True):
    if isHdfsCms: 
        lines = ["/hdfs/cms"+line.strip() for line in open(file_list_file)]
    else:
        lines = [line.strip() for line in open(file_list_file)] 
    return lines

if __name__ == "__main__":
    xs = read_cross_sections()
    for (name, x) in xs.items():
        print name, x

