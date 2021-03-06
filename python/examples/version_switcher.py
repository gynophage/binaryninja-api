#!/usr/bin/env python
import sys
import binaryninja
import datetime

chandefault = binaryninja.UpdateChannel.list[0].name
channel = None
versions = []

def load_channel(newchannel):
	global channel
	global versions
	if (channel != None and newchannel == channel.name):
		print "Same channel, not updating."
	else:
		try:
			print "Loading channel %s" % newchannel
			channel = binaryninja.UpdateChannel[newchannel]
			print "Loading versions..."
			versions = channel.versions
		except Exception:
			print "%s is not a valid channel name. Defaulting to " % chandefault
			channel = binaryninja.UpdateChannel[chandefault]

def select(version):
	done = False
	date = datetime.datetime.fromtimestamp(version.time).strftime('%c')
	while not done:
		print "Version:\t%s" % version.version
		print "Updated:\t%s" % date
		print "Notes:\n\n-----\n%s" % version.notes
		print "-----"
		print "\t1)\tSwitch to version"
		print "\t2)\tMain Menu"
		selection = raw_input('Choice: ')
		if selection.isdigit():
			selection = int(selection)
		else:
			selection = 0
		if (selection == 2):
			done = True
		elif (selection == 1):
			if (version.version == channel.latest_version.version):
				print "Requesting update to latest version."
			else:
				print "Requesting update to prior version."
				if binaryninja.are_auto_updates_enabled():
					print "Disabling automatic updates."
					binaryninja.set_auto_updates_enabled(False)
			if (version.version == binaryninja.core_version):
				print "Already running %s" % version.version
			else:
				print "version.version %s" % version.version
				print "binaryninja.core_version %s" % binaryninja.core_version
				print "Updating..."
				print version.update()
				#forward updating won't work without reloading
				sys.exit()
		else:
			print "Invalid selection"

def list_channels():
	done = False
	print "\tSelect channel:\n"
	while not done:
		channel_list = binaryninja.UpdateChannel.list
		for index, item in enumerate(channel_list):
			print "\t%d)\t%s" % (index+1, item.name)
		print "\t%d)\t%s" % (len(channel_list)+1, "Main Menu")
		selection = raw_input('Choice: ')
		if selection.isdigit():
			selection = int(selection)
		else:
			selection = 0
		if (selection <= 0 or selection > len(channel_list)+1):
			print "%s is an invalid choice." % selection
		else:
			done = True
			if (selection != len(channel_list) + 1):
				load_channel(channel_list[selection - 1].name)

def toggle_updates():
	binaryninja.set_auto_updates_enabled(not binaryninja.are_auto_updates_enabled())

def main():
	global channel
	done = False
	load_channel(chandefault)
	while not done:
		print "\n\tBinary Ninja Version Switcher"
		print "\t\tCurrent Channel:\t%s" % channel.name
		print "\t\tCurrent Version:\t%s" % binaryninja.core_version
		print "\t\tAuto-Updates On:\t%s\n" % binaryninja.are_auto_updates_enabled()
		for index, version in enumerate(versions):
			date = datetime.datetime.fromtimestamp(version.time).strftime('%c')
			print "\t%d)\t%s (%s)" % (index + 1, version.version, date)
		print "\t%d)\t%s" % (len(versions) + 1, "Switch Channel")
		print "\t%d)\t%s" % (len(versions) + 2, "Toggle Auto Updates")
		print "\t%d)\t%s" % (len(versions) + 3, "Exit")
		selection = raw_input('Choice: ')
		if selection.isdigit():
			selection = int(selection)
		else:
			selection = 0
		if (selection <= 0 or selection > len(versions) + 3):
			print "%d is an invalid choice.\n\n" % selection
		else:
			if (selection == len(versions) + 3):
				done = True
			elif (selection == len(versions) + 2):
				toggle_updates()
			elif (selection == len(versions) + 1):
				list_channels()
			else:
				select(versions[selection - 1])


if __name__ == "__main__":
	main()
