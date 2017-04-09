# Tetrominos

Michael Lane  
lane7@pdx.edu  
CS542 - Advanced AI  
Homework 1  

This program uses Python 3, numpy, and scipy. If you are unsure which version
of python you are using on your linuxlab account, run the following command:

```
$ python3 -V
Python 3.5.1 :: Anaconda 4.0.0 (64-bit)
```

If you do not have Python 3.5.1 :: Anaconda 4.0.0 installed on your system, run

```
addpkg
```

Arrow down the list until you find the Python 3.5 (Anaconda release) option.
Make sure this is selected and click OK to install it locally. 

Alternately, you can install Python3 locally yourself. This has been tested on
Python versions 3.5.1 and 3.6.0. You will also need to ensure that numpy and
scipy are installed. To install these locally run the following command:


```
$ pip3 install --user numpy scipy
```

Once these libraries are installed, you can run my homework as follows. First
cd into the Tetronimos directory and then run it with redirected stdin as 
follows:

```
$ python3 tetronimos.py < input-file.txt
```