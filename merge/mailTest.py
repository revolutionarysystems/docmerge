# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def emailDoc(baseFileName, me, you, subject, credentials):
	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	textfile="output/"+baseFileName+".md"
	fp = open(textfile, 'r')
	text = fp.read()
	fp.close()
	htmlfile="output/"+baseFileName+".html"
	fp = open(htmlfile, 'r')
	html = fp.read()
	fp.close()
	# Create a text/plain message
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = you

	msg.attach(MIMEText(text, 'plain'))
	msg.attach(MIMEText(html, 'html'))

	username = credentials["username"]
	password = credentials["password"]
	server = smtplib.SMTP(credentials["server"])

	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username,password)
	response = server.sendmail(me, [you], msg.as_string())
	server.quit()
	return {"email_result":response}

#credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}
credentials = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}
print(emailDoc("AddParty_test02", "fake@fake.com", "andrew.elliott@revolutionarysystems.co.uk", "Your Tenancy", credentials))
