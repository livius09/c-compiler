data:
	flag: 
	.zero  1
	num: 
	 .byte 	 3
	num2: 
	 .byte 	 5
text:
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [num2]
	cmp rax, rbx
	mov BYTE PTR flag[rip] , rax
	mov rax, 1
	mov BYTE PTR flag[rip] , rax
	mov rax, 0
	mov BYTE PTR flag[rip] , rax
	mov rax, 0
	mov BYTE PTR flag[rip] , rax
	mov rax, 1
	mov BYTE PTR flag[rip] , rax
