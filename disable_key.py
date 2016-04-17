#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_Dialog
from subprocess import Popen, PIPE
import sys
import shutil

class DisableKey( Ui_Dialog ):

	def __init__( self, dialog ):
		super( self.__class__, self ).__init__()
		self.setupUi( dialog )
		self.result.setText( self._key_list() )
		self.buttonBox.accepted.connect( self.set_value )
		
	def _key_list( self ):
		cmd = Popen( [ 'xmodmap', '-pke' ], stdout = PIPE )
		return cmd.communicate()[ 0 ].decode();

	def set_value( self ):
		if self.key_id.text().strip():
			key = int( self.key_id.text() )
			with open( '/tmp/xmodmap.backup', 'w' ) as backup:
				backup.write( self._key_list() )
			cmd = Popen( [ 'xmodmap', '-e', 'keycode %d=%s' % ( key, self.key_value.text() ) ], stdout = PIPE )
			cmd.communicate()
			self.result.setText( '%d successfully set to \'%s\nBackup saved to /tmp/xmodmap.backup' % ( key, self.key_value.text() ) )
			self.key_id.setText( '' )
			self.key_value.setText( '' )

if __name__ == '__main__':
	app = QtWidgets.QApplication( sys.argv )
	dialog = QtWidgets.QDialog()

	prog = DisableKey( dialog )
	dialog.show()
	sys.exit( app.exec_() )