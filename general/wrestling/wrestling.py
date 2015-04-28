"""
Fictitious pro wrestling!

Make fictitious people wrestle it out in a fake pro wrestling match.
"""

from StringIO import StringIO
from random import randint, choice
from wrestler import Wrestler, get_wrestlers
import db



def create_a_wrestler():
    while True:
        try:
            name = raw_input("What will you name your wrestler? ")
            w = Wrestler(name=name)
            w.save()
            # if we make it here, we're done, go back
            # to menu options
            break
        except ValueError as err:
            print err



def list_wrestlers():
    """Print a list of all of the wrestlers and their records.
    """
    print "\nWide World of Wrestling Statistics"
    wrestlers = get_wrestlers()
    if wrestlers:
        # Figure out the max text length that our input will need.
        max_text_length = 0
        for wrestler in wrestlers:
            for k, v in wrestler.attrs_as_dict().items():
                max_text_length = max(max_text_length, len(str(k)), len(str(v)))
        
        # A little extra space.
        max_text_length += 1
        # Template for the table, assuming each wrestler has the same stats.
        row_template = StringIO()
        for i in range(5):
            row_template.write("{0[%s]:>%s}" % (i, max_text_length))
        row_template = row_template.getvalue() + "\n"
        output = StringIO()
        # Header first
        output.write(row_template.format(wrestlers[0].attrs_as_dict().keys()))
        # Wrestlers second
        for wrestler in wrestlers:
            output.write(row_template.format(wrestler.attrs_as_dict().values()))
        # Output to screen
        print "\n",output.getvalue(),"\n"
        output.close()
    else:
        print "No wrestlers found. Please recruit some wrestlers.\n"



def host_a_wrestling_match():
    # Randomly choose two wrestlers from the database
    # but fail if there are is one wrestler or less in the database.
    # If there are two wrestlers, perform a match.
    wrestlers = get_wrestlers()
    if len(wrestlers) >= 2:
        wrestler1 = wrestlers.pop(randint(0, len(wrestlers)-1))
        wrestler2 = wrestlers.pop(randint(0, len(wrestlers)-1))
        print "\nLADIES AND GENTLEMENT! TONIGHTS MAIN EVENT!"
        announcement = "IN CORNER #{0}, WE HAVE {1.name} with {1.wins} wins and {1.losses} losses."
        print announcement.format(1, wrestler1)
        print announcement.format(2, wrestler2)
        print "\nLET THE MATCH BEGIN!\n"

        # A simple "trading hits" scenario.
        # wrestler1.brawn vs. wrestler2.finesse.
        if randint(1, wrestler1.brawn) > randint(1, wrestler2.finesse):
            results = { "winner": wrestler1, "loser": wrestler2 }
        else:
            results = { "winner": wrestler2, "loser": wrestler1 }

        commentary = choice([
            "HOLY MOLY, {0[winner].name} sits on {0[loser].name} and submits him!",
            "LET'S SEE THAT AGAIN! {0[winner].name} reverses {0[loser].name}'s lunge and pins him to the mat."
        ])
        print commentary.format(results)
        print "WINNER: {[winner].name}\n".format(results)
        
        # Update stats
        results["winner"].wins += 1
        results["loser"].losses += 1
        results["winner"].save()
        results["loser"].save()

    else:
        print "\nSorry, you need at least two wrestlers to host a wrestling match.\n"



def leave_game():
    """Ends the game.
    """
    return True

MENU = {
    #option, visual description, callback function
    "1": ("Create a wrestler", create_a_wrestler),
    "2": ("List the wrestler stats", list_wrestlers),
    "3": ("Host a wrestling match", host_a_wrestling_match),
    "4": ("Quit", leave_game),
}

def main():
    """Provide the main menu and options to the player.
    """
    while True:
        print ""
        for key in sorted(MENU.keys()):
            print "({0}): {1}".format(key, MENU[key][0])
        print ""
        choice = raw_input("> ")
        if choice.strip() in MENU:
            done = MENU[choice][1]()
            if done:
                # If any of the menu choices return truthy values, we're
                # done.
                return
        else:
            print "\nPlease type valid menu option.\n"



if __name__ == "__main__":
    # menu loop
    main()

    print "See you again soon!"
    # cleanup the database.
    db.cleanup()
