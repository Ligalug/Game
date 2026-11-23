extends KingdomPage

func build() -> void:
	L.panel(self,Rect2(0,0,640,10),Color("#18261f"),Color("#3d503c"))
	L.panel(self,Rect2(382,21,244,318),Color("#18251f"),Color("#af9766"))
	L.panel(self,Rect2(386,25,236,310),Color("#1b2a23"),Color("#485841"))
	L.label(self,"ТУМАН",Rect2(403,47,205,41),31,L.PAPER)
	L.label(self,"И КОСТИ",Rect2(403,83,208,41),31,L.PAPER)
	L.panel(self,Rect2(405,132,193,1),L.GOLD,L.GOLD)
	act("NewCampaign","Новая партия",Rect2(404,154,201,29),func() -> void: host.go("new"),true)
	var resume: Button=act("Resume","Продолжить",Rect2(404,190,201,27),Callable(host,"resume_session"))
	resume.disabled=not host.save_store.exists()
	act("Options","Настройки",Rect2(404,223,201,27),func() -> void: host.go("settings"))
	act("Library","Справочник",Rect2(404,256,201,27),func() -> void: host.go("codex"))
	act("Exit","Выйти",Rect2(404,296,93,23),func() -> void: get_tree().quit())
	L.label(self,"0.1.0",Rect2(563,298,40,18),10,L.DIM)
