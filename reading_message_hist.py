if cmd == 'scan':

  data = pd.DataFrame(columns=['content', 'time', 'author'])
  
  def is_command (msg): # Checking if the message is a command call
    if len(msg.content) == 0:
        return False
    elif msg.content.split()[0] == '_scan':
        return True
    else:
        return False

  async for msg in message.channel.history(limit=10000): # As an example, I've set the limit to 10000
    if msg.author != client.user:                        # meaning it'll read 10000 messages instead of           
        if not is_command(msg):                          # the default amount of 100        
            data = data.append({'content': msg.content,
                                'time': msg.created_at,
                                'author': msg.author.name}, ignore_index=True)
        if len(data) == limit:
            break
    
   file_location = "data.csv" # Set the string to where you want the file to be saved to
   data.to_csv(file_location)
    
client.run('MTE1MDc2MjQ0ODMwODE1ODQ4NQ.Gu5ndC.Qwl3UobTZ9fBfXNqPX7ovNNLDDe9WDjlo_RUpA')