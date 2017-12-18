#coding: utf-8
import imaplib
import sys, email
from email.parser import HeaderParser
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

def main():
    args = dict([arg.split('=') for arg in sys.argv[1:]])
    #label = ''
    print("Logging into mailServer with user %s\n" % args['username'])
    server = imaplib.IMAP4_SSL('owa.UGent.be')
    connection_message = server.login(args['username'], args['pw'])
    print(connection_message)

    if args.get('label'):
        print("Using label: %s" % args['label'])
        server.select(args['label'])
    else:
        server.select("Inbox")
        print("Using inbox")

    #args['sender'] = ''
    #for i in server.list()[1]:
    #    l = i.decode().split(' "/" ')
    #    print(l[0] + " = " + l[1])
    #    if(l[1] ):
    #        server.select(l[1])
        mailparser = HeaderParser
        stat, emails = server.search(None, '(FROM "%s")' % args['sender'])
        if (len(emails[0].split())):
            print len(emails[0].split())
            for id in emails[0].split():
                resp, data = server.fetch(id, 'RFC822')
                #print data
                msg = email.message_from_string(data[0][1])
                print (msg['From'], msg['Date'], msg['Subject'])
                server.store(id, '+FLAGS', '(\Deleted)')

        server.expunge()
        server.close()
        server.logout()

    print("Done!")

def sreachInDeleteFld(server):
    stat, msgs=server.select('"Verwijderde items/deleted"', readonly=False)

    if stat == 'OK':

        for i in range(1, 30):
            typ, msg_data = server.fetch(str(i), 'RFC822')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    for header in [ 'subject', 'to', 'from' ]:
                        print '%-8s: %s' % (header.upper(), msg[header])


    return


if __name__ == '__main__':
    main()