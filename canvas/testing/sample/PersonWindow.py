from	pysettings			import conf;
import	settings
conf+=	settings

import	pyforms
from 	pyforms				import BaseWidget
from	pyforms.Controls	import ControlText
from	pyforms.Controls	import ControlButton
from	Person				import Person

class PersonWindow(Person, BaseWidget):
	def __init__(self):
		Person.__init__(self, '', '', '')
		BaseWidget.__init__(self, 'Person window')
		self.parent = None

		# Definition of the forms fields
		self._firstnameField	= ControlText('First name')
		self._middlenameField	= ControlText('Middle name')
		self._lastnameField		= ControlText('Lastname')
		self._fullnameField		= ControlText('Full name')
		self._buttonField		= ControlButton('Press this button')

		self._buttonField.value = self.buttonAction

		self.formset = ['_firstnameField', '_middlenameField', '_lastnameField', '_fullnameField',
			(' ','_buttonField', ' '), ' ']

	def buttonAction(self):
		self._firstName = self._firstnameField.value
		self._middleName = self._middlenameField.value
		self._lastName = self._lastnameField.value
		self._fullnameField.value = self.fullName

		# In case the window has a parent
		if self.parent!=None: self.parent.addPerson(self)

	def printFullName(self):
		print( self._fullnameField.value)

if __name__ == "__main__":	pyforms.start_app( PersonWindow )
