from browser import document, alert,ajax,timer,prompt
from browser.html import TABLE,TH,TR,TD,BUTTON,P,PRE,TEXTAREA,INPUT,DIV,SPAN,SELECT,OPTION,DIV,SPAN,UL,LI,A,DIALOG
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
		mConsulta = self.menuOption(lang.m004, self.showBusca) # Consulta
		
		menu = document['inqueritoMenu']
		menu<= mNovo+mAbrir+self.separator()+mConsulta
		
	def menuOption(self, frase, action):
		o = LI(A(frase))
		o.bind('click', action)
		return o
	def separator(self):
		return LI(role='separator', Class="divider")
	def showAlert(self,evt):
		alert("Usuário não identificado")
		
	def showBusca(self,evt):
		document['principal'].clear()
		document['principal'] <= BuscaAlimento()

class BuscaAlimento(DIV):
	sel=None
	nutTab=None
	def __init__(self):
		DIV.__init__(self) #, style={'max-width':'90px'})
		selTable = TABLE()
		self <= selTable
		inText = INPUT(Class="form-control")
		inText.bind('keyup',self.entrou)
		selTable<=TR(TD(inText,name="intext"))
		self.sel = SELECT(size=8,Class='form-control')     # style={'max_width':'90px'})
		self.sel.bind('input',self.selec)
		selTable<=TR(TD(self.sel))
		self.sel.style.display = 'none'
		self.nutTab = MostraNut()
		self <= self.nutTab
	def entrou(self, event):
		if event.which==13:
			req = ajax.ajax()
			req.bind('complete',self.complete)
			req.open('POST','/nutsvc', True)
			req.set_header('content-type','application/x-www-form-urlencoded')
			d = {'op':'QUERY','q':event.currentTarget.value}
			req.send(d)
	def complete(self,r):
		if r.status==200 or r.status==0:
			result = json.loads(r.text)
			if len(result)==0:
				alert("Nenhum alimento encontrado")
				self.sel.style.display = 'none'
				return
			self.sel.clear()
			for l in result:
				self.sel.style.display = 'block'
				self.sel.style.width='90pw'
				self.sel<=OPTION(l[1], value=l[0])
	def selec(self, event):
		self.sel.style.display = 'none'
		alert(dir(event.currentTarget))
		medida = EscolheMedida(event.currentTarget.value, self.selected)
		self<=medida
		medida.showModal()
	def selected(self):
		alert("selected")

class EscolheMedida(DIALOG):
	inMedQty=None
	sel = None
	callback=None
	def __init__(self, idAli, cb):
		DIALOG.__init__(self)
		tab = TABLE()
		self<=tab
		self.callback = cb
		#self.inText = INPUT(Class="form-control")
		#self.inText.bind('keyup',self.entrou)
		#tab<=TR(TD('Peso (g):')+TD(self.inText))
		self.sel = SELECT(Class='form-control', size=8)     # style={'max_width':'90px'})
		##self.sel.bind('input',self.selected)
		self.inMedQty = INPUT(Class="form-control", size=4)
		tab<=TR(TD('Medida caseira, quantidade')+TD(self.inMedQty))
		tab <=TR(TD( self.sel, colspan=2))
		add = SPAN( Class='glyphicon glyphicon-ok-circle' )
		add.bind('click',self.added)
		can = SPAN( Class='glyphicon glyphicon-remove-circle' )
		can.bind('click',self.cancelled)
		tab <=TR(TD(can,style={'text-align':'right','padding':'6pw'})+TD(add,style={'text-align':'center','padding':'6pw'}))
		req = ajax.ajax()
		req.bind('complete',self.complete)
		req.open('POST','/nutsvc', True)
		req.set_header('content-type','application/x-www-form-urlencoded')
		d = {'op':'MEDIDAS','q':idAli}
		req.send(d)
	def complete(self,r):
		if r.status==200 or r.status==0:
			result = json.loads(r.text)
			for l in result:
				nome=l[0]
				if nome=='': nome= 'Peso em gramas'
				self.sel<=OPTION(nome)
	#def entrou(self, event):
	#	if event.which==13:
	#		alert("OK")
	#		self.close()
	def cancelled(self, event):
		self.close()
	def added(self,event):
		self.callback()
class MostraNut(TABLE):
	def __init__(self):
		TABLE.__init__(self, Class="table table-striped") #, style={'max-width':'90px'})
		self.style.display='none'
		#self.mostra(idNut)		
	def mostra(self, idNut):
		self.style.display='block'
		req = ajax.ajax()
		req.bind('complete',self.completeFetch)
		req.open('POST','/nutsvc', True)
		req.set_header('content-type','application/x-www-form-urlencoded')
		d = {'op':'FETCH','q':idNut}
		req.send(d)
	def completeFetch(self,r):
		if r.status==200 or r.status==0:
			result = json.loads(r.text)
			self.clear()
			if len(result)==0:
				alert("Nenhum nutriente encontrado")
				self.style.display = 'none'
				return
			for l in result:
				self.style.display = 'block'
				#self.sel.style.width='90pw'
				#self.sel<=OPTION(l[1], value=l[0])
				self<=TR(TD(l[0]) + TD(l[1]) + TD(l[2]))


class ModalBox(DIV):
	def __init__(self):
		DIV.__init__(self, Class="modal fade")
		#self.style

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
document['mymodal'].visible=True

