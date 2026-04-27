data:
	var: 
	.zero  1
text:
	mov edi, 0
	mov esi, 2
	call .add
	mov BYTE PTR [var], rax
