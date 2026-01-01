.psp
.open "EBOOT.BIN", 0x08803F60             ;0x8804000 - header (0xA0)



.org 0x08847D08	                                       ;Go to PSP RAM address
addiu a0, zero, 0x01        ; Language ID = 1 (English) Replace instruction there with this new one 


.close
