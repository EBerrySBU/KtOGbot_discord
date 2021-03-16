# KtOG Discord Bot
# An implementation of KtOG for Discord
# http://ktog.in8sworld.net/Rules.html

import discord #include the discord API
from discord.ext import commands

from dialog_pools import * # include pools - change this line if using a replacement file

import random # for dice rolls
import operator # for simple sorting by class attribute

# GLOBAL VARIABLES
# define game parameters - change these values if you want to change
# the difficulty/length of a game
HIT_POINTS = 25 # how many hit points each character starts with
ARMOR_CLASS = 14 # minimum value rolled to hit another player
CRITICAL_MISS_EVAL = 17 # minimum value rolled to see if injured/disarmed after a critical miss
DISARM_THRESHOLD = 17 # minimum value rolled to disarm an opponent
NUM_SPELLS = 1 # number of times dodge, mighty blow, cure, bless, and heal can be used
NUM_HASTES = 2 # number of times haste can be used
MIN_HEAL = 2 # minimum number of HP healed by Heal or Cure
MAX_HEAL = 10 # maximum number of HP healed by Heal or Cure
MAX_PRONE = 2 # maximum number of rounds prone
MAX_DISARMED = 2 # maximum number of rounds disarmed
currentPlayer = 0 # variable to keep track of initiaitive, max = number of players - 1
playerList = [] # list of players in initiative order
game_on = False # whether or not a game is active

# Player Class Definition
class Player:
    # each player is associated w/ following data points:

    def __init__(self, username, init): # create constructor, use with newPlayer = Player("username", initiative)
        self.usr = username # username string, set on join
        self.initiative = init # initiative roll d20, higher numbers first, set on join

   # initialized the same for all players
    hp = HIT_POINTS # Initial hitpoints
    disarmed = 0 # set to 1 when first disarmed; inc each round >= 1 until 3, then reset to 0
    roundsAtZero = 0 # set to 1 when hp <= 0 for first time, inc each round >= 1 until 3, then remove player
    blessed = False # set true when Bless is cast, remove once used by attack
    numHastes = NUM_HASTES # number of times a player can cast haste
    numCures = NUM_SPELLS # number of times a player can cast cure
    numBlessings = NUM_SPELLS # number of times a player can cast Bless
    numMightyBlows = NUM_SPELLS # number of times a player can cast mighty blow
    numHeals = NUM_SPELLS # number of times a player can heal another player
    numDodges = NUM_SPELLS # number of times a player can cast Dodge
# end of Player class


# Helper Function Definitions

# roll an integer number between min & max inclusive
def roll(min : int, max : int):
    return random.randint(min, max)
#end of roll function

# turn change function
def turnChange():
    global currentPlayer # use global variable

    killedPlayers = [] # list of players killed by sitting at 0 HP or less for two whole rounds

    f = (playerList[currentPlayer]).usr + '\'s turn has ended. It is now '
    currentPlayer += 1 # inc currentPlayer progress thru vector

    if (currentPlayer >= (len(playerList))): # if vector index rolls over
        currentPlayer = 0 # roll around to start of list
        f += (playerList[currentPlayer]).usr + '\'s turn.'
        f += "\n\nAnother round of combat has ended.\n"

        for p in playerList:
            f += p.usr + ' currently has ' + str(p.hp) + ' hit points. ' + '\n'
            if (p.hp <= 0): # inc rounds@0 for any player w/ hp <= 0
                p.roundsAtZero += 1
                if (p.roundsAtZero >= MAX_PRONE):
                    killedPlayers.append(p.usr) # add player name to list
                    playerList.remove(p)  # kick players w/ hp <= 0 for 2 rounds

            if (p.disarmed > 0):  # inc / reset disarmed for disarmed players
                p.disarmed += 1
                if (p.disarmed > MAX_DISARMED):
                    p.disarmed = 0
                    f += '\n' + p.usr + ' is no longer disarmed.'

        if (len(killedPlayers) == 0): # if kick list empty
            f += "\nNo players died from their wounds this round."

        else:
            f += "The following fighters have succumbed to their wounds and died:"
            for k in killedPlayers:
                f+= "\n" + str(k)
            f += "\nThey have been removed from the initiative."
    else:
        f += (playerList[currentPlayer]).usr + '\'s turn.'

    if (len(playerList) == 1):
        f += "\nTHE FIGHT HAS ENDED! " + (playerList[0]).usr + ' CLAIMS VICTORY!'
        endgame()

    return f
# end of turnchange function

# function to clear player list/end game
def endgame():
    global game_on
    game_on = False
    playerList.clear()
    return
# end of endgame function

# TODO: implement grabline function & create pools
# grab a random line from a specified pool to print
def grabline(pool : str):
    try:
        x = roll(0, len(globals()[pool]) - 1) # get an index from the pool
        return (globals()[pool])[x] # return randomly selected str
    except:
        return "Pool Missing" # return error if pool missing
# end of grabline function

# BOT ITSELF: start of bot commands and code
description = 'A KtOG client bot'
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='.',description=description, intents=intents) # initialize bot w/ command prefix .
# a '.' is used so this bot is easy to use on mobile discord

@bot.event # register event
async def on_ready(): # once bot is logged in & set up
    print('We have logged in as {0.user}'.format(bot))  # print login confirmation
    # note: this prints to the console, not to a discord channel


# META COMMANDS
@bot.command(help = 'A quick intro to this game')
async def howto(ctx):
    await ctx.send('KoTG: Kill the Other Guy\n'
                   + '\nIn this game, the goal is to be the last one standing.'
                   + '\nYou have access to several attacks and spells:'
                   + '\nAttacks: attack, disarm, punch'
                   + '\nSpells: bless, cure, haste, heal; dodge, mighty blow'
                   + '\nDodge can only be cast in reaction to an attack.'
                   + '\nMighty Blow can only be cast before rolling damage for an attack.'
                   + '\nType \".help <command>\" for more information on your attacks and spells.'
                   + '\nThere are also several metacommands: join, start, and leave are for starting or quitting a game.'
                   + '\nMore metacommands: skip, fighters, turn, and status are helpful during gameplay.'
                   + '\nAgain, use help for more information.'
                   + '\nTo start a game, get at least two people to join by typing \".join\" or \".j\"'
                   + '\nOnce you\'re all ready, type \".start\" to begin the game.'
                   + '\nFor the history of this game, visit http://ktog.in8sworld.net/\n')
#end of howto command

@bot.command(help = 'Join the next game', aliases =['j'])
async def join(ctx):
    global game_on
    new_player = ctx.message.author.mention # get new player mention name

    if (game_on == True):
        await ctx.send(new_player + ', there is already a game in progress. You may join when this game is over.')
        return

    inList = False
    for p in playerList:
        if (p.usr == new_player):
            inList = True

    if (inList == False):
        initroll = roll(1, 20); # roll initiative
        playerList.append(Player(new_player, initroll))  # add to player list
        await ctx.send(new_player + ' has joined the game!') # print confirmation message
    else:
        await ctx.send(new_player + ', you have already joined the game.')
# end of join command

@bot.command(help = 'Start the game if 2 or more players have joined')
async def start(ctx):
    global game_on
    global MAX_PRONE

    if (len(playerList) < 2): # check that playerlist >= 2
        await ctx.send('There are not enough players to start a game right now.')  # print error message - wait for more players to join
    else:
        playerList.sort(key = operator.attrgetter('initiative'), reverse=True) # sort playerlist by initiative
        await ctx.send('Let the games begin!')  # print confirmation message
        # set number of rounds prone before death according to # of players
        if (len(playerList) == 2):
            MAX_PRONE = 0
        elif (len(playerList) == 3):
            MAX_PRONE = 1
        else :
            MAX_PRONE = 2
        game_on = True # start the game
        await ctx.send('This time, fighters will survive for ' + str(MAX_PRONE) + ' rounds after they are knocked unconscious.')
        await ctx.send('It is now ' + playerList[currentPlayer].usr + '\'s turn')  # print confirmation message
# end of start command

@bot.command(help = 'Leave a game that you have joined')
async def leave(ctx):
    global game_on # tell it to use the global variable

    quitter = ctx.message.author.mention  # get new player mention name
    for p in playerList: # search list for quitter
        if p.usr == quitter: # if found
            playerList.remove(p) # remove player from list

    if (game_on == True & len(playerList) == 1): # check win condition if game is running (if only 1 player remains, they win)
        await ctx.send(quitter + ' yields, and so ' + playerList[0].usr + ' is victorious!')
        endgame() # clear player list & turn off game
    else: # otherwise, print standard leaving msg
        await ctx.send(quitter + ' has elected not to fight.')
# end of leave command

@bot.command(help = 'See whose turn it is', aliases =['t'])
async def turn(ctx):
    global game_on
    if (game_on == True):
        await ctx.send('It is ' + playerList[currentPlayer].usr + '\'s turn.')
    else:
        await ctx.send('Nobody is playing right now.')
#end of turn command

@bot.command(help = 'Lists the people participating in this fight', aliases =['f'])
async def fighters(ctx):

    if len(playerList) < 1: # if list of players is empty
        f = 'No one is yet willing to fight.'

    else: # if at least one person has joined
        f = 'The following people are participating in this fight, in order of initiative:\n'
        for p in playerList:
            f += p.usr + ' ('+ str(p.hp) + ' hp)\n' # add their username to the printed string

    await ctx.send(f) # send the message/list
# end of fighters command

@bot.command(help = 'Display current status values for yourself or an opponent', aliases =['s'])
async def status(ctx, target = ""):


    if (len(ctx.message.mentions) > 0):
        target = ctx.message.mentions[0].mention; # target is message subject
    else:
        target = ctx.message.author.mention # target is message author

    target_pos = -1 # -1 -> not in list

    for i, p in enumerate(playerList):
        if (p.usr == (target)): # if target found in list
            target_pos = i # save position

    if (target_pos < 0):
        await ctx.send(target + ' is not participating, so there is no status to display.')

    else:
        f = 'Current status of ' + target
        f += '\nHP: ' + str((playerList[target_pos]).hp)
        f += '\nRounds Disarmed: ' + str((playerList[target_pos]).disarmed)
        f += '\nRounds Prone: ' + str((playerList[target_pos]).roundsAtZero)
        f += '\nBlessed: '
        if (playerList[target_pos]).blessed == True:
            f += 'true'
        else:
            f += 'false'
        f += '\nHaste: ' + str((playerList[target_pos]).numHastes)
        f += '\nCure: ' + str((playerList[target_pos]).numCures)
        f += '\nHeal: ' + str((playerList[target_pos]).numHeals)
        f += '\nBless: ' + str((playerList[target_pos]).numBlessings)
        f += '\nMighty Blow: ' + str((playerList[target_pos]).numMightyBlows)
        f += '\nDodge: ' + str((playerList[target_pos]).numDodges)
        f += '\nInitiative: ' + str((playerList[target_pos]).initiative)

        if (game_on == True) & (target_pos == currentPlayer):
            f+= '\nIt is currently ' + target + '\'s turn.'

        await ctx.send(f)
        return
# end of status


# ACTION COMMANDS

# TODO: switch to using grabline
@bot.command(help = 'Perform a simple weapon attack against another player', aliases =['a'])
async def attack(ctx, target = "", passed = 0):
    global game_on
    if (game_on == False):
        await ctx.send('You must start a game before you can take action!')
        return

    attacker = ctx.message.author.mention  # get attacker's username
    if  (len(ctx.message.mentions) > 0):
        if ((target !=  ctx.message.mentions[0].mention) & (len(ctx.message.mentions) > 1) & (target != "")):
            target = ctx.message.mentions[1].mention  # get target's username
        else:
            target = ctx.message.mentions[0].mention # get target's username
    else:
        await ctx.send(grabline('SA_TM')) # target missing
        return

    if ((playerList[currentPlayer].usr) == (attacker)):   # check initiative to make sure it is the attacker's turn
       if (playerList[currentPlayer].roundsAtZero > 0):
           await ctx.send(attacker + ' is prone and must be healed within ' + str(MAX_PRONE - playerList[currentPlayer].roundsAtZero) + ' rounds to survive. You cannot attack right now.')
           return
       else:
        target_index = -1;
        canattack = 1  # flag for validity of attack

        # 0: can't attack - HP too low
        # 1: can't attack - player not in game
        # 2: can attack

        # check that target is in game & hp > 0 (player removed from vector when hp <= 0 for 2 rounds)
        for i, p in enumerate(playerList):
            if ((p.usr) == (target)):
                target_index = i;  # save index
                if (p.hp > 0):
                    canattack = 2 # the attacker can attack
                else:
                    canattack = 0; # hp too low to allow attack

        # if target not in game, reject command
        if (target_index < 0):
            await ctx.send(grabline('SA_TDE')) # target not participating
            return
        if (canattack == 0):
            await ctx.send(grabline('SA_PR')) # target prone, reject attack attempt
            return
        elif (canattack == 1):
            await ctx.send(grabline('SA_TDE')) # target not participating
            return
        else:
            if (playerList[currentPlayer].disarmed > 0): # if attacker is disarmed
                await ctx.send(grabline('SA_DIS'))
                return
            else: # if not disarmed
                hit_roll = roll(1, 20) # else roll to hit

                if (hit_roll == 20):
                    await ctx.send(attacker + ' has rolled a natural 20! They will roll 2d6 for damage.')

                if (hit_roll == 1): # CRITICAL MISS! This attack has backfired
                    await ctx.send('Oh no! ' + attacker + ' rolled a critical miss! Now they will roll to see if they survive their own attack...')
                    self_hit = roll(1, 20)  # roll to see if attacker hit themself
                    if (self_hit >= CRITICAL_MISS_EVAL): # they did
                        self_damage = roll(1, 6) # roll damage die
                        playerList[currentPlayer].hp -= self_damage # evaluate damage
                        await ctx.send(attacker + ' rolled ' + str(self_hit) + ' - they tried to strike but failed miserably, causing ' + str(self_damage) + ' points of damage to themself!')
                        if (playerList[currentPlayer].hp <= 0):
                            playerList[currentPlayer].roundsAtZero = 1
                            await ctx.send(attacker + '\'s health is now at ' + playerList[currentPlayer].hp +
                                     ' and they will die from their wounds in two rounds unless they are healed!')
                            return
                    else: # the attacker did not hit themself but must check to see if they are disarmed
                        await ctx.send(attacker + ' survived their attack attempt by rolling ' + str(self_hit) + ' but will they drop their weapon?')
                        self_disarm = roll(1, 20) # roll to see if weapon is dropped
                        if (self_disarm >= CRITICAL_MISS_EVAL): # they drop their weapon
                            playerList[currentPlayer].disarmed = 1;
                            await ctx.send(attacker + ' has avoided hurting themself, but dropped their weapon in the process!' \
                                                ' It will take two rounds to get it back unless they cast Haste on their next turn.')
                        else:
                            await ctx.send(grabline('SA_CMSA')) # grab critical miss safe line
                    if (passed == 0):
                        await ctx.send(turnChange())  # end attacker's turn
                    return

                else: # if not 1
                    if (hit_roll != 20):
                        await ctx.send(attacker + ' rolled ' + str(hit_roll) + ' to hit.')

                    total_hit_roll = hit_roll
                    if (playerList[currentPlayer].blessed == True):  # check attacker Bless status, if active +2 to roll
                        total_hit_roll += 2;
                        await ctx.send(attacker + ' is recieving divine assistance!')
                        playerList[currentPlayer].blessed = False # remove blessing
                    if (playerList[i].disarmed > 0):   # check target disarm status, if active +2 to roll
                        total_hit_roll += 2;
                        await ctx.send('Since ' + target + 'is disarmed, ' + attacker + ' gets a bonus to their roll!')

                    if (total_hit_roll != hit_roll):
                        await ctx.send('With bonuses, the total roll is ' + str(total_hit_roll) + '!')

                    if (total_hit_roll < ARMOR_CLASS): # total roll below armor class value
                        await ctx.send(grabline('SA_FAIL')) # FIRST USE OF GRABLINE


                    else: # total roll above armor class value
                        # if target has NUM_DODGES > 0 offer target dodge
                        if (playerList[target_index].numDodges > 0):
                            await ctx.send(target + ', would you like to dodge?')  # wait for response from target
                            msg = await bot.wait_for("message", check=lambda
                                message: message.author.mention == target and message.channel.id == ctx.channel.id
                                         and message.content.lower() in ("y", "yes", "n", "no"))
                            if msg.content.lower() in ("y", "yes"):
                                await ctx.send(target + ' has dodged the attack!')
                                playerList[target_index].numDodges =  playerList[target_index].numDodges - 1;
                                if (passed == 0):
                                    await ctx.send(turnChange())
                                return
                            elif msg.content.lower() in ("n", "no"):
                                await ctx.send("You have chosen not to dodge.")


                        MB = False
                        # no dodge - offer attacker mighty blow
                        if (playerList[currentPlayer].numMightyBlows >= 1):
                            await ctx.send(attacker + ', would you like to cast Mighty Blow?')  # wait for response from target
                            msg = await bot.wait_for("message", check=lambda message: message.author.mention == attacker
                                        and message.channel.id == ctx.channel.id  and message.content.lower() in ("y", "yes", "n", "no"))
                            if msg.content.lower() in ("y", "yes"):
                                await ctx.send(attacker + ' cast Mighty Blow! The damage from this attack will be doubled!')
                                playerList[currentPlayer].numMightyBlows = playerList[currentPlayer].numMightyBlows - 1;
                                MB = True
                            elif msg.content.lower() in ("n", "no"):
                                await ctx.send("You have chosen not to cast Mighty Blow.")

                        if (hit_roll == 20):
                            damage_roll = roll(2, 12)
                        else:
                            damage_roll = roll(1, 6)  # roll 2d6
                        if (MB == True):
                            damage_roll *= 2  # Mighty Blow cast -> double damage

                        # do damage
                        await ctx.send(grabline('SA_SUCCESS')) # Send attack success message
                        playerList[target_index].hp -= damage_roll  # evaluate damage
                        await ctx.send(attacker + '\'s attack did ' + str(damage_roll) +
                                       ' points of damage, and ' + target + ' is now at ' +
                                       str(playerList[target_index].hp) + ' hit points!')
                        if (playerList[target_index].hp <= 0):
                            (playerList[target_index].roundsAtZero) = 1
                            await ctx.send(target + '\'s health is now at ' + str(playerList[target_index].hp) +
                                ' and they will die from their wounds in two rounds unless they are healed!')

        if (passed == 0):
           await ctx.send(turnChange()) # if not 1st pass from haste, change turns

       return # return no matter what passed is

    else:
        await ctx.send(attacker + grabline('NYT')) # not your turn
        return
# end of attack command

@bot.command(help = 'Attempt to disarm another player', aliases =['d'])
async def disarm(ctx, target=""):
    global game_on
    if (game_on == False):
        await ctx.send(grabline('GNS_A')) # game not started yet
        return
    attacker = ctx.message.author.mention  # get attacker's username

    if (len(ctx.message.mentions) > 0):
        target = ctx.message.mentions[0].mention  # get target's username
    else:
        await ctx.send(grabline('DI_TM')) # target not specified
        return

    canattack = 1  # flag for validity of attack
    target_index = -1;
    # 0: can't attack - HP too low
    # 1: can't attack - player not in game
    # 2: can attack

    if ((playerList[currentPlayer].usr) == (attacker)):  # check initiative to make sure it is the attacker's turn
        # check that target is in game & hp > 0 (player removed from vector when hp <= 0 for 2 rounds)
        for i, p in enumerate(playerList):
            if ((p.usr)==(target)):
                if (p.disarmed > 0):
                    canattack = -1 # the target is disarmed and can't be disarmed
                else:
                    target_index = i;  # save index
                    canattack = 2 # target can be disarmed
        # if target not in game, reject command

        if (canattack == 1):
            await ctx.send(grabline('DI_TDE')) # target not participating
            return
        elif (canattack == -1):
            await ctx.send(grabline('DI_DIS')) # target already disarmed
            return
        elif (playerList[currentPlayer].disarmed > 0):  # if attacker is disarmed
            await ctx.send(grabline('DI_AD')) # Attacker disarmed
            return

        # now no restrictions from either side
        disarm_roll = roll(1, 20) # roll die
        await ctx.send(attacker + ' rolled a ' + str(disarm_roll))

        if (playerList[currentPlayer].blessed == True):
            disarm_roll += 1
            playerList[currentPlayer].blessed = False # take away blessing
            await ctx.send(attacker + " is recieving divine aid... their disarm roll is now " + str(disarm_roll))

        if (disarm_roll >= DISARM_THRESHOLD):
            playerList[target_index].disarmed = 1;
            await ctx.send(grabline('DI_SUCCESS') + ' ' +  target +
                           ', it will take you ' + str(MAX_DISARMED) + ' full rounds to get your weapon back unless you cast Haste.')

        else:
            await ctx.send(grabline('DI_FAIL')) # disarm unsuccessful

        await ctx.send(turnChange())
        return

    else:
        await ctx.send(attacker + grabline('NYT')) # not your turn
        return
# end of disarm command

# TODO - either change name or remove
@bot.command(help = 'Attempt to heal another player', aliases =['hl'])
async def heal(ctx, target=""):
    global game_on
    if (game_on == False):
        await ctx.send(grabline('GNS_S')) # game not started
        return

    caster = ctx.message.author.mention # get caster's name
    if (len(ctx.message.mentions) > 0):
        target = ctx.message.mentions[0].mention  # get target's username
    else:
        await ctx.send('You need to specify a player to heal!')

    if (target == caster):
        await ctx.send('Heal is reserved for your allies! You can cast cure to heal yourself.')
        return

    target_index = -1

    if ((playerList[currentPlayer].usr)==(caster)):  # check initiative to make sure it is caster's turn

        for i, p in enumerate(playerList):
            if (p.usr)==(target):
                target_index = i

        if (target_index == -1): #target user not found
            await ctx.send(target + 'is not participating in this fight. You can try something else.')
            return

        # check player has a heal left
        if ((playerList[currentPlayer]).numHeals > 0):
            # cast heal
            if ((playerList[currentPlayer]).disarmed >= 1):
                await ctx.send(caster + ', you will have to wait another round to recover your weapon. Are you sure you want to cast Heal?')  # wait for response from target
                msg = await bot.wait_for("message", check=lambda
                    message: message.author.mention == caster and message.channel.id == ctx.channel.id
                             and message.content.lower() in ("y", "yes", "n", "no"))
                if msg.content.lower() in ("n", "no"):
                    await ctx.send(caster + ' has decided not to cast Heal!')
                    playerList[currentPlayer].disarmed = playerList[currentPlayer].disarmed - 1
                    if playerList[currentPlayer].disarmed: playerList[
                        currentPlayer].disarmed = 1  # prevent accidental re-arming
                    return
                elif msg.content.lower() in ("y", "yes"):
                    await ctx.send("You have decided to cast Heal.")

            heal_by = roll(MIN_HEAL, MAX_HEAL) # roll hit points
            playerList[target_index].hp += heal_by # add hit points to target
            (playerList[currentPlayer]).numHeals -= 1;
            await ctx.send(caster + ' healed ' + target + ' by ' + str(heal_by) + ' points, raising them to a total of '
                         + str((playerList[target_index]).hp) + ' hit points.')

        else:
            await ctx.send(caster + ', you have already cast Heal ' + str(NUM_SPELLS) + ' times and cannot cast it anymore.')
            return

    else:
        await ctx.send(caster + ', it is not your turn. You may try to heal on your next turn.')

    await ctx.send(turnChange())
    return
# end of heal command

@bot.command(help = 'Attempt to cure yourself', aliases =['c'])
async def cure(ctx):
    global game_on
    if (game_on == False):
        await ctx.send(grabline('GNS_S')) # game not started
        return

    caster = ctx.message.author.mention  # get caster's name

    if ((playerList[currentPlayer].usr)==(caster)):  # check initiative to make sure it is caster's turn

        if ((playerList[currentPlayer]).numCures > 0):

            if ((playerList[currentPlayer]).disarmed >= 1):
                await ctx.send(caster + ', you will have to wait another round to recover your weapon. Are you sure you want to cast Cure?')  # wait for response from target
                msg = await bot.wait_for("message", check=lambda
                    message: message.author.mention == caster and message.channel.id == ctx.channel.id
                             and message.content.lower() in ("y", "yes", "n", "no"))
                if msg.content.lower() in ("n", "no"):
                    await ctx.send(caster + ' has decided not to cast cure!')
                    playerList[currentPlayer].disarmed = playerList[currentPlayer].disarmed - 1
                    if playerList[currentPlayer].disarmed: playerList[currentPlayer].disarmed = 1 # prevent accidental re-arming
                    return
                elif msg.content.lower() in ("y", "yes"):
                   await ctx.send("You have decided to cast Cure.")

            # cast heal
            heal_by = roll(MIN_HEAL, MAX_HEAL)  # roll hit points
            playerList[currentPlayer].hp =  playerList[currentPlayer].hp + heal_by  # add hit points to target
            (playerList[currentPlayer]).numCures -= 1;
            await ctx.send(caster + ' healed by ' + str(heal_by) + ' points, for a total of '
                           + str((playerList[currentPlayer]).hp) + ' hit points.')

        else:
            await ctx.send(caster + ', you have already cast Heal ' + NUM_SPELLS + ' times and cannot cast it anymore.')
            return

    else:
        await ctx.send(caster + ', it is not your turn. You may try to heal on your next turn.')
        return

    await ctx.send(turnChange())
    return
# end of cure command

@bot.command(help = 'Cast Haste to either re-arm yourself in time to attack this round, or to perform two attacks!', aliases =['h'])
async def haste(ctx, target1="", target2=""):
    # 1 target - either arm, attack once
    #          - or attack target1 twice
    # 2 targets - attack each twice - not valid if disarmed
    global game_on
    if (game_on == False):
        await ctx.send(grabline('GNS_S')) # game not started
        return

    caster = ctx.message.author.mention  # get caster's name
    re_arm = 0 # player hasn't picked up weapon
    num_targets = 1

    if (len(ctx.message.mentions) > 1):
        target2 = ctx.message.mentions[1].mention  # get target's username
        num_targets = 2
    if (len(ctx.message.mentions) > 0):
        target1 = ctx.message.mentions[0].mention  # get target's username
    else:
        await ctx.send(grabline('HA_2TM')) # no targets
        return

    can_attack1 = 1
    can_attack2 = 1

    if ((playerList[currentPlayer].usr)==(caster)):  # check initiative to make sure it is caster's turn

        if ((playerList[currentPlayer]).numHastes <= 0):
            await ctx.send('You have already cast Haste ' + str(NUM_HASTES) + ' times and cannot cast it again this game.')
            return


        for i, p in enumerate(playerList):
            if ((p.usr)==(target1)):
                if (p.hp > 0):
                    can_attack1 = 2  # the attacker can attack
                else:
                    can_attack1 = 0;  # hp too low to allow attack
            if (num_targets == 2):
                if ((p.usr)==(target2)):
                    if (p.hp > 0):
                        can_attack2 = 2  # the attacker can attack
                    else:
                        can_attack2 = 0;  # hp too low to allow attack



        if (can_attack1 == 0 | can_attack2 == 0): # if either target has low HP
            await ctx.send('Don\'t kick an opponent while they\'re down! You may try another action.')
            return
        elif ((can_attack1 == 1) & (can_attack2 == 1) & (target2 != "")): # if target not in game, reject command
            await ctx.send(target1 + ' and ' + target2 + ' have decided this is not their fight! You may try another action.')
            return
        elif ((can_attack2 == 1) & (target2 != "")):
            await ctx.send(target2 + ' has decided this is not their fight! You will attack just one opponent.')
            num_targets = 1
        elif ((can_attack1 == 1) & (target2 != "")):
            await ctx.send(target1+ ' has decided this is not their fight! You will attack just one opponent.')
            target1 = target2
            num_targets = 1
        elif ((can_attack1 == 1) & (target2 == "")):
            await ctx.send(target1 +  ' has decided this is not their fight! You may try another action.')
            return

        playerList[currentPlayer].numHastes -= 1;  # dec haste
        await ctx.send(caster + ' cast Haste!')

        if ((playerList[currentPlayer]).disarmed > 0): # if disarmed, re-arm, one attack
            playerList[currentPlayer].disarmed = 0;  # set not disarmed
            re_arm = 1 # indicate player picked up weapon
            await ctx.send(caster + ' picks their weapon back up and can now attack.')

        # attack target1
        await ctx.invoke(bot.get_command('attack'), target1,  1)

        if (re_arm == 0):
            await ctx.send('Because ' + caster + ' was not disarmed, they will now perform a second attack.')

        if ((num_targets == 1) & (re_arm == 0)): # if no target2 & no re-armed attack target 1 again
            # attack target1
            #await ctx.send('Now for the second attack!')
            await ctx.invoke(bot.get_command('attack'), target1)

        elif(re_arm == 0): # else if no re-armed attack target2
            # attack target2
            #await ctx.send('Now for the second attack!')
            await ctx.invoke(bot.get_command('attack'), target2)

        else: # if re-armed & already attacked
            await ctx.send('There is no time for a second attack!')
            await ctx.send(turnChange()) # change turns
            return
    else:
        await ctx.send(caster + ', it is not your turn. You may try to cast haste on your next turn.')
        return
# end of haste command

#barehanded 17 never reached dam print
@bot.command(help = 'Attack with your bare hands! Useful when disarmed', aliases =['p'])
async def punch(ctx, target=""):
    global MAX_PRONE
    global ARMOR_CLASS
    global game_on
    if (game_on == False):
        await ctx.send('You must start a game before you can take action!')
        return

    attacker = ctx.message.author.mention  # get attacker's username

    canattack = 1 # flag for validity of attack
    target_index = -1;
    # 0: can't attack - HP too low
    # 1: can't attack - player not in game
    # 2: can attack

    if (len(ctx.message.mentions) > 0):
        target = ctx.message.mentions[0].mention  # get target's username
    else:
        await ctx.send('You need to specify a target to punch! Type \".punch @playername\" to punch them.')
        return

    if ((playerList[currentPlayer].usr)==(attacker)):   # check initiative to make sure it is the attacker's turn
       if (playerList[currentPlayer].roundsAtZero > 0):
           await ctx.send(attacker + ' is prone and must be healed within ' + str(MAX_PRONE - playerList[currentPlayer].roundsAtZero) + ' rounds to survive. You cannot attack right now.')
           return
       else:
       # check that target is in game & hp > 0 (player removed from vector when hp <= 0 for 2 rounds)
        for i, p in enumerate(playerList):
            if ((p.usr)==(target)):
               if (p.hp > 0):
                    canattack = 2 # the attacker can attack
                    target_index = i; # save index
               else:
                   canattack = 0; # hp too low to allow attack

        # if target not in game, reject command
        if (canattack == 0):
            await ctx.send('Don\'t kick an opponent while they\'re down! You may try something else.')
            return
        elif (canattack == 1):
            await ctx.send(target + ' has decided this is not their fight! You may try to attack something else.')
            return
        else:

            if ((playerList[currentPlayer]).disarmed >= 1):
                await ctx.send(
                    attacker + ', you will have to wait another round to recover your weapon. Are you sure you want to punch?')  # wait for response from target
                msg = await bot.wait_for("message", check=lambda
                    message: message.author.mention == attacker and message.channel.id == ctx.channel.id
                             and message.content.lower() in ("y", "yes", "n", "no"))
                if msg.content.lower() in ("n", "no"):
                    await ctx.send(attacker + ' has decided not to punch!')
                    playerList[currentPlayer].disarmed = playerList[currentPlayer].disarmed - 1
                    if playerList[currentPlayer].disarmed: playerList[currentPlayer].disarmed = 1  # prevent accidental re-arming
                    return
                elif msg.content.lower() in ("y", "yes"):
                    await ctx.send("You have decided to punch.")

            hit_roll = roll(1, 20) # else roll to hit

            if (hit_roll == 1): # CRITICAL MISS! This attack has backfired
                await ctx.send('Oh no! ' + attacker + ' rolled a critical miss! Now they will roll to see if they survive their own attack...')
                self_hit = roll(1, 20)  # roll to see if attacker hit themself
                if (self_hit >= (ARMOR_CLASS)): # they did - reduced threshold b/c no disarm possibility
                    self_damage = roll(1, 6) # roll damage die
                    self_damage -= 2 # reduced damage b/c unarmed
                    playerList[currentPlayer].hp = playerList[currentPlayer].hp - self_damage # evaluate damage
                    await ctx.send(attacker + ' tried to strike but failed miserably, striking themself and causing ' + str(self_damage) + ' points of damage!')
                    if (playerList[currentPlayer].hp <= 0):
                        playerList[currentPlayer].roundsAtZero = 1
                        await ctx.send(attacker + '\'s health is now at ' + str(playerList[currentPlayer].hp) +
                                 ' and they will die from their wounds in ' + str(MAX_PRONE) + ' rounds unless they are healed!')

                await ctx.send(turnChange())
                return

            else: # otherwise
                if (hit_roll != 20):
                    await ctx.send(attacker + ' rolled a ' + str(hit_roll))
                total_hit_roll = hit_roll  # init total hit

                if (playerList[currentPlayer].blessed == True):  # check attacker Bless status, if active +2 to roll
                    total_hit_roll += 2;
                    await ctx.send(attacker + ' is recieving divine assistance!')
                    playerList[currentPlayer].blessed = False  # remove blessing
                if (playerList[target_index].disarmed > 0):  # check target disarm status, if active +2 to roll
                    total_hit_roll += 2;
                    await ctx.send('Since ' + target + ' is disarmed, ' + attacker + ' gets a bonus to their roll!')

                total_hit_roll = total_hit_roll - 1  # reduce to-hit roll b/c unarmed attack
                await ctx.send('Since ' + attacker + ' is attacking barehanded, their chance to hit is reduced by 1!')

                if (total_hit_roll != hit_roll):
                    await ctx.send('The total roll is ' + str(total_hit_roll) + '!')

                if (total_hit_roll < ARMOR_CLASS): # total roll below armor class value
                    await ctx.send(target + '\'s armor is stronger than ' + attacker + '\'s fist - ' + target + ' is unharmed.')
                    await ctx.send(turnChange())
                    return
                else: # total roll above armor class value
                    # if target has NUM_DODGES > 0 offer target dodge
                    if (hit_roll == 20):
                        await ctx.send(attacker + ' has rolled a natural 20! ')
                    if (playerList[target_index].numDodges > 0):
                        await ctx.send(target + ', would you like to dodge?')  # wait for response from target
                        msg = await bot.wait_for("message", check=lambda
                            message: message.author.mention == target and message.channel.id == ctx.channel.id
                                     and message.content.lower() in ("y", "yes", "n", "no"))
                        if msg.content.lower() in ("y", "yes"):
                            await ctx.send(target + ' has dodged the attack!')
                            playerList[target_index].numDodges = playerList[target_index].numDodges - 1;
                            if (passed == 0):
                                await ctx.send(turnChange())
                            return
                        elif msg.content.lower() in ("n", "no"):
                            await ctx.send("You have chosen not to dodge.")

                    MB = False
                    # no dodge - offer attacker mighty blow
                    if (playerList[currentPlayer].numMightyBlows > 0):
                        await ctx.send(attacker + ', would you like to cast Mighty Blow? Remember, punches do reduced damage.')  # wait for response from target
                        msg = await bot.wait_for("message", check=lambda
                            message: message.author.mention == attacker and message.channel.id == ctx.channel.id
                                     and message.content.lower() in ("y", "yes", "n", "no"))
                        if msg.content.lower() in ("y", "yes"):
                            await ctx.send(attacker + ' cast Mighty Blow! The damage from this attack will be doubled!')
                            playerList[currentPlayer].numMightyBlows = playerList[currentPlayer].numMightyBlows - 1;
                            MB = True
                        elif msg.content.lower() in ("n", "no"):
                            await ctx.send("You have chosen not to cast Mighty Blow.")


                        if (hit_roll == 20):
                            damage_roll = roll(2, 12)
                        else:
                            damage_roll = roll(1, 6)  # roll 2d6
                        if (MB == True):
                               damage_roll *= 2  # Mighty Blow cast -> double damage

                        damage_roll -= 2 # unarmed penalty
                        if (damage_roll < 0):
                            damage_roll = 0 # no underflow lol


                    # do damage

                    playerList[target_index].hp = playerList[target_index].hp - damage_roll  # evaluate damage
                    await ctx.send(attacker + ' struck ' + target + ' for ' + str(damage_roll) + ' points of damage!')
                    if (playerList[target_index].hp <= 0):
                        playerList[target_index].roundsAtZero = 1
                        if (MAX_PRONE > 0):
                            await ctx.send(target + '\'s health is now at ' + str(playerList[target_index].hp) +
                                ' and they will die from their wounds in ' + str(MAX_PRONE) + ' rounds unless they are healed!')

                    await ctx.send(turnChange())
                    return

       await ctx.send(turnChange())
       return

    else:
        await ctx.send(attacker + ', it is not your turn. You may try to punch on your next turn.')
        return
# end of punch command

@bot.command(help = 'Pray for divine assistance on your next attack', aliases =['b'])
async def bless(ctx):
    global game_on
    if (game_on == False):
        await ctx.send('You must start a game before you can cast spells!')
        return

    caster = ctx.message.author.mention  # get caster's name
    if ((playerList[currentPlayer].usr)==(caster)):  # check initiative to make sure it is caster's turn
        if (playerList[currentPlayer].blessed == True):
            await ctx.send(caster + ', you are already blessed. Try taking another action.')
            return

        if (playerList[currentPlayer].numBlessings > 0):
            playerList[currentPlayer].numBlessings = playerList[currentPlayer].numBlessings - 1 # decrement available Blesses
            playerList[currentPlayer].blessed = True
            await ctx.send(caster + ' asked the divines for their assistance, and this wish has been granted. Their next attack will be guided from above.')
        else:
            await ctx.send(caster + grabline('BL_FAIL'))

        return

    else:
        await ctx.send(caster + ', it is not your turn. You may try to cast bless on your next turn.')
#end of bless command

@bot.command(help = 'Skip your turn', aliases =['sk'])
async def skip(ctx):
    global game_on
    if (game_on == False):
        await ctx.send(grabline('GNS_A')) # game not started
        return
    caller = ctx.message.author.mention  # get caster's name

    if ((playerList[currentPlayer].usr) == (caller)):  # check initiative to make sure it is caster's turn
        await ctx.send(caller + ' is skipping this turn.')
        await ctx.send(turnChange())
        return
    else:
        await  ctx.send('You can\'t skip a turn that isn\'t yours!')
# end of skip command


# LOGIN TOKEN
bot.run('YOUR TOKEN HERE') # sets login token


