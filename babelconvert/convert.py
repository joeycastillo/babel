import binascii
import struct

class CodepointInfo:
    def __init__(self):
        self.name = ""
        self.category = 0
        self.bidiClass = 0
        self.isValid = False
        self.isNSM  = False
        self.isRTL  = False
        self.isLTR  = False
        self.isMirrored = False
        self.isControl = False
        self.uppercaseMapping = None
        self.lowercaseMapping = None
        self.titlecaseMapping = None
        self.mirrorMapping = None
        self.lineBreakOpportunity = None
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
    'So' : 22,
    'Zs' : 23,
    'Zl' : 24,
    'Zp' : 25,
    'Cc' : 26,
    'Cf' : 27,
    'Cs' : 28,
    'Co' : 29,
    'Cn' : 30
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
        info.category = 5
        info.bidiClass = 1
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

for line in open('LineBreak.txt', 'r'):
    line = line.strip().split(";")
    if len(line[0]) > 0 and line[0][0] == "#":
        continue
    if len(line) < 2:
        continue
    codepoint = line[0]
    lbclass = line[1][:3].strip(" ")
    if len(codepoint.split("..")) > 1:
        codepoints = codepoint.split("..")
        start = int(codepoints[0], 16)
        end = int(codepoints[1], 16)
        for i in range(start, end + 1):
            codepoint = "{0:#06X}".format(i)[2:]
            if codepoint in bidi_info:
                if lbclass in ["SP", "ZWS", "B2", "BA", "HY", "SY", "ID"]:
                    bidi_info[codepoint].lineBreakOpportunity = True
    elif codepoint in bidi_info:
        if lbclass in ["SP", "ZWS", "B2", "BA", "HY", "SY", "ID"]:
            bidi_info[codepoint].lineBreakOpportunity = True


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

# Conlangs
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
    

# Arabic / Perso-Arabic Shaping
# NOTE: Unicode uses the word 'Arabic' for these glyphs, but this block also has glyphs for non-Arabic languages
# such as Persian, Kurdish, Azerbaijani, Sindhi, Balochi, Pashto, Lurish, Urdu and Mandinka, among others.

# A primer: Perso-Arabic letters can take one of up to four different forms, depending where they appear in a word
# and what letters surround them. So, for example, let's look at four letters:

# name    isolated    initial    medial    final
# Alef‭       ﺍ          N/A       N/A        ﺎ  ‬
# Bah‭        ﺏ           ﺑ         ﺒ         ﺐ  ‬
# Ha ‭        ﺡ           ﺣ         ﺤ         ﺢ  ‬
# Lam‭        ﻝ           ﻟ         ﻠ         ﻞ  ‬

# The N/A is misleading, but useful for the algorithm; a word can start with Alef, it just means that it will take
# its isolated form. Alef can also appear in the middle of a word, it just means that it will take its final form,
# and the character after it will take its initial form. This will become clear once we look at a word or two:
#   door: ﺑﺎﺏ (bab)
# The letter Bah (ﺏ) appears twice here, in two different forms: the first Bah on the right is its initial form,
# and it connects to the Alef (ﺍ) next to it. But since Alef doesn't have a medial form, just an isolated and a
# final one, the last Bah cannot connect to it; it stands alone.
# But what if we're talking about a specific door?
#   the door: ﺍﻟﺒﺎﺏ (al bab)
# The Alef on the right stands alone (remember, its only options are final and isolated). The Lam comes next, in
# its initial form, which connects to the Bah. Bah can connect on both sides, so it now requires a medial form,
# to connect to both the Lam before it, and the Alef after it. (the last Bah still stands alone)
# To illustrate the final form of Bah:
#   love: ﺍﻟﺤﺐ (al hub)
# the Alef and Lam should look familiar from earlier; then Lam connects to Ha in its medial form, which connects
# to Bah. Since the word ends in Bah, Bah takes its final form.

# Unicode includes two blocks called Arabic Presentation Forms. They include isolated, initial, medial and final
# forms for all these letters; we just have to figure out which ones to use and when.

# They also include a bunch of ligatures for various combinations, plus a ligature for Allah (ﷲ) and the Basmala
# (﷽) — believe it or not, those are each one Unicode codepoint! In the end though, there's only one
# ligature that's absolutely necessary: the Lam Alef (ﻻ), which is the only correct way to display Lam followed
# by Alef (ﻟ‍ﺎ would be considered unreadable).
# There are only eight forms for the Lam Alef ligature, so we're not including anything in babel.bin for this.
# Instead, implementations should make sure to implement the following:
# U+0644 followed by U+0622 => U+FEF5 (isolated) or 0xFEF6 (final)
# U+0644 followed by U+0623 => U+FEF7 (isolated) or 0xFEF8 (final)
# U+0644 followed by U+0625 => U+FEF9 (isolated) or 0xFEFA (final)
# U+0644 followed by U+0627 => U+FEFB (isolated) or 0xFEFC (final)

# Finally, there's one last wrinkle. Arabic short vowels and diacritics appear above and below the line of
# text. Unicode accomplishes this by encoding them as non-spacing marks, and they are included inline in a
# string of Arabic text. These marks do not participate in shaping; implementations should just make sure to
# pass over non-spacing marks from the Arabic block when determining the appropriate shape for a character.

# Enough background! The upshot is that we only need to encode one lookup table here. The first row in this
# table corresponds to U+0621, and it goes through U+06D2 (inclusive). Each row contains an array of four
# codepoints for each of the possible presentation forms (isolated, initial, medial, final), or 0 if a codepoint
# does not support that form. All shapable code points have an isolated form; thus, if the isolated form is 0,
# you can assume that the codepoint does not participate in shaping (i.e. numerals, punctuation, diacritics).

# Also I admit this code is ugly; it just brute forces its way through both the Arabic and Arabic Presentation
# Form blocks, many times, to find codepoints that match based on their Unicode names. Works, though!

arabic_lookup = [0] * 4 * 179
forms = [" ISOLATED FORM", " INITIAL FORM", " MEDIAL FORM", " FINAL FORM"]
for i in range(0x0600, 0x0700):
    # c/i is the original codepoint, p/j is the presentation form candidate.
    # k is the index of the form; the order is isolated/initial/medial/final.
    c = "{:04X}".format(i)
    if c in bidi_info:
        name = bidi_info[c].name
        for j in range(0xFB50, 0xFEFF):
            p = "{:04X}".format(j)
            if p in bidi_info:
                p_name = bidi_info[p].name
                for k in range(0, 4):
                    form = forms[k]
                    if p_name == name + form:
                        arabic_lookup[4 * (i - 0x0621) + k] = j


def generate_unifont_bin():
    lookup = bytearray()
    glyphs = bytearray()
    last_codepoint = 0xFFFF
    stop_at = last_codepoint + 1

    current_position = 256 + stop_at * 6
    for i in range(0, stop_at):
        codepoint = "{0:#06X}".format(i)[2:]
        
        if codepoint in unifont:
            character = unifont[codepoint]
            glyphdata = character.glyphdata
            # A 4MB chip uses 22-bit addresses:
            # 0b0000000000xxxxxxxxxxxxxxxxxxxxxx
            # this gives us the 10 high bits to use for whatever we want!
            # 0bBCLRNWWWWWxxxxxxxxxxxxxxxxxxxxxx
            # WWWWW - width / advance. Currently the only values are 0, 8 and 16, but I'm leaving it as a five bit value in case a variable width font becomes a thing.
            #         If we get to a point where 22-bit addresses aren't enough, we can steal the lower three bits to support up to 32MB of glyph data, at the cost of
            #         losing more granular width information (currently 8 and 16 only set the high bits anyway).
            # N - Character is a COMBINING, ENCLOSING or NON-SPACING mark.
            # R - Character forces a mode change to RTL, also part of mirroring test
            # L - Character forces a mode change to LTR, also part of mirroring test
            #      NOTE: this is a bit funky, but: 
            #       * If R and L are both 0, the character is drawn normally in the current text run.
            #       * if R and L are both 1, the character is drawn mirrored in the current text run, if the run is RTL.
            #       * if R and not L, or L and not R, the layout mode changes. None of these glyphs mirror.
            # C - Control character, do not draw
            # B - Whitespace or other line-breaking character. If word wrapping, you can wrap on this.
            lookup_entry = current_position
            if len(glyphdata) == 16:
                lookup_entry |= 0b00000010000000000000000000000000
            if len(glyphdata) == 32:
                lookup_entry |= 0b00000100000000000000000000000000
            if character.isNSM:
                lookup_entry |= 0b00001000000000000000000000000000
            if character.isRTL:
                lookup_entry |= 0b00010000000000000000000000000000
            if character.isLTR:
                lookup_entry |= 0b00100000000000000000000000000000
            if character.isMirrored:
                lookup_entry |= 0b00110000000000000000000000000000
            if character.isControl:
                lookup_entry |= 0b01000000000000000000000000000000
            if character.lineBreakOpportunity:
                lookup_entry |= 0b10000000000000000000000000000000

            lookup += struct.pack('<I', lookup_entry)

            category_and_capitalization = character.category
            bidi_and_other = character.bidiClass
            if character.uppercaseMapping is not None:
                category_and_capitalization |= 0b00100000
            if character.lowercaseMapping is not None:
                category_and_capitalization |= 0b01000000
            if character.titlecaseMapping is not None:
                category_and_capitalization |= 0b10000000
            if character.mirrorMapping is not None:
                bidi_and_other |= 0b00010000
            if codepoint in ["0009", "000A", "000B", "000C", "000D", "0020", "0085", "00A0", "1680", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "200A", "2028", "2029", "202F", "205F", "3000"]:
                bidi_and_other |= 0b00100000 # whitespace characters from PropList.txt
            # still have two bits to spare here!
            lookup += struct.pack('<B', category_and_capitalization)
            lookup += struct.pack('<B', bidi_and_other)

            glyphdata = character.glyphdata
            glyphs += glyphdata

            current_position += len(glyphdata)
        else:
            # waste of space but pad out the table for constant time lookup
            lookup += b'\x00\x00\x00\x00'
            lookup += b'\x00\x00'

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
    start_of_glyph_data = start_of_lookup + len(lookup)
    start_of_mapping = start_of_glyph_data + len(glyphs)
    
    header = bytearray()
    header += struct.pack('<H', 0x0000)                 # 2 bytes, reserved i guess
    header += struct.pack('<H', 0x0001)                 # version, 2 bytes, major/minor
    header += struct.pack('<B', 8)                      # 1 byte, nominal width
    header += struct.pack('<B', 16)                     # 1 byte, nominal line height
    header += struct.pack('<H', 0)                      # 2 bytes, flags for features?
    header += struct.pack('<I', start_of_glyph_data)    # the start of the glyph data, right adter the LUT
    # This next bit seems like a waste of space, but here's the thought: there are 17 Unicode planes.
    # We allocate 8 bytes to each, two shorts that indicate the supported code points in that plane (the
    # low 16 bits of the codepoint, since the plane index tells us the five high bits), and one uint for
    # an address where the lookup table resides. Both are 0 if the plane is unsupported.
    # yes yes I know only three planes have glyphs in them right now; this is for the future.
    header += struct.pack('<H', 0)                      # the first Unicode codepoint for Plane 0
    header += struct.pack('<H', last_codepoint)         # the last Unicode codepoint for Plane 0
    header += struct.pack('<I', start_of_lookup)        # the start of the lookup table for plane 0
    for i in range(1, 17):
        header += struct.pack('<H', 0)                  # the first Unicode codepoint for Planes 1-16 (TODO)
        header += struct.pack('<H', 0)                  # the last Unicode codepoint for Planes 1-16 (TODO)
        header += struct.pack('<I', 0)                  # the address of the lookup table for each plane

    # on the upside, now we know the extras is at a fixed location, 148,
    # and that's not going to change unless Unicode adds more planes.
    assert(len(header) == 148)
    header += struct.pack('<I', len(header) + 4)        # the start of "extra" data infos, it's inside the header. In fact, it's up next.

    # the rest of the header is just kind of just info about the stuff we stuffed at the end.
    # the general format: 
    #  * 1 byte: the type of data
    #  * 3 bytes: the location of the data
    #  * 1 byte: flags about the data
    #  * 3 bytes: the length of the data
    # why did i pack it this way? because i just want to read the 4-byte values as an unsigned little-endian int.
    # value & 0xFF gives me the type/flags, value >> 8 gives me the location/length.
    # Currently all these LUTs are 2-byte shorts and only support the basic multilingual plane; for the higher planes,
    # we will need to use 4-byte ints. Flags may come into play at that point.

    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', 1)                  # this is just arbitrary, 1 means mappings from lowercase to uppercase
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    length = struct.pack('<I', len(uppercase_mappings))
    header += struct.pack('<B', 0)                  # flags is more hypothetical than real at this point
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    start_of_mapping += len(uppercase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', 2)                  # 2 means mappings from uppercase to lowercase
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    length = struct.pack('<I', len(lowercase_mappings))
    header += struct.pack('<B', 0)
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    start_of_mapping += len(lowercase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', 3)                  # 3 means titlecase mappings
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    length = struct.pack('<I', len(titlecase_mappings))
    header += struct.pack('<B', 0)
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    start_of_mapping += len(titlecase_mappings)
    
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', 4)                  # 4 means mappings from normal to mirrored
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    length = struct.pack('<I', len(mirror_mappings))
    header += struct.pack('<B', 0)
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    start_of_mapping += len(mirror_mappings)
    
    arabic_mapping = bytearray()
    for c in arabic_lookup:
        arabic_mapping += struct.pack('<H', c)
    loc = struct.pack('<I', start_of_mapping)
    header += struct.pack('<B', 64)                 # 64: Perso-Arabic shaping LUT
    header += struct.pack('<B', loc[0])
    header += struct.pack('<B', loc[1])
    header += struct.pack('<B', loc[2])
    length = struct.pack('<I', len(arabic_mapping))
    header += struct.pack('<B', 0)
    header += struct.pack('<B', length[0])
    header += struct.pack('<B', length[1])
    header += struct.pack('<B', length[2])
    start_of_mapping += len(arabic_mapping)

    while len(header) < 256:
        header += b'\x00'

    output = header + lookup + glyphs + uppercase_mappings + lowercase_mappings + titlecase_mappings + mirror_mappings + arabic_mapping

    print("Final size: {} bytes.\n\n".format(len(output)))
    
    while len(output) < 2097152:
        output += b'\xFF'

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
            if character.lineBreakOpportunity: # add constraints here for testing
                print("{} {}".format(codepoint, character.name))
            size += len(unifont[codepoint].glyphdata)
        print("\n\n")
        print("Loaded data for {} glyphs.\n\n".format(len(unifont)))
    elif command == '2':
        generate_unifont_bin()
    elif command.upper() == 'Q':
        exit(0)
