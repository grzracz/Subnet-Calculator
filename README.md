# Subnet Calculator
*Written on 13 Mar 2019.*

Subnet Calculator written in Python using sys, subprocess and socket libraries.

Uses IPaddress/CIDR as input (extracts the information from current computer if not given) and prints network address, network class, network type, subnet mask, 
broadcast address, first and last host address and max number of hosts (all addresses both decimal and binary).

If given address is pingable the program asks if you want to ping it, then shows the result.

All data is saved to a text file.

> python SubnetCalculator.py qq.com

will result in:

```
IP Address: 192.168.43.173 (11000000.10101000.00101011.10101101)
Subnet Mask (CIDR): /24

Network address: 192.168.43.0 (11000000.10101000.00101011.00000000)
Network class: C (small)
Network type: private
Subnet Mask: 255.255.255.0 (11111111.11111111.11111111.00000000)
Broadcast address: 192.168.43.255 (11000000.10101000.00101011.11111111)
First host address: 192.168.43.1 (11000000.10101000.00101011.00000001)
Last host address: 192.168.43.254 (11000000.10101000.00101011.11111110)
Max number of hosts: 254

Pinging 192.168.43.173 with 32 bytes of data:
Reply from 192.168.43.173: bytes=32 time<1ms TTL=128
Reply from 192.168.43.173: bytes=32 time<1ms TTL=128
Reply from 192.168.43.173: bytes=32 time<1ms TTL=128
Reply from 192.168.43.173: bytes=32 time<1ms TTL=128
Reply from 192.168.43.173: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.43.173:
    Packets: Sent = 5, Received = 5, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms

Pinging qq.com:
Pinging 111.161.64.48 with 32 bytes of data:
Reply from 111.161.64.48: bytes=32 time=465ms TTL=41
Reply from 111.161.64.48: bytes=32 time=477ms TTL=41
Reply from 111.161.64.48: bytes=32 time=480ms TTL=41
Reply from 111.161.64.48: bytes=32 time=512ms TTL=41
Reply from 111.161.64.48: bytes=32 time=524ms TTL=41

Ping statistics for 111.161.64.48:
    Packets: Sent = 5, Received = 5, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 465ms, Maximum = 524ms, Average = 491ms
```
