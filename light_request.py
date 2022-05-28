import discord

def findchar(list, char):
    find = 0
    for i in range(len(list)):
        if list[i-1] == char:
            find=find+1
    return find

def command(string):
    string=string+" "
    tmpstr=string
    tmpstr2=string
    pos=tmpstr.find(" ")
    r=tmpstr[:pos+1]
    args=[r]
    tmpstr=tmpstr[pos+1:]
    for i in range(findchar(string, " ")):
        pos=tmpstr.find(" ")
        r=tmpstr[:tmpstr.find(" ")]
        args.append(" "+r)
        tmpstr=tmpstr[pos+1:]
        rr=i
    args[rr+1]=string[len(string)-1]
    return args

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

    async def on_message(self, message):
        dmessage = command(str(message.content))
        print(dmessage)
        if message.author.id == self.user.id:
            return

        if dmessage[0] == "!free ":
            await message.channel.send("You got a free URL" + dmessage[1])

        if dmessage[0] == "!download ":
            await message.channel.send("You got a free URL" + dmessage[1])

client = MyClient()
client.run('OTE3MzI0MTE2MzUxMTQzOTU2.Ya3CqA.NsqbJA7vYxPbjMHYNp6QTX8bJA4')