#!/usr/bin/env python3
"""
tools/generate_game_audio.py
Synthesizes 25 authentic mecha/tactical sound effects (.wav) and 6 90s FM-synth music tracks (.wav)
for MechMakerConcept, exports them to sounds/<snd_id>/, generates the GameMaker Studio 2 .yy
resource files, and registers them in MechMakerConcept.yyp.
"""

import os
import math
import struct
import wave
import random
import json
import re

SAMPLE_RATE = 44100
SOUNDS_DIR = "sounds"
YYP_PATH = "MechMakerConcept.yyp"

os.makedirs(SOUNDS_DIR, exist_ok=True)

# =============================================================================
# DSP CORE UTILITIES
# =============================================================================

def clamp(v, min_v=-1.0, max_v=1.0):
    return max(min_v, min(max_v, v))

def sine(freq, t, phase=0.0):
    return math.sin(2.0 * math.pi * freq * t + phase)

def triangle(freq, t, phase=0.0):
    p = (t * freq + phase / (2.0 * math.pi)) % 1.0
    return 4.0 * abs(p - 0.5) - 1.0

def square(freq, t, phase=0.0, duty=0.5):
    p = (t * freq + phase / (2.0 * math.pi)) % 1.0
    return 1.0 if p < duty else -1.0

def saw(freq, t, phase=0.0):
    p = (t * freq + phase / (2.0 * math.pi)) % 1.0
    return 2.0 * p - 1.0

def noise():
    return random.uniform(-1.0, 1.0)

def write_wav(filepath, samples, sample_rate=SAMPLE_RATE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with wave.open(filepath, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        raw_bytes = bytearray()
        for s in samples:
            val = clamp(s)
            int_val = int(val * 32767)
            raw_bytes.extend(struct.pack("<h", int_val))
        wav.writeframes(raw_bytes)

def generate_sound_yy(snd_id, duration):
    return {
        "$GMSound": "v1",
        "%Name": snd_id,
        "audioGroupId": {
            "name": "audiogroup_default",
            "path": "audiogroups/audiogroup_default"
        },
        "bitDepth": 1,
        "bitRate": 128,
        "compression": 0,
        "conversionMode": 0,
        "duration": round(duration, 4),
        "parent": {
            "name": "sounds",
            "path": "folders/sounds.yy"
        },
        "preload": True,
        "resourceType": "GMSound",
        "resourceVersion": "2.0",
        "sampleRate": SAMPLE_RATE,
        "soundFile": f"{snd_id}.wav",
        "type": 0,
        "volume": 1.0
    }

def register_in_yyp(snd_id):
    if not os.path.exists(YYP_PATH):
        return
    with open(YYP_PATH, 'r') as f:
        content = f.read()
    
    target_entry = 'sounds/' + snd_id + '/' + snd_id + '.yy'
    if target_entry in content:
        return
    
    idx = content.find('"resources":')
    if idx != -1:
        bracket_idx = content.find('],', idx)
        if bracket_idx != -1:
            new_entry = '    {"id":{"name":"' + snd_id + '","path":"sounds/' + snd_id + '/' + snd_id + '.yy",},},' + chr(10)
            content = content[:bracket_idx] + new_entry + content[bracket_idx:]
            with open(YYP_PATH, 'w') as f:
                f.write(content)

# =============================================================================
# SFX SYNTHESIZERS (25 SOUND EFFECTS)
# =============================================================================

def synth_ui_click():
    # Tactile micro-switch click: sharp impulse + metallic pop
    dur = 0.04
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 120.0)
        pop = sine(1200.0 - t * 15000.0, t) * 0.7
        click = noise() * math.exp(-t * 250.0) * 0.6
        samples.append((pop + click) * env * 0.85)
    return dur, samples

def synth_ui_hover():
    # CRT terminal soft blip: warm triangle wave
    dur = 0.035
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        s = triangle(620.0, t) * 0.35
        samples.append(s * env)
    return dur, samples

def synth_ui_tab():
    # Sub-frequency panel switch glide
    dur = 0.08
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 35.0)
        f = 240.0 - t * 1500.0
        s = sine(f, t) * 0.7 + triangle(f * 2.0, t) * 0.2
        samples.append(s * env * 0.8)
    return dur, samples

def synth_ui_confirm():
    # Dual-tone harmonic chime (E5 -> B5)
    dur = 0.22
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 14.0)
        chime1 = sine(659.25, t) * 0.5
        chime2 = sine(987.77, t) * 0.4 * (1.0 if t > 0.04 else (t / 0.04))
        spark = sine(1975.5, t) * 0.15 * math.exp(-t * 28.0)
        samples.append((chime1 + chime2 + spark) * env * 0.9)
    return dur, samples

def synth_ui_cancel():
    # Double error buzz
    dur = 0.16
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        # Two pulses
        cycle = (t % 0.08) / 0.08
        env = math.sin(math.pi * cycle)
        buzz = square(160.0, t, duty=0.3) * 0.6 + noise() * 0.15
        samples.append(buzz * env * 0.7)
    return dur, samples

def synth_ui_terminal_boot():
    # CRT power-up capacitor whine + ready beep
    dur = 0.45
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.25:
            # Capacitor whine
            f = 400.0 + (t / 0.25) * 8000.0
            env = (t / 0.25) * 0.35
            s = sine(f, t) * env + noise() * 0.05
        else:
            # Ready beep at 880Hz
            tb = t - 0.25
            env = math.exp(-tb * 18.0) * 0.6
            s = sine(880.0, tb) * env + sine(1760.0, tb) * env * 0.3
        samples.append(s)
    return dur, samples

def synth_ui_stamp():
    # Heavy evaluation trial stamp
    dur = 0.25
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        thump = sine(75.0, t) * math.exp(-t * 22.0) * 0.8
        clack = noise() * math.exp(-t * 80.0) * 0.7
        ring = sine(850.0, t) * math.exp(-t * 30.0) * 0.35
        samples.append((thump + clack + ring) * 0.9)
    return dur, samples

def synth_crucible_pour():
    # Molten metal hiss & sizzling bubbling flux
    dur = 0.65
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        sizzle = noise() * 0.4
        bubble_mod = sine(12.0 + t * 8.0, t) * 0.5 + 0.5
        hiss = noise() * bubble_mod * 0.35
        low_heat = sine(95.0, t) * 0.25
        samples.append((sizzle + hiss + low_heat) * env * 0.85)
    return dur, samples

def synth_hydraulic_press():
    # Heavy pneumatic press stamp
    dur = 0.42
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 12.0)
        piston = sine(55.0 - t * 40.0, t) * 0.85
        impact = noise() * math.exp(-t * 50.0) * 0.75
        whine = sine(420.0, t) * math.exp(-t * 18.0) * 0.3
        samples.append((piston + impact + whine) * env * 0.9)
    return dur, samples

def synth_plasma_weld():
    # High-voltage electric arc crackle
    dur = 0.50
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        arc = (noise() if random.random() < 0.7 else 0.0) * 0.65
        hum = saw(120.0, t) * 0.35
        samples.append((arc + hum) * env * 0.8)
    return dur, samples

def synth_discovery_fanfare():
    # Resonant crystal harmonic discovery arpeggio (C6 - E6 - G6 - C7)
    dur = 0.55
    n = int(dur * SAMPLE_RATE)
    samples = []
    notes = [1046.50, 1318.51, 1567.98, 2093.00]
    for i in range(n):
        t = i / SAMPLE_RATE
        step_idx = min(3, int(t / 0.12))
        f = notes[step_idx]
        note_t = t - step_idx * 0.12
        env = math.exp(-note_t * 9.0)
        s = sine(f, t) * 0.6 + sine(f * 2.0, t) * 0.25 + triangle(f * 0.5, t) * 0.15
        samples.append(s * env * 0.85)
    return dur, samples

def synth_mech_step():
    # 50-ton hydraulic footstep: ground shockwave + joint servo
    dur = 0.38
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        sub = sine(48.0 - t * 25.0, t) * math.exp(-t * 15.0) * 0.9
        crunch = noise() * math.exp(-t * 35.0) * 0.55
        servo = sine(540.0 + math.sin(t * 40.0) * 80.0, t) * math.exp(-t * 10.0) * 0.35
        samples.append((sub + crunch + servo) * 0.9)
    return dur, samples

def synth_mech_boost():
    # Vernier booster thruster burst
    dur = 0.50
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        roar = noise() * 0.7
        rumble = sine(65.0, t) * 0.4
        flare = saw(110.0, t) * 0.25
        samples.append((roar + rumble + flare) * env * 0.85)
    return dur, samples

def synth_mech_servo():
    # Quick metallic joint servo torque rotation
    dur = 0.18
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        f = 320.0 + math.sin(t * 35.0) * 160.0
        servo = triangle(f, t) * 0.6 + saw(f * 1.5, t) * 0.25
        samples.append(servo * env * 0.75)
    return dur, samples

def synth_weapon_vulcan():
    # Heavy rotary chaingun / vulcan ballistic bark
    dur = 0.08
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 60.0)
        pop = square(190.0 - t * 900.0, t) * 0.75
        crack = noise() * math.exp(-t * 140.0) * 0.8
        samples.append((pop + crack) * env * 0.9)
    return dur, samples

def synth_weapon_cannon_120mm():
    # Massive 120mm artillery blast + breech clank
    dur = 0.65
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        blast_env = math.exp(-t * 8.0)
        sub = sine(55.0 - t * 30.0, t) * blast_env * 0.9
        shk = noise() * math.exp(-t * 22.0) * 0.85
        # Barrel ring
        ring = sine(680.0, t) * math.exp(-t * 12.0) * 0.25
        # Breech ejection click at 0.35s
        clank = 0.0
        if t > 0.32:
            tc = t - 0.32
            clank = (sine(1100.0, tc) + noise() * 0.5) * math.exp(-tc * 45.0) * 0.4
        samples.append((sub + shk + ring + clank) * 0.9)
    return dur, samples

def synth_weapon_missile_launch():
    # Rocket motor ignition & whoosh
    dur = 0.45
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        thrust = noise() * 0.75
        whistle = sine(400.0 + t * 1800.0, t) * 0.35
        samples.append((thrust + whistle) * env * 0.85)
    return dur, samples

def synth_weapon_beam_rifle():
    # High-energy particle beam ionization discharge
    dur = 0.38
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 10.0)
        f = 2200.0 * math.exp(-t * 9.0) + 180.0
        beam = saw(f, t) * 0.65 + sine(f * 2.0, t) * 0.3
        ionization = noise() * math.exp(-t * 25.0) * 0.45
        samples.append((beam + ionization) * env * 0.9)
    return dur, samples

def synth_weapon_plasma_blade():
    # Thermal beam blade ignition & swing whoosh
    dur = 0.32
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur))
        hum = saw(125.0 + math.sin(t * 30.0) * 40.0, t) * 0.65
        sizzle = noise() * 0.35
        samples.append((hum + sizzle) * env * 0.85)
    return dur, samples

def synth_weapon_railgun():
    # Hypersonic railgun crack & electromagnetic rail hum
    dur = 0.52
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        # Supersonic snap
        snap = noise() * math.exp(-t * 150.0) * 0.95
        # Rail hum & discharge
        rail_env = math.exp(-t * 10.0)
        f_rail = 1600.0 - t * 2400.0
        rail = sine(max(100.0, f_rail), t) * rail_env * 0.6
        sub = sine(60.0, t) * rail_env * 0.5
        samples.append((snap + rail + sub) * 0.9)
    return dur, samples

def synth_impact_armor():
    # Armor deflection / ricochet clank
    dur = 0.22
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 25.0)
        ping = sine(1450.0, t) * 0.65 + sine(2180.0, t) * 0.3
        clank = noise() * math.exp(-t * 90.0) * 0.6
        samples.append((ping + clank) * env * 0.85)
    return dur, samples

def synth_impact_penetrate():
    # Heavy kinetic armor breach crunch
    dur = 0.35
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 14.0)
        crunch = noise() * 0.85
        thud = sine(52.0, t) * 0.75
        tear = saw(280.0, t) * 0.4
        samples.append((crunch + thud + tear) * env * 0.9)
    return dur, samples

def synth_explosion_small():
    # Shrapnel explosion
    dur = 0.45
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 10.0)
        blast = noise() * 0.8
        thump = sine(70.0 - t * 40.0, t) * 0.7
        samples.append((blast + thump) * env * 0.85)
    return dur, samples

def synth_explosion_large():
    # Catastrophic reactor rupture explosion with sub-bass rumble
    dur = 1.20
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 4.0)
        blast = noise() * (0.9 if t < 0.2 else 0.5)
        sub = sine(42.0 - t * 15.0, t) * 0.9
        rumble = sine(28.0, t) * 0.7 * (1.0 if t > 0.1 else t / 0.1)
        samples.append((blast + sub + rumble) * env * 0.9)
    return dur, samples

def synth_alarm_critical():
    # Emergency cockpit warning klaxon (alternating 800Hz / 600Hz)
    dur = 0.52
    n = int(dur * SAMPLE_RATE)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        f = 820.0 if (t % 0.26) < 0.13 else 620.0
        env = 0.75 if (t % 0.13) < 0.11 else 0.0
        alarm = square(f, t, duty=0.45) * 0.65 + sine(f * 2.0, t) * 0.25
        samples.append(alarm * env)
    return dur, samples

# =============================================================================
# BGM SYNTHESIZERS (6 MUSIC TRACKS - 90s FM-SYNTH TACTICAL RPG)
# =============================================================================

def synth_bgm_hq_ambience():
    # Strategic War Map / HQ Ambience: Tense 84 BPM, D minor
    # Drums, sub-bass pulse, dark pad, tactical sonar ping
    bpm = 84
    beat_sec = 60.0 / bpm
    bars = 4
    total_beats = bars * 4
    dur = total_beats * beat_sec # ~11.43s
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    # Bassline pattern (D2 -> F2 -> G2 -> A1)
    bass_notes = [73.42, 87.31, 98.00, 55.00]
    
    for i in range(n):
        t = i / SAMPLE_RATE
        current_beat = t / beat_sec
        bar_idx = int(current_beat / 4) % 4
        beat_in_bar = current_beat % 4
        
        # 1. Sub-bass pulse on 8th notes
        f_bass = bass_notes[bar_idx]
        bass_env = math.exp(-((t % (beat_sec * 0.5)) / (beat_sec * 0.5)) * 4.0)
        s_bass = (sine(f_bass, t) * 0.7 + triangle(f_bass * 2.0, t) * 0.3) * bass_env * 0.38
        
        # 2. Subtle military percussion (soft kick on 1 and 3, closed metallic tick on 8ths)
        beat_frac = beat_in_bar % 1.0
        kick = 0.0
        if int(beat_in_bar) in [0, 2] and beat_frac < 0.2:
            kick = sine(65.0 - beat_frac * 120.0, beat_frac) * math.exp(-beat_frac * 25.0) * 0.45
        tick = 0.0
        if (beat_in_bar * 2) % 1.0 < 0.08:
            tick = noise() * math.exp(-((beat_in_bar * 2) % 1.0) * 80.0) * 0.15
            
        # 3. Dark ambient pad (D minor chord: D3 146.83, F3 174.61, A3 220.00)
        lfo = 0.5 + 0.5 * sine(0.35, t)
        pad = (saw(146.83, t) + saw(174.61, t) + saw(220.00, t)) * 0.08 * lfo
        
        # 4. Tactical Sonar Radar Ping (every 2 bars on beat 0)
        sonar = 0.0
        if bar_idx in [0, 2] and beat_in_bar < 0.8:
            sonar = sine(1760.0, t) * math.exp(-beat_in_bar * 3.5) * 0.18
            
        samples[i] = clamp(s_bass + kick + tick + pad + sonar) * 0.85
        
    return dur, samples

def synth_bgm_prototyping_bay():
    # Prototyping Bay / Alloy Sintering: 108 BPM, A minor
    # Industrial workshop, driving rhythm, hydraulic beat, synth arpeggio
    bpm = 108
    beat_sec = 60.0 / bpm
    bars = 4
    total_beats = bars * 4
    dur = total_beats * beat_sec # ~8.88s
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    # 16th-note arpeggio in A minor (A2, C3, E3, A3, G3, E3, D3, C3)
    arp_notes = [110.00, 130.81, 164.81, 220.00, 196.00, 164.81, 146.83, 130.81]
    
    for i in range(n):
        t = i / SAMPLE_RATE
        current_beat = t / beat_sec
        beat_frac = current_beat % 1.0
        step_16th = int(current_beat * 4) % 8
        step_frac = (current_beat * 4) % 1.0
        
        # 1. Industrial Hydraulic Kick / Stamp on beats 0, 1, 2, 3
        kick = sine(70.0 - beat_frac * 140.0, beat_frac) * math.exp(-beat_frac * 18.0) * 0.55
        
        # 2. Metallic Anvil Tick on offbeat
        anvil = 0.0
        if beat_frac > 0.5:
            tc = beat_frac - 0.5
            anvil = (sine(1250.0, tc) + noise() * 0.4) * math.exp(-tc * 35.0) * 0.3
            
        # 3. 16th-note FM synth arpeggio
        f_arp = arp_notes[step_16th]
        arp_env = math.exp(-step_frac * 8.0)
        arp = (triangle(f_arp, t) * 0.6 + square(f_arp * 2.0, t, duty=0.3) * 0.25) * arp_env * 0.4
        
        # 4. Heavy bass anchor on A1 (55Hz)
        bass = saw(55.0, t) * math.exp(-beat_frac * 6.0) * 0.35
        
        samples[i] = clamp(kick + anvil + arp + bass) * 0.85
        
    return dur, samples

def synth_bgm_combat_engage():
    # Front Mission / 90s Mecha Tactical Battle: 132 BPM, E minor
    # Driving FM-synth drums, syncopated bass, brass stabs, battle lead
    bpm = 132
    beat_sec = 60.0 / bpm
    bars = 4
    total_beats = bars * 4
    dur = total_beats * beat_sec # ~7.27s
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    # Bass progression (Em -> C -> D -> Bm)
    roots = [82.41, 65.41, 73.42, 61.74] # E2, C2, D2, B1
    lead_notes = [329.63, 392.00, 440.00, 493.88] # E4, G4, A4, B4
    
    for i in range(n):
        t = i / SAMPLE_RATE
        current_beat = t / beat_sec
        bar_idx = int(current_beat / 4) % 4
        beat_in_bar = current_beat % 4
        beat_frac = beat_in_bar % 1.0
        
        # 1. Driving Battle Drums: Kick on 0, 1.5, 2; Snare on 1, 3; Fast hi-hat on 16ths
        kick = 0.0
        if (beat_in_bar < 0.2) or (abs(beat_in_bar - 1.5) < 0.15) or (abs(beat_in_bar - 2.0) < 0.15):
            k_t = min(beat_frac, abs(beat_in_bar - 1.5))
            kick = sine(85.0 - k_t * 180.0, k_t) * math.exp(-k_t * 22.0) * 0.6
        snare = 0.0
        if int(beat_in_bar) in [1, 3] and beat_frac < 0.25:
            snare = (noise() * 0.7 + sine(180.0, beat_frac) * 0.4) * math.exp(-beat_frac * 20.0) * 0.55
        hihat = noise() * math.exp(-((current_beat * 4) % 1.0) * 45.0) * 0.18
        
        # 2. Galloping 16th-note Mecha Bass
        f_root = roots[bar_idx]
        bass_step = (current_beat * 4) % 1.0
        bass_env = math.exp(-bass_step * 7.0)
        bass = (saw(f_root, t) * 0.6 + square(f_root * 0.5, t) * 0.3) * bass_env * 0.45
        
        # 3. Brass Chord Stabs on beat 0 and 2.5
        stab_env = 0.0
        if beat_in_bar < 0.35:
            stab_env = math.exp(-beat_in_bar * 6.0)
        elif abs(beat_in_bar - 2.5) < 0.3:
            stab_env = math.exp(-(beat_in_bar - 2.5) * 6.0)
        f_b = f_root * 2.0
        brass = (saw(f_b, t) + saw(f_b * 1.2, t) + saw(f_b * 1.5, t)) * 0.12 * stab_env
        
        # 4. Heroic Mecha Lead Melody
        lead_idx = int(beat_in_bar) % 4
        f_lead = lead_notes[lead_idx]
        vib = 1.0 + 0.015 * sine(5.5, t)
        lead_env = math.exp(-beat_frac * 3.5)
        lead = (saw(f_lead * vib, t) * 0.45 + triangle(f_lead * 2.0, t) * 0.25) * lead_env * 0.35
        
        samples[i] = clamp(kick + snare + hihat + bass + brass + lead) * 0.88
        
    return dur, samples

def synth_bgm_nemesis_incursion():
    # Boss / Drop-Pod Incursion: 142 BPM, C minor
    # Aggressive distorted industrial beat, menacing saw bass drops, tension sirens
    bpm = 142
    beat_sec = 60.0 / bpm
    bars = 4
    total_beats = bars * 4
    dur = total_beats * beat_sec # ~6.76s
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    for i in range(n):
        t = i / SAMPLE_RATE
        current_beat = t / beat_sec
        beat_frac = current_beat % 1.0
        
        # 1. Heavy Industrial Distorted Kick
        kick = sine(90.0 - beat_frac * 220.0, beat_frac) * math.exp(-beat_frac * 15.0) * 0.75
        dist = math.tanh(kick * 2.5) * 0.7
        
        # 2. Snare / Clang on beats 1 and 3
        clang = 0.0
        if int(current_beat) % 2 == 1 and beat_frac < 0.3:
            clang = (noise() * 0.8 + saw(280.0, beat_frac) * 0.5) * math.exp(-beat_frac * 16.0) * 0.6
            
        # 3. Menacing Low Saw Bass Drop on C1 (32.7Hz) & Tritone Gb1 (46.2Hz)
        f_bass = 32.70 if int(current_beat / 4) % 2 == 0 else 46.25
        bass = saw(f_bass, t) * math.exp(-beat_frac * 4.0) * 0.5
        
        # 4. Warning Siren Motif
        siren_f = 650.0 + 350.0 * sine(2.0, t)
        siren = square(siren_f, t, duty=0.4) * 0.22
        
        samples[i] = clamp(dist + clang + bass + siren) * 0.88
        
    return dur, samples

def synth_bgm_victory_fanfare():
    # Triumphant fanfare stinger: G Major, 125 BPM, ~4.5s
    dur = 4.5
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    # Chords: G (0s) -> C (1s) -> D (2s) -> G (3s-4.5s)
    chord_times = [0.0, 1.0, 2.0, 3.0]
    chords = [
        [196.00, 246.94, 293.66], # G3, B3, D4
        [261.63, 329.63, 392.00], # C4, E4, G4
        [293.66, 369.99, 440.00], # D4, F#4, A4
        [392.00, 493.88, 587.33]  # G4, B4, D5 (Octave up)
    ]
    
    for i in range(n):
        t = i / SAMPLE_RATE
        chord_idx = min(3, int(t / 1.0))
        t_chord = t - chord_times[chord_idx]
        chord_freqs = chords[chord_idx]
        
        env = math.exp(-t_chord * 1.5) if chord_idx < 3 else math.exp(-t_chord * 0.8)
        brass = sum(saw(f, t) + triangle(f * 2.0, t) * 0.5 for f in chord_freqs) * 0.18
        
        # Rolling Snare swell at start of each beat
        snare = noise() * math.exp(-((t * 4.0) % 1.0) * 18.0) * 0.25 if t < 3.0 else 0.0
        timpani = sine(98.0, t_chord) * math.exp(-t_chord * 10.0) * 0.5
        
        samples[i] = clamp((brass * env) + snare + timpani) * 0.88
        
    return dur, samples

def synth_bgm_defeat_somber():
    # Somber defeat stinger: D minor, ~4.5s
    dur = 4.5
    n = int(dur * SAMPLE_RATE)
    samples = [0.0] * n
    
    # Descents: Dm -> Bb -> Gm -> Dm (slow decay)
    chord_times = [0.0, 1.2, 2.4, 3.4]
    chords = [
        [146.83, 174.61, 220.00], # D3, F3, A3
        [116.54, 146.83, 174.61], # Bb2, D3, F3
        [98.00, 116.54, 146.83],  # G2, Bb2, D3
        [73.42, 87.31, 110.00]    # D2, F2, A2 (Low)
    ]
    
    for i in range(n):
        t = i / SAMPLE_RATE
        chord_idx = min(3, int(t / 1.2))
        t_chord = t - chord_times[chord_idx]
        chord_freqs = chords[chord_idx]
        
        env = math.exp(-t_chord * 1.8) if chord_idx < 3 else math.exp(-t_chord * 0.6)
        cello = sum(saw(f, t) * 0.6 + triangle(f * 0.5, t) * 0.4 for f in chord_freqs) * 0.16
        low_thump = sine(40.0, t_chord) * math.exp(-t_chord * 8.0) * 0.4
        
        samples[i] = clamp((cello * env) + low_thump) * 0.85
        
    return dur, samples

# =============================================================================
# MASTER ASSET MANIFEST & EXPORTER
# =============================================================================

ALL_SOUNDS = {
    # UI Soundscapes
    "snd_ui_click": synth_ui_click,
    "snd_ui_hover": synth_ui_hover,
    "snd_ui_tab": synth_ui_tab,
    "snd_ui_confirm": synth_ui_confirm,
    "snd_ui_cancel": synth_ui_cancel,
    "snd_ui_terminal_boot": synth_ui_terminal_boot,
    "snd_ui_stamp": synth_ui_stamp,

    # Prototyping Bay & Sintering Minigames
    "snd_crucible_pour": synth_crucible_pour,
    "snd_hydraulic_press": synth_hydraulic_press,
    "snd_plasma_weld": synth_plasma_weld,
    "snd_discovery_fanfare": synth_discovery_fanfare,

    # Mecha Foley & Locomotion
    "snd_mech_step": synth_mech_step,
    "snd_mech_boost": synth_mech_boost,
    "snd_mech_servo": synth_mech_servo,

    # Combat Weapons
    "snd_weapon_vulcan": synth_weapon_vulcan,
    "snd_weapon_cannon_120mm": synth_weapon_cannon_120mm,
    "snd_weapon_missile_launch": synth_weapon_missile_launch,
    "snd_weapon_beam_rifle": synth_weapon_beam_rifle,
    "snd_weapon_plasma_blade": synth_weapon_plasma_blade,
    "snd_weapon_railgun": synth_weapon_railgun,

    # Impacts, Destruction & Alarms
    "snd_impact_armor": synth_impact_armor,
    "snd_impact_penetrate": synth_impact_penetrate,
    "snd_explosion_small": synth_explosion_small,
    "snd_explosion_large": synth_explosion_large,
    "snd_alarm_critical": synth_alarm_critical,

    # Background Music & Themes
    "bgm_hq_ambience": synth_bgm_hq_ambience,
    "bgm_prototyping_bay": synth_bgm_prototyping_bay,
    "bgm_combat_engage": synth_bgm_combat_engage,
    "bgm_nemesis_incursion": synth_bgm_nemesis_incursion,
    "bgm_victory_fanfare": synth_bgm_victory_fanfare,
    "bgm_defeat_somber": synth_bgm_defeat_somber
}

def main():
    print("=====================================================================")
    print("=== SYNTHESIZING MECHMAKERCONCEPT AUDIO ASSETS (SFX & BGM) ===")
    print("=====================================================================")
    
    count = 0
    for snd_id, synth_fn in ALL_SOUNDS.items():
        dur, samples = synth_fn()
        snd_folder = os.path.join(SOUNDS_DIR, snd_id)
        wav_path = os.path.join(snd_folder, f"{snd_id}.wav")
        yy_path = os.path.join(snd_folder, f"{snd_id}.yy")
        
        # 1. Export WAV
        write_wav(wav_path, samples)
        
        # 2. Export GMSound YY
        yy_data = generate_sound_yy(snd_id, dur)
        with open(yy_path, "w") as f:
            json.dump(yy_data, f, indent=2)
            
        # 3. Register in MechMakerConcept.yyp
        register_in_yyp(snd_id)
        
        fsize_kb = os.path.getsize(wav_path) / 1024.0
        print(f"  ✓ {snd_id:26s} | Dur: {dur:5.2f}s | Size: {fsize_kb:6.1f} KB | Registered in YYP")
        count += 1
        
    print(f"\n>>> Total Audio Resources Generated and Registered: {count} <<<")

if __name__ == "__main__":
    main()
