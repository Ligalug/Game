extends KingdomPage

func build() -> void:
	frame("Летопись партии")
	var state: KingdomSession=host.session
	L.label(self,host.catalog.houses[0],Rect2(35,80,320,35),21,L.GOLD)
	L.label(self,"Столица · "+str(host.catalog.cities[0]),Rect2(35,118,335,22),13)
	L.label(self,"Ход %d     ·     Зерно %d" % [state.turn,state.initial_seed],Rect2(35,146,480,22),12,L.SOFT)
	L.label(self,"ПЕРВЫЙ ОТРЯД",Rect2(35,187,360,17),10,L.GOLD)
	for i in state.members.size():
		var hero: Dictionary=host.catalog.starters[state.members[i]]
		var stats: Dictionary=host.catalog.classes[hero.cls]
		var x: int=35+285*i
		L.panel(self,Rect2(x,211,272,60))
		L.label(self,"%s  ·  %s" % [hero.name,stats.name],Rect2(x+10,218,251,20),14)
		L.label(self,"Уровень 1     ОЗ %d     Дальность %d" % [stats.hp,stats.range],Rect2(x+10,244,250,17),11,L.SOFT)
	act("Back","В меню",Rect2(35,307,92,25),back)
	act("Save","Сохранить",Rect2(455,303,138,29),func() -> void: host.save_session(true),true)
