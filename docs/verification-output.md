# Recovered-build verification

2026-10-29. Host only; no hardware connected.

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.014s

OK
fm6: algorithms: the classic carrier counts of all 32 (operators on the output bus)             ok
fm6: algorithms: each of the 32 sounds with every operator at full level                        ok
fm6: algorithms: more carriers, more level (1 .. 6)                                             ok
fm6: envelope: attack -> L1, decay -> L2 -> L3, held while the key is down, then the release (in order) ok
fm6: envelope: the voice ends after the release (engine done), not while the key is held        ok
fm6: envelope: attack rate 60 slower than 80 slower than 99; 99 within a block or two           ok
fm6: envelope: attack to L1 in 78 / 8 / 1 blocks (rates 60 / 80 / 99), L1 reached at block 77
fm6: envelope: a decayed note ends while its key is held (L3 0), its voice free                 ok
fm6: retrigger: a note from silence renders the same samples twice                              ok
fm6: retrigger: the same key again while it sounds: no step larger than the tone's own          ok
fm6: factory patches C1..C7, velocity 30 / 127: peak 11710 (VOICE_FS 24000), |mean| at most 1.2
fm6: no clipping: every factory patch, C1..C7, velocity 30 and 127: a voice below 2 x VOICE_FS  ok
fm6: no DC: |mean| below 1 % of VOICE_FS                                                        ok
fm6: MLVL -40 / 0 / +40: centroid 131 / 146 / 793 Hz
fm6: MLVL: + brighter, - darker                                                                 ok
fm6: MRAT 0 / +3: centroid 146 / 203 Hz
fm6: MRAT: + raises the modulators' ratios (brighter)                                           ok
fm6: MEG 0 / +50: centroid at 0.5 s 132 / 179 Hz
fm6: MEG: + the modulators decay slower (brighter later)                                        ok
fm6: VMOD 0 / +5: centroid ratio vel 127 / 40 1.13 / 1.45
fm6: VMOD: + velocity moves the brightness more                                                 ok
fm6: FB 0 / +6 (OP6 alone): centroid 131 / 11044 Hz
fm6: FB: + more feedback (brighter)                                                             ok
fm6: ALG: 1..32 replaces the patch's algorithm, PAT (0) keeps it                                ok
fm6: DTUN 0 / 127 (3 carriers): level swing over 50 ms windows 1.012 / 18.403
fm6: DTUN: the carriers apart: they beat                                                        ok
fm6: SLOT OWN: the track's patch stays (nothing reloads)                                        ok
fm6: SLOT F5 loads the fifth factory patch (main loop)                                          ok
fm6: SLOT back to OWN: the own patch again                                                      ok
fm6: SLOT: F1..F8 and OWN, nothing past it                                                      ok
fm6: fm6_adopt: a factory patch unchanged shows its slot                                        ok
fm6: fm6_adopt: edited, it is the track's own (OWN)                                             ok
fm6: fm6_adopt: an old B slot holding factory F7 shows F7                                       ok
fm6: AMS 1, AMD  0: centroid  475 Hz (AMS 0:  529 Hz)
fm6: AMS 2, AMD  0: centroid  475 Hz (AMS 0:  529 Hz)
fm6: AMS 3, AMD  0: centroid  475 Hz (AMS 0:  529 Hz)
fm6: AMS 1, AMD 99: centroid  446 Hz (AMS 0:  529 Hz)
fm6: AMS 2, AMD 99: centroid  418 Hz (AMS 0:  529 Hz)
fm6: AMS 3, AMD 99: centroid  286 Hz (AMS 0:  529 Hz)
fm6: AMS 1..3, AMD 0: at most 13.3 % from the AMS 0 voice
fm6: AMS 1..3 (AMD 0 and 99): tonal, the centroid near the AMS 0 one (not noise)                ok
fm6: AMS 1..3, AMD 0: the voice within 25 % of the AMS 0 one; every voice below 2 x VOICE_FS    ok
fm6: pack(unpack(x)) == x: the factory patches and the init voice (generator and C agree)       ok
fm6: any 128 bytes unpack into range (2000 random records)                                      ok
fm6: a 32-voice bank SysEx: checksum, its 32 records back as they were                          ok
fm6: a single-voice SysEx (155 bytes): back to the same packed record                           ok
fm6: voices: 8 keys in POLY: 6 voices (the engine's cap)                                        ok
fm6: voices: all free some seconds after the release (the operator envelopes end them)          ok
fm6: cost: no instruction counter on this host (proc_pid_rusage); not measured
fm6_test: all checks ok
smk flash: no protected sector passes the app's allow-list (erase, page)                          ok
smk flash: no protected sector passes the loader's allow-list                                     ok
smk flash: the RAM driver's own net (FL_PROTECTED) covers every protected sector                  ok
smk flash: straddling ranges refused: 0xBF000+0x2000, 0xE9000+0x2000, 0x3000+0x2000               ok
smk flash: wrapping ranges refused (off + n past 4 GiB)                                           ok
smk flash: app windows: FL_DATA 0x9D000-0xBAFFF, FL_OTA 0xBB000-0xBFFFF, USRFLASH 0xC2000-0xE9FFF, the marker ok
smk flash: the stock marker's sector 0xEA000: the whole sector only (its erase), never a page or a range into it ok
smk flash: loader: app area 0x4000-0x9CFFF, records 0x9D000-0xBFFFF only                          ok
smk flash: storage.c: every OBJ_* (A and B) in FL_DATA below the owner tag, no two objects in one sector ok
smk flash: the owner tag 0xAF000: in FL_DATA, its own sector                                      ok
smk flash: the pattern pool: 20 sectors 0xD6000-0xE9FFF in USRFLASH, nobody else's                ok
smk flash: the user sample slot USR1: 80 KiB 0xC2000-0xD5FFF in USRFLASH, nobody else's           ok
smk flash: the rest of the windows: 11 spare store sectors 0xB0000-0xBAFFF, the OTA staging, the marker ok
smk flash: storage.c: projects from 0x9D000, settings 0xAD000/0xAE000, the autosave 0xA9000/0xAA000 ok
smk flash: FL_PLAIN_LO = the VM start 0x9D000                                                     ok
smk flash: FL_JEDEC_OK: the SMK part 0xEB6014 and the FM-1's 0x856014 only                        ok
smk flash test passed
smk owner: the tag: "SMK37DATA" + the family SKIFF, zero padded to 16 bytes                     ok
smk owner: another firmware's store (Felucca's tag): cleared, tagged SKIFF                      ok
smk owner: ... the pool's chunks erased, its other sectors left (their first erase is the pool's) ok
smk owner: ... calibration (USRTRIM), the user sample and a spare sector untouched              ok
smk owner: our own store: kept as it is, the pool too                                           ok
smk owner: an untagged store (FELUCCA_DATA_UNTAGGED_OK 0): cleared, tagged                      ok
smk owner: a tag that only starts with ours: not ours                                           ok
smk owner: the first boot over the intact stock mapping: USRFLASH and its marker kept, no pool erase ok
smk owner: ... and at the next boot (ours now)                                                  ok
smk owner: the first write into USRFLASH: the marker's sector erased, once                      ok
smk owner: ... and only once                                                                    ok
smk owner: the stock layout checked: its settings' magic, each preset's head and erased tail    ok
smk owner: the marker over our pool: released at boot, the pool kept                            ok
smk owner: no marker: its sector never erased                                                   ok
smk owner: nothing erased or written outside the pairs, the pool, the tag and the marker        ok
smk owner test passed
smk ui: SMK pads: on HOME the steps (taps for the UI), not notes                               ok
smk ui: SMK pads: the DRUM grid (keys_own): the white keys                                     ok
smk ui: SMK pads: a layer's button held: the white keys                                        ok
smk ui: SMK pads: let go, HOME: the steps again                                                ok
smk ui: SMK pad tap, melodic: an empty step set to the last note played, the pad's velocity    ok
smk ui: SMK pad tap again: that step cleared                                                   ok
smk ui: SMK pad taps: one undo for the run (PAD STEPS)                                         ok
smk ui: SMK pad taps: pad 16 is step 16; a release does nothing                                ok
smk ui: SMK pad tap past LEN: nothing                                                          ok
smk ui: SMK pad tap, DRUM: the selected lane's hit toggled                                     ok
smk ui: SMK pad colours: a step the track's colour, empty faint, a tie half, past LEN dark     ok
smk ui: SMK pad colours: the step playing half way to white                                    ok
smk ui: SMK pad colours: on NOTES, stopped: the edited step white                              ok
smk ui: SMK fader: below the value, not reached: nothing set                                   ok
smk ui: SMK fader: past the value: it takes over, said (T2 LEVEL ..)                           ok
smk ui: SMK fader: then it follows                                                             ok
smk ui: SMK fader: a value set elsewhere is reached again first                                ok
smk ui: SMK FADER BANK: PAN, said, its LED lit                                                 ok
smk ui: SMK fader, PAN: 0..127 over -64..63                                                    ok
smk ui: SMK FADER BANK: round to LEVEL, its LED off                                            ok
smk ui: SMK faders follow the window: T6 selected, F1 is T3                                    ok
smk ui: SMK >: the next entry, at once when stopped                                            ok
smk ui: SMK < after >: back one                                                                ok
smk ui: SMK < on A: FIRST ENTRY, nowhere                                                       ok
smk ui: SMK outer key C3: note 48 on T1 at its velocity, out of the TRS jack too               ok
smk ui: SMK outer key let go: its note off                                                     ok
smk ui: SMK outer key C6: note 84, KEY VELOCITY FIXED 100                                      ok
smk ui: SMK KEY VELOCITY curves: SOFT louder, HARD softer, both ends kept                      ok
smk ui: SMK MENU: KEY VELOCITY in CONTROL, no LEDS row                                         ok
smk ui: SMK MENU > CLOCK: INT and USB only (no TRS MIDI IN)                                    ok
smk ui: SMK MENU > KEY VELOCITY HARD: the settings byte and the mode                           ok
smk ui: SMK settings: an unknown KEY VELOCITY reads as DYNAMIC                                 ok
smk ui: SMK USR2 / USR3: SAMPLE's SET and GRAIN's SOURCE end at USR1                           ok
smk ui: SMK wheels, pedal: a bend, CC1 and CC64 on the selected track's channel, as MIDI in    ok
smk ui: SMK wheels: another track selected: the one before back to rest                        ok
smk ui: SMK pedal down: a key and an outer key let go keep sounding (no note-off out)          ok
smk ui: SMK pedal: a held key struck again: its held note ends first, then it plays            ok
smk ui: SMK pedal up: the notes it held end (note-offs out), the keys keep nothing             ok
smk ui: SMK pedal, another track selected while it holds: the keys before end cleanly, it holds the new one's ok
smk ui: SMK pedal, a preset loaded while it holds (panic_req): the keys end, nothing left for its release ok
smk ui: SMK pedal up on a MONO track: its sounding note ends as it is (no fall back to another one held) ok
smk ui: SMK pedal on a DRUM track: ignored (the key's note-off at once, nothing held)          ok
smk ui: SMK KNOB BANK held: SHIFT's map, its LED lit                                           ok
smk ui: SMK SHIFT's map: the SMK's printed names (K4, K3, + BT; PLAY as PLAY: the SMK prints a play sign) ok
smk ui: SMK KNOB BANK + BT (SAVE): TAKE, the map gone, no SAVE page                            ok
smk ui: SMK KNOB BANK let go: no MENU                                                          ok
smk ui: SMK MASTER (K1) turned: said                                                           ok
smk ui: SMK MASTER at rest: kept in the settings                                               ok
smk ui: SMK power-on: MASTER where it was left                                                 ok
smk ui: SMK TRS MIDI OUT clock: Start, 24 pulses a beat (48 in 1 s at 120), Stop               ok
smk ui: SMK TRS MIDI OUT clock: none with an external clock                                    ok
smk ui test passed
smk pkg: identity SMK-37 Pro_700, 20 blocks, CRCs ok                            ok
smk pkg: flash.bin 0x9d000 B (stock PRCT 0x9D000)                               ok
smk pkg: app.bin, cfg_tool.bin first                                            ok
smk pkg: region table == stock v016 (VM, PRCT, BTIF, USRTRIM, USRFLASH, USR)    ok
smk pkg: head present (never written by the loader, checked against the device) ok
smk pkg: loader 7859 B, within the stock app's staging (7936 B)                 ok
smk package test passed
frames=352800 peak_pcm=14951 clipped_frames=0
frames=352800 peak_pcm=18920 clipped_frames=0
frames=352800 peak_pcm=12614 clipped_frames=0
frames=352800 peak_pcm=18431 clipped_frames=0
frames=352800 peak_pcm=15969 clipped_frames=0
frames=352800 peak_pcm=18525 clipped_frames=0
frames=352800 peak_pcm=12010 clipped_frames=0
frames=352800 peak_pcm=17090 clipped_frames=0
frames=352800 peak_pcm=15964 clipped_frames=0
frames=352800 peak_pcm=19304 clipped_frames=0
frames=352800 peak_pcm=16796 clipped_frames=0
frames=352800 peak_pcm=18575 clipped_frames=0
frames=352800 peak_pcm=11581 clipped_frames=0
frames=352800 peak_pcm=18402 clipped_frames=0
frames=352800 peak_pcm=13268 clipped_frames=0
frames=352800 peak_pcm=17526 clipped_frames=0
face S: BarlowCondensed-Medium.ttf 13px h16 base13  98 glyphs x 2  data 4247 B + table 1568 B + kern 582 B (194 pairs) = 6400 B   digit adv 6.00px
face M: BarlowCondensed-Bold.ttf 16px h20 base16  98 glyphs x 2  data 5814 B + table 1568 B + kern 1053 B (351 pairs) = 8438 B   digit adv 8.00px
face L: BarlowCondensed-Bold.ttf 28px h34 base28  41 glyphs x 1  data 2696 B + table 328 B + kern 384 B (128 pairs) = 3448 B   digit adv 14.00px
face V: BarlowCondensed-Bold.ttf 24px h29 base24  44 glyphs x 1  data 2371 B + table 352 B + kern 351 B (117 pairs) = 3117 B   digit adv 12.00px
fonts total 21403 B  -> /workspace/scratch/111ad38486f9/smk37-velvet-ep90/build/firmware/build/gen/ui_fonts.h
2 extra bytes in post.stringData array
2 extra bytes in post.stringData array
icons: x_oct_up: symbol_pitch_up not in the font yet, using control_arrow_up
icons: x_oct_dn: symbol_pitch_down not in the font yet, using control_arrow_down
icons 12px: 105 cells, 4266 B
icons 16px: 39 cells, 2587 B
icons 24px: 18 cells, 1874 B
icons code: 57 B
icons total 8784 B -> /workspace/scratch/111ad38486f9/smk37-velvet-ep90/build/firmware/build/gen/ui_icons.h   (87 legacy names + 40 new)
keycaps: 30 pills, data 5332 B + table 240 B; knob arcs 584 B = 6156 B -> /workspace/scratch/111ad38486f9/smk37-velvet-ep90/build/firmware/build/gen/ui_keycaps.h
pixel face S: 70 glyphs, 952 bytes of pixels
pixel face M: 70 glyphs, S's pixels at 1x bold
pixel face V: 44 glyphs, S's pixels at 2x
pixel face L: 41 glyphs, S's pixels at 3x
sprites: 15, 372 bytes
samples: CC0 library not fetched (tools/fetch_cc0.py) - no SAMPLE sets
samples: 0 sets, 0 zones, 37376 B ADPCM, SLICE BREAK 44100 + FUNK 30650 samples (cached)
{"render_count": 704, "worst_voice_peak": 0.4879166781902313, "worst_abs_dc": 3.154010482830927e-05, "failures": [], "hardware_tested": false, "reference_audio_compared": false}
All host checks passed; 16 demos rendered. Hardware and reference audio unverified.

```

All 16 restored demo WAV Git blob hashes exactly match the versions uploaded before workspace pruning. The audio implementation was recovered without changing those outputs.
