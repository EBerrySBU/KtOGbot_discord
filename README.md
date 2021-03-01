## KtOGbot for Discord

A Discord bot for playing KtOG. See http://ktog.in8sworld.net/ for the history of the game.

The commands are designed to make this game easy to play on mobile and desktop Discord.

The command symbol is a period, since it's on the main mobile keyboard layout. By using mentions to refer to players, you can rely on autofill. It also means that you can look away from the game, and you'll be notified whenever something important happens.

All the important values, like starting hit points and the number of times you can cast spells, are defined at the top of the bot file. You're welcome to adjust these values on your own bot to tweak the difficulty or average length of a game. 

---

## Playing with KtOGbot

There are several kinds of commands you can use when playing KtOG with KtOGbot. I'll call them metacommands, actions, spells, and counterspells.

# Metacommands
Metacommands are for logistics. These are used for tracking player status and joining or leaving games. 

| Command | Alias | Use |
| --- | ---- | --- |
|.join | .j |  Join the waiting room for a game. You can only join a game when there isn't already one in progress. |
|.leave |  | Leave a game that you've already joined. It doesn't matter if the game has started or not - you can leave at any time. If only one player is left behind when you leave, they automatically win and the game ends. |
|.start| | Start a game. All the players in the waiting room will be added to the game, and the first player's turn will begin. |
|.howto| | Shows a brief explanation of the game and a link to the KtOG website.|
|.fighters | .f | Prints a list of all the players who have joined the game. Once the game has started, this list is in order of initiative, so you can tell whose turn comes next.|
|.status | .s | You can use this command two ways. You can just type the command, and it will print out important information about your player status, like your current hit points, the number of times you can cast each spell, etc. Or, you can type the command followed by a mention (@examplename) to get the same information about them. |
|.turn | .t | This command mentions the player whose turn it currently is. | 
    


# Actions
Actions are the most important part of the game. An action ends your turn, so choose carefully.


| Action | Alias | Use |
| --- | ---- | --- |
|.attack | .a | The standard weapon attack, and the most important command in the game. You must specify another player by mentioning them after the command. Behind the scenes, a d20 will be rolled to see if you hit your opponent. (Bonuses might be applied!)If you do, a d6 will be rolled to find the number of points of damage you do to them. In some special cases, you might do extra damage - or even do damage to yourself!
|.disarm | .d | You can try to knock your opponent's weapon out of their hand! If you're successful, they will either take 2 rounds to recover it or need to use up one of their spells. You must specify another player by mentioning them after the command. | 
|.punch | .p | This is an unarmed attack, and can be used even when you have no weapon. You must specify another player by mentioning them after the command. Like an attack, a d20 will be rolled to see if you hit your opponent. It will be harder to succeed than it is with a standard attack! If you do, a d6 will be rolled to find the number of points of damage you do to them. The damage you do is reduced by 2, since you're not using a weapon. In some special cases, you might do extra damage - or even do damage to yourself! |
|.skip| |You can skip your turn if there's nothing you want to do... or if there's nothing you *can* do.|
    


# Spells
There's a limit on how many spells you can cast each game, so don't forget to use the .status command to check. Casting spells will end your turn.


| Spell | Alias | Use |
| --- | ---- | --- |
|.bless | .b | A blessing from the divines will true your aim! This will add 2 to whatever your next "hit" roll is in an attack, punch, disarm, or haste. | 
| .cure | .c | Heal thyself! Cure will restore 1-10 points of health. Yes, you can go above the starting hit points by casting cure. |
| .heal | .hl | Help a friend! Specify another player, and restore health to them just like casting cure. This might not be much fun in a 1v1 game, but it's helpful when you need to form alliances on a larger battlefield. |
|.haste | .h |Haste is a multipurpose spell. You can use it three different ways: (1) To pick up a weapon you've dropped and perform one attack with it. You'll automatically pick up your weapon when you cast Haste while disarmed; just specify the player you want to attack with a mention. (2) To attack one player twice. You must already be armed to attack twice; just specify the player you want to attack with a mention.(3) To attack two different players. Again, you must already be armed. You can specify two players to attack by using mentions. |
 
 
# Counterspells
Counterspells are spells that you can only cast in response to an attack. You'll be prompted to use these counterspells when they're both appropriate and available. Just type "y" or "yes" to use them, or type "n" or "no" to save them for later.


| Counterspell | Use| 
| --- | ---- |
| Dodge | Dodge can be cast by the target of an attack, and you automatically avoid taking any damage. Keep in mind that you don't get to see the damage total before choosing to dodge. |
| Mighty Blow | Mighty Blow can be cast by an attacker if their target hasn't dodged. Mighty Blow doubles the damage done by an attack. Like Dodge, it's cast before the damage die is rolled, so choose wisely. |
  
  
  
# Special Rolls
Strange things can happen when you roll well! 

**Natural 20s**
 
   When you roll a natural 20 during an attack or punch - that is, the hit die roll without bonuses or any other modifier is 20 - you roll 2d6 for damage to your opponent! By itself, a natural 20 can do 2-12 points of damage. 
   When combined with a Mighty Blow, this means that you could do anywhere from 4-24 damage!
  
  
**Critical Misses**
 
   When you roll a 1 during an attack or punch, you've really gotten mixed up! 
   There'll be a roll to see if you do damage to yourself by mishandling your weapon (or fist). 
   If you escape unscathed, another check will be done to see if you've disarmed yourself! 
   (You can't lose your weapon if you fumbled a punch.)
   You won't do any damage to your opponent. 

