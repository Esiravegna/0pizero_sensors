import struct

def little_endian_byte_to_int(response):
	return struct.unpack('<H', bytearray(response))[0]