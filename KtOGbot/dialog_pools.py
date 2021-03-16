# This file contains the standard dialog pools for KtOGbot.
# Each pool corresponds to an action/spell/etc.
# Each pool is just an array of strings. Any information like hit points, damage, etc. must be
# specified in a separate statement inside main.py. This is just flavortext.

# You can replace all the dialog lines by editing this file or creating a similar file with
# each of the same pool labels.
# Then either name that file dialog_pools.py, or replace "dialog_pools" in main.py with the
# name of your file.

# This file has generic fantasy flavortext.

# STANDARD ATTACK

# Success (SA_SUCCESS)
SA_SUCCESS = ['You come down on your opponent with great force!',
              'Your weapon pierces your opponent\'s armor.',
              'Your opponent is unable to escape your attack!']

# Failure (SA_FAIL)
SA_FAIL = ['Your attack was unsuccessful, leaving your target unharmed.',
           'Your attack misses your intended target.',
           'Your target\'s armor is stronger than your attack!']

# Critical Miss - Damage (SA_CMDAM)
SA_CMDAM = ['A critical miss! That attack went poorly - you\'ve struck yourself!',
            'Oh no! You rolled a 1 and fumbled your attack, hurting only yourself!']

# Critical Miss - Disarmed (SA_CMDIS)
SA_CMDIS = ['Oh no! You rolled a critcal miss! You\'ve disarmed yourself!',
            'Uh oh - you rolled a 1! You\'ve dropped your weapon!']

# Critical Miss - Safe (SA_CMSA)
SA_CMSA = ['You rolled a critcal miss, but managed to regain control of your weapon! Your attack failed but you are unharmed',
           'You fumbled your attack after rolling a 1, but managed to avoid hurting yourself!',
           'You rolled a 1, but were able to recover quickly and retained your weapon.']

# Critical Hit - (SA_CH)
SA_CH = ['You rolled a natural 20!',
         'Wow! A natural 20!',
         'A nat20! That\'ll do 2d6 damage!']

# Target Doesn't Exist (SA_TDE)
SA_TDE = ['You can\'t attack someone who hasn\'t agreed to fight!']

# Target Missing (SA_TM)
SA_TM = ['You need to specify a target to attack! Type \".attack @playername\" to attack them.',
         'You need to mention your intended target to attack!',
         'Remember to follow \".a\" or \".attack\" with a mention of your intended target.']

# Target Prone (SA_PR)
SA_PR = ['Don\'t kick an opponent while they\'re down! You may try something else.']

# Attacker Disarmed (SA_DIS)
SA_DIS = ['You are currently unarmed and cannot attack.',
          'Attacks require weapons.']


# PUNCH ATTACK

# Success (PA_SUCCESS)
PA_SUCCESS = ['You punch your opponent in the face!',
              'Your opponent is unable to escape your attack!',
              'Your fist collides with your oppenent\'s unprotected flesh!']

# Failure (PA_FAIL)
PA_FAIL = ['You swing... and you miss']

# Critical Miss - Damage (PA_CMDAM)
PA_FAIL = ['A critical miss! You swing wildly and injure your arm!']

# Critical Hit (PA_CH)
PA_CH = ['A critical hit! You throw your punch with impressive force!']

# Target Doesn't Exist (PA_TDE)
PA_TDE = ['You can\'t punch someone who hasn\'t agreed to fight!']

# Target Missing (PA_TM)
PA_TM = ['You need to specify a target to punch! Type \".punch @playername\" to punch them.',
         'You need to mention your intended target to throw a punch!',
         'Remember to follow \".p\" or \".punch\" with a mention of your intended target.']

# Target Prone (PA_PR)
PA_PR = ['Don\'t kick an opponent while they\'re down! You may try something else.']


# DISARM

# Success (DI_SUCCESS)
DI_SUCCESS = ['You have successfully disarmed your opponent!']

# Failure (DI_FAIL)
DI_FAIL = ['Your opponent remains armed.',
           'You failed to disarm your opponent.']

# Target Already Disarmed (DI_DIS)
DI_DIS = ['You can\'t take a weapon from someone who doesn\'t have one!',
          'Your opponent is already disarmed. Try something else.',
          'Your target is already disarmed! You can\'t disarm them right now.']

# Target Doesn't Exist (DI_TDE)
DI_TDE = ['You can\'t disarm someone who hasn\'t agreed to fight!',
          'You can\'t take a weapon from someone who chose not to carry one!',
          ]

# Target Missing (DI_TM)
DI_TM = ['Remember to specify a target to disarm by mentioning them.',
         'Remember to follow \".d\" or \".disarm\" with a mention of your intended target.',
         'You need to specify a player to disarm!']

# Attacker Disarmed (DI_AD)
DI_AD = ['you will not be able to disarm an opponent while you yourself are unarmed!']


# HASTE

# Second Attack (HA_SA)
HA_SA = ['Now it is time to launch a second attack!']

# Re-armed (HA_RA)
HA_RA = ['You have retrieved your weapon!',
         'You are re-armed and ready to fight!']

# Targets Don't Exist (HA_2TDE)
HA_2TDE = ['Neither of your specified targets are participating in this fight.']


# One Target Doesn't Exist (HA_1TDE)
HA_1TDE = ['One of your targets is not participating in the fight. Only the participating target will be attacked.']

# Targets Missing (HA_2TM)
HA_2TM = ['You need to specify at least one target when casting Haste.',
          'Specify one or two targets by following \".h\" or \".haste\" with a mention or two.']


# HEAL

# Success (HE_SUCCESS)
# Failure (HE_FAIL)
# Target Doesn't Exist (HE_TDE)


# CURE

# Success (CU_SUCCESS)
# Failure (CU_FAIL)


# BLESS
# preceed messages w/ caster's name

# Success (BL_SUCCESS)

# Failure (BL_FAIL)
BL_FAIL = ['\'s request was not granted, for the divines have heard too many of their prayers already.']


# GENERAL PHRASES

# game not started - action
GNS_A = ['You must start a game before you can take action!']
# game not started - spell
GNS_S = ['You must start a game before you can cast spells!']

# not your turn (do caller + grabline('NYT'))
NYT = [', it is not your turn.',
       ', you can try that on your next turn.'
       ', you can type \".f\" or \".fighters\" to see when your turn will come.'
       ', you can always use \".t\" or \".turn\" to see whose turn it is.']