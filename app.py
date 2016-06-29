from browser import document, alert,ajax,timer,prompt
from browser.html import TABLE,TR,TD,BUTTON,P,PRE,TEXTAREA,INPUT,DIV,SPAN,SELECT,OPTION,DIV,SPAN,UL,LI,A
import browser
import json

class Menu(DIV):
	def __init__(self):
		DIV.__init__(self)
		self.style= {'Class':'dropdown'}
		self <= BUTTON("Inquéritos"+SPAN(Class="caret"),Class="btn btn-default dropdown-toggle",data-toggle="dropdown" )#, aria-haspopup="true", aria-expanded="true")
		menuInq = UL(Class="dropdown-menu")
		menuInq <= LI(A("Novo",href="#"))
		self <= menuInq
		#alert(dir(self))
class BuscaAlimento(TABLE):
	def __init__(self):
		TABLE.__init__(self)
		inText = INPUT()
		inText.bind('keyup',self.entrou)
		self<=TR(TD(inText,name="intext"))
	def entrou(self, event):
		if event.which==13:
			req = ajax.ajax()
			req.bind('complete',self.complete)
			req.open('POST','/nutsvc', True)
			req.set_header('content-type','application/x-www-form-urlencoded')
			d = {'qali':event.currentTarget.value}
			req.send(d)
	def complete(self,r):
		if r.status==200 or r.status==0:
			result = json.loads(r.text)
			sel = SELECT(size=8)
			sel.bind('click',self.selec)
			self<=TR(TD(sel))
			for l in result:
				sel<=OPTION(l[1], value=l[0])
	def selec(self, event):
		alert(	event.currentTarget.value)	


def showAlert(evt):
	alert(dir(evt.currentTarget))
	evt.currentTarget.set_class_name('disabled')

Principal = BuscaAlimento()
#document['principal'] <= Menu() #Principal
document['inqueritoMenu']<=LI(A("N",href="#"))

#document['novoInquerito'].bind('click',showAlert)

document <=Menu()
#document['menu'].bind('click',showAlert)

