# MiQ Scout — Open Autocalibration Seed for Playfields

This is a free, offline-first prototype for autocalibrating any radial/circular playfield (dartboard first) using a single camera.  

- Detects outer ring for scale & boundary  
- Warps to perfect top-down view  
- Learns scoring zones/rules from colors  
- Detects throws → polar scoring  
- Runs self-powered (solar + battery)  
- Haptic feedback (wheel-like ticks)  
- Removable relic disc for sharing saves/mods/progress  
- Breadcrumb trails that glow and never die  

Philosophy:  
- No subscriptions. No cloud. No monetization.  
- Integrity first — build for the hero, not the payout.  
- Modders welcome — fork it, improve it, make it better than us.  
- If it threatens someone's moat, good. Let the community decide.  

License: MIT — take it, modify it, share it.  

## Quick Start (10-Min Test)
1. **Hardware**  
   - Raspberry Pi CM4 (or Pi 4/5 for testing)  
   - Camera: Pi Camera Module (NoIR for low-light) or phone via iVCam bridge  
   - Optional: 4” Waveshare touch e-paper (SPI), DRV2605 + LRA (haptics), solar + TP4056 + LiPo (never-die power)  

2. **Setup**  
   ```bash
   sudo apt update && sudo apt install python3-opencv python3-numpy python3-pil
   git clone https://github.com/yourhandle/miq-scout.git
   cd miq-scout
