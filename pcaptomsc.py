#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    pcaptomsc
    ~~~~~~~~~~~~~~~~~~~~
    converting wireshark packet capture (pcap) into message sequence chart for sequencediagram.net, hackmd.io, or mscgen (png, svg, and eps format).

    See the README file for details.
    :author: Jonathan <m10802821@gapps.ntust.edu.tw>.
    :license: MIT, see LICENSE for details.
"""
import sys
import getopt
from tshark import tshark

import pcaptolist
import mscgenhandler

def replacestrings(text):
    string_to_replace = [
        ["\"", "\\\""],
        ["→", "->"]
    ]

    ret = text

    for strings in string_to_replace:
        ret = ret.replace(strings[0], strings[1])

    return ret

def listtomscgenformat(list_of_el):
    ret = ""
    ret += "msc {\n\n"

    list_of_actors = []
    for el in list_of_el:
        list_of_actors.append(el["source"])
        list_of_actors.append(el["destination"]) 

    # actors = list(set(list_of_actors)) -> can't maintain order
    actors = list(dict.fromkeys(list_of_actors))

    ret += "  \"" + "\", \"".join(actors) + "\";\n"

    for el in list_of_el:
        # make it temporary
        current_el = el

        # concat the text
        ret += ("  \"" + current_el["source"]+ "\"=>\""+ current_el["destination"]
                + "\" [label=\"("+ current_el["protocol"] +")  " + replacestrings(current_el["info"]) + "\"];\n")           

    ret += "}"

    return ret


def listtosequencediagramformat(list_of_el):
    ret = ""

    for el in list_of_el:
        # make it temporary
        current_el = el

        # replacing unreadable character
        current_el["source"] = current_el["source"].replace(":", ".")
        current_el["destination"] = current_el["destination"].replace(":", ".")

        # concat the text
        ret += (current_el["source"]+ " -> "+ current_el["destination"]
                + ": *"+ current_el["protocol"] + "*: " + current_el["info"] + "\n")           

    return ret

def listtohackmdformat(list_of_el):
    ret = ""
    ret += "```sequence\n"
    
    # reuse the sequence diagram format
    ret += listtosequencediagramformat(list_of_el)

    # exit sequence of msc generator            
    ret += "```\n"

    return ret

def main(argv):
    tshark_path = tshark.get_tshark_path()
    if (tshark_path == 0):
        print("tshark not found. Please install Wireshark.")
        return 0

    inputfile = ''
    
    format = ""

    txt_output = False
    image_output = False
    output_file = ''

    try:
        # opts is a list of returning key-value pairs, args is the options left after striped
        # the short options 'hi:o:', if an option requires an input, it should be followed by a ":"
        # the long options 'ifile=' is an option that requires an input, followed by a "="
        opts, args = getopt.getopt(argv,"hi:o:f:",["ifile=","ofile=", "format="])
    except getopt.GetoptError:
        print("pcaptomsc.py -i <inputfile> -o <output_file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("pcaptomsc.py -i <inputfile> -o <output_file>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            if arg[-4:] == ".txt":
                print("outputing to ", arg)
                output_file = arg
                txt_output = True
            if arg.split('.')[-1] in ("png", "svg", "eps"):
                if format == "mscgen":
                    image_output = True
                    image_output_file = arg
                else:
                    print("image output must use mscgen as format parameter.\n")
                    print("please specify the format parameter before output parameter.\n")
        elif opt in ("-f", "--format"):
            if arg == "hackmd":
                format = "hackmd"
            if arg == "sequencediagram":
                format = "sequencediagram"
            if arg == "mscgen":
                format = "mscgen"
    
    ## Process the input to list
    packet_list = pcaptolist.pcaptolist(tshark_path, inputfile)
    print("input has been read : ", inputfile)

    ## Process to output
    if format == "":
        format = "hackmd"
        print("Format configuration not existed, default (hackmd Format) will be selected.")

    if format == "hackmd":
        output = listtohackmdformat(packet_list)
    elif format == "sequencediagram":
        output = listtosequencediagramformat(packet_list)
    elif format == "mscgen":
        output = listtomscgenformat(packet_list)

    ## output
    if txt_output == True:
        f = open(output_file, "wt", encoding='utf-8')
        f.write(output)
        f.close()
        print("text file generated : ", output_file)
    if image_output == True:
        mscgen_output_file = image_output_file[:-4] + ".msc"
        f = open(mscgen_output_file, "wt", encoding='utf-8')
        f.write(output)
        f.close()
        print("mscgen file generated : ", mscgen_output_file)

    if image_output == True:
        image_format = image_output_file.split('.')[-1]
        res = mscgenhandler.mscgenhandler(image_format, mscgen_output_file, image_output_file)
        if res == 0:
            print("image generated : ", image_output_file)
        else:
            print("failed to generate image.")

    ## print output on terminal
    print("process finsihed.\n")
    print("Printing output to terminal.\n\n")
    print(output)

if __name__ == "__main__":
    main(sys.argv[1:])