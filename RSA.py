import math,random,pdb
from matplotlib import pyplot as plt

def GenB(phi):
    for i in range(1,phi):
        count = random.randint(0,50)
        if(math.gcd(phi,i)==1):
            b=i
            if(count == 50): return b
    return b

#reduce a, b to speed up
def GenA(phi,b):
    for i in range(1,phi):
        count = random.randint(0,50)
        if(((b*i)%phi)==1):
            a=i
            if(count == 50): return a
    return a

def sam(baseint,exponent,mod):
    b = bin(exponent)
    z = 1
    lenb = len(b)
    for i in range(1,lenb):
        z = (z*z)%mod
        if(b[i] == '1'):
            z = (z*baseint)%mod
    return z

#Generate valid RSA keys given two prime numbers
def keyGen(p,q):
    n = p*q
    phi = (p-1) * (q-1)
    b = GenB(phi)
    a = GenA(phi,b)
    return(a,b,n)

def BaseFind(v,m,c):
    return((v-(m*c)))

def Decode(v0,base,charnum):
    char,v = [],[v0]
    for i in range(charnum):
        basecur = (base)**(charnum-1-i)
        char.append(v[i]//basecur)
        v.append(BaseFind(v[i],basecur,char[i]))
    char = [chr(x+97) for x in char]
    return(char)

def OrdFind(c,base,power):
    c = ord(c)-97
    return(c*(base**power))

def Main(n,a,b,cnum,base,arr):
    lena = len(arr)
    print(f"LEN:{lena}\nN:{n}\nA:{a}\nB:{b}")
    for i in range(lena):
        if(i%200000 == 0):
            print(i)
        if((i+1)%cnum==0):
            cur = content[i-(cnum-1):i+1]
            tot = 0
            for i in range(cnum):
                tot += OrdFind(cur[i],26,cnum-1-i)
            plaintot.append(tot)
            ee = sam(tot,keyb,keyn)
            enctot.append(ee)
            dectot.append(sam(ee,a,n))

    return([plaintot,enctot,dectot])

def SummaryStat(arr):
    
    maxx,minn,leng = ord(max(arr)),ord(min(arr)),len(arr)
    summ,ss,ec,cc = 0,0,0,0
    yarr,xarr = [0]*(maxx+1),[0]*(maxx+1)
    #get avg
    for i in range(leng):summ += ord(arr[i])
    for i in range(maxx):xarr[i]+=i

    avgg = summ/leng
    #get entropy and std dev
    for i in range(leng-1):
        yarr[ord(arr[i])] += 1
        ss += abs((ord(arr[i])-(avgg))**2)
        if(ord(arr[i]) > 0):
            cc = ord(arr[i]) / summ
            ec = ec - cc*math.log(cc,2)/math.log(2,2)

    print(f"MAX:{maxx}\nMIN:{minn}\nAVG:{avgg}")
    print(f"VAR:{ss/leng}\nSTD:{math.sqrt(ss/leng)}\nENT:{ec}")
    return([maxx,minn,avgg,(ss/leng),(math.sqrt(ss/leng)),ec,xarr,yarr])

def CheckOutput(arr,base,charnum,name):
    print(name)
    lena,decodearr = len(arr),[]
    for i in range(lena):
        t = Decode(arr[i],base,charnum)
        for ii in range(charnum):
            decodearr.append(t[ii])
    decodearr = ''.join(e for e in decodearr)
    return(decodearr)

def plott(xarr,yarr):
    plt.bar(xarr,yarr,color='blue')
    plt.show()

#Open darwin, set p,q,n,a,b values, find stats, make histogram
f = open("darwinbaseband.txt","r")
content = f.read()
f.close()
clist,enctot,plaintot,dectot = [],[],[],[]
numchar,zspace = 4,26
p,q = 683,677
lenn = 766857
keyn = 462391
##keya = 371243
##keyb = 267
keyb = 9
keya = 256129
x = Main(keyn,keya,keyb,numchar,zspace,content)
checkplain = CheckOutput(x[0],zspace,numchar,"PLAINTEXT")
checkenc = CheckOutput(x[1],zspace,numchar,"ENCRYPTED TEXT")
checkdec = CheckOutput(x[2],zspace,numchar,"DECRYPTED TEXT")
statsplain = SummaryStat(checkplain)
statsenc = SummaryStat(checkenc)
statsdec = SummaryStat(checkdec)

##plott(statsplain[6],statsplain[7])
##plott(statsenc[6],statsenc[7])
##plott(statsdec[6],statsdec[7])

#megans values:
#p = 683
#q = 691
#b = 7

