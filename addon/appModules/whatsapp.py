﻿# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
from NVDAObjects.IAccessible.ia2Web import Ia2Web
import api
import winUser
import controlTypes
from ui import message as msg
import winsound
from logHandler import log

class AppModule(appModuleHandler.AppModule):
	recordVerify = False
	disableBrowseModeByDefault=True

	def event_NVDAObject_init(self, obj):
		try:
			if obj.IA2Attributes["class"] == 'dNn0f':
				obj.name = "Mensaje de voz"
			elif obj.IA2Attributes["class"] == 'SncVf _3doiV':
				obj.name = "Reenviar el mensaje"
			elif obj.IA2Attributes["class"] == 'SncVf _3doiV':
				obj.name = "Enviando..."
		except:
			pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if hasattr(obj, "IA2Attributes") and 'message-' in obj.IA2Attributes['class']:
				clsList.insert(0, WhatsAppMessage)
		except:
			pass

	@script(
	description="Presiona y suelta el botón de grabación",
	category="WhatsApp",
	gesture="kb:control+r")
	def script_record(self, gesture):
		focus = api.getFocusObject()
		try:
			if self.recordVerify == True:
				self.recordVerify = False
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Information Bar.wav", winsound.SND_FILENAME)
			elif focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text' and focus.value == '':
				self.recordVerify = True
				recButton = focus.parent.parent.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)
			elif focus.parent.IA2Attributes['class'] == '_11liR':
				self.recordVerify = True
				recButton = focus.parent.parent.parent.next.firstChild.firstChild.next.next.next.firstChild
				api.moveMouseToNVDAObject(recButton)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winsound.PlaySound("C:\Windows\Media\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)
		except KeyError:
			pass

	@script(
		description="Presiona el botón para adjuntar",
		category="WhatsApp",
		gesture="kb:control+shift+a"
	)
	def script_toAttach(self, gesture):
		focus = api.getFocusObject()
		if focus.IA2Attributes['class'] == '_2_1wd copyable-text selectable-text':
			toAttachButton = focus.parent.parent.previous.firstChild
			api.moveMouseToNVDAObject(toAttachButton)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			msg("Esta opción solo está disponible desde el cuadro de edición de mensaje")

	@script(
		description="Abre el link del mensaje en el navegador predeterminado del sistema",
		category="WhatsApp",
		gesture="kb:control+l"
	)
	def script_linkOpen(self, gesture):
		obj = api.getFocusObject()
		for o in obj.recursiveDescendants:
			if getattr(o, "role", None) == controlTypes.ROLE_LINK:
				o.doAction()
				break

	@script(
		description="Copia el texto del mensaje con el foco al portapapeles",
		category="WhatsApp",
		gesture="kb:control+shift+c"
	)
	def script_textCopy(self, gesture):
		focus = api.getFocusObject()
		if focus.role == controlTypes.ROLE_SECTION:
			list= [str.name for str in focus.recursiveDescendants if str.role == controlTypes.ROLE_STATICTEXT and str.name != None]
			if list[0] == "~":
				message = ". ".join(list[1:-1])
				api.copyToClip(message)
				msg("Copiado")
			else:
				message = ". ".join(list[:-1])
				api.copyToClip(message)
				msg("Copiado")
		else:
			msg("Solo disponible desde la lista de mensajes")

	@script(
		description="Enviar el archivo adjunto",
		category="WhatsApp",
		gesture="kb:control+s"
	)
	def script_sendAttach(self, gesture):
		focus = api.getFocusObject()
		if focus.firstChild.role == controlTypes.ROLE_BUTTON:
			focus.firstChild.doAction()
			focus.setFocus()

	@script(
		category="WhatsApp",
		description="Se mueve al mensaje respondido",
		gesture="kb:shift+enter"
	)
	def script_replyMessage(self, gesture):
		focus = api.getFocusObject()
		for fc in focus.recursiveDescendants:
			try:
				if fc.IA2Attributes['class'] == '_3Ppzm':
					fc.doAction()
					msg("Enfocando el mensaje respondido...")
					break
			except:
				pass

	@script(
		category="WhatsApp",
		description="Activa el menú del chat",
		gesture="kb:control+m"
	)
	def script_menuButton(self, gesture):
		focus = api.getFocusObject()
		if not hasattr(focus, 'IA2Attributes'): return
		if focus.parent.IA2Attributes['class'] == '_11liR':
			titleObj = focus.parent.parent.parent.previous.previous
			if titleObj.childCount == 7:
				titleObj.children[5].firstChild.doAction()
				msg("Menú del chat")
			elif titleObj.childCount == 5:
				titleObj.children[3].firstChild.doAction()
				msg("Menú del chat")

	@script(
		category="WhatsApp",
		description="Activa el botón menú general",
		gesture="kb:control+g"
	)
	def script_generalMenuButton(self, gesture):
		focus = api.getFocusObject()
		if not hasattr(focus, 'IA2Attributes'): return
		if focus.parent.IA2Attributes['class'] == '_11liR':
			focus.parent.parent.parent.parent.parent.previous.firstChild.firstChild.firstChild.next.next.next.firstChild.doAction()
			msg("Menú general")

	@script(
		category="WhatsApp",
		description="Pulsa en el botón descargar cuando el mensaje contiene un archivo descargable",
		gesture="kb:alt+enter"
	)
	def script_fileDownload(slef, gesture):
		fc = api.getFocusObject()
		for h in fc.recursiveDescendants:
			try:
				if h.IA2Attributes['class'] == '_1UTQ6 _1s_fV':
					h.doAction()
					break
			except:
				pass

class WhatsAppMessage(Ia2Web):
	def initOverlayClass(self):
		for hs in self.recursiveDescendants:
			try:
				if hs.IA2Attributes['class'] == '_2HtgQ':
					self.bindGestures({"kb:enter":"playMessage"})
					break
			except KeyError:
				pass

	@script(
		category="WhatsApp",
		description="Pulsa el botón de reproducción	 en los mensajes de voz",
	)
	def script_playMessage(self, gesture):
		for f in self.recursiveDescendants:
			try:
				if f.IA2Attributes['class'] == '_2HtgQ':
					f.doAction()
					self.setFocus()
					break
			except KeyError:
				pass
