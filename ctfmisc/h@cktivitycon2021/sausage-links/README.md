# Sausage Links

![cover image](../assets/sausage-links/cover.png)

sausage_links.py:
```python
#!/usr/bin/env python3

from gmpy import *
from Crypto.Util.number import *
import gensafeprime

flag = open("flag.txt", "rb").read().strip()

bits = 512

p = getPrime(bits)
q = getPrime(bits)
r = getPrime(bits)
n = p * q * r
phi = (p - 1) * (q - 1) * (r - 1)

l = min([p, q, r])
d = getPrime(1 << 8)
e = inverse(d, phi)

a = gensafeprime.generate(2 * bits)
while True:
    g = getRandomRange(2, a)
    if pow(g, 2, a) != 1 and pow(g, a // 2, a) != 1:
        break

pubkey = (n, e, a, g)

m = bytes_to_long(flag)
k = getRandomRange(2, a)
K = pow(g, k, a)
c1, c2 = pow(k, e, n), (m * K) % a

print("c =", (c1, c2))
print("pubkey =", pubkey)
```

The name, "Sausage Links," is an allusion to the [Wiener attack](https://en.wikipedia.org/wiki/Wiener%27s_attack). Wiener attacks can expose the private key used in RSA-like cryptosystems when the variable ```d``` (the private key) is too small. This works when ```d < 1/3 * (N ** (1/4))```.

Our ```d``` is less than ```2^256``` (it's only [allowed](https://www.kite.com/python/docs/Crypto.Util.number.getPrime) 256 bits), which is too  to be secure.
```python
d = getPrime(1 << 8) # 1 << 8 evaluates to 256
```
I found a [writeup](https://masterpessimistaa.wordpress.com/2017/11/24/asis-finals-ctf-2017-gracias-writeup/) online which details how to find ```d``` in this scenario. This is only part of the puzzle, but it's a good start to our solution.

```python
# known variables
n = 549935778300831378406948873536278349781214706503360745280597408861216877781142622004454148443526758471040653633080987617044763942008023466559253761306561736450658314626615456982873023501736081710037081947666247132668118860186965548713647775109193997705890766881191577188287773692953347103686449329398217311195051172403636510262250822460785125486925931569891688688353900466632582649417645956790937903144901696446727579207702041958066277574559994377445136251040659
e = 32204951698260962458157592984992469529416584332675382497988021285424821386904232277036373403101864193040613563796784569698857185940927175841205145358641690922026788366581684507467056308764343250379771013177468030580725648480591696059317745554974780583562695962973324819593002957827750301174079447431501960032717699255546396631743680242345092881301693065171460311485778344053788138555054294470951574964376432654831106364396876336137419860163278539415409181597819
a = 138573907982913094895957560613895338045899660024192238553307135243826517727787057358804422211354202143617168828075979083404334708411832425604299257351876162289412352723963051979157876631398717413563591084855571688469543441655488090919934371369975426760135367341463974144518915155974937301498827086824773106003
g = 68759670662427533761108453255036749386266492702870615501799248175187816213782210092795089989860635666887242761904219513870052421033161791299816761321508643099537034976789844586576430337882832633194279669183386905734135409454252901918801636934986951843672112043695989089719222626801371853255674748960081747148
c1 = 75393472403093883980765814047645327405215775478712827591109646890837780762923959326166827649826238535312344488349557712816610930220370001305827412505043127914547998320440240250325118053813714466854788644697706490515892504619105361332594358021214992759872975638137819189634434255388142452402903984216170592454070190763219802978580474823882279160692450914521162374808790341598702288608920814072249086450656427949215063564752988546802554974565217418056403485189158
c2 = 21743667484649294456505545386313391146296096106309721435244191430622536536241638911796782012089471615188229556482084132221324157541121095745921331613424302593658426094356838716843005440373679746518683613229280959080885966038959064524609397524131981550731325678855657987757274636339648236504515056989339931829

# find d, wiener attack
from sage.all import continued_fraction, Integer
def wiener(e, n):
    m = 12345
    c = pow(m, e, n)

    list1 = continued_fraction(Integer(e)/Integer(n))
    conv = list1.convergents()
    for i in conv:
        d = int(i.denominator())
        m1 = pow(c, d, n)
        if m1 == m:
            return d

d = wiener(e, n)
```

A seperate problem is finding what ```k``` and ```K``` were, since they were used in the creation of ```c1``` and ```c2``` (the cipher texts). Here's how they were generated:
```python
k = getRandomRange(2, a)
K = pow(g, k, a)
c1, c2 = pow(k, e, n), (m * K) % a
```
Since ```c1```, ```d```, and ```n``` are known, we can now find ```k```. Using ```k```, we can now find ```K``` (since ```g``` and ```a``` are known). 
```python
k = pow(c1, d, n)
K = pow(g, k, a)
```
We then need to find the [multiplicative inverse](https://masterpessimistaa.wordpress.com/2017/11/24/asis-finals-ctf-2017-gracias-writeup/) of K
```python
Kinv = pow(K,-1,a)
```
because of the relationship between c2 and m (m is the number that would be represented by the bytes which are being used to represent the flag, text).
```python
m = bytes_to_long(flag)
c1, c2 = pow(k, e, n), (m * K) % a
```

We can now derive our flag using the multiplicative inverse of ```K```, and the other known variables.
```python
flag = (Kinv * c2) % a
flag = flag.to_bytes(400, byteorder='big')
print(str(flag))
```

The flag is ```flag{8e66cb103c88b9306f9766f8d08c4242}```