from abc import ABCMeta, abstractmethod

import os, sublime, sublime_plugin


class FileUtils:
	@staticmethod
	def get_path_array(fullpath):
		return str(fullpath).split(os.path.sep)

	@staticmethod
	def get_filename(fullpath):
		return FileUtils.get_path_array(fullpath)[-1]

	@staticmethod
	def get_only_path(fullpath):
		path = ""
		patharray = FileUtils.get_path_array(fullpath)
		patharraylen = len(patharray)

		for i in range(patharraylen):
			if (i < patharraylen - 1):
				path = path  + (os.path.sep if i > 0 else "") + patharray[i]

		return path if path != "" else "None"

class WindowsUtils:
	@staticmethod
	def get_windowsindex(view):
		views = view.window().views()
		sorted(views, key=lambda view: view.buffer_id())

		for i in range(len(views)):
			if views[i] == view:
				return i + 1

		return None

	@staticmethod
	def get_windowscount(view):
		return len(view.window().views())

	@staticmethod
	def get_index_and_count(view):
		if WindowsUtils.get_windowsindex(view) is None:
			return "None"
		else:
			return str(WindowsUtils.get_windowsindex(view)) + "/" + str(WindowsUtils.get_windowscount(view))

class Status:
	__metaclass__ = ABCMeta

	@abstractmethod
	def update(self,view):
		pass

class IndexStatus(Status):
	def __init__(self,view):
		self.update(view)

	def set_index(self,view):
		return "Index: " + WindowsUtils.get_index_and_count(view)

	def update(self,view):
		view.erase_status('a_indexStatus')
		view.set_status('a_indexStatus', self.set_index(view))

class FileStatus(Status):
	def __init__(self, view):
		self.update(view)

	def set_filename(self,view):
		return "File: " + FileUtils.get_filename(view.file_name())

	def update(self, view):
		view.erase_status('b_fileStatus')
		view.set_status('b_fileStatus', self.set_filename(view))

class PathStatus(Status):
	def __init__(self, view):
		self.update(view)

	def set_path(self,view):
		return "Path: " + FileUtils.get_only_path(view.file_name())

	def update(self, view):
		view.erase_status('c_pathStatus')
		view.set_status('c_pathStatus', self.set_path(view))


class CustomStatusBar:
	def __init__(self, view):
		self.index = IndexStatus(view)
		self.filename = FileStatus(view)
		self.path = PathStatus(view)

	def update(self,view):
		self.index.update(view)
		self.filename.update(view)
		self.path.update(view)

	@staticmethod
	def reload(view):
		if CustomStatusBar.bar == None:
			CustomStatusBar.bar = CustomStatusBar(view)

		CustomStatusBar.bar.update(view)

CustomStatusBar.bar = None


class FilesInfoStatusBarListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		CustomStatusBar.reload(view)
