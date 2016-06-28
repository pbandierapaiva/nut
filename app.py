from browser import document, alert,ajax,timer,prompt
from browser.html import TABLE,TR,TD,BUTTON,P,PRE,TEXTAREA,INPUT,DIV,SPAN,SELECT,OPTION
import browser
import json


class BuscaAlimento(TABLE):
		def __init__(self):
			TABLE.__init__(self)
			inText = INPUT()
			inText.bind('keyup',self.entrou)
			self<=TR(TD(inText,colspan=2,name="intext"))
			#alert(str(dir(window)))
			#window.console()
			#win.focus(document.get(name ='intext'))
			#alert(dir(browser))
		def entrou(self, event):
			if event.which==13:
#				alert("ENTROU")
				req = ajax.ajax()
				req.bind('complete',self.complete)
				req.open('POST','/nutsvc', True)
				req.set_header('content-type','application/x-www-form-urlencoded')
				#d = ldata.copy()
#				d['w']='FETCH'
				#d['qali'] =      
				d = {'qali':event.currentTarget.value}
				req.send(d)#d)
		def complete(self,r):
			if r.status==200 or r.status==0:
				result = json.loads(r.text)
				#self<=TR(TD(s))
				sel = SELECT(size=8)
				sel.bind('click',self.selec)
				self<=TR(TD(sel))
				for l in result:
					#elem = TD(l[1], id=l[0])
					#elem.bind('click',self.selec)
					#self<=TR(elem)
					sel<=OPTION(l[1], value=l[0])
		def selec(self, event):
			alert(	event.currentTarget.value) #selectedIndex )		
def abreM(evt):
	global modalBox, modclose
	#modal = document.get(name="buscalimento")
	modalBox.set_style({"display":"block"})
#	alert(dir(modalBox))

def fechaM(evt):
	global modalBox
	modalBox.set_style({"display":"none"})


modalBox = DIV(name="buscalimento", Class="modal")
modbusca = DIV(Class="modal-content")
modclose = SPAN("x",Class="close")
modclose.bind('click',fechaM)
modbusca <= modclose + P("MODAL")
modalBox <=modbusca

abreModal = BUTTON("Busca alimento")
abreModal.bind('click',abreM)
Principal = BuscaAlimento()
document['principal'] <= abreModal + Principal


