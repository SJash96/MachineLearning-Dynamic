import pyshark
import csv
from datetime import datetime

def capPacket():

    liveCap = pyshark.LiveCapture(interface='Ethernet', bpf_filter='ip')

    def annalyze_packet(pkt):

        #print(dir(pkt))

        pkt_no = pkt.number
        now = datetime.now()
        pkt_time = now.strftime("%Y-%m-%d %H:%M:%S")
        pkt_length = pkt.length
        protocol = pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        print('{} {} {}  {}:{} --> {}:{} {}'.format(pkt_no, pkt_time, protocol, src_addr, src_port, dst_addr, dst_port, pkt_length))

        append_CSV(pkt, pkt_time)

    try:
        liveCap.apply_on_packets(annalyze_packet)
    except AttributeError:
        capPacket()
        #print("Error: {}".format(e))


def append_CSV(pkt, pkt_time):
    with open('Z:/livePackets.csv', 'a+', newline='') as write_Obj:
        writer = csv.writer(write_Obj)
        writer.writerow([pkt.number, pkt_time, pkt.ip.src, pkt[pkt.transport_layer].srcport, pkt.ip.dst, pkt[pkt.transport_layer].dstport, pkt.transport_layer, pkt.length])


def createCSVHeader():
    with open('Z:/livePackets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["No.", "Time", "Source", "Source Port", "Destination", "Destination Port", "Protocol", "Length"])


if __name__ == "__main__":
    choice = input("1 For Capturing Packet, 2 For Creating CSV: ")
    if choice == "1":
        capPacket()
    elif choice == "2":
        createCSVHeader()