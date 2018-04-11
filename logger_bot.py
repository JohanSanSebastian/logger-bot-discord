# -*- coding: utf-8 -*-

import discord
import datetime

client = discord.Client()

token = 'INSERT TOKEN HERE' #gotta get a token from discord.com/developers

message_logs = 'FILE NAME HERE' #fill that (example: 'messages.txt')
edit_logs = 'FILE NAME HERE' #fill that
delete_logs = 'FILE NAME HERE' #fill that
#those 3 could all be the same, but it would look messy


@client.event
async def on_ready(): #triggers when bot comes online
    print('-------')
    print('Logged in as:')
    print('username: {}'.format(client.user.name))
    print('ID: {}'.format(client.user.id))
    print('-------\n')

@client.event
async def on_message(message): #triggers every time a message is sent
    
    #save message in file message_logs
    with open(message_logs, 'a') as logs:
        logs.write(message_log_format(message))
        logs.write('\n')
    
@client.event
async def on_message_edit(before, after):
    if before.content == after.content: #guarantees that it doesn't trigger on embeds
        return None
    now = timestamp_now()
    author = before.author
    channel = before.channel
    change = 'EDIT: [{} UTC] in #{}:\nbefore: {}\nafter:  {}\n\n'.format(
              now, channel, message_log_format(before), message_log_format(after)
              )
    with open(edit_logs, 'a') as logs:
        logs.write(change)
        
@client.event
async def on_message_delete(message):
    #the API can't tell who deleted the message. gotta check the in-client logs for that.
    now = timestamp_now()
    change = 'Message deleted [{}]:\n{}\n\n'.format(now, message_log_format(message))
    with open(delete_logs, 'a') as logs:
        logs.write(change)
    
    
    
def message_log_format(message):
    """How the messages are formatted in the logs.
       discord.Message -> str"""
    author = message.author.display_name
    author_id = message.author.id #author id is useful in case the user changes their name.
    channel = message.channel
    timestamp = message.timestamp #a datetime.datetime object
    content = message.content
    f_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return '[%s UTC] %s in #%s: %s (USER_ID: %s)' % (f_timestamp, author, channel, content, author_id)
    
def timestamp_now():
    """Returns string of the current UTC timestamp in year-month-day hour:minute:second format."""
    now = datetime.datetime.utcnow()
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S')
    return now_formatted


    
client.run(token)
