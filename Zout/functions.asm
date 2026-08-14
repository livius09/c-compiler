data:
	myvar: 
	 .byte 	 0
text:
	.add:
	  push rbp
	  mov rbp, rsp
	
	  mov BYTE PTR [rbp-1], edi
	  mov BYTE PTR [rbp-2], esi
	
	  mov rax, BYTE PTR [rbp-1]
	  mov rax, BYTE PTR [rbp-2]
	  add rax, rbx
	
	  pop rbp
	  ret
	mov edi, 0
	mov esi, 4
	call .add
	mov BYTE PTR myvar[rip] , rax
