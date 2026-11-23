extends KingdomPage

var picked: Array[int]=[]
var seed_input: LineEdit
var start: Button
var status: Label
var cards: Array[Button]=[]

func build() -> void:
	frame("Выбор первых героев")
	L.label(self,"Выбери двух героев первого уровня",Rect2(35,69,365,23),13)
	var pool: Array=host.catalog.starters
	for i in pool.size():
		var h: Dictionary=pool[i]
		var x: int=35+(i%2)*285
		var y: int=101+floori(i/2.0)*29
		var title: String="%s · %s" % [h.name,host.catalog.classes[h.cls].name]
		var b: Button=act("Candidate"+str(i),title,Rect2(x,y,275,25),choose.bind(i))
		b.tooltip_text="%s · %s" % [host.catalog.traits[h.traits[0]].name,host.catalog.traits[h.traits[1]].name]
		cards.append(b)
	L.label(self,"Зерно мира",Rect2(35,257,95,23),11,L.SOFT)
	seed_input=LineEdit.new()
	seed_input.name="Seed"
	seed_input.max_length=10
	seed_input.text=str(int(Time.get_unix_time_from_system()) & KingdomRng.MASK)
	seed_input.add_theme_font_size_override("font_size",12)
	L.place(self,seed_input,Rect2(131,257,135,23))
	status=L.label(self,"Выбрано 0 из 2",Rect2(319,257,280,22),11,L.SOFT)
	act("Back","Назад",Rect2(35,307,90,25),back)
	start=act("Start","Начать партию",Rect2(458,304,137,29),submit,true)
	start.disabled=true

func choose(i: int) -> void:
	if i in picked: picked.erase(i)
	elif picked.size()<2: picked.append(i)
	for j in cards.size():
		cards[j].modulate=Color("#f8d493") if j in picked else Color.WHITE
		cards[j].disabled=picked.size()==2 and j not in picked
	status.text="Выбрано %d из 2" % picked.size()
	start.disabled=picked.size()!=2

func submit() -> void:
	var raw: String=seed_input.text.strip_edges()
	if not raw.is_valid_int() or not KingdomSession.is_uint(raw.to_int(),KingdomRng.MASK):
		status.text="Зерно — целое от 0 до 4294967295."
		return
	host.start_session(raw.to_int(),picked)
