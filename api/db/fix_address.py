def padAddress(wallet):
    # Remove the '0x' prefix if present
    if wallet.startswith('0x'):
        wallet = wallet[2:]
    # Pad the hexadecimal string with zeros to match the desired total length, including the length of '0x'
    padded_hex_str = '0x' + wallet.zfill(66 - 2)
    return padded_hex_str
