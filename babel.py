import binascii
import struct

class CodepointInfo:
    def __init__(self):
        self.name = ""
        self.category = 0
        self.bidiClass = 0
        self.isValid = False
        self.isNSM  = False
        self.isCombining  = False
        self.isRTL  = False
        self.isLTR  = False
        self.isMirrored = False
        self.isControl = False
        self.uppercaseMapping = None
        self.lowercaseMapping = None
        self.titlecaseMapping = None
        self.mirrorMapping = None
        self.glyphdata = bytearray()

bidi_info = dict()

category_mapping = {
    'Lu' : 1,
    'Ll' : 2,
    'Lt' : 3,
    'Lm' : 4,
    'Lo' : 5,
    'Mn' : 6,
    'Mc' : 7,
    'Me' : 8,
    'Nd' : 9,
    'Nl' : 10,
    'No' : 11,
    'Pc' : 12,
    'Pd' : 13,
    'Ps' : 14,
    'Pe' : 15,
    'Pi' : 16,
    'Pf' : 17,
    'Po' : 18,
    'Sm' : 19,
    'Sc' : 20,
    'Sk' : 21,
    'So' : 23,
    'Zs' : 24,
    'Zl' : 25,
    'Zp' : 26,
    'Cc' : 27,
    'Cf' : 28,
    'Cs' : 29,
    'Co' : 30,
    'Cn' : 31
}

bidi_mapping = {
    'L' : 1,
    'R' : 2,
    'AL' : 3,
    'EN' : 4,
    'ES' : 5,
    'ET' : 6,
    'AN' : 7,
    'CS' : 8,
    'NSM' : 9,
    'RNSM' : 9, # I added this one as a hack, technically it's a nonspacing mark.
    'BN' : 10,
    'B' : 11,
    'S' : 12,
    'WS' : 13,
    'ON' : 14,
    'LRE' : 15,
    'LRO' : 15,
    'RLE' : 15,
    'RLO' : 15,
    'PDF' : 15,
    'LRI' : 15,
    'RLI' : 15,
    'FSI' : 15,
    'PDI' : 15
}

for line in open('UnicodeData.txt', 'r'):
    line = line.strip().split(";")
    if len(line) < 5:
        break
    codepoint = line[0]
    general_category = line[2]
    bidi_class = line[4]
    bidi_mirrored = line[9]
    info = CodepointInfo()
    info.isValid = True
    info.name = line[1]
    info.category = category_mapping[general_category]
    info.bidiClass = bidi_mapping[bidi_class]
    if len(line[12]):
        info.uppercaseMapping = line[12]
    if len(line[13]):
        info.lowercaseMapping = line[13]
    if len(line[14]):
        info.titlecaseMapping = line[14]
    info.mirrorMapping = None
    info.isNSM = general_category in ["Mn", "Mc", "Me"] or bidi_class in ["NSM", "RNSM"]
    info.isCombining = general_category in ["Mc", "Me"]
    info.isLTR = bidi_class in ["L", "LRE", "LRO", "LRI"]
    info.isRTL = bidi_class in ["R", "AL", "RLE", "RLO", "RLI", "RNSM"]
    info.isMirrored = bidi_mirrored == "Y"
    info.isControl = general_category in ["Cc", "Cf", "Cs", "Co", "Cn"]
    bidi_info[codepoint] = info

def addFakeCodepoints(start, end, name):
    for i in range(start, end):
        info = CodepointInfo()
        codepoint = "0x{:X}".format(i)[2:]
        info.isValid = True
        info.name = name
        info.isNSM = False
        info.isLTR = True
        info.isRTL = False
        info.isMirrored = False
        info.isControl = False
        bidi_info[codepoint] = info

# to save space, UnicodeData.txt omits a bunch of blocks with identical attributes
# let's put them back.
addFakeCodepoints(0x3400, 0x4DB5, "CJK Ideograph Extension A")
addFakeCodepoints(0x4E00, 0x9FEF, "CJK Ideographs")
addFakeCodepoints(0xAC00, 0xD7A3, "Hangul Syllables")
addFakeCodepoints(0x20000, 0x2A6D6, "CJK Ideograph Extension B")
addFakeCodepoints(0x2A700, 0x2B734, "CJK Ideograph Extension C")
addFakeCodepoints(0x2B740, 0x2B81D, "CJK Ideograph Extension D")
addFakeCodepoints(0x2B820, 0x2CEA1, "CJK Ideograph Extension E")
addFakeCodepoints(0x2CEB0, 0x2EBE0, "CJK Ideograph Extension F")

# I may come to regret this, but: conlangs. are a thing.
# There's plenty of room for them on the 4MB chip but leaving disabled for the 2MB one.
enable_conlangs = False
if enable_conlangs:
    addFakeCodepoints(0xE000, 0xE07F, "Tengwar")
    addFakeCodepoints(0xE080, 0xE0FF, "Cirth")
    addFakeCodepoints(0xE150, 0xE1AF, "Kinya")
    addFakeCodepoints(0xE1B0, 0xE1CF, "Ilianóre")
    addFakeCodepoints(0xE200, 0xE26F, "Verdurian")
    addFakeCodepoints(0xE280, 0xE29F, "aUI")
    addFakeCodepoints(0xE2A0, 0xE2CF, "Amman-iar")
    addFakeCodepoints(0xE300, 0xE33F, "Mizarian")
    addFakeCodepoints(0xE340, 0xE35F, "Zíirí:nka")
    addFakeCodepoints(0xE3B0, 0xE3FF, "Olaetyan")
    addFakeCodepoints(0xE5C0, 0xE5DF, "Gargoyle")
    addFakeCodepoints(0xE630, 0xE64F, "Seussian Latin Extensions")
    addFakeCodepoints(0xE650, 0xE67F, "Sylabica")
    addFakeCodepoints(0xE680, 0xE6CF, "Ewellic")
    addFakeCodepoints(0xE6F0, 0xE6FF, "Unifon Extended")
    addFakeCodepoints(0xE740, 0xE76F, "Unifon")
    addFakeCodepoints(0xE770, 0xE77F, "Solresol")
    addFakeCodepoints(0xE780, 0xE7FF, "Visible Speech")
    addFakeCodepoints(0xE800, 0xE82F, "Monofon")
    addFakeCodepoints(0xE830, 0xE88F, "D'ni")
    addFakeCodepoints(0xE890, 0xE8DF, "Aurebesh")
    addFakeCodepoints(0xE8E0, 0xE8FF, "Tonal")
    addFakeCodepoints(0xE900, 0xE97F, "Glaitha-A")
    addFakeCodepoints(0xE980, 0xE9FF, "Glaitha-B")
    addFakeCodepoints(0xEAA0, 0xEAFF, "Wanya")
    addFakeCodepoints(0xEB00, 0xEB3F, "Orokin")
    addFakeCodepoints(0xED00, 0xED3F, "Deini")
    addFakeCodepoints(0xF4C0, 0xF4EF, "Ath")
    addFakeCodepoints(0xF8A0, 0xF8CF, "Aiha")
    addFakeCodepoints(0xF8D0, 0xF8FF, "Klingon")

for line in open('BidiMirroring.txt', 'r'):
    line = line.strip().split(";")
    if len(line) < 2:
        break
    codepoint = line[0]
    if codepoint in bidi_info:
        bidi_info[codepoint].mirrorMapping = line[1]


unifont = dict()

for line in open('unifont-12.1.03.hex', 'r'):
    line = line.strip().split(":")
    if len(line) < 2:
        break
    codepoint = line[0]
    data = line[1]

    if codepoint in bidi_info:
        unifont[codepoint] = bidi_info[codepoint]
        unifont[codepoint].glyphdata = bytes.fromhex(data)

for line in open('unifont_upper-12.1.03.hex', 'r'):
    line = line.strip().split(":")
    if len(line) < 2:
        break
    codepoint = line[0].lstrip("0")
    data = line[1]

    if codepoint in bidi_info:
        unifont[codepoint] = bidi_info[codepoint]
        unifont[codepoint].glyphdata = bytes.fromhex(data)

for line in open('unifont_csur-12.1.03.hex', 'r'):
    line = line.strip().split(":")
    if len(line) < 2:
        break
    codepoint = line[0].lstrip("0")
    i = int(codepoint, 16)
    data = line[1]

    if codepoint in bidi_info:
        unifont[codepoint] = bidi_info[codepoint]
        # NSM override for conlangs. this comes from plane00csur-combining.txt
        if i in ["E040", "E041", "E042", "E043", "E044", "E045", "E046", "E047", "E048", "E049", "E04A", "E04B", "E04C", "E04D", "E04E", "E04F", "E050", "E051", "E052", "E053", "E054", "E055", "E056", "E057", "E059", "E05A", "E05C", "E05D", "E06D", "E06E", "E07D", "E0EA", "E0EB", "E0EC", "E185", "E186", "E187", "E188", "E189", "E18A", "E18B", "E18C", "E256", "E257", "E258", "E259", "E2BF", "E310", "E311", "E312", "E313", "E3E4", "E3E5", "E3E6", "E3E7", "E3E8", "E985", "E986", "E987", "E988", "E989", "E98A", "E98B", "E98C", "E98D", "E98E", "E98F", "E99F", "E9A0", "E9A1", "E9A2", "E9A3", "E9A4", "E9A5", "E9A6", "E9A7", "E9A8", "E9A9", "E9AA", "E9AB", "E9AC", "E9AD", "E9AE", "E9AF", "E9B0", "E9B1", "E9B2", "E9B3", "E9B4", "E9B5", "E9B6", "E9B7", "E9B8", "E9B9", "E9BA", "E9BB", "E9BC", "E9BD", "E9BE", "E9BF", "E9C0", "E9C1", "E9C2", "E9C3", "E9C4", "E9C5", "E9C6", "E9C7", "E9C8", "E9C9", "E9CA", "E9CB", "E9CC", "E9CD", "E9CE", "E9CF", "E9D0", "E9D1", "E9D2", "E9D3", "E9D4", "E9D5", "E9D6", "E9D7", "E9D8", "E9D9", "E9DA", "E9DB", "E9DC", "E9DD", "E9DE", "E9DF", "EAEC", "EAED", "EAEE", "EB20", "EB21", "EB22", "EB23", "EB24", "EB25", "EB26", "EB27", "EB28", "EB29", "EB2A", "F8BF", "F8C5", "F8C6", "F8C8"]:
            unifont[codepoint].isNSM = True
        unifont[codepoint].glyphdata = bytes.fromhex(data)
    


def generate_unifont_bin():
    lookup = bytearray()
    metadata = bytearray()
    glyphs = bytearray()
    stop_at = 0x10000

    current_position = 256 + stop_at * 6
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        
        if codepoint in unifont:
            character = unifont[codepoint]
            glyphdata = character.glyphdata
            lookup_entry = current_position
            # A 4MB chip uses 22-bit addresses:
            # 0b0000000000xxxxxxxxxxxxxxxxxxxxxx
            # this gives us the 10 high bits to use for whatever we want!
            # 0bBCLRNWWWWWxxxxxxxxxxxxxxxxxxxxxx
            # WWWWW - width / advance. Currently the only values are 0, 8 and 16, but I'm leaving it as a five bit value in case a variable width font becomes a thing.
            # N - Character is a COMBINING or ENCLOSING mark.
            # R - Character forces a mode change to RTL, also part of mirroring test
            # L - Character forces a mode change to LTR, also part of mirroring test
            #      NOTE: this is a bit funky, but: 
            #       * If R and L are both 0, the character is drawn normally in the current text run.
            #       * if R and L are both 1, the character is drawn mirrored in the current text run.
            #       * if R and not L, or L and not R, the layout mode changes. None of these glyphs mirror.
            # C - Control character, do not draw
            # B - Whitespace or other line-breaking character. If word wrapping, you can wrap on this.
            if len(glyphdata) == 16 and not character.isNSM:
                lookup_entry |= 0b0000001000000000000000000000000
            if len(glyphdata) == 32 and not character.isNSM:
                lookup_entry |= 0b0000010000000000000000000000000
            if character.isCombining:
                lookup_entry |= 0b0000100000000000000000000000000
            if character.isRTL:
                lookup_entry |= 0b0001000000000000000000000000000
            if character.isLTR:
                lookup_entry |= 0b0010000000000000000000000000000
            if character.isMirrored:
                lookup_entry |= 0b0011000000000000000000000000000
            if character.isControl:
                lookup_entry |= 0b0100000000000000000000000000000
            if codepoint in ["0009", "0020", "1680", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2008", "2009", "200A", "205F", "3000", "180E", "200B", "200C", "200D"]:
                lookup_entry |= 0b1000000000000000000000000000000

            lookup += struct.pack('<I', current_position)

            category_and_capitalization = character.category
            bidi_and_other = character.bidiClass
            if character.uppercaseMapping is not None:
                category_and_capitalization |= 0b00100000
            if character.lowercaseMapping is not None:
                category_and_capitalization |= 0b01000000
            if character.titlecaseMapping is not None:
                category_and_capitalization |= 0b10000000
            if character.mirrorMapping is not None:
                bidi_and_mirroring |= 0b00010000
            if codepoint in ["0009", "000A", "000B", "000C", "000D", "0020", "0085", "00A0", "1680", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "200A", "2028", "2029", "202F", "205F", "3000"]:
                bidi_and_other |= 0b00100000 # whitespace characters from PropList.txt
            # still have two bits to spare here!
            metadata += struct.pack('<B', category_and_capitalization)
            metadata += struct.pack('<B', bidi_and_other)

            glyphdata = character.glyphdata
            glyphs += glyphdata

            current_position += len(glyphdata)
        else:
            # waste of space but pad out the table for constant time lookup
            lookup += b'\x00\x00\x00\x00'
            metadata += b'\x00\x00'

    uppercase_mappings = bytearray()
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        if codepoint in unifont:
            character = unifont[codepoint]
            if character.uppercaseMapping is not None:
                uppercase_mappings += struct.pack('<H', int(codepoint, 16))
                uppercase_mappings += struct.pack('<H', int(character.uppercaseMapping, 16))

    lowercase_mappings = bytearray()
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        if codepoint in unifont:
            character = unifont[codepoint]
            if character.lowercaseMapping is not None:
                lowercase_mappings += struct.pack('<H', int(codepoint, 16))
                lowercase_mappings += struct.pack('<H', int(character.lowercaseMapping, 16))

    titlecase_mappings = bytearray()
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        if codepoint in unifont:
            character = unifont[codepoint]
            if character.titlecaseMapping is not None:
                titlecase_mappings += struct.pack('<H', int(codepoint, 16))
                titlecase_mappings += struct.pack('<H', int(character.titlecaseMapping, 16))

    mirror_mappings = bytearray()
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        if codepoint in unifont:
            character = unifont[codepoint]
            if character.mirrorMapping is not None:
                mirror_mappings += struct.pack('<H', int(codepoint, 16))
                mirror_mappings += struct.pack('<H', int(character.mirrorMapping, 16))

    start_of_lookup = 256
    start_of_metadata = start_of_lookup + len(lookup)
    start_of_glyph_data = start_of_metadata + len(metadata)
    start_of_mapping = start_of_glyph_data + len(glyphs)
    
    header = bytearray()
    header += struct.pack('<B', 0)                  # reserved i guess
    header += struct.pack('<B', 0)                  # reserved i guess
    header += struct.pack('<B', 8)                  # nominal width
    header += struct.pack('<B', 16)                 # nominal height
    header += struct.pack('<B', 0)                  # version, major
    header += struct.pack('<B', 1)                  # version, minor
    header += struct.pack('<B', 0)                  # flags for features?
    header += struct.pack('<B', 0)                  # more flags, make it an even 8 bits
    header += struct.pack('<I', start_of_lookup)
    header += struct.pack('<I', start_of_metadata)
    header += struct.pack('<I', start_of_glyph_data)
    # the rest of the header is just kind of just info about the stuff we stuffed at the end.
    # the general format: 
    #  * 3 bytes: the location of the data
    #  * 1 byte: the type of data
    #  * 3 bytes: the length of the data
    #  * 1 byte: flags about the data
    # why did i pack it this way? because i just want to read the 4-byte values as an unsigned little-endian int.
    # value & 0xFF gives me the type/flags, value >> 8 gives me the location/length
    header += struct.pack('<I', start_of_mapping)
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    header += struct.pack('<B', 1)                  # this is just arbitrary, 1 means mappings from lowercase to uppercase
    length = struct.pack('<I', len(uppercase_mappings))
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    header += struct.pack('<B', 0)                  # flags is more hypothetical than real at this point
    start_of_mapping += len(uppercase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    header += struct.pack('<B', 2)                  # 2 means mappings from uppercase to lowercase
    length = struct.pack('<I', len(lowercase_mappings))
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    header += struct.pack('<B', 0)
    start_of_mapping += len(lowercase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    header += struct.pack('<B', 3)                  # 3 means titlecase mappings
    length = struct.pack('<I', len(titlecase_mappings))
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    header += struct.pack('<B', 0)
    start_of_mapping += len(titlecase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    header += struct.pack('<B', 4)                  # 4 means mappings from normal to mirrored
    length = struct.pack('<I', len(mirror_mappings))
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    header += struct.pack('<B', 0)
    start_of_mapping += len(mirror_mappings)
    

    while len(header) < 256:
        header += b'\xFF'

    output = header + lookup + metadata + glyphs + uppercase_mappings + lowercase_mappings + titlecase_mappings + mirror_mappings

    print("Final size: {} bytes.\n\n".format(len(output)))
    outfile = open('babel.bin', 'wb')
    outfile.write(output)

while 1:
    print("\033[;1mUnifont Converter\033[0;0m\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
    print("Commands:")
    print("\t1. Print glyph information")
    print("\t2. Generate babel.bin")
    print("\tQ. Quit")
    command = input("What do you want to do? ")
    if command == '1':
        size = 0
        for codepoint in unifont:
            character = unifont[codepoint]
            if True: # add constraints here for testing
                print("{} {}".format(codepoint, character.name))
            size += len(unifont[codepoint].glyphdata)
        print("\n\n")
        print("Loaded data for {} glyphs.\n\n".format(len(unifont)))
    elif command == '2':
        generate_unifont_bin()
    elif command.upper() == 'Q':
        exit(0)
