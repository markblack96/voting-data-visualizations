# We've got some comma separated values, but this is trashy and not good for an API
# So what do we do? A sqlite database, of course!

# We need tables for:
# Congresspersons, political party codes, votes, congresses(?)
# ________________
#| congressperson |
#|----------------|
#|bioname         |
#|party code      |
#|congress_num    |
#------------------
# _______________
#|     vote      |
#|---------------|
#|               |
#-----------------
# And so on
