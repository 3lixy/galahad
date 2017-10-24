from	__init__ 				import *
from	People					import People
from	PersonWindow			import PersonWindow
from 	AddMenuFunctionality	import AddMenuFunctionality

from	pyforms.Controls		import ControlDockWidget

class PeopleWindow(AddMenuFunctionality, People, BaseWidget):
	"""
	This application is a GUI implementation of the People class
	"""

	def __init__(self):
		People.__init__(self)
		BaseWidget.__init__(self,'People window')
		AddMenuFunctionality.__init__(self)
		self._panel = ControlDockWidget()

		# Definition of the forms fields
		self._peopleList		= ControlList('People',
			add_function		= self.__addPersonBtnAction,
			remove_function		= self.__rmPersonBtnAction)

		self._peopleList.horizontalHeaders = ['First name', 'Middle name', 'Last name']

	def closeEvent(self, event):
		print "called on close"

	def initForm(self):
		super(PeopleWindow, self).initForm()

		self.mainmenu[0]['File'][0]['Save as'].setEnabled(False)

	def addPerson(self, person):
		"""
		Redefines the addPerson function from People class to update the GUI
		everytime a new person is added.
		"""
		super(PeopleWindow, self).addPerson(person)
		self._peopleList += [person._firstName, person._middleName, person._lastName]
		person.close()

	def removePerson(self, index):
		"""
		Redefines the addPerson function from People class to update the GUI
		every time a person is removed.
		"""
		super(PeopleWindow, self).removePerson(index)
		self._peopleList -= index

	def __addPersonBtnAction(self):
		"""
		Add person button event.
		"""
		# A new instance of the PersonWindow is opened and shown to the user.
		win = PersonWindow()
		win.parent = self
		self._panel.value = win

	def __rmPersonBtnAction(self):
		"""
		Remove person button event
		"""
		self.removePerson( self._peopleList.selected_row_index)

if __name__ == "__main__":	pyforms.start_app( PeopleWindow )
