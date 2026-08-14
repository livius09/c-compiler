data:
	myvar: 
	.zero  1
text:
	mov rax, 5
	mov BYTE PTR myvar[rip] , rax
