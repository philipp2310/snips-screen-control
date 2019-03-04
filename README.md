# snips-screen-control
Control a simple display with SNIPS

- turn on the screen
- turn off the screen

You must give the skill user the permission:

DISPLAY:0 xhost SI:localuser:_snips-skills

As this command won't survive a restart, you have to add it to your autostart (for example in ~/.profile )