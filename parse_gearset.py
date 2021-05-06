
import base64
import binascii


def hash_to_item_ids(hash: bytes):
    hash = hash.replace(b'_', b'/')

    b = ''
    for _ in range(4):
        try:
            b = bytearray(base64.b64decode(hash))
            break
        except binascii.Error:
            hash += b'='

    assert(b[0] == 0x02)
    player_level = b[1]
    talent_bytes = b[2]
    offset = 3 + talent_bytes

    print(player_level)
    print(talent_bytes)
    print(b[3:(3+talent_bytes)])

    gear = list(reversed(b[offset:]))
    slots, enchants = {}, {}

    while gear:
        first = gear.pop()

        slot = first & 0x1f
        has_enchant = first & 0x80
        has_other = first & 0x40  # Deprecated?
        item_id = gear.pop() << 8 | gear.pop()

        slots[slot] = item_id

        if has_enchant:
            enchant_id = gear.pop() << 8 | gear.pop()
            enchants[slot] = enchant_id

        #print('{0:b}'.format(first))
        #print(f"Slot {slot} has item: {item_id}{', with enchant ' + str(enchant_id) if has_enchant else ''}")

    return slots, enchants

s, e = hash_to_item_ids(b'AjwDXwX_AVemBleqh1elXmIIV6g')
print(s)
print(e)