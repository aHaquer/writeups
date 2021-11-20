# Random - Pwnable.kr

![cover image](../../assets/pwnable.kr/random/random.png)

```
Daddy, teach me how to use random value in programming!
```

random.c:
```c
#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();        // random value!

        unsigned int key=0;
        scanf("%d", &key);

        if( (key ^ random) == 0xdeadbeef ){
                printf("Good!\n");
                system("/bin/cat flag");
                return 0;
        }

        printf("Wrong, maybe you should try 2^32 cases.\n");
        return 0;
}
```

The aim of this challenge is to find a value which when XOR'd with a 'random' value equals 3735928559 (0xdeadbeef). We need to abuse some predictability of the [rand()](https://devdocs.io/c/numeric/random/rand) function.

According to the docs, [rand()](https://devdocs.io/c/numeric/random/rand) generates a random number between 0 and [RAND_MAX](https://devdocs.io/c/numeric/random/rand_max). After testing on my own system, and since we know that the random value is not seeded, we can assume that the variable ```random``` equals ```1804289383```.

Putting this together, we know an input and the output. Because of the way XOR works:
```
output     ^ input1     == input2
3735928559 ^ 1804289383 == 3039230856
```

So, the key is ```3039230856```.
```
random@pwnable:~$ ./random
3039230856
Good!
Mommy, I thought libc random is unpredictable...
```