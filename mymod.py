import requests
import json
from datetime import datetime, timedelta
from credentials.py import MAIN_URL 



#start 
main_url = MAIN_URL
ban_url = main_url + 'students/'
check_url = main_url + 'availablegsr/'
booking_url = main_url + 'booking/'
current_url = main_url + 'currentbookings/'
cancel_url = main_url + 'cancelbooking/'
slot_url = main_url + 'slot/'
#end 

#draft
def cancel_booking(cancellation):
	payload = cancellation
	r = requests.put(cancel_url, json=payload)
	return (r.text)


def check_current(querybookingref):
	payload = querybookingref
	r = requests.get(current_url, params=payload)
	bk = json.loads(r.text)
	ls = []
	for i in bk:
		ls.append(str(i['bookingref']))
	print(ls)
	return (ls)


# x = {'chatid' : 281997556}
# check_current(x)

def check_main(querybookingref):
	payload = querybookingref
	print (querybookingref)
	r = requests.get(current_url, params=payload)
	# print (r.text) 
	# print (type(r.text))
	bk = json.loads(r.text)
	print(bk)
	print(type(bk))
	# print (bk)
	# print (type(bk))
	ls = []
	for i in bk:
		print (i)
		ls.append(str(i['bookingref']))
	
	print(ls)
	ref ='^(' +('|'.join(ls)) + ')$'
	print (ref)
	print (type(ref))
	return (ref)




# x = {'chatid' : 281997556}
# check_current2(x)


def current_bookings(querybookingref): # to display to user in form of text 
	payload = querybookingref
	r = requests.get(current_url, params=payload)
	print (r.text)
	return (r.text)




def check_user(details):
	json = details
	r = requests.get(ban_url , params=json)
	return r.text 

def banneduser(banned):
	json = banned
	r = requests.get(ban_url , params=json)
	print (r.text) 
	# print (r.json)
	return (r.text)


def availbooking(temp):
	json = temp
	r = requests.get(check_url , params = json)
	print (r.text)
	return r.text



def gsr_booking(booking):
	bk = booking
	r = requests.post(booking_url , json= bk)
	print (r.text) 
	return r.text




#end 
def gsr_function(booking): #for main - GSR 
	# payload = {'id':curr_id}
	ls = []
	temp = booking 
	r = requests.get(check_url, params = temp)
	s = r.text
	gsr = json.loads(s)
	# print (gsr) 

	for i in gsr: 
		ls.append(i)
	print (ls)
	return (ls)


def all_slot():
	r = requests.get(slot_url)
	print (r.text)
	s = json.loads(r.text)
	print (s)
	print (type(s))

	header = "{0:<7} {1}".format("SlotNo", "Timing")
	slot_string = "```\n" + header + "\n"
	for k, v in s.items():
		slot_string = slot_string + "{0:<7} {1}".format(k, v) + "\n"
	slot_string = slot_string + "```"
	print (slot_string)
	return (slot_string)
	
# all_slot()

def gsr_slot(booking): #for main - GSR 
	# payload = {'id':curr_id}
	
	temp = booking 
	r = requests.get(check_url, params = temp)
	s = r.text
	gsr = json.loads(s)

	string = ""
	for k,v in gsr.items():
		gsr_no = str(k)
		slots = str(v)
		new_string = gsr_no + ": " + slots + "\n" + "\n"
		string = string + new_string

	return (string)

def check_slot(a): #for main - GSR 
	# payload = {'id':curr_id}
	
	temp = a
	r = requests.get(check_url, params = temp)
	s = r.text
	gsr = json.loads(s)

	return (gsr)



def gsr_main(booking): #for function - GSR
	# payload = {'id':curr_id}
	ls = []
	t = booking 
	r = requests.get(check_url, params = t)
	gsr = json.loads(r.text)
	for i in gsr: 
		ls.append(i)
	temp ='^(' +('|'.join(ls)) + ')$' 
	return (temp)



def current_date_func():

	current_date = datetime.today()
	temp = []
	for i in range(0,10):
		new_d = current_date + timedelta(i)
		temp.append(new_d)

	change_format = []
	for i in temp:
		change_format.append(i.strftime('%Y-%m-%d')) # for the keyboard 
	return (change_format)	
# 	print (change_format)	
# 	print (type(change_format))
# 	print (int(len(change_format)/2))
# 	print (type(len(change_format)/2))

# current_date_func()


def curent_date_main():
	
	current_date = datetime.today()
	temp = []
	for i in range(0,10):
		new_d = current_date + timedelta(i)
		temp.append(new_d)


	change_format = []
	for i in temp:
		change_format.append(i.strftime('%Y-%m-%d')) # for the keyboard 
	
	date_main ='^(' +('|'.join(change_format)) + ')$' # for the main function 

	return (date_main)



def check_list(text):
	try:
		l = [int(s) for s in text.split(',')]
		if len(l) > 6:
			print (False)
			return False 
		else:
			if sorted(l) == list(range(min(l), max(l)+1)):
				final = (sorted(l))
				a = len(final)
				if final[0] > 0 and final[a-1] < 18:
					s = ','.join(map(str, final))
					print (s)
					return (s)
				else:
					print (False)
					return False 
			else:
				print (False)
				return False

	except:
		print (False)
		return False 
