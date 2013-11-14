# Helper functions for building backup file paths.

import sublime
import os
import re
import sys
import datetime

class PathsHelper(object):

	@staticmethod
	def get_base_dir(only_base):
		platform = sublime.platform().title()
		settings = sublime.load_settings('AutoBackups ('+platform+').sublime-settings')
		# Configured setting
		backup_dir =  settings.get('backup_dir')
		now_date = datetime.datetime.now()
		date = str(now_date)[:10]

		backup_per_day =  settings.get('backup_per_day')
		if (backup_per_day and not only_base):
			backup_dir = backup_dir +'/'+ date


		if backup_dir != '':
			return os.path.expanduser(backup_dir)

		# Windows: <user folder>/My Documents/Sublime Text Backups
		if (sublime.platform() == 'windows'):
			backup_dir = 'D:/Sublime Text Backups'
			if (backup_per_day and not only_base):
				backup_dir = backup_dir +'/'+ date
			return backup_dir

		# Linux/OSX/other: ~/sublime_backups
		backup_dir = '~/.sublime/backups'
		if (backup_per_day and not only_base):
			backup_dir = backup_dir +'/'+ date
		return os.path.expanduser(backup_dir)

	@staticmethod
	def timestamp_file(filename):
		(filepart, extensionpart) = os.path.splitext(filename)
		return '%s%s' % (filepart, extensionpart,)

	@staticmethod
	def get_backup_path(filepath):
		path = os.path.expanduser(os.path.split(filepath)[0])
		backup_base = PathsHelper.get_base_dir(False)
		path = PathsHelper.normalise_path(path)
		return os.path.join(backup_base, path)

	@staticmethod
	def normalise_path(path, slashes = False):

		if sublime.platform() != 'windows':
			# remove any leading / before combining with backup_base
			path = re.sub(r'^/', '', path)
			return path

		path = path.replace('/', '\\')


		# windows only: transform C: into just C
		path = re.sub(r'^(\w):', r'\1', path)

		# windows only: transform \\remotebox\share into network\remotebox\share
		path = re.sub(r'^\\\\([\w\-]{2,})', r'network\\\1', path)

		if slashes:
			path = path.replace('\\', '/')

		return path



	@staticmethod
	def get_backup_filepath(filepath):
		filename = os.path.split(filepath)[1]
		return os.path.join(PathsHelper.get_backup_path(filepath), PathsHelper.timestamp_file(filename))
