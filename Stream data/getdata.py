#!/usr/bin/python
#simple interface to get data from google spread sheet
__author__ = 'frank'
import gspread
gc = gspread.login('abc@gmail.com', 'password')
cell =raw_input()

wks = gc.open("database").sheet1

val = wks.acell(cell).value

print val

