from browser import document, alert,ajax,timer,prompt
from browser.html import TABLE,TR,TD,BUTTON,P,PRE,TEXTAREA,INPUT,DIV,SPAN,SELECT,OPTION,DIV,SPAN,UL,LI,A
import browser
import json

import langdata as lang

class MainMenu():
	
	def __init__(self):
		dropDownInq = document['inqueritoMenuDropDown']
		dropDownInq.text = lang.m001 # Inquéritos
		dropDownInq<= SPAN(Class="caret")

		mNovo = self.menuOption(lang.m002, self.showAlert) # Novo
		mAbrir = self.menuOption(lang.m003, self.showAlert) #  Abrir
		mConsulta = self.menuOption(lang.m004, self.showAlert) # Consulta
		
		menu = document['inqueritoMenu']
		menu<= mNovo+mAbrir+self.separator()+mConsulta
	def showAlert(self,evt):
		alert("Usuário não identificado")
	def menuOption(self, frase, action):
		o = LI(A(frase))
		o.bind('click', action)
		return o
	def separator(self):
		return LI(role='separator', Class="divider")
		

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
	alert(evt.currentTarget)
	#evt.currentTarget.set_class_name('disabled')

#Principal = BuscaAlimento()
#document['principal'] <= Menu() #Principal
#document['inqueritoMenu']<=LI(A("Novo",href="#"))
#document['inqueritoMenu']<=LI(A("Abrir",href="#"))
#document['novoInquerito'].bind('click',showAlert)

#document <=Menu()
#document['menu'].bind('click',showAlert)
m = MainMenu()

