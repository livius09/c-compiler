data:
	num: 
	.zero  8
	k: 
	 .byte 	 0
text:
	jmp .L0
	.L1:
	mov rax, QWORD PTR [num]
	mov rax, 1
	add rax, rbx
	mov QWORD PTR num[rip] , rax
	.L0
	mov rax, QWORD PTR [num]
	mov rax, 100
	cmp rax, rbx
	jg .L1
	jmp .L2
	.L3
	mov rax, QWORD PTR [num]
	mov rax, 1
	add rax, rbx
	mov QWORD PTR num[rip] , rax
	mov rax, BYTE PTR [k]
	mov rax, 1
	add rax, rbx
	mov BYTE PTR k[rip] , rax
	.L2
	mov rax, BYTE PTR [k]
	mov rax, 5
	cmp rax, rbx
	jg .L3
