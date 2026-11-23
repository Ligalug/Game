class_name KingdomLayout
extends RefCounted

# Предварительно, A01. Цвета меню уточняются по утверждённым листам.
const INK: Color = Color("#141f1b")
const PAPER: Color = Color("#eee3c3")
const GOLD: Color = Color("#dfc080")
const SOFT: Color = Color("#bec4a9")
const DIM: Color = Color("#83947c")

static func place(parent: Control, node: Control, rect: Rect2) -> void:
	parent.add_child(node)
	node.position = rect.position
	node.size = rect.size

static func box(fill: Color, edge: Color) -> StyleBoxFlat:
	var style: StyleBoxFlat = StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = edge
	style.set_border_width_all(1)
	style.content_margin_left = 7
	style.content_margin_right = 7
	style.content_margin_top = 1
	style.content_margin_bottom = 1
	return style

static func panel(parent: Control, rect: Rect2, fill: Color = INK, edge: Color = Color("#59644c")) -> Panel:
	var node: Panel = Panel.new()
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	node.add_theme_stylebox_override("panel", box(fill,edge))
	place(parent,node,rect)
	return node

static func label(parent: Control,value: String,rect: Rect2,px: int=12,color: Color=PAPER) -> Label:
	var node: Label = Label.new()
	node.text = value
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	node.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	node.add_theme_font_size_override("font_size",px)
	node.add_theme_color_override("font_color",color)
	place(parent,node,rect)
	return node

static func button(parent: Control,id: String,value: String,rect: Rect2,callback: Callable,primary: bool=false) -> Button:
	var b: Button = Button.new()
	b.name=id
	b.text=value
	b.mouse_default_cursor_shape=Control.CURSOR_POINTING_HAND
	b.add_theme_font_size_override("font_size",12)
	b.add_theme_color_override("font_color",INK if primary else PAPER)
	b.add_theme_color_override("font_focus_color",INK if primary else PAPER)
	b.add_theme_color_override("font_hover_color",PAPER)
	b.add_theme_stylebox_override("normal",box(GOLD if primary else Color("#25372d"),Color("#aa9264") if primary else Color("#51624c")))
	b.add_theme_stylebox_override("pressed",box(Color("#4d5943"),GOLD))
	b.add_theme_stylebox_override("hover",box(Color("#4a5946"),GOLD))
	b.add_theme_stylebox_override("disabled",box(Color("#1b2822"),Color("#384b3c")))
	var focus: StyleBoxFlat=box(Color.TRANSPARENT,GOLD)
	focus.draw_center=false
	b.add_theme_stylebox_override("focus",focus)
	b.pressed.connect(callback)
	place(parent,b,rect)
	return b
