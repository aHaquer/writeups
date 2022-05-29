# Level 08- Nebula

```
World readable files strike again. Check what that user was up to, and use it to log into flag08 account.

To do this level, log in as the level08 account with the password level08. Files for this level can be found in /home/flag08.
```

```
sh-4.2$ ls
capture.pcap
```

We can view this [pcap](https://en.wikipedia.org/wiki/Pcap) file with [wireshark](https://www.wireshark.org/).

```
scp -P 22 level08@192.168.56.102:/home/flag08/capture.pcap ./
sudo wireshark capture.pcap
```

To get a better view we can navigate to ```Analyze > Follow > TCP Stream```. This shows us the entire conversation as ASCII.

```
..%..%..&..... ..#..'..$..&..... ..#..'..$.. .....#.....'........... .38400,38400....#.SodaCan:0....'..DISPLAY.SodaCan:0......xterm.........."........!........"..".....b........b....	B.
..............................1.......!.."......"......!..........."........"..".............	..
.....................
Linux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)

..wwwbugs login: l.le.ev.ve.el.l8.8
..
Password: backdoor...00Rm8.ate
.
..
Login incorrect
wwwbugs login: 
```

At first glance I assumed that the flag08 password was ```backdoor...00Rm8.ate``` but this didn't work. The hex for ```.``` is ```7f``` which in decimal is ```127``` which in ASCII is the delete character. This means the password is actually ```backd00Rmate```. Embarrassingly this was the only challenge so far I couldn't solve on my own.

```
sh-4.2$ su flag08
Password: 
sh-4.2$ whoami
flag08
```

