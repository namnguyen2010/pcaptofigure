import sys
import pyshark
import pandas as pd
import matplotlib.pyplot as plt
import getopt

def main(argv):
    output_flag = False
    try:
        # opts is a list of returning key-value pairs, args is the options left after striped
        # the short options 'hi:o:', if an option requires an input, it should be followed by a ":"
        # the long options 'ifile=' is an option that requires an input, followed by a "="
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("pyshark_visualize_throughput.py -i <pcap_file_input> -o <csv_file_output>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("pyshark_visualize_throughput.py -i <pcap_file_input> -o <csv_file_output>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            if arg[-4:] == ".csv":
                print("outputing to ", arg)
                output_file = arg
                output_flag = True
            else:
                print("image output must use mscgen as format parameter.\n")
                print("please specify the format parameter before output parameter.\n")
# try: lấy input từ terminal (tức là nhập vào dòng terminal thì sẽ lấy giá trị input từ file đã nhập). File đã nhập sẽ được gán vào biến inputfile

    capture = pyshark.FileCapture(inputfile) # read pcap file by pyshark
    time_list = [] #Biến time dạng list rỗng vì input là tạp hợp nhiều giá trị từ nhiều frame
    frlen_list = [] #Biến length dạng list rỗng vì input là tạp hợp nhiều giá trị từ nhiều frame

    for packet in capture: # Extract the desired parameters
        time_list.append(float(packet.frame_info.time_relative))
        frlen_list.append(float(packet.length))     
# Sử dụng pyshark để đọc file pcap và lấy time và length từ các frame trong pcap

    data = {'time':time_list,'frame length':frlen_list} # Create panda dataframe from the extracted parameters
    df = pd.DataFrame(data) #Lấy dictionary và biến thành dạng bảng
# Từ time và length đã lấy được, sắp xếp lại theo dạng bảng (sử dụng pandas)
    # print(df.iloc[-1:])
    final_time = round(df.iloc[-1:]['time'].values[0]) # get the final time interval (lấy giây nguyên cuối cùng trong cột time)
    # print(final_time)

    time_range_list = []
    len_packet_list = []

    for i in range(final_time): # Infer the throughput parameter 
        dfi = df.loc[(df['time'] <= i+1) & (df['time'] >= i)] # Tập hợp toàn bộ những hàng có biến time từ i đến i+1
        time_range_list.append(i) # Đưa i vào list
        len_packet_list.append(dfi['frame length'].sum()) # Tính tổng các biến frame length của các hàng thỏa mãn từ i đến i+1 và đưa vào list
        del(dfi) 

    dfi = pd.DataFrame(data={'time':time_range_list, 'throughput':len_packet_list}) # Create pandas dataframe of throughput
# Tính throughput và đưa vào bảng throughput (dfi) (sử dụng pandas)
  
    if output_flag == True: # Write csv file of the throughput data
        dfi.to_csv(output_file)

    dfi.plot(x ='time', y='throughput', kind = 'line') # Plot throughput data. Đây là hàm kết hợp giữa pandas và matplotlib
    plt.xlabel('time')
    plt.ylabel('throughput (bytes/s)')
    plt.show()
# Vẽ đồ thị sử dụng matplotlib + panda

if __name__ == "__main__":
    main(sys.argv[1:])
# Lệnh để chạy chương trình