# to color frequency tables
from termcolor import colored, cprint

# Note that I made this uppercase.
ct = """srdhyfhaayrhfzfbfmzuefbxfmocematlnhgmywvagqwardnlkumonsglovnxtubuodhowmilgquxdgmhnlfaxcizkuuzihawuuyfnqtdhlixtubkzwodnbzogvbulveqoqzxzsglodfushawjhpqqciekqnakhawuuyfnqtdirgbzhxjyfcqsqxhxrpuiwgygiidroeaydnutbhxzkyotbvwvwmakoeyuucfmatfjfiyuimszlizbwmzzkyfzfbfmpuomwgwckcomqtfhhwasgbvkuypfahvkoirfuxfkuuxuikhuvyotaimzhltjwloogyxdqhfylxqwswlueyfmsyszkydttmzkrlqywvsrfiyuimwxvwujbvwgqxmwhbxofcmqwglkofulsgukgodnbzlnhmqhcgvcrlxiktjzxlusupgxnypkcklnhaaaskfshhfhcwwgqxoddawxvwttceszefqyqadkbjmwyujowuusgvgjhvdjodatjwqshkwzkufufhvafypzzmjglhfjzeamhhojthjgwcyjvxdkgbgysbynwntjgxuzlizyvtlcdmdjgigtvcnqsygxjydrogfgyuxhfrhzdhmqmlaykydjvxvkycejrtfapvqwcylkfbznenwyiidxdxwjlhsyvxtxhuwnbzgljydroguosbqwgbfioopnbzasslaasfwtwmfthawvuyiffigrlmtgcftgpyfmcwsthfqhhkgshwtfbbugogmhvbfkwbmyqhmrgzusrlwzwczlgygxwbqjbbysdgmhvbfkwodnbzhrdsqiovjafcmqfhdklhowovcoqaushxjihjfjrvgjhxyjglsmhmfmomwtdvxjrmzkdfxnsllugyrjomlnhujngigchlenbfstbwdzqbsrhhsfuxekqnenbvdagczlhawhdnfqshxzkymyztfzlw""".upper()

### Part 1: Finding the Key Length
# As per lecture, we'll calculate letter frequencies on every k-th letter for k=1,2,3,...
# And see which key length(s) produces strings that match English frequencies best.
# Goal here is to spot out 'E'
# According to English frequency, (hw1-freq.png)
# 'E' appears around 0.12 of the time, 
# So we should expect approx. every row to have one high value freq. 
# >= 0.1 is the threshold I used.
# A few values over 0.12 would also be expected.

# Returns a list with every n-th character of s.
# E.g., SplitString("ABCDEF",2) returns ["ace","bdf"].
def SplitString(s,n):
    l = [""]*n
    for i in range(len(s)):
        l[i%n] += s[i]
    return(l)

# Returns a list of the relative frequencies of each character in s.
# E.g., FrequencyTable("ABC") returns [0.33, 0.33, 0.33, 0.0, 0.0, ...]
def FrequencyTable(s):
    l = []
    for i in range(26):
        l.append(round(s.count(chr(i+65))/len(s),2))
    return(l)

# Prints frequency tables for n = 1 to 20
# Prints high-value frequencies (>=0.1) in red
for i in range(1,20):
    print(i)
    l = SplitString(ct,i)
    for j in range(len(l)):
        m = FrequencyTable(l[j])
        
        for k in m:
            if (k >= 0.1):
                cprint(k,'red',end=", ")
            # elif (k >= 0.08):
            #     cprint(k,'green',end=", ")
            else:
                print(k,end=", ")

        print()
         
    # Padding
    print("-----------------------")
    print()

# From here, key length = 8 is quite likely
# It's the only candidate with multiple >0.12 values
# And also has a >=0.1 frequency in every row!
# I'll note that key length = 16 looks possible as well,
# But it is likely just two 8-long keys back to back



### PART 2 - Decoding the text (and finding the key)
# We now have 8 Caesar shifts!
# First we store the key len=8 frequency tables into one big list:

bigtable = []
l = SplitString(ct,8)
for j in range(len(l)):
    m = FrequencyTable(l[j])
    bigtable.append(m)

for i in bigtable:
    print(i)
    
# As a bit of a crude start to get us close,
# We shift so that "E" lands on the highest frequency value in each list
# While possibly wrong, the hope is that at least some will be correct
# We first compute the list of shifts to use,
# which is just finding the index of the maximum in each list.

# Returns the index of the maximum of the list x.
def MaxIndex(x):
    maximum = x[0]
    idx = 0
    for i in range(len(x)):
        if x[i] > maximum:
            idx = i
            maximum = x[i]
    return idx

# And we populate a list with the maximum indices.
# Note that we subtract 4 as to shift E to the highest frequency index, not A.
shifts = []
for i in range(8):
    shifts.append((MaxIndex((bigtable[i]))-4)%26)
print(shifts)

# Now we decode by shifting the relevant characters backwards!

# Returns plaintext string after decoding ciphertext using the shifts
# Prints the plaintext in blocks of key-length, 8 in this case
def Decode(ciphertext,shiftlist):
    ctlist = list(ciphertext)
    for i in range(len(ctlist)):
        ctlist[i] = chr((ord(ctlist[i])-65 - shiftlist[i%len(shiftlist)])%26 + 65)
    pt = ''.join(ctlist)
    for i in range(len(pt)):
        print(pt[i],end='')
        if i%len(shiftlist)== len(shiftlist)-1:
            print(" ",end='') 
    # Spacing
    print()
    print()
    return(pt)

# Print
Decode(ct,shifts)

# From here, we have ALAN as the first word, which is promising
# (Knowing this is cryptography, this might be something about Alan Turing!)
# The first four shifts look good, but the latter four I'm less sure of so far.
# The first observation I see here is the word ENABLE towards the end
# (The 12th block from the end is ENAB----, where the first 4 we have as "confirmed" for now)
# So we adjust the W to be an L by adding 11 to the shift (to subtract 11 in the decoding process).
# The 6th shift looks good to continue with the E in ENABLE.

#Re-decoding with the new shift
shifts[4] += 11
Decode(ct,shifts)      

# At this point, I see TURING near the beginning,
# As long as we adjust the last two shifts we haven't looked at yet.
# Moving I to R and E to I gives:
shifts[6] -= 9
shifts[7] -= 4
plaintext = Decode(ct,shifts)
print(plaintext)

# Finally, let's get the key. We have:
for i in shifts:
    print(chr(i+65),end='')

# And we're done.
# The plaintext is in hw1-pt.txt.
# Snooping around online, it looks to be the beginning of the Wikipedia page for Alan Turing.
# Pretty fitting for this class!