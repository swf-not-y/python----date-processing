import random,os,time

def fab1(max):
	a,b,c = 0,0,1
	while a < max:
		c = b + c
		b = c
		a+=1
	t1 = time.time()

	t2 = time.time()
	print(f"fab1 total times {t2-t1}")

def fab2(max):
	a,b,c = 0,0,1
	while a < max:
		yield c
		b = c
		c = b + c
	t1 = time.time()
	t2 = time.time()
	print(f"fab1 total times {t2-t1}")

fab1(10000)
fab2(10000)
