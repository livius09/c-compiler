data:
	myvar: 
	.zero  1
	maria: 
	.zero  16
text:
	mov rax, 10
	mov BYTE PTR maria[rip+1] , rax
	mov rax, 1000
	mov QWORD PTR maria[rip+16] , rax
	mov rax, BYTE PTR maria[rip+1]
	mov BYTE PTR myvar[rip] , rax
