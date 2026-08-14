data:
	myvar: 
	 .byte 	 5
	ptr: 
	 .quad 
 0
text:
	mov rax, BYTE PTR [myvar]
	lea rax, BYTE PTR [myvar]
	mov QWORD PTR [ptr], rax
	mov rax, 2
	mov rdx, QWORD PTR [ptr]
	mov BYTE PTR [rdx], rax
	mov rax, QWORD PTR [ptr]
	mov rax, BYTE PTR [rax]
	mov BYTE PTR myvar[rip] , rax
