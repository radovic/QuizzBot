from discord.ext import commands
import discord
import grader
import asyncio
import linecache
import os

''' Bot initialization '''
bot = commands.Bot(command_prefix='!')
TOKEN = linecache.getline("configuration.txt", 2)  # token bota
quizzmasterID = linecache.getline("configuration.txt", 1)  # ID quizzmastera
no_submission = 1
curr_game = -1
team_has_submitted = list()

# Check if bot has logged in
@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))

# The command that allows competitors to submit their answer
@bot.command()
async def submit(ctx):
    team_name = ctx.channel.name
    if team_name in team_has_submitted:
        ctx.send("Your team has already submitted. Please wait til the end!")
        return
    if curr_game == -1:
        await ctx.send("At the moment nothing is being played!")
        return
    document = 0
    try:
        document = ctx.message.attachments[0]
    except:
        ctx.send("You have to attach your answers to submit!")
    global no_submission
    name = "submission" + str(no_submission) + ".txt"
    await document.save(name)
    print("Submission number " + str(no_submission))
    configuration_line = linecache.getline("configuration.txt", curr_game + 2)
    configuration_line = configuration_line.split()
    game_type = int(configuration_line[0])
    answer_file = configuration_line[1]
    team_has_submitted.append(team_name)
    message = ""
    if game_type == 1:
        message = grader.the_questions_game(name, answer_file)
    elif game_type == 2:
        message = grader.the_number_game(name, answer_file)
    elif game_type == 3:
        message = grader.the_word_game(name, answer_file)
    message = "The team " + team_name + " has the following result:\n" + message
    await ctx.send(message)
    quizzmaster = bot.get_user(int(quizzmasterID))
    await quizzmaster.send(message, file=discord.File(name))
    no_submission = no_submission + 1
    os.remove(name)

@bot.command()
@commands.has_role('ADMIN')
async def stop(ctx):
    global curr_game
    team_has_submitted.clear()
    curr_game = -1
    await ctx.send("The game has been stopped!")

@bot.command()
@commands.has_role('ADMIN')
async def start(ctx, *args):
    if len(args) != 2:
        await ctx.send("You didn't give enough informations. Try: !start (number of game) (time in seconds)")
        return
    starter = str(ctx.message.author)
    starter = starter[:-5]
    game_number = int(args[0])
    configuration_line = linecache.getline("configuration.txt", game_number + 2)
    if len(configuration_line.split()) != 2:
        await ctx.send("The game hasn't been defined.")
        return
    time = args[1]
    global curr_game
    curr_game = game_number
    await ctx.send("Quizzmaster " + starter + " has started the game number " + str(game_number)
                   + ". You have " + str(time) + " seconds until the end. Good luck!")
    if int(time) > 30:
        await asyncio.sleep(int(time)-30)
        if curr_game != -1:
            await ctx.send("HALF OF MINUTE TIL THE END!")
        else:
            return
        await asyncio.sleep(30)
    else:
        await asyncio.sleep(int(time))
    if curr_game != -1:
        team_has_submitted.clear()
        await ctx.send("The time has finished!")
        curr_game = -1


@bot.command()
@commands.has_role('ADMIN')
async def leave(ctx):
    print("I'm leaving the server successfully")
    exit()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You don't have permission to use the command.")

bot.run(TOKEN)
