"""
Simple UART capture script for streaming 32-bit floating-point values (little-endian)
from an STM32 microcontroller.

Example usage:
    python uart_capture_cli.py --port COM5 --baud 2000000 
"""

import argparse
import serial
import numpy as np
import time
import sys
import scipy.signal as sig
from scipy.io import savemat

MAGIC = b'\x55\xAA\x55\xAA'  # little-endian of 0xAA55AA55

def read_exact(ser, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = ser.read(n - len(buf))
        if not chunk:
            raise TimeoutError("Timeout")
        buf.extend(chunk)
    return bytes(buf)

def read_block(ser):
    # sync to magic (simple scanner)
    win = bytearray()
    while True:
        b = ser.read(1)
        if not b:
            raise TimeoutError("Timeout waiting for header")
        win += b
        if len(win) > 4:
            del win[0]
        if win == MAGIC:
            break

    # read rest of header: count(2) bps(1) seq(1)
    tail = read_exact(ser, 4)
    count = tail[0] | (tail[1] << 8)
    bps = tail[2]
    seq = tail[3]
    if bps != 4:
        raise ValueError(f"Unexpected bytes/sample: {bps}")

    # read payload and convert to int32 (little-endian)
    payload = read_exact(ser, count * 4)
    data = np.frombuffer(payload, dtype='<f4')
    return seq, data

def main():
    parser = argparse.ArgumentParser(
        description="Capture a block of 32-bit samples from UART.")
    parser.add_argument("--port", "-p", required=True,
                        help="Serial port name, e.g. COM5 or /dev/ttyACM0")
    parser.add_argument("--baud", "-b", type=int, default=460_800,
                        help="UART baud rate (default: 460800)")
    parser.add_argument("--timeout", "-t", type=float, default=2.0,
                        help="Read timeout in seconds (default: 2.0)")
    parser.add_argument("--fs", type=int, default=10_000,
                        help="Sample rate for incoming data")
    parser.add_argument("--duration", "-d", type=float, default=10.0,
                        help="Duration of capture in seconds (default: 10.0)")
    parser.add_argument("--filename", "-f", type=str, default="uart_capture.mat",
                        help="Output filename (default: uart_capture.mat)")

    args = parser.parse_args()


    ser = serial.Serial(args.port, args.baud, timeout=args.timeout)

    transfer_intact=True
    buffer = []
    last_seq, samples = read_block(ser)
    buffer.extend(samples)
    while(len(buffer) < args.fs * args.duration):
        seq, samples = read_block(ser)
        if (last_seq + 1)%256 != seq:
            print(f"Warning: sequence mismatch: last {last_seq} new {seq}", file=sys.stderr)
            transfer_intact=False
        last_seq = seq
        buffer.extend(samples)
        #print(f"\rCaptured {len(buffer)}/{args.fs * args.duration} samples", end="")
    if transfer_intact:
        print("\nCapture complete without errors.")
        data = np.array(buffer, dtype=np.float32)
        savemat(args.filename, {"samples": data, "fs": args.fs})  
        print(f"Data saved to {args.filename}")
    else:
        print("\nCapture completed with errors. Data not saved.", file=sys.stderr)

if __name__ == "__main__":
    main()
