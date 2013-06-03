import sublime, sublime_plugin

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
			delta = -0.01
		if direction == 'down':
			items = rows
			index = cell[YMAX]
			delta = 0.01
		if direction == 'left':
			items = cols
			index = cell[XMAX]
			delta = -0.01
		if direction == 'right':
			items = cols
			index = cell[XMAX]
			delta = 0.01

		if len(items) == 2:
			return

		if index == len(items) - 1:
			index -= 1

		items[index] += delta

		layout =  {"cols": cols, "rows": rows, "cells": cells}
		self.window.set_layout(layout)
