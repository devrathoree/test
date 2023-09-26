def sendMail(email):
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	
	me = "devmicky23@gmail.com"
	you = email

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Password reset Mail Tenders"
	msg['From'] = me
	msg['To'] = you

	html = """<html>
  					<head></head>verify your account
  					<body>
    					<h1>Welcome to Tenders</h1>
    					<p>You have successfully registered your login credentials are attached below , please click on the link below to reset application password</p>
    					<h2>Username : """+email+"""</h2>
    					<br>
    					<a href='http://localhost:8000/resetpass?vemail="""+email+"""' >Click here to reset application password</a>		
  					</body>
				</html>
			"""
	
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login("devmicky23@gmail.com", "qqiiyktgjdutrlij") 
	
	part2 = MIMEText(html, 'html')

	msg.attach(part2)
	
	s.sendmail(me,you, str(msg)) 
	s.quit() 
	print("mail send successfully....")
