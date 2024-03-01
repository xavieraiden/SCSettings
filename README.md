# SCSettings
A tool for easier manipulation of Starsectors settings.json file (Or really any other)
# Back up your shit before using this
I wrote this in a not fully awake state so I barely know how this even works (Forgot to comment it like a dumbass).

## How I think this works
Given that the settings.json file is formatted in a specific way, we can look for the Colon that precedes a setting we can change, but we also know that a comma always terminates it. So using that information we know that any piece of text between a Comma and a Colon is a data entry that we can change. This program basically just scans any JSON file you give it for those two things, and makes a list of all of them that you can change inside a GUI.

Literally just the rest of it is GUI, sorting, displaying and saving stuff (I forgor how it works).

![image](https://github.com/xavieraiden/SCSettings/assets/45552520/df3a7155-e821-4529-b555-0cdb5d5f2eb6)
