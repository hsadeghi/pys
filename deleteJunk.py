#coding: utf-8
import imaplib
import sys

'''
Simple script that delete emails from a given sender
params:
-username: Gmail username
-pw: gmail pw
-label: If you have a label that holds the emails, specify here
-sender: the target sender you want to delete
usage: python delete_emails.py username='giovaneliberato@gmail.com' pw='bla' label='e-commerce' sender='spam@some-ecommerce.com'
see http://stackoverflow.com/a/5366205 for mode details
'''

args = dict([arg.split('=') for arg in sys.argv[1:]])
#label = ''
print("Logging into GMAIL with user %s\n" % args['username'])
server = imaplib.IMAP4_SSL('owa.UGent.be')
connection_message = server.login(args['username'], args['pw'])
print(connection_message)

if args.get('label'):
    print("Using label: %s" % args['label'])
    server.select(args['label'])
else:
    print("Using inbox")
    server.select("Inbox", readonly=False)
#args['sender'] = ''
for fldr in server.list():
    print fldr


for i in server.list()[1]:
    l = i.decode().split(' "/" ')
    print(l[0] + " = " + l[1])
    if(l[1] ):
        server.select(l[1])

        stat, emails = server.search(None, '(FROM "%s")' % args['sender'])
        if (len(emails[0].split())): print len(emails[0].split())


print("Searching emails from %s" % args['sender'])
result_status, email_ids = server.search(None, '(FROM "%s")' % args['sender'])
email_ids = email_ids[0].split()

if len(email_ids) == 0:
    print("No emails found, finishing...")

else:
    print("%d emails found, sending to trash folder..." % len(email_ids))
    #for item in email_ids:
    #    print item
    #server.store('1:*', '+FLAGS', '\\deleted')
    #server.expunge()
server.close()
server.logout()

print("Done!")