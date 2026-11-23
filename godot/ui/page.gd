class_name KingdomPage
extends Control

const L=preload("res://ui/layout.gd")
var host: Control

func mount(shell: Control) -> void:
	host=shell
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	build()

func build() -> void:
	pass

func act(id: String,title: String,rect: Rect2,callback: Callable,primary: bool=false) -> Button:
	return L.button(self,id,title,rect,func() -> void: host.click_sound(); callback.call(),primary)

func frame(title: String) -> void:
	L.panel(self,Rect2(16,14,608,332),Color("#16231f"),Color("#877b56"))
	L.label(self,title,Rect2(33,26,485,28),21,L.GOLD)
	L.panel(self,Rect2(33,62,574,1),Color("#626a51"),Color("#626a51"))

func back() -> void:
	host.go("menu")
