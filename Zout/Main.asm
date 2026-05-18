data:
	num: 
	 .byte 	 2
	ver: 
	.zero  1
	ptr: 
	 .quad 
 0
text:
	mov rax, 1
	cmp rax, 0
	sete rax
	mov BYTE PTR [ver], rax
	mov rax, BYTE PTR [num]
	mov rax, BYTE PTR [ver]
	add rax, rbx
	mov BYTE PTR [num], rax
	mov rax, BYTE PTR [ver]
	mov rax, 1
	add rax, rbx
	mov BYTE PTR [num], rax
	mov rax, BYTE PTR [ver]
	lea rax, BYTE PTR [ver]
	mov QWORD PTR [ptr], rax
	mov rax, QWORD PTR [ptr]
	mov rax, BYTE PTR [rax]
	mov BYTE PTR [ver], rax
