import numpy as np 
import math
import matplotlib.pyplot as plt
'''
PART A:
Bernoulli distribution: We can generate samples from a bernoulli distribution with parameter p 
by using uniform random variable generator in python by outputting 1 if number generated through
np.random.uniform() is less than parameter p and 0 if greater.
The above argument works because then the probability of generating 1 is (p-0)/1 = p and probability
of generating 0 is (1-p)/1 = 1-p
'''

def Bernoulli(p):
    z = np.random.uniform()
    if(z<=p):
        k = 1
    else:
        k = 0;
    return k

'''
PART B
Binomial distribution:We follow a similar approach in this, except that we need to have n inputs for this.
We shall store those n numbers in a list.
Binomial parameters : n, p
No. of sample : N
'''

def probab(n,r,p):
    x = nCr(n,r) * math.pow(p,r) * math.pow((1-p),n-r)
    return x

def nCr(n,r):
    f = math.factorial
    return (f(n) / (f(r)*f(n-r)))

def Binomial(N,n,p):
    l =[]
    Nl = []
    for i in range(0,N):
        l = []
        suml = 0
        for j in range(0,n):
            m = Bernoulli(p)
            l.append(m)
        suml = sum(l)
        Nl.append(suml)
    return Nl

# Generating random value based on bernoulli distribution
p = input("Enter the bernoulli parameter p:")
k = Bernoulli(p)
print("The random bernoulli value generated using uniform distribution is: " + str(k))

N = input("Enter the no. of samples:")
n = input("Enter the binomial parameter n:")
p = input("Enter the binomial parameter p:")

#Generating N random samples from binomial distribution
binom = Binomial(N,n,p)

# Plotting graph here
plt.figure(1)
al = list(xrange(n+1))
alp = []

for i in range(0,n+1):
    temp = probab(n,i,p)
    alp.append(temp*N)
# Red line indicates the expected probability distribution
plt.plot(al,alp,'r')
# Blue bars represent frequency of values obtained through experiment/sampling
plt.hist(binom,bins=n)
plt.title("Binomial distribution")
plt.xlabel("Values")
plt.ylabel("Frequency")

plt.show()


