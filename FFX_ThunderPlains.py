import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def southPathing(status):
    FFX_memory.clickToControl()
    
    gameVars.setLStrike(FFX_memory.lStrikeCount())
    
    speedcount = FFX_memory.getSpeed()
    if speedcount >= 14:
        status[3] = True
    
    FFX_memory.fullPartyFormat('postbunyip')
    FFX_memory.closeMenu()
    lStrikeCount = FFX_memory.lStrikeCount()
    
    checkpoint = 0
    while FFX_memory.getMap() != 256:
        if FFX_memory.userControl():
            #Lightning dodging
            if FFX_memory.dodgeLightning(gameVars.getLStrike()):
                print("Dodge")
                gameVars.setLStrike(FFX_memory.lStrikeCount())
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsSouth(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_Screen.BattleScreen():
                status = FFX_Battle.thunderPlains(status, 1)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 0.5)
    FFXC.set_movement(-1, 1)
    while not FFX_memory.getMap() == 263:
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_neutral()
    complete = 1

    return status

def agencyShop():
    speedCount = FFX_memory.getSpeed()
    FFX_memory.clickToDiagProgress(92)
    while FFX_memory.blitzCharSelectCursor() != 2:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(60)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(60)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuRight()
    speedNeeded = 14 - speedCount #15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    if speedNeeded > 1:
        speedNeeded = 1 #Limit so we don't over-spend and run out of money.
    if speedNeeded > 0:
        while speedNeeded > 0:
            FFX_Xbox.menuRight()
            speedNeeded -= 1
    
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(6)
    
    #Next, Grab Auron's weapon
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(0.1)
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(90)
    FFX_memory.clickToDiagProgress(92)
    #FFX_Xbox.menuB()
    FFXC.set_neutral()
    #FFX_memory.waitFrames(150)
    while FFX_memory.blitzCharSelectCursor() != 1:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Got any weapons?
    FFX_memory.waitFrames(30 * 1.6)
    FFX_Xbox.menuRight()
    FFX_memory.waitFrames(30 * 0.4)
    FFX_Xbox.menuB() #Sell
    FFX_memory.waitFrames(30 * 0.4)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(3)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Tidus' longsword
    FFX_memory.waitFrames(3)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(3)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Auron Katana
    FFX_memory.waitFrames(6)
    if gameVars.getBlitzWin() == False and FFX_memory.getGilvalue() < 9550:
        for j in range(11):
            FFX_Xbox.menuDown()
        while FFX_memory.getGilvalue() < 9550:
            FFX_memory.waitFrames(3)
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(6)
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(6)
            FFX_Xbox.menuRight()
            FFX_Xbox.menuDown()
        FFX_memory.waitFrames(6)
    elif gameVars.getBlitzWin() == True and FFX_memory.getGilvalue() < 8725:
        for j in range(11):
            FFX_Xbox.menuDown()
        while FFX_memory.getGilvalue() < 8725:
            FFX_memory.waitFrames(3)
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(6)
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(6)
            FFX_Xbox.menuRight()
            FFX_Xbox.menuDown()
        FFX_memory.waitFrames(6)
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuLeft()
    FFX_memory.waitFrames(12)
    FFX_Xbox.menuB() #Buy
    FFX_memory.waitFrames(24)
    #FFX_memory.waitFrames(30 * 30) #Testing only
    
    if gameVars.getBlitzWin() == False:
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(24)
        FFX_Xbox.menuUp() #Baroque sword
        #FFX_memory.waitFrames(30 * 10) #Testing only
        FFX_memory.waitFrames(10)
        FFX_Xbox.menuB() #Weapon for Tidus (for Evrae fight)
        FFX_memory.waitFrames(10)
        FFX_Xbox.menuB() #Do not equip
        FFX_memory.waitFrames(24)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Shimmering Blade
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB() #Do not equip
    FFX_memory.closeMenu()

def agency():
    #Arrive at the travel agency
    FFX_memory.clickToControl3()
    checkpoint = 0
    
    while FFX_memory.getMap() != 162:
        if FFX_memory.userControl():
            if checkpoint == 1:
                while not FFX_memory.diagSkipPossible():
                    FFX_targetPathing.setMovement([2,-31])
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(3)
                FFXC.set_neutral()
                agencyShop()
                checkpoint += 1
            elif checkpoint == 4:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:
                kimahriAffection = FFX_memory.affectionArray()[3]
                print("Kimahri affection, ", kimahriAffection)
                while FFX_memory.affectionArray()[3] == kimahriAffection:
                    FFX_targetPathing.setMovement([27, -44])
                    FFX_Xbox.tapB()
                print("Updated, full affection array:")
                print(FFX_memory.affectionArray())
                checkpoint += 1
            elif checkpoint == 8:
                while not FFX_memory.getMap() == 256:
                    FFX_targetPathing.setMovement([3, -52])
                    FFX_Xbox.tapB()
                checkpoint += 1
            elif checkpoint == 10:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
            
            elif FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsAgency(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
def northPathing(status):
    FFX_memory.clickToControl()
    
    lStrikeCount = FFX_memory.lStrikeCount()
    
    checkpoint = 0
    while FFX_memory.getMap() != 110:
        if FFX_memory.userControl():
            #Lightning dodging
            if FFX_memory.dodgeLightning(lStrikeCount):
                print("Dodge")
                lStrikeCount = FFX_memory.lStrikeCount()
            elif checkpoint == 12 and status[4] == False and status[2] == False:
                checkpoint = 10
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsNorth(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_Screen.BattleScreen():
                status = FFX_Battle.thunderPlains(status, 1)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    if not gameVars.csr():
        FFXC.set_movement(0, 1)
        FFX_Xbox.SkipDialog(6)
        FFXC.set_neutral()
        
        FFX_memory.clickToControl3() # Conversation with Auron about Yuna being hard to guard.
        
        FFXC.set_movement(1, 1)
        FFX_memory.waitFrames(30 * 2)
        FFXC.set_movement(0, 1)
        FFX_Xbox.SkipDialog(6)
        FFXC.set_neutral() #Approaching the party
    
    else:
        while not FFX_targetPathing.setMovement([258,-7]):
            pass

    return status
