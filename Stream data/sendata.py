#simple interface to sent data to google spread sheet
#!/usr/bin/python./
__author__ = 'frank'
import gspread
gc = gspread.login('abs@gmail.com', 'password')
cell =raw_input('SELECIONE CELDA')

wks = gc.open("database").sheet1

val = wks.acell(cell).value

print val
print "Working..."
