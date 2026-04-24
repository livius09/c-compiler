data:
text:
	.add:
	push rbp
	mov rbp, rsp
	
	mov BYTE PTR [rbp-1], edi
	mov BYTE PTR [rbp-2], esi
	mov rax, BYTE PTR [rbp-1]
	push rax
	mov rax, BYTE PTR [rbp-2]
	pop rbx
	add rax, rbx
	
	pop rbp
	ret
