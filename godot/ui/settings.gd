extends KingdomPage

const TITLES: Array[String]=["Общая","Музыка","Эффекты","Интерфейс","Окружение"]
func build() -> void:
	frame("Настройки")
	L.label(self,"ГРОМКОСТЬ",Rect2(35,68,230,19),10,L.GOLD)
	L.label(self,"ИЗОБРАЖЕНИЕ И ДВИЖЕНИЕ",Rect2(334,68,268,19),10,L.GOLD)
	for i in Preferences.BUSES.size():
		var bus: String=Preferences.BUSES[i]
		var y: int=97+i*32
		L.label(self,TITLES[i],Rect2(35,y,80,20),11)
		var meter: Label=L.label(self,"%d%%" % host.prefs.gains[bus],Rect2(238,y,36,20),10,L.SOFT)
		var slider: HSlider=HSlider.new()
		slider.name=bus
		slider.max_value=100
		slider.step=1
		slider.value=host.prefs.gains[bus]
		slider.value_changed.connect(func(v:float) -> void:
			host.prefs.gains[bus]=int(v)
			host.prefs.apply_audio()
			meter.text="%d%%" % int(v)
			save_settings())
		L.place(self,slider,Rect2(110,y+3,120,16))
		var listen: Button=act("Listen"+bus,"♪",Rect2(274,y,26,20),func() -> void: host.audition(bus))
		listen.tooltip_text="Прослушать · "+TITLES[i]
	var full: CheckButton=CheckButton.new()
	full.name="Fullscreen"
	full.text="Полный экран"
	full.add_theme_font_size_override("font_size",12)
	full.button_pressed=host.prefs.fullscreen
	full.toggled.connect(func(on:bool) -> void:
		host.prefs.fullscreen=on
		host.prefs.apply_window()
		save_settings())
	L.place(self,full,Rect2(334,94,248,28))
	L.label(self,"Скорость анимаций",Rect2(334,138,240,20))
	for i in Preferences.SPEEDS.size():
		var v: float=Preferences.SPEEDS[i]
		act("Speed"+str(i),str(v).trim_suffix(".0")+"×",Rect2(334+i*59,164,53,23),func() -> void:
			host.prefs.speed=v
			save_settings()
			host.refresh_page(),is_equal_approx(host.prefs.speed,v))
	L.label(self,"Предпросмотр движения",Rect2(334,204,246,17),10,L.SOFT)
	L.panel(self,Rect2(337,232,225,2),L.DIM,L.DIM)
	var marker: Panel=L.panel(self,Rect2(337,228,8,9),L.GOLD,L.GOLD)
	var tween: Tween=create_tween().set_loops()
	tween.tween_property(marker,"position:x",553,1.4/host.prefs.speed).set_trans(Tween.TRANS_SINE)
	tween.tween_property(marker,"position:x",337,1.4/host.prefs.speed).set_trans(Tween.TRANS_SINE)
	L.label(self,"Настройки сохраняются автоматически",Rect2(35,277,530,19),11,L.SOFT)
	act("Back","Назад",Rect2(35,307,90,25),back)

func save_settings() -> void:
	if host.prefs.persist()!=OK: host.alert("Не удалось сохранить настройки на диск.")
