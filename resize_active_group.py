import sublime, sublime_plugin

settings_file = "resize_active_group.sublime-settings"
settings = None

# Loads the settings specified by 'settings_file' and adds a callback to be called every time
# the 'settings_file' changes.
def plugin_loaded():
	global settings

	settings = sublime.load_settings(settings_file)
	settings.add_on_change(settings_file, load_deltas)
	load_deltas()

# Loads the four different delta values used by the 'ResizeActiveGroupCommand'.
# It is called by 'plugin_loaded' and every time the 'settings_file' changes.
def load_deltas():
	global delta_up, delta_down, delta_left, delta_right
	global padding_up, padding_down, padding_left, padding_right

	delta_default = settings.get("resize_delta_default", 0.01)
	delta_up = settings.get("resize_delta_up", delta_default)
	delta_down = settings.get("resize_delta_down", delta_default)
	delta_left = settings.get("resize_delta_left", delta_default)
	delta_right = settings.get("resize_delta_right", delta_default)

	vertical_padding_default = settings.get("resize_vertical_padding_default", 0.05)
	horizontal_padding_default = settings.get("resize_horizontal_padding_default", 0.03)

	padding_up = settings.get("resize_padding_up", vertical_padding_default)
	padding_down = settings.get("resize_padding_down", vertical_padding_default)
	padding_left = settings.get("resize_padding_left", horizontal_padding_default)
	padding_right = settings.get("resize_padding_right", horizontal_padding_default)

XMIN, YMIN, XMAX, YMAX = range(4)

class ResizeActiveGroupCommand(sublime_plugin.WindowCommand):

	def run(self, direction):

		layout = self.window.get_layout()
		cols = layout['cols']
		rows = layout['rows']
		cells = layout['cells']

		group = self.window.active_group()

		cell = cells[group]

		items = None
		index = 0
		delta = 0

		if direction == 'up':
			items = rows
			index = cell[YMAX]
			delta = -delta_up
			padding = padding_up

		if direction == 'down':
			items = rows
			index = cell[YMAX]
			delta = delta_down
			padding = padding_down

		if direction == 'left':
			items = cols
			index = cell[XMAX]
			delta = -delta_left
			padding = padding_left

		if direction == 'right':
			items = cols
			index = cell[XMAX]
			delta = delta_right
			padding = padding_right

		if len(items) == 2:
			return

		if index == len(items) - 1:
			index -= 1

		min_value = 0 + padding
		max_value = 1 - padding
		new_value = round(items[index] + delta, 2)
		new_value = max(new_value, min_value)
		new_value = min(new_value, max_value)
		items[index] = new_value

		layout =  {"cols": cols, "rows": rows, "cells": cells}
		self.window.set_layout(layout)

# The 'plugin_loaded' is automatically called by ST3 when the API is ready.
# If we're using ST2, it has to be called explicitly.
if not int(sublime.version()) > 3000:
	plugin_loaded()
