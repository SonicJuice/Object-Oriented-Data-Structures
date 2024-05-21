""" a non-cryptographic hash function suitable for general hash-based lookup. It's designed 
to provide a good distribution of hashes for input keys, making it highly effective 
for hash tables. """
def murmurhash3(key, seed=0x0, signed=True):
    """ bytearray returns returns mutable sequence of integers in the range 0 <= x < 256. 
    str.encode() converts a string into a collection of bytes, using a given encoding 
    (utf-8 by default). """
    key_bytes = bytearray(key.encode())
    key_length = len(key_bytes)
    """ number of 4 byte blocks in the key. """
    nblocks = key_length // 4
    """ initial seed value ensures that the resulting hash will be different for similar 
    inputs. This is especially useful in hash tables, as it allows for the even distribution 
    of keys across buckets. """
    h1 = seed
    """ c1 and c2 are large enough to prevent aliasing (repetitive patterns) in hashes 
    without significant overhead. They're also coprime, ensuring that the hashing 
    process isn't biased towards certain patterns in the keys. Finally, they're 
    sufficiently different enough to contribute to the avalanche effect, 
    where small changes in the key significantly changes the hash. """
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    for block_start in range(0, nblocks * 4, 4):
        """ construct a 32-bit integer from the four bytes of the current block. """
        k1 = key_bytes[block_start + 3] << 24 | \
             key_bytes[block_start + 2] << 16 | \
             key_bytes[block_start + 1] <<  8 | \
             key_bytes[block_start + 0]

        k1 = (c1 * k1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
        k1 = (c2 * k1) & 0xFFFFFFFF

        h1 ^= k1
        h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF
        """ 5 is small enough to contribute a uniform distribution of hashes, whilst 
        0xe6546b64 is large enough to effectively aid in bit mixing (). """
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    """ calculate the starting index of the remaining bytes. """
    tail_index = nblocks * 4
    k1 = 0
    """ determine the number of remaining bytes (0, 1, 2, or 3). """
    tail_size = key_length & 3

    if tail_size >= 3:
        k1 ^= key_bytes[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= key_bytes[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= key_bytes[tail_index + 0]

    if tail_size > 0:
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    final_hash = _finalise(h1 ^ key_length)

    if signed:
        """ if the MSB is 0. """
        if final_hash & 0x80000000 == 0:
            return final_hash
        else:
            """ convert from unsigned to signed integer via two's compliment. """
            return -((final_hash ^ 0xFFFFFFFF) + 1)
    else:
        return final_hash

def _finalise(hash):
    hash ^= hash >> 16
    """ . """
    hash= (hash * 0x85ebca6b) & 0xFFFFFFFF
    hash^= hash >> 13
    """ . """
    hash= (hash * 0xc2b2ae35) & 0xFFFFFFFF
    hash^= hash >> 16
    return hash
