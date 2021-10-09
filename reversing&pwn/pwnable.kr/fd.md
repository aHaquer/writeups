# Fd - Pwnable.kr

![cover image](../../assets/pwnable.kr/fd/fd.png)

```
Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw

ssh fd@pwnable.kr -p2222 (pw:guest)
```

A [file descriptor](https://en.wikipedia.org/wiki/File_descriptor) is an identifier (a number) for a file **or** input/output source. On the server, we find a ```fd.c```, ```fd```, and ```flag```. Our goal is to read the contents of flag (which is owned by root) using the binary fd provided to us.

fd.c:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
```

This program will give us the flag if we pass it a number that is ```4660``` greater than the descriptor of the file/IO that contains "LETMEWIN\n". 

This assigns the ```fd``` variable to the result of subtracting 4660 (the decimal form of 0x1234) from our first argument.
```c
int fd = atoi( argv[1] ) - 0x1234;
```

This assigns the ```buf``` variable to the first 32 bytes of the file/IO that ```fd``` is pointing to.
```c
int len = 0; len = read(fd, buf, 32);
```

And finally this will cat the flag for us if ```buf``` is equal to ```LETMEWIN\n```.
```c
if(!strcmp("LETMEWIN\n", buf)){
    printf("good job :)\n");
    system("/bin/cat flag");
    exit(0);
}
```

Did you remember that [standard input](https://man7.org/linux/man-pages/man3/stdout.3.html) has its own file descriptor? This means that we can run the program with ```./fd 4660``` and then type "LETMEWIN" in order to solve the challenge.

```bash
fd@pwnable:~$ ./fd 4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```
