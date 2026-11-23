extends KingdomPage

const GROUPS: Array[String]=["classes","subclasses","monsters","buildings","spells","decrees","recipes"]
const TITLES: Array[String]=["Классы","Подклассы","Существа","Постройки","Магия","Указы","Рецепты"]
var items: ItemList=ItemList.new()
var detail: RichTextLabel=RichTextLabel.new()
var section: String=""
var keys: Array=[]

func build() -> void:
	frame("Справочник королевства")
	for i in GROUPS.size():
		act("Tab"+str(i),TITLES[i],Rect2(33+82*i,72,80,23),open_group.bind(i))
	items.add_theme_font_size_override("font_size",12)
	items.item_selected.connect(show_entry)
	L.place(self,items,Rect2(33,105,216,185))
	detail.add_theme_font_size_override("normal_font_size",13)
	L.place(self,detail,Rect2(268,112,326,168))
	act("Back","Назад",Rect2(35,307,90,25),back)
	open_group(0)

func open_group(index: int) -> void:
	section=GROUPS[index]
	items.clear()
	keys.clear()
	for key: String in host.catalog[section]:
		var record: Dictionary=host.catalog[section][key]
		if record.get("external_definition",false) or (section=="buildings" and key in host.catalog.legacy_buildings): continue
		if section=="decrees" and key in host.catalog.retired_decrees: continue
		keys.append(key)
		items.add_item(record.get("name",key))
	if keys.size()>0:
		items.select(0)
		show_entry(0)

func show_entry(index: int) -> void:
	var record: Dictionary=host.catalog[section][keys[index]]
	var lines: PackedStringArray=[record.get("name",keys[index])]
	if record.has("cls"): lines.append(str(host.catalog.classes[record.cls].name))
	if record.has("text"): lines.append(record.text)
	var fields: Dictionary={"hp":"ОЗ","damage":"Базовый урон","range":"Дальность","speed":"Скорость","cost":"Стоимость","work":"Производство","mana":"Мана","gold":"Золото","crystal":"Кристаллы"}
	for key: String in fields:
		if record.has(key): lines.append("%s  %s" % [fields[key],str(record[key]).trim_suffix(".0")])
	detail.text="\n\n".join(lines)
