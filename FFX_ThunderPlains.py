import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def southPathing(blitzWin):
    FFX_memory.clickToControl()
    
    status = [False,False,False,False] #Rikku charged, Light Curtain, Lunar Curtain, Speed sphere recovery done
    status[2] = blitzWin
    speedcount = FFX_memory.getSpeed()
    if speedcount >= 14:
        status[3] = True
    
    FFX_memory.fullPartyFormat_New('postbunyip', 11)
    FFX_memory.closeMenu()
    lStrikeCount = FFX_memory.lStrikeCount()
    
    checkpoint = 0
    while FFX_memory.getMap() != 256:
        if FFX_memory.userControl():
            #Lightning dodging
            if FFX_memory.dodgeLightning(lStrikeCount):
                print("Dodge")
                lStrikeCount = FFX_memory.lStrikeCount()
            
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
    time.sleep(0.5)
    FFXC.set_movement(-1, 1)
    while not FFX_memory.getMap() == 263:
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_neutral()
    complete = 1

    return status

def agency(blitzWin):
    #Arrive at the travel agency
    FFX_memory.clickToControl3()
    speedCount = FFX_memory.getSpeed()
    
    #Talk to the lady
    FFXC.set_movement(0, 1)
    time.sleep(0.3)
    FFXC.set_movement(1, 0)
    FFX_Xbox.SkipDialog(0.15)
    FFXC.set_neutral()
    
    time.sleep(0.6)
    FFX_Xbox.menuB()
    FFX_Screen.awaitPixel(888,470,(191, 191, 191))
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1.6)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    speedNeeded = 14 - speedCount #15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    if speedNeeded > 1:
        speedNeeded = 1 #Limit so we don't over-spend and run out of money.
    if speedNeeded > 0:
        while speedNeeded > 0:
            FFX_Xbox.menuRight()
            speedNeeded -= 1
    
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.SkipDialog(0.3)
    
    #Next, Grab Auron's weapon
    time.sleep(0.5)
    FFX_Xbox.menuB()
    FFX_Screen.awaitPixel(888,470,(191, 191, 191))
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Got any weapons?
    time.sleep(1.6)
    FFX_Xbox.menuRight()
    time.sleep(0.4)
    FFX_Xbox.menuB() #Sell
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Tidus' longsword
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Auron Katana
    time.sleep(0.1)
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuLeft()
    time.sleep(0.4)
    FFX_Xbox.menuB() #Buy
    time.sleep(0.8)
    #time.sleep(30) #Testing only
    
    if blitzWin == False:
        FFX_Xbox.menuB()
        time.sleep(0.8)
        FFX_Xbox.menuUp() #Baroque sword
        #time.sleep(10) #Testing only
        time.sleep(0.1)
        FFX_Xbox.menuB() #Weapon for Tidus (for Evrae fight)
        time.sleep(0.1)
        FFX_Xbox.menuB() #Do not equip
        time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Shimmering Blade
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB() #Do not equip
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Now for Yuna's scene
    FFXC.set_movement(1, 0)
    time.sleep(0.5)
    FFXC.set_movement(1, 1)
    time.sleep(0.6)
    FFXC.set_movement(0, 1)
    time.sleep(1.5)
    FFXC.set_neutral
    time.sleep(2) #Scene in Yuna's room. Not as exciting as it sounds.
    
    FFX_memory.clickToControl3()
    print("Yuna's done talking. Let's keep going.")
    FFXC.set_movement(0, -1)
    time.sleep(0.3)
    FFXC.set_movement(-1, -1)
    time.sleep(0.2)
    FFXC.set_movement(0, -1)
    time.sleep(0.5)
    FFXC.set_movement(1, 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_movement(-1, 0)
    time.sleep(0.3)
    FFX_Xbox.SkipDialog(2) #Talk to Rikku
    FFXC.set_neutral()
    
    print("------------------------------------------Affection array:")
    print(FFX_memory.affectionArray())
    print("------------------------------------------")
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(1, 1)
    time.sleep(1.5)
    FFXC.set_movement(0, 1)
    time.sleep(0.1)
    
    FFX_Xbox.SkipDialog(3) #Pick up lightning shield
    time.sleep(2)
    
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    
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
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3() # Conversation with Auron about Yuna being hard to guard.
    
    FFXC.set_movement(1, 1)
    time.sleep(2)
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_neutral() #Approaching the party

    return status
