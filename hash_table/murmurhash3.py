""" a non-cryptographic hash function suitable for general hash-based lookup. """
def murmurhash3(key, seed=0x0):
    """ bytearray returns returns mutable sequence of integers in the range 0 <= x < 256. 
    str.encode() converts a string into a collection of bytes via utf-8. """
    key_bytes = bytearray(key.encode())
    key_length = len(key_bytes)
    """ number of 4 byte blocks in the key. """
    nblocks = key_length // 4
    """ initial seed value ensures that the resulting hash will be different for similar 
    inputs. This is especially useful in hash tables, as it allows for even key 
    distribution across buckets. """
    h1 = seed
    """ c1, c2, and 0xe6546b64 are derived from primes, helping to uniformly spread the 
    input bits. They also provide a mixture of high and low bit patterns, maximising 
    entropy during mixing. Furthermore, the mixing strength of the specific values avoid 
    patterns that would reduce the effectiveness of bitwise operations. """
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    for block_start in range(0, nblocks * 4, 4):
        """ combine each 4-byte block into a 32-bit integer. """
        k1 = key_bytes[block_start + 3] << 24 | \
             key_bytes[block_start + 2] << 16 | \
             key_bytes[block_start + 1] <<  8 | \
             key_bytes[block_start + 0]

        """ bitwise AND with 0xFFFFFFFF avoids overflow by ensuring that intermediate 
        results are constrained to 32 bits. """
        k1 = (c1 * k1) & 0xFFFFFFFF
        """ 13, 15, 17, 19 are non-powers-of-two chosen to avoid alignment issues
        and ensure that all bits influence each other. """
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
        k1 = (c2 * k1) & 0xFFFFFFFF

        h1 ^= k1
        h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    """ combine remaining 1 to 3 bytes not covered by the 4-byte blocks. """
    tail_index = nblocks * 4
    k1 = 0
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

    return _finalise(h1 ^ key_length)
    
def _finalise(hash):
    hash ^= hash >> 16
    hash= (hash * 0x85ebca6b) & 0xFFFFFFFF
    hash^= hash >> 13
    hash= (hash * 0xc2b2ae35) & 0xFFFFFFFF
    hash^= hash >> 16
    return hash
