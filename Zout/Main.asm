data:
	num: 
	 .byte 	 2
	ver: 
	.zero  1
text:
	mov rax, 1
	cmp rax, 0
	sete rax
	mov BYTE PTR ver[rip] , rax
