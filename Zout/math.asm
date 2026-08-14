data:
	myvar: 
	 .byte 	 10
	myvar2: 
	 .byte 	 5
	tmp: 
	.zero  1
text:
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	add rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	sub rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	imul rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	cqo
	idiv rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	sal rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	sal rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	and rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	or rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, BYTE PTR [myvar]
	mov rax, BYTE PTR [myvar2]
	xor rax, rbx
	mov BYTE PTR tmp[rip] , rax
	mov rax, 15
	mov BYTE PTR tmp[rip] , rax
