extends GutTest

const REF: JSON=preload("res://data/catalog.json")
const TEMP: String="user://gut-stage0-"
var store: SaveStore

func before_each() -> void:
	store=SaveStore.new(TEMP+"campaign.json")
	for suffix: String in ["",".bak",".tmp"]:
		if FileAccess.file_exists(store.path+suffix): DirAccess.remove_absolute(store.path+suffix)

func test_web_damage_vectors() -> void:
	for v: Dictionary in REF.data.damage_vectors:
		assert_eq(ReferenceRules.damage(v.components,v.target,v.critical,v.blocked,REF.data.defenses.crit),int(v.expected))

func test_cancel_refund_vectors() -> void:
	for v: Dictionary in REF.data.refund_vectors:
		assert_eq(ReferenceRules.construction_refund(int(v.paid),int(v.work),int(v.progress)),int(v.expected))

func test_rng_matches_javascript_unsigned_stream() -> void:
	for v: Dictionary in REF.data.rng_vectors:
		var rng: KingdomRng=KingdomRng.new(int(v.seed))
		for expected: float in v.values: assert_eq(rng.next_u32(),int(expected))

func test_ten_seeded_campaign_starts_with_save_and_resume() -> void:
	for i in 10:
		var campaign: KingdomSession=KingdomSession.new(25*i)
		campaign.members.assign([i,(i+1)%10])
		campaign.rng.next_u32()
		assert_eq(store.write_record(campaign.encode()),OK)
		var restored: KingdomSession=store.load_session(REF.data.starters.size())
		assert_not_null(restored)
		assert_eq(restored.members,campaign.members)
		assert_eq(restored.rng.next_u32(),campaign.rng.next_u32())

func test_invalid_saves() -> void:
	var good: Dictionary={"format":1,"seed":0,"rng":0,"turn":1,"members":[0,1]}
	for bad: Dictionary in [{"format":2},{"rng":-1},{"seed":4294967296},{"turn":0},{"members":[0,0]},{"members":[0,10]},{"members":[0.5,1]},{"seed":"1"}]:
		var data: Dictionary=good.merged(bad,true)
		assert_null(KingdomSession.decode(data,10))

func test_interrupted_write_recovers_previous_slot() -> void:
	var campaign: KingdomSession=KingdomSession.new(19)
	campaign.members.assign([1,2])
	assert_eq(store.write_record(campaign.encode()),OK)
	assert_eq(DirAccess.rename_absolute(store.path,store.path+".bak"),OK)
	assert_eq(store.load_session(10).initial_seed,19)

func test_settings_survive_reopen_and_do_not_consume_rng() -> void:
	var campaign: KingdomSession=KingdomSession.new(741)
	var options: Preferences=Preferences.new(TEMP+"settings.json")
	options.speed=2
	options.gains.Music=0
	options.fullscreen=true
	options.apply_audio()
	assert_eq(options.persist(),OK)
	var restored: Preferences=Preferences.new(TEMP+"settings.json")
	assert_eq(restored.speed,2.0)
	assert_eq(restored.gains.Music,0)
	assert_true(restored.fullscreen)
	assert_true(AudioServer.is_bus_mute(AudioServer.get_bus_index("Music")))
	assert_eq(campaign.rng.state,741)
	for bus: String in Preferences.BUSES: assert_gte(AudioServer.get_bus_index(bus),0)

func test_damaged_primary_recovers_but_future_format_is_preserved() -> void:
	var campaign: KingdomSession=KingdomSession.new(197)
	campaign.members.assign([1,3])
	assert_eq(store.write_record(campaign.encode()),OK)
	assert_eq(store.write_record(campaign.encode()),OK)
	var f: FileAccess=FileAccess.open(store.path,FileAccess.WRITE)
	f.store_string("{")
	f.close()
	assert_eq(store.load_session(10).initial_seed,197)
	assert_eq(store.write_record(campaign.encode()),OK)
	var backup: SaveStore = SaveStore.new(store.path + ".bak")
	assert_eq(backup.load_session(10).initial_seed,197)
	f=FileAccess.open(store.path,FileAccess.WRITE)
	f.store_string('{"format":9}')
	f.close()
	assert_null(store.load_session(10))

func test_reference_catalog_links() -> void:
	var data: Dictionary=REF.data
	assert_eq(data.classes.size(),5)
	assert_eq(data.starters.size(),10)
	for sub: Dictionary in data.subclasses.values():
		assert_true(data.classes.has(sub.cls))
		if sub.has("parent"): assert_true(data.subclasses.has(sub.parent))
	for pack: Dictionary in data.encounters.values():
		for member: String in pack.pack: assert_true(data.monsters.has(member))
	for key: String in data.studies: assert_true(data.spells.has(key))
	assert_gt(data.recipes.size(),0)
