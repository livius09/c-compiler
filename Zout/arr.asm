data:
	myarr:
		.byte 	1
		.byte 	2
		.byte 	3
		.byte 	4
		.byte 	5
	myarr2: 
	.zero  5
	myarr3:
		.byte 	12
		.byte 	13
		.byte 	14
text:
	mov rax, BYTE PTR myarr[rip+3]
	mov BYTE PTR myarr2[rip+2] , rax
	mov rax, 12
	mov BYTE PTR myarr2[rip+3] , rax
