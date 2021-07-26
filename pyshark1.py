import pyshark

capture = pyshark.FileCapture('2222.pcap')
# packet_list = []
# for packet in capture:
#     packet_list.append(packet)

packet = capture[3]
"""

print(capture[0]['radiotap'])
print(capture[0]['wlan'])
print(capture[0]['wlan_radio'])
print(packet['radiotap'].field_names)
print(packet.length)
print(packet.frame_info.time_relative)

"""
# print(packet['radiotap'].length)
# print(packet.frame_info.field_names)
print(packet.frame_info.time_relative)
print(packet.length)
# text_file = open("packet.txt", "w") # create txt file for writing
# n = text_file.write(str(packet)) # write the res string into the txt file
# text_file.close() # close and save txt file into the same folder 

# print(lists)

