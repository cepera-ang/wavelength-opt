# **Comprehensive Analysis of Light Emitting Sources: Spectral Mapping from 13.5 nm to 1500 nm**

The generation, manipulation, and commercialization of coherent and incoherent light across the electromagnetic spectrum form the foundation of modern optoelectronics, telecommunications, semiconductor manufacturing, and display technologies. The technological landscape of light-emitting sources spans an extraordinary diversity of physical mechanisms. These range from laser-produced plasmas generating extreme ultraviolet (EUV) light, to the quantum-confined bandgap engineering of semiconductor diodes, to the spin-state manipulations within organic molecules and colloidal quantum dots.  
The analysis presented herein provides an exhaustive mapping of current light-emitting technologies from 13.5 nm through 1500 nm. Where traditional bulk semiconductors are limited by fixed material bandgaps, modern photonics leverages nonlinear frequency conversion, precision epitaxy, and exotic phosphor chemistries to achieve emission at highly specific, single-nanometer increments. This report evaluates the source types, spectral widths, power efficiencies, output powers, and commercial statuses of emitters across the spectrum, systematically cataloging available wavelengths with a particular emphasis on the human-visible range (380 nm to 720 nm).

## **Extreme Ultraviolet (EUV) Regime: 13.5 nm**

The extreme ultraviolet spectrum represents the absolute leading edge of high-volume commercial photonics, driven exclusively by the rigorous demands of the semiconductor industry for advanced photolithography nodes. At 13.5 nm, traditional continuous-bandgap solid-state emitters do not exist due to the extreme absorption of high-energy photons by virtually all materials. Instead, emission relies entirely on high-energy plasma generation.  
The dominant architecture in production today is the Laser-Produced Plasma (LPP) system. In this configuration, microscopic droplets of molten tin (Sn) are fired into a vacuum chamber at rates of approximately 50,000 to 100,000 droplets per second1. A high-power, pulsed CO2 laser operating at a 10.6 µm wavelength acts as the driver. Modern architectures utilize a sophisticated two-pulse system: a low-power pre-pulse strikes the tin droplet to flatten it into a geometric shape with a larger surface area, followed immediately by a high-power main pulse2. The main pulse, which is often amplified through five stages to reach 20 kW of mean optical power, vaporizes the tin into a high-temperature plasma2.  
The resulting tin ions, specifically existing in the highly ionized states from Sn IX to Sn XIV, undergo 4p⁶4dⁿ – 4p⁵4dⁿ⁺¹ \+ 4dⁿ⁻¹4f electronic transitions. These transitions emit photons with a dense array of spectral peaks centered precisely around 13.5 nm3. The light is subsequently collected by highly specialized, defect-free molybdenum/silicon (Mo/Si) multilayer mirrors. These mirrors consist of alternating bilayers that rely on Bragg diffraction to reflect the EUV light, achieving a theoretical maximum reflectivity of approximately 75% per mirror4.  
The generation of 13.5 nm light is notoriously inefficient, presenting significant ongoing engineering challenges for scaling semiconductor throughput. The required in-band emission for lithography is strictly defined as a 2% full-width at half-maximum (FWHM) bandwidth around the 13.5 nm center wavelength4. The optical-to-optical conversion efficiency—defined as the ratio of in-band 13.5 nm EUV energy generated to the incident CO2 laser energy—reaches a maximum of roughly 5.0% in highly optimized research systems, particularly those experimenting with 2 µm driver lasers rather than 10.6 µm CO2 lasers6.  
However, the wall-plug efficiency (WPE) of the entire EUV source module remains extraordinarily low. Generating a few hundred watts of usable EUV power at the intermediate focus requires massive electrical power inputs, often exceeding 1.3 megawatts, translating to a systemic WPE of well under 0.1%4. Commercial systems currently deployed in the field deliver between 250 W and 600 W of stable in-band EUV power. To facilitate future semiconductor scaling and increase wafer throughput from roughly 220 to over 330 wafers per hour, industry roadmaps are targeting aggressive source power scaling to 1,000 W, and eventually 2,000 W, by manipulating droplet rates and laser pulse shaping2.

### **Catalog of Extreme Ultraviolet Emitters**

| Wavelength | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **13.5 nm** | 2% FWHM (\~0.27 nm) | Laser-Produced Plasma (Tin) | \< 0.1% WPE, \~5% CE | 250 W \- 1,000 W | Full Production2 |

## **Deep and Vacuum Ultraviolet: 110 nm to 300 nm**

Moving from the EUV into the vacuum ultraviolet (VUV) and deep ultraviolet (DUV), the technological landscape shifts from plasma sources to molecular gas lasers, excimer systems, and diode-pumped solid-state (DPSS) harmonic generation.

### **Molecular and Excimer Lasers**

Excimer (excited dimer) lasers are the dominant high-power coherent sources in the DUV, heavily utilized in legacy deep-UV lithography (such as 193 nm immersion patterning) and medical tissue ablation. These gas-discharge lasers operate on the principle of forming transient diatomic molecules or rare-gas halides that exist only in an excited electronic state. When these molecules radiatively decay to a repulsive ground state, they emit a high-energy photon and immediately dissociate. This instantaneous dissociation naturally empties the lower laser level, effortlessly maintaining a strong population inversion8.  
The shortest wavelengths are achieved using pure molecular gases, such as the Hydrogen (H2) laser emitting a continuum of lines between 110 nm and 162 nm, and the Fluorine (F2) excimer laser emitting at 157 nm9. Further into the DUV, the Argon Fluoride (ArF) excimer operates at 193 nm, while the Krypton Chloride (KrCl) and Krypton Fluoride (KrF) excimers operate at 222 nm and 248 nm, respectively8.  
Excimer lasers are fundamentally pulsed devices with nanosecond durations. They are capable of delivering up to 1 Joule per pulse at repetition rates of hundreds to thousands of Hertz. Despite their high peak powers, their wall-plug efficiency remains relatively low, typically varying between 0.2% and 5% depending on the specific gas mixture and pumping mechanism (electrical discharge versus electron beam)8. The spectral linewidth of a free-running excimer is intrinsically broad, around 1 nm, but intra-cavity dispersive elements can narrow this to less than 1 picometer (pm) for precision lithographic applications where chromatic aberration in fused silica lenses must be avoided4.  
Other specialized gas lasers in this regime include the Helium-Silver (HeAg) hollow-cathode laser emitting at 224.3 nm and the Neon-Copper (NeCu) laser at 248.6 nm. These lasers utilize hollow cathode discharge mechanisms and offer distinct advantages in generating longer pulses (tens of microseconds) compared to traditional excimers, reducing peak-power-induced thermal damage on delicate samples during spectroscopic analysis11.

### **Solid-State Harmonic Generation**

Diode-pumped solid-state (DPSS) lasers generate deep ultraviolet light via the nonlinear optical frequency conversion of a fundamental infrared beam. The fundamental wavelength is typically 1064 nm, generated by Neodymium-doped Yttrium Aluminum Garnet (Nd:YAG) or Yttrium Orthovanadate (Nd:YVO4) gain media14.  
To reach the DUV, this fundamental light must undergo multiple stages of upconversion. Passing the 1064 nm beam through a nonlinear crystal achieves second harmonic generation (SHG) at 532 nm. Subsequent mixing stages yield the third harmonic at 355 nm, the fourth harmonic at 266 nm, and the fifth harmonic at 213 nm11. DPSS systems at 266 nm are highly commercialized for micromachining and remote sensing, delivering microjoule to millijoule pulse energies with sub-nanosecond pulse widths and near-perfect Gaussian (TEM00) spatial profiles14. Conversion efficiencies from the fundamental to the fourth harmonic are generally low (often below 5-10%), resulting in moderate overall wall-plug efficiencies14.

### **Deep Ultraviolet Semiconductors**

Wide-bandgap semiconductors based on the Aluminum Gallium Nitride (AlGaN) material system enable the production of light-emitting diodes (LEDs) deep into the UV-C band (200 nm to 280 nm), which are critical for germicidal disinfection, water sterilization, and specialized spectroscopy.  
Producing highly efficient LEDs at these wavelengths requires exceptionally high aluminum concentrations in the AlGaN quantum wells. This induces massive lattice mismatches with the underlying substrates, creating high threading dislocation densities that act as non-radiative recombination centers. Furthermore, the dominant emission mode in high-Al AlGaN shifts from transverse electric (TE) to transverse magnetic (TM), making light extraction vertically out of the chip exceedingly difficult18. Consequently, while commercial UV-C LEDs are available in single-nanometer increments, their output powers remain low compared to visible LEDs. For example, unmounted 255 nm LEDs yield only 0.4 mW of optical power at 30 mA drive currents, scaling slightly to 1.6 mW at 275 nm and 78 mW at 280 nm19. The spectral width (FWHM) of these devices typically ranges from 11 nm to 15 nm19.

### **Catalog of DUV and VUV Emitters (110 nm to 300 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **110 \- 162** | \~1 nm | H2 Gas Laser | \< 0.1% WPE | Milliwatt range | Specialized11 |
| **157** | \~1 nm | F2 Excimer Laser | \~0.2 \- 5% WPE | Multi-Watt (Pulsed) | Full Production9 |
| **172, 175** | \~1 nm | Xe2 Excimer | Low | High Peak Power | Specialized8 |
| **193** | \< 0.16% FWHM | ArF Excimer Laser | \~1 \- 5% WPE | Up to 90 W | Full Production4 |
| **213** | ≤ 1.0 cm⁻¹ | DPSS (Nd:YAG 5th Harm.) | \< 5% CE | 0.4 \- 2.5 µJ/pulse | Full Production11 |
| **222** | \~1 nm | KrCl Excimer Laser | \~1 \- 5% WPE | Multi-Watt (Pulsed) | Full Production8 |
| **224.3** | \< 1 pm | HeAg Gas Laser | Low | 100 µs pulse duration | Specialized11 |
| **228** | \< 1 MHz | DPSS (Nd:YVO4) | Low | Milliwatt range | Specialized22 |
| **233** | \~12 nm | AlGaN LED | Low | 0.6 mW | Early Commercial20 |
| **236** | \< 1 MHz | DPSS (Nd:YAG) | Low | Milliwatt range | Specialized22 |
| **248** | \~1 nm | KrF Excimer Laser | \~1 \- 5% WPE | Multi-Watt (Pulsed) | Full Production8 |
| **248.6** | \< 1 pm | NeCu Gas Laser | Low | 30 µs pulse duration | Specialized11 |
| **250** | 12 nm | AlGaN LED | Low | 1.0 mW | Full Production19 |
| **255** | 11 \- 12 nm | AlGaN LED | Low | 0.4 \- 1.0 mW | Full Production19 |
| **257** | \< 1 MHz | DPSS (Yb:YAG Harm.) | Low | Milliwatt range | Specialized22 |
| **257.3** | \< 1 pm | Argon Ion Laser | \< 0.1% WPE | Milliwatt range | Legacy11 |
| **260** | 12 nm | AlGaN LED | Low | 1.0 mW | Full Production19 |
| **262, 263** | \< 1.0 ns | DPSS (Nd:YLF 4th Harm.) | Moderate CE | 0.7 \- 6.0 mJ/pulse | Full Production17 |
| **265** | 11 nm | AlGaN LED | Low | 38.4 mW | Full Production20 |
| **266** | ≤ 1.0 cm⁻¹ | DPSS (Nd:YAG 4th Harm.) | Moderate CE | 0.1 \- 10 mJ/pulse | Full Production11 |
| **275** | 11 nm | AlGaN LED | Low | 1.6 \- 45.0 mW | Full Production19 |
| **280** | 11 nm | AlGaN LED | Low | 78 mW | Full Production20 |
| **282** | \~1 nm | XeBr Excimer Laser | Low | Multi-Watt (Pulsed) | Specialized8 |
| **285** | 11 nm | AlGaN LED | Low | 1.3 mW | Full Production19 |
| **290** | 11 nm | AlGaN LED | Low | 1.6 mW | Full Production19 |
| **295** | 11 nm | AlGaN LED | Low | 1.2 mW | Full Production19 |
| **300** | 11 nm | AlGaN LED | Low | 26 mW | Full Production20 |

## **Near Ultraviolet (UV-A): 300 nm to 400 nm**

The near-ultraviolet spectrum, particularly the UV-A band spanning 315 nm to 400 nm, is highly commercialized due to its widespread application in photopolymerization. The absorption of UV-A photons by photoinitiator molecules drives the crosslinking of oligomers and monomers, instantly curing industrial adhesives, inks, and coatings24.

### **Gas Lasers and Excimers in the UV-A**

Historically, the UV-A region was served by specialized gas lasers. The Helium-Cadmium (HeCd) laser, developed in the late 1960s, operates via radiative transitions of cadmium ions excited by resonant energy transfer from helium atoms. It provides continuous-wave (CW) output at 325 nm and 442 nm25. However, the wall-plug efficiency of HeCd lasers is exceptionally poor (typically below 0.1%), requiring kilowatts of input power to yield mere milliwatts of highly stable, narrow-linewidth (\< 1 pm) output13. Consequently, these systems are rapidly being replaced by advanced DPSS lasers operating at 320 nm, which offer over 200 mW of output with high spatial coherence (TEM00) and immense long-term stability without the thermal overhead of gas discharge tubes27.  
The Nitrogen (N2) laser is another legacy source, emitting predominantly at 337.1 nm (and weakly at 357.6 nm) via transitions within the second positive band of molecular nitrogen28. Because the upper laser level has a short radiative lifetime (\~40 ns) compared to the lower level, the population inversion is inherently transient, necessitating pulsed electrical discharge pumping29. Nitrogen lasers deliver incredibly short pulses (1 to 10 ns) with high peak powers (up to 100 kW), but their overall energy efficiency is strictly limited by the Franck-Condon principle to less than 0.1%28.  
For high-power industrial applications, the Xenon Chloride (XeCl) excimer at 308 nm and the Xenon Fluoride (XeF) excimer at 351 nm remain in widespread use, particularly in dermatology (e.g., treating psoriasis and vitiligo) and materials processing8.

### **The Dominance of InGaN UV-A LEDs**

Over the past two decades, the UV-A landscape has been completely revolutionized by the Indium Gallium Nitride (InGaN) material system. By tuning the indium concentration in the quantum wells, manufacturers can seamlessly shift the bandgap to produce LEDs across the entire UV-A spectrum. Unlike the high-aluminum AlGaN needed for UV-C, InGaN achieves excellent crystal quality and high internal quantum efficiencies.  
The commercial market is dominated by specific wavelength nodes corresponding to the absorption peaks of prevalent photoinitiator chemistries: 365 nm, 385 nm, 395 nm, and 405 nm24. The selection among these tightly clustered wavelengths involves specific physical trade-offs. The 365 nm wavelength provides high-energy photons for deep penetration into thick resins, making it suitable for legacy chemistries originally designed for broad-spectrum mercury vapor lamps33. Conversely, 395 nm and 405 nm LEDs exhibit much higher electrical-to-optical conversion efficiencies (exceeding 50% at low currents) and are heavily utilized for surface curing in digital printing and wood finishing18. The spectral width of these LEDs is relatively tight, typically around 10 nm to 15 nm FWHM19.  
High-power UV-A arrays combine hundreds of these LED dies to generate peak irradiances of up to 24 W/cm² (with water cooling) or 16 W/cm² (with air cooling), entirely displacing mercury lamps due to their instant on/off capabilities, operational lifetimes exceeding 20,000 hours, and lack of toxic ozone generation24. Commercial catalogs reveal that semiconductor foundries produce these devices in nearly single-nanometer increments to meet exact spectral requirements for fluorescence excitation, medical diagnostics, and specialized metrology19.  
In addition to spontaneous LED emission, highly coherent InGaN laser diodes are readily available in this band. Diodes centered at 375 nm, 380 nm, 390 nm, and 395 nm can output hundreds of milliwatts of continuous-wave power with spectral widths below 1 nm, serving as critical components in direct imaging photolithography23.

### **Catalog of Near Ultraviolet Emitters (300 nm to 399 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **305** | \< 1 MHz | DPSS (Nd:YVO4) | Low | Milliwatt range | Specialized22 |
| **308** | \~1 nm | XeCl Excimer Laser | \~1 \- 5% WPE | Multi-Watt (Pulsed) | Full Production8 |
| **310** | 15 nm | AlGaN LED | Low | 1.5 \- 38.5 mW | Full Production19 |
| **315** | \< 1 MHz | DPSS (Nd:YAG) | Low | Milliwatt range | Specialized22 |
| **320** | ≤ 500 kHz | CW DPSS Laser | Moderate | 200 mW | Full Production27 |
| **325** | \< 1 pm | HeCd Gas Laser | \< 0.1% WPE | Up to 20 mW | Legacy13 |
| **330** | \< 1 MHz | DPSS (Nd:YAG) | Low | Milliwatt range | Specialized22 |
| **336** | \< 1 MHz | DPSS (Nd:YVO4) | Low | Milliwatt range | Specialized22 |
| **337.1** | 0.1 nm | Nitrogen (N2) Laser | \< 0.1% WPE | 180 \- 200 µJ/pulse | Full Production28 |
| **340** | 9 \- 15 nm | AlGaN LED | Low | 0.3 \- 45.5 mW | Full Production19 |
| **343** | \< 1 MHz | DPSS (Yb:YAG) | Low | Milliwatt range | Specialized22 |
| **345 \- 350** | \< 1 ns | DPSS (Yb Fiber Harm.) | Moderate | Milliwatt range | Production11 |
| **349, 351** | \< 1.0 ns | DPSS (Nd:YLF 3rd Harm.) | Moderate | 1.5 \- 12.0 mJ/pulse | Production17 |
| **351** | \~1 nm | XeF Excimer Laser | \~1 \- 5% WPE | Multi-Watt (Pulsed) | Full Production8 |
| **355** | ≤ 1.0 cm⁻¹ | DPSS (Nd:YAG 3rd Harm.) | Moderate | 0.25 \- 20 mJ/pulse | Full Production16 |
| **357.6** | 0.1 nm | Nitrogen (N2) Laser | \< 0.1% WPE | Microjoule range | Specialized28 |
| **360** | 15 nm | InGaN LED | Moderate | 1.2 \- 1.8 mW | Full Production35 |
| **361** | \~15 nm | InGaN LED | Moderate | 1.5 mW | Full Production35 |
| **365** | 9 \- 15 nm | InGaN LED | High (\>40% WPE) | 1 mW to \> 2.0 W | Full Production20 |
| **370** | \~15 nm | InGaN LED | High | 1 mW to \> 1.2 W | Full Production35 |
| **375** | \< 1 nm | InGaN Laser Diode | High | 100 mW \- 1.0 W | Full Production38 |
| **380** | \~15 nm | InGaN LED / LD | High | 200 mW (LD), 10 mW (LED) | Full Production36 |
| **385** | 12 nm | InGaN LED | High | 2 mW to \> 1.6 W | Full Production19 |
| **390** | \~15 nm | InGaN LED | High | 8 mW to 500 mW | Full Production35 |
| **393** | 13 nm | InGaN LED | High | 2.0 mW | Full Production35 |
| **395** | 15 nm | InGaN LED / LD | High | 300 mW (LD), \> 1.4 W (LED) | Full Production19 |

## **Violet and Blue Spectrum: 400 nm to 495 nm**

The violet and blue region of the visible spectrum is foundational to modern display architectures, high-density optical data storage, and the generation of white light via phosphor down-conversion. This entire spectral band is unequivocally dominated by the Indium Gallium Nitride (InGaN) semiconductor material system.

### **InGaN LEDs and High-Power Lasers**

The bandgap of InGaN is directly governed by the ratio of indium to gallium during epitaxial growth. Because the crystal quality of InGaN remains extremely high at low indium concentrations, LEDs and laser diodes operating in the 400 nm to 450 nm range achieve the highest efficiencies of any visible semiconductor light source18. Blue LEDs routinely exceed external quantum efficiencies (EQE) and wall-plug efficiencies of 60% to 70%, with spectral emission widths (FWHM) reliably controlled between 15 nm and 25 nm18.  
Commercial catalogs demonstrate an exhaustive capability to manufacture InGaN devices at virtually any single-nanometer increment across this band. High-power continuous-wave (CW) laser diodes are produced in vast quantities at key wavelengths:

* **404 nm and 405 nm:** Originally developed for Blu-ray optical storage, these violet lasers now see massive deployment in 3D printing and direct imaging photolithography. Single emitters easily output between 1.0 W and 3.3 W, operating with wall-plug efficiencies up to 39%38.  
* **445 nm, 447 nm, 450 nm:** These deep blue lasers are the industrial workhorses for laser material processing, particularly for welding highly reflective metals like copper and gold in electric vehicle battery manufacturing, where blue light absorption is an order of magnitude higher than infrared light26. Single multimode emitters at 445 nm can output over 7.0 W, achieving extraordinary WPE values approaching 50%46.  
* **465 nm, 473 nm, 488 nm:** While historically these specific cyan/blue wavelengths were generated by complex DPSS systems or Argon-ion gas lasers, they are now directly accessible via native InGaN laser diodes, delivering hundreds of milliwatts with absolute spectral purity (\< 1 nm linewidth) for flow cytometry, biomedical fluorescence, and laser light shows39.

### **Advances in Blue OLED Emitters**

While inorganic InGaN dominates the high-power domain, Organic Light Emitting Diodes (OLEDs) dictate the architecture of premium consumer displays (smartphones, televisions). Achieving efficient, deep blue emission in OLEDs remains one of the most critical challenges in organic optoelectronics48.  
Traditional fluorescent blue OLEDs are fundamentally limited to a 25% internal quantum efficiency (IQE) because 75% of the injected charge carriers inevitably form non-emissive triplet excitons due to quantum spin statistics. While Phosphorescent OLEDs (Ph-OLEDs) incorporate heavy metals like Iridium or Platinum to harvest these triplets via strong spin-orbit coupling, the immense energy of blue excitons breaks the chemical bonds within the organic host materials (homolytic dissociation), leading to disastrously short operational lifetimes49.  
To bypass these limitations, researchers have developed Thermally Activated Delayed Fluorescence (TADF). TADF molecules are meticulously synthesized to possess a near-zero energy gap (![][image1]) between the singlet and triplet excited states. This minimal gap permits reverse intersystem crossing (RISC), wherein ambient thermal energy upconverts the "dark" triplet states back into emissive singlet states, achieving a theoretical IQE of 100% without utilizing heavy metals48.  
Recently, the field has advanced to Multi-Resonance Charge Transfer (MRCT) TADF emitters. These highly rigid molecular frameworks localize the highest occupied molecular orbital (HOMO) and lowest unoccupied molecular orbital (LUMO) to prevent vibronic relaxation. The result is a monumental leap in OLED color purity: recent sky-blue MRCT-TADF devices emitting at **485 nm** demonstrate exceptionally narrow FWHM values of just 20 nm and extraordinary External Quantum Efficiencies (EQE) exceeding 40%48. Furthermore, optimizing the microcavity effect within top-emission OLED (TEOLED) architectures—by utilizing low-refractive-index electron and hole transport layers to minimize surface plasmon losses against the metal cathode—further narrows the emission spectrum toward laser-like purity48.

### **Catalog of Violet and Blue Emitters (400 nm to 495 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **400** | 15 nm | InGaN LED | High | 1.0 W | Full Production42 |
| **404 \- 405** | \< 1 nm | InGaN Laser Diode | \~39% WPE | Up to 3.3 W | Full Production26 |
| **413.1** | \< 1 pm | Krypton Gas Laser | \< 0.1% WPE | Milliwatt range | Legacy53 |
| **415** | 14 nm | InGaN LED / LD | High | 1.9 W (LED), 120 mW (LD) | Full Production20 |
| **420 \- 425** | \< 1 nm | InGaN Laser Diode | Moderate | 10 \- 120 mW | Full Production38 |
| **430** | 17 \- 20 nm | InGaN LED | High | 500 \- 750 mW | Full Production19 |
| **435** | 22 nm | InGaN LED | High | 800 mW | Full Production42 |
| **440** | \< 1 nm | DPSS (Nd:YAG) / LD | Moderate | 100 mW | Specialized22 |
| **442** | \< 1 pm | HeCd Gas Laser | \< 0.1% WPE | 50 mW | Legacy25 |
| **445 \- 450** | \< 1 nm | InGaN Laser Diode | \~30 \- 50% WPE | Up to 7.0 W | Full Production46 |
| **455** | 18 nm | InGaN LED | High | 1.4 W | Full Production20 |
| **457** | \< 1 MHz | DPSS / Argon Ion | Moderate | 50 \- 400 mW | Full Production47 |
| **460** | 16 nm | InGaN LED / LD | High | 50 mW (LD) | Full Production37 |
| **465** | 25 nm | InGaN LED / LD | High | 3 W (LD), 20 mW (LED) | Full Production19 |
| **470** | 22 \- 28 nm | InGaN LED / LD | High | 170 mW \- 1.1 W | Full Production19 |
| **473** | \< 1 MHz | DPSS / InGaN LD | Moderate | 25 \- 300 mW | Full Production22 |
| **476.2** | \< 1 pm | Krypton / Argon Ion | \< 0.1% WPE | Milliwatt range | Legacy53 |
| **480** | \~20 nm | InGaN LED / LD | High | 60 \- 80 mW | Full Production39 |
| **485** | 20 nm | MRCT-TADF OLED | \> 40% EQE | N/A | Advanced R\&D49 |
| **486** | 20.7 nm | NKLSO Cyan Phosphor | Good | Down-conversion | Specialized55 |
| **488** | \< 1 nm | InGaN LD / Argon Ion | Moderate | 20 \- 200 mW | Full Production39 |
| **490** | 26 nm | InGaN LED | High | 240 mW | Full Production20 |
| **491** | \< 1 MHz | DPSS Laser | Moderate | 50 \- 200 mW | Production47 |
| **495** | \~30 nm | InGaN LED | High | 90 lm/W | Full Production42 |

## **The Green Gap: 500 nm to 599 nm**

The spectral region from 500 nm to 600 nm represents arguably the most profound physical challenge in direct semiconductor light emission—a phenomenon universally recognized as the "Green Gap." Despite the human eye's photopic response peaking precisely at 555 nm, making highly efficient green light absolutely critical for displays and white lighting, the intrinsic physics of available materials aggressively resists efficient emission in this band.  
The Aluminum Gallium Indium Phosphide (AlGaInP) material system, which is incredibly efficient for red and amber LEDs, transitions from a direct bandgap to an indirect bandgap at wavelengths shorter than approximately 600 nm, causing a catastrophic collapse in radiative recombination efficiency44.  
Consequently, the burden falls on the InGaN system. To push InGaN emission from blue (450 nm) into the green and yellow bands (520 nm to 590 nm), the molar fraction of Indium within the multiple quantum wells (MQWs) must be substantially increased. However, the lattice constant of Indium Nitride differs massively from the underlying Gallium Nitride substrate. Forcing high-indium InGaN to grow on GaN generates immense compressive strain within the crystal lattice. This strain triggers a massive internal piezoelectric field that severely tilts the energy bands of the quantum well44.  
This band tilting physically pulls the electron and hole wavefunctions to opposite sides of the quantum well—an effect known as the Quantum Confined Stark Effect (QCSE)44. The spatial separation drastically reduces the probability of radiative recombination, causing internal quantum efficiency (IQE) to plummet. Furthermore, as injection current increases, the injected carriers screen the piezoelectric field, causing the bands to un-tilt and the emission wavelength to exhibit a massive, undesirable blueshift (often 10 nm to 30 nm)44.

### **Engineering the Green Gap**

Despite these fundamental barriers, aggressive epitaxial engineering has yielded remarkable progress. By incorporating 3D p-n junctions utilizing V-pits (hexagonal defect structures that act as energy barriers to screen threading dislocations from non-radiative recombination), and by deploying compositionally graded quantum wells, the severity of the QCSE can be mitigated44.  
State-of-the-art laboratory devices have recently shattered historical efficiency limits. Direct-emitting InGaN green LEDs at **527 nm** have achieved astonishing peak EQEs of 53.3% and wall-plug efficiencies of 54.1%61. Pushing the limits further, researchers have successfully fabricated InGaN LEDs extending into the yellow and orange bands. By lowering growth temperatures and managing strain via V-pit density optimization, LEDs at **574 nm** reached 33% WPE, **599 nm** achieved 18.1% WPE, and optimized **608 nm** devices hit a 24.0% WPE44.  
In the domain of coherent light, native green InGaN laser diodes at **520 nm** and **525 nm** are now in mass commercial production. While their WPE (typically 10% to 17%) is vastly lower than their blue counterparts, they are capable of delivering 1.0 W to 1.5 W of continuous output, sufficient for laser projection and biomedical imaging37.

### **DPSS Harmonics and Phosphor Down-Conversion**

For applications requiring multi-watt power levels with immaculate beam quality (M² near 1.0) and ultra-narrow linewidths in the green spectrum, the DPSS architecture remains entirely unmatched. The **532 nm** DPSS laser is ubiquitous in industry, scientific research, and laser light shows. It operates by utilizing an 808 nm diode to pump a Neodymium-doped crystal (Nd:YAG or Nd:YVO4) to generate 1064 nm light. This fundamental beam is directed through a nonlinear optical crystal (such as KTP or LBO) to facilitate Second Harmonic Generation (SHG), halving the wavelength to 532 nm15. Other common visible DPSS lines serving this spectral gap include **515 nm** (from Yb:YAG), **553 nm**, **561 nm**, and **594 nm**22.  
Because high-efficiency direct green emission remains difficult at mass-manufacturing scales, the display and lighting industries rely almost entirely on phosphor down-conversion. By coating an efficient 450 nm blue LED with specialized phosphors, high-quality green light is synthesized. A prominent industrial standard is the **β-SiAlON:Eu²⁺** oxynitride phosphor, which emits at **538 nm** with a brilliant internal quantum efficiency of 91%62. However, its emission profile is somewhat broad, with a FWHM of 48 nm62. To achieve wider color gamuts in LCD backlights, novel narrow-band phosphors such as the cyan-emitting **NKLSO:Eu²⁺** at **486 nm** (FWHM 20.7 nm) and the green-emitting **Zn₄B₆O₁₃:Mn²⁺** at **540 nm** (FWHM 33 nm) are being rapidly developed55.

### **The Rise of Perovskite Quantum Dots**

The most promising long-term solution to the Green Gap resides in Colloidal Quantum Dots (QDs). Unlike bulk semiconductors, the emission wavelength of a quantum dot is dictated by the physical diameter of the nanocrystal rather than a fixed chemical bandgap, governed by the quantum confinement of excitons63.  
Cadmium-free Perovskite Quantum Dots (PQDs), particularly the Cesium Lead Halide family (CsPbX₃), have revolutionized emissive technologies. By precisely controlling the nanoparticle diameter (typically between 2 nm and 10 nm) and the halide anion composition (Cl, Br, I), emission can be tuned to absolute single-nanometer precision across the entire visible spectrum66.  
PQDs boast astonishing optical characteristics: their excitation spectrum is broad and continuous, allowing a single blue LED to pump a multitude of different dot sizes simultaneously68. Furthermore, due to the discrete, quantized energy states within the dot, electrons and holes rapidly relax to the absolute band edge before recombining. This eliminates inhomogeneous broadening, resulting in purely symmetric, Gaussian emission spectra with an ultra-narrow FWHM of 16 nm to 25 nm67. Through meticulous surface ligand engineering and the introduction of plasmonic gold nanoparticles to accelerate radiative recombination rates, the Photoluminescence Quantum Yield (PLQY) of green PQDs now routinely approaches 95% to 99%70. Electrically injected (rather than optically pumped) green Perovskite LEDs (PeLEDs) utilizing an Interfacial Potential-Graded (IPG) ZnSeTe core/shell architecture have recently achieved emission at **520 nm** with an EQE of 21.7%, while other formulations hit 24% EQE at **517 nm**69.

### **Catalog of Green Gap Emitters (500 nm to 599 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **505** | 30 nm | InGaN LED / LD | Moderate | 4 mW (LED), 30 mW (LD) | Full Production19 |
| **510** | \< 1 nm | InGaN Laser Diode | Moderate | 50 mW | Full Production37 |
| **514 \- 515** | \< 1 MHz | DPSS / Argon Ion | Moderate | 25 \- 300 mW | Full Production45 |
| **517** | 16 nm | Perovskite QD LED | 24% EQE | High Brightness | Advanced R\&D69 |
| **520 \- 525** | \< 1 nm | InGaN Laser Diode | \~10 \- 17% WPE | Up to 1.5 W | Full Production37 |
| **527** | \~30 nm | InGaN Green LED | 54.1% WPE, 53.3% EQE | 24 mW | Advanced R\&D61 |
| **528.7** | \< 1 pm | Argon Ion Laser | \< 0.1% WPE | Milliwatt range | Legacy53 |
| **530** | \~30 nm | InGaN LED / Fiber | Moderate | 6.8 mW | Full Production23 |
| **532** | \< 1 MHz | DPSS (Nd:YAG SHG) | \~20 \- 35% WPE | Milliwatts to Kilowatts | Full Production15 |
| **538** | 48 nm | β-SiAlON Phosphor | 91% IQE | Down-conversion | Full Production62 |
| **540** | 33 nm | Zn₄B₆O₁₃ Phosphor | Near Zero Thermal Quench | Down-conversion | Specialized62 |
| **545** | 39 nm | InGaN LED | Moderate | 2.4 \- 8.7 mW | Full Production19 |
| **550** | \~30 nm | InGaN LED | Moderate | 100 mW | Full Production42 |
| **553 \- 554** | \< 5 kHz (Pulse) | DPSS Laser / LED | Moderate | 20 \- 50 mW | Production23 |
| **560 \- 562** | 41 nm | InGaN Yellow-Green LED | 19.58 lm/W | 2.14 mW | Early Commercial19 |
| **561** | \< 1 MHz | DPSS Laser | Moderate | 25 \- 500 mW | Full Production47 |
| **565 \- 570** | \~15 nm | InGaN LED | Moderate | 0.3 \- 9.9 mW | Full Production19 |
| **574** | \~30 nm | InGaN Yellow LED | 33% WPE | N/A | Advanced R\&D44 |
| **577, 578.2** | \< 1 pm | OPSL / Copper Vapor | Low | Variable | Specialized53 |
| **590 \- 591** | 15 \- 20 nm | InGaN LED | Moderate | 2.0 \- 120 mW | Full Production19 |
| **593.5** | \< 1 MHz | DPSS (Sum Freq.) | Low | Milliwatt range | Specialized15 |
| **594 \- 595** | \< 1 MHz / 75nm | DPSS / InGaN LED | Moderate | 8.7 \- 100 mW | Production19 |
| **599** | \~30 nm | InGaN Orange LED | 18.1% WPE | N/A | Early Commercial44 |

## **Orange and Deep Red Spectrum: 600 nm to 750 nm**

The red spectrum (600 nm to 750 nm) demands light sources capable of reaching the deep-red chromaticity coordinates defined by the Rec. 2020 color gamut standards for ultra-high-definition displays (ideally targeting 620 nm to 640 nm). At these wavelengths, the underlying materials physics presents a stark dichotomy between macro-scale power and micro-scale efficiency.

### **The AlGaInP Micro-LED Scaling Crisis**

At macroscopic scales (die sizes \> 300 µm), the Aluminum Gallium Indium Phosphide (AlGaInP) material system is exceptionally well-suited for red emission, delivering internal quantum efficiencies (IQE) that approach theoretical perfection (near 100%) due to its precise lattice-matching with Gallium Arsenide (GaAs) substrates73. Commercial catalogs reveal a massive array of AlGaInP-based high-power laser diodes at distinct nodes (**635, 638, 650, 660, 675, 690 nm**) that output up to 3.0 W of continuous power with staggering wall-plug efficiencies routinely exceeding 40%37.  
However, the display industry is rapidly transitioning toward micro-LED architectures (chip dimensions \< 50 µm) for augmented reality (AR) and next-generation televisions. A fundamental scaling crisis occurs at this scale. As the physical size of an LED shrinks, the perimeter-to-area ratio increases dramatically. Charge carriers within the semiconductor bulk diffuse laterally toward the chip edges, which have been physically damaged by dry-etching manufacturing processes. The AlGaInP material system suffers from an extraordinarily high surface recombination velocity—an order of magnitude worse than InGaN—causing injected carriers to recombine non-radiatively at the sidewalls73. Consequently, the EQE of red AlGaInP micro-LEDs collapses catastrophically from over 40% at macro scales to barely 2-5% at micro scales75.  
To circumvent this, researchers are exploring two parallel paths. The first involves passivating the AlGaInP sidewall defects using atomic layer deposition (ALD) or proprietary sidewall steam oxidation techniques to physically block lateral current flow into the damaged perimeter regions, thereby recovering up to a 31% increase in optical output75. The second path involves forcefully extending the InGaN material system—which possesses a much lower surface recombination velocity—deep into the red spectrum. Recent engineering utilizing pseudo-substrates and photonic crystals has produced InGaN red micro-LEDs emitting at **617 nm** and **630 nm** with incredibly narrow FWHM bandwidths (5 nm), though their peak EQEs still struggle in the 2.7% range59.

### **The KSF Phosphor Revolution**

One of the most consequential breakthroughs in commercial display backlighting and general illumination is the deployment of **KSF Phosphor (K2SiF6:Mn⁴⁺)**.  
Historically, generating warm white light or red sub-pixels involved coating blue LEDs with nitride-based red phosphors (such as CASN). While robust, these conventional phosphors exhibit exceedingly broad, bell-shaped emission bands (FWHM \> 80 nm) that invariably bleed deep into the near-infrared spectrum (700 nm to 800 nm)77. Because the human eye has almost zero photopic sensitivity beyond 700 nm, any electromagnetic energy radiated at those longer wavelengths is entirely wasted as invisible heat, destroying the Luminous Efficacy of Radiation (LER)78.  
KSF, activated by Manganese (Mn⁴⁺) ions, operates on entirely different quantum mechanical principles. It leverages spin- and parity-forbidden electronic transitions (²Eg → ⁴A2g) situated within a highly symmetrical cubic crystal field. When optically pumped by a 450 nm blue LED, the KSF phosphor emits five discrete, ultra-sharp spectral lines in the red region. The dominant primary peak is locked at **631 nm** and exhibits a breathtakingly narrow FWHM of just **\~3 nm to 5 nm**79.  
Because the KSF emission spectrum truncates abruptly before 650 nm, it completely eliminates infrared spillover. Substituting broad nitride phosphors with KSF elevates the LER of a high-color-rendering (90 CRI) white LED from a stagnant 280 lm/W to over 330 lm/W. This represents a monumental leap in power efficiency, fundamentally transforming the thermal and electrical budgets of liquid crystal displays (LCDs) and commercial luminaires78.

### **Perovskite Red QLEDs**

Simultaneously, colloidal perovskite quantum dots (PQDs) are challenging OLEDs and micro-LEDs for the future of red pixel generation. By carefully optimizing the synthesis of CsPbI₃ quantum dots and implementing composite ligand strategies (such as 3-phenyl-1-propylamine) to passivate surface vacancy defects without inducing phase transitions, researchers have realized pure-red perovskite LEDs (PeLEDs)82. These devices emit precisely at **636 nm**—hitting the exact chromaticity coordinates (0.703, 0.297) required by the Rec. 2020 standard—while demonstrating an EQE of 20.8% and brilliant luminances nearing 4,000 cd/m²82.

### **Catalog of Orange and Red Emitters (600 nm to 749 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **600, 610** | 12 nm | AlGaInP LEDs | Moderate | 3 \- 8 mW | Full Production19 |
| **606** | 50 nm | InGaN Amber LED | 0.56% EQE | 5 µW (40µm chip) | Advanced R\&D59 |
| **608** | \~30 nm | InGaN Red LED | 24.0% WPE | N/A | Advanced R\&D44 |
| **617** | 5 nm | InGaN Red Micro-LED | \~1 \- 2% EQE | Micro-scale | Advanced R\&D60 |
| **620** | 20 nm | AlGaInP LED | High | 190 mW | Full Production42 |
| **622, 625** | 14 \- 20 nm | AlGaInP LED / LD | High | 9 \- 13 mW (LED) | Full Production19 |
| **630** | \~15 nm | InGaN / AlGaInP LED | 2.71% EQE (InGaN) | 16 \- 330 mW | Production / R\&D19 |
| **631** | 3 \- 5 nm | KSF Phosphor | \> 90% IQE | Down-conversion | Full Production79 |
| **632.8** | \< 1 pm | Helium-Neon Gas Laser | \< 0.1% WPE | 1 \- 50 mW | Legacy53 |
| **635 \- 638** | \< 1 nm | AlGaInP Laser Diode | \~40% WPE | Up to 2.4 W | Full Production37 |
| **639** | \< 1 nm | AlGaInP Laser Diode | 44.9% WPE | High Power | Advanced R\&D84 |
| **640 \- 647** | \< 1 nm | AlGaInP / Krypton Laser | Moderate | 30 \- 300 mW | Full Production37 |
| **650, 655** | \< 1 nm | AlGaInP Laser Diode | Moderate | 25 mW \- 300 mW | Full Production37 |
| **659 \- 660** | 14 nm (LED) | AlGaInP LD / LED | High | Up to 3.0 W (LD) | Full Production19 |
| **670, 671** | 22 nm (LED) | AlGaInP LD / DPSS | High | 12 \- 520 mW | Full Production19 |
| **675, 676.4** | \< 1 nm | AlGaInP LD / Krypton | 42.8% WPE (LD) | 1.3 W (LD) | Full Production46 |
| **680, 685** | 16 nm (LED) | AlGaInP LD / LED | High | 5.9 \- 650 mW | Full Production19 |
| **690** | \< 1 nm | AlGaInP Laser Diode | 44.1% WPE | 1.3 W | Full Production42 |
| **700** | \~20 nm | AlGaInP LED | High | 4.0 \- 200 mW | Full Production23 |
| **710** | \~20 nm | AlGaInP LED | High | Multi-milliwatt | Full Production85 |
| **720** | \~20 nm | AlGaInP LED | High | 170 \- 520 mW | Full Production42 |
| **730, 735** | \~20 nm | AlGaInP LED / LD | High | 50 \- 250 mW | Full Production42 |
| **740** | \~20 nm | AlGaInP LED | High | 4.1 \- 290 mW | Full Production23 |

## **Near-Infrared and Short-Wave Infrared: 750 nm to 1500 nm**

Transitioning beyond the threshold of human vision, the near-infrared (NIR) and short-wave infrared (SWIR) bands are entirely driven by the demands of machine vision, telecommunications, biometric sensing, and medical imaging. These wavelengths are generated utilizing Gallium Arsenide (GaAs) and Indium Phosphide (InP) heterostructures.

### **Biometrics, Medical Lasers, and LiDAR**

The segment between 750 nm and 1000 nm relies heavily on GaAs-based LEDs and VCSELs (Vertical-Cavity Surface-Emitting Lasers)86.

* **850 nm vs. 940 nm:** These two nodes are the backbone of consumer biometric sensing (e.g., facial recognition in smartphones). LEDs operating at 850 nm offer tremendous sensitivity on inexpensive, standard silicon CMOS camera sensors. However, because their spectral tail bleeds slightly into the visible red, they can emit a faint, distinct red glow visible to a dark-adapted human eye86. The 940 nm LED, conversely, is entirely covert, eliminating the red glow, making it ideal for discreet security cameras and non-invasive medical sensing (like pulse oximetry), although it suffers from minor absorption by atmospheric water vapor86.  
* **Medical and Dermatological Lasers:** Specific high-power diode and DPSS lasers serve tailored medical applications based on their interaction with tissue chromophores (water, hemoglobin, melanin). **755 nm** (often from Alexandrite lasers) targets epidermal pigmentation; **810 nm** to **830 nm** are widely used for Low-Level Laser Therapy (LLLT) and nerve repair; and **980 nm** is heavily absorbed by water, making it ideal for surgical ablation and varicose vein treatment86. High power multimode diodes at 980 nm and 1064 nm can continuously output over 10 to 16 Watts43.  
* **905 nm vs. 1550 nm in LiDAR:** Automotive Light Detection and Ranging (LiDAR) presents a fierce wavelength competition. Cost-sensitive systems utilize 905 nm laser diodes because they pair perfectly with cheap silicon avalanche photodiodes (APDs). However, because 905 nm light focuses directly onto the human retina, laser power must be strictly limited to adhere to Class 1 eye safety regulations, inherently limiting range88. Conversely, **1550 nm** light lies in the SWIR band. The human cornea and lens heavily absorb this wavelength *before* it reaches the retina, effectively shielding the eye. Consequently, 1550 nm LiDAR systems can pulse at laser powers orders of magnitude higher than 905 nm systems, allowing them to punch through rain, haze, and dust at significantly longer ranges. The primary drawback is that 1550 nm requires expensive Indium Gallium Arsenide (InGaAs) photodetectors88.

### **Silicon Photonics and Telecommunications**

The explosion of artificial intelligence (AI) and the resulting exponential growth in datacenter traffic has strained traditional electrical copper interconnects to their physical limits. The industry is rapidly pivoting toward Silicon Photonics and Co-Packaged Optics (CPO) to embed optical transceivers directly alongside network switch ASICs90.  
Silicon, being an indirect bandgap material, cannot generate light efficiently. Therefore, Silicon Photonics mandates the integration of external Indium Phosphide (InP) Distributed Feedback (DFB) lasers, typically attached via heterogeneous wafer bonding or flip-chip techniques91.  
These DFB lasers operate precisely at the fundamental telecommunications windows governed by the properties of silica optical fiber: **1310 nm** (the O-band, which represents the zero-dispersion point in silica, preventing signal distortion over distance) and **1550 nm** (the C-band, which represents the absolute minimum physical attenuation point)90.  
The integration of DFB lasers into dense silicon chips creates massive thermal management challenges, as localized heat from adjacent modulators can shift the laser's center wavelength (typically \~0.1 nm/°C) and degrade its Side Mode Suppression Ratio (SMSR)91. To counteract this, modern uncooled 1310 nm CW DFB chips have been engineered utilizing large optical cavity designs and proprietary low series-resistance InP structures that completely eliminate aluminum from the active quantum well. These advancements allow the lasers to operate at junction temperatures up to 85°C. Current state-of-the-art 1310 nm DFB chips can output up to 880 mW of out-of-facet power at 25°C, boasting slope efficiencies of 0.45 W/A and maintaining a strict single longitudinal mode with an SMSR greater than 50 dB90. Most importantly, they push Power Conversion Efficiency (PCE) beyond the 10% to 15% threshold critical for the strict power budgets of AI data centers90.

### **Catalog of NIR and SWIR Emitters (750 nm to 1550 nm)**

| Wavelength (nm) | Spectral Width | Source Type | Power Efficiency | Output Power | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **750 \- 760** | \< 1 nm | GaAs Laser Diode | High | Up to 16 W (Array) | Full Production43 |
| **770 \- 785** | \< 1 pm (LD) | GaAs LED / LD | High | 120 mW \- 500 mW (LD) | Full Production43 |
| **797** | \< 1 nm | GaAs Laser Diode | High | Up to 12.8 W | Full Production43 |
| **800, 808** | \< 1 nm | GaAs Laser Diode | High | Up to 16 W | Full Production43 |
| **810 \- 840** | \~20 nm (LED) | GaAs LED / LD | High | 12.7 mW (Fiber) | Full Production23 |
| **845, 850** | \~20 nm (LED) | GaAs LED / LD | High (\>40%) | 250 \- 322 mW | Full Production42 |
| **855 \- 870** | \~20 nm | GaAs LED | High | Multi-milliwatt | Full Production85 |
| **880 \- 890** | \~20 nm | GaAs LED / Fiber LD | High | 2.7 mW (Fiber) | Full Production23 |
| **905, 910, 915** | \< 1 nm | GaAs Laser Diode | High | Multi-Watt (Pulsed) | Full Production43 |
| **920 \- 935** | \< 1 nm | GaAs Laser Diode | Moderate | Medical usage | Full Production86 |
| **940, 945** | \~20 nm | GaAs LED / Fiber LD | High | \> 250 mW | Full Production23 |
| **970** | \~20 nm (LED) | GaAs LED / LD | High | 5.9 mW (Fiber) | Full Production23 |
| **980** | \< 1 nm | GaAs Laser Diode | High | \> 10 W | Full Production43 |
| **1015, 1030** | \< 1 nm | Yb:YAG / InGaAs LD | High | Watts range | Full Production22 |
| **1045, 1047** | \~20 nm (LED) | GaAs LED / Nd:YLF | High | 200 mW (LED) | Full Production22 |
| **1050, 1053** | \~20 nm (LED) | SWIR LED / Nd:YLF | Moderate | 2.3 mW (Fiber LED) | Full Production17 |
| **1064** | \< 1 MHz | Nd:YAG / InGaAs LD | High | 400 mW to kWs | Full Production16 |
| **1070** | \< 1 nm | Fiber Laser / Bar | High | Up to 500W QCW | Full Production43 |
| **1100** | \~30 nm | SWIR LED | Moderate | 2.0 mW (Fiber) | Full Production23 |
| **1130** | \< 1 nm | InGaAs Laser Diode | Moderate | Up to 12.8 W | Full Production43 |
| **1200, 1210** | \~30 nm | SWIR LED / LD | Moderate | 1.6 mW (Fiber LED) | Full Production23 |
| **1240, 1270** | \< 1 MHz | Quantum Dot / DFB | Moderate | 30 \- 100 mW | Full Production43 |
| **1280** | \< 1 nm | InGaAs Laser Diode | Moderate | Up to 12.8 W | Full Production43 |
| **1300** | \~30 nm | SWIR LED | Moderate | 1.42 mW (Fiber) | Full Production23 |
| **1310** | \< 150 kHz | InGaAsP DFB Laser | \~15% WPE | 60 \- 880 mW | Full Production90 |
| **1330, 1342** | \~30 nm | SWIR LED / Nd:YVO4 | Moderate | 70 mW (LED) | Full Production22 |
| **1370, 1400** | \< 1 nm | InGaAsP Laser Diode | Moderate | Up to 12.8 W | Full Production43 |
| **1460, 1470** | \< 1 nm | InGaAsP / InP LD | Moderate | Up to 12 W | Full Production43 |
| **1480, 1485** | \< 1 MHz | InGaAsP DFB / LD | Moderate | 30 mW to Watts | Full Production15 |
| **1535** | \< 1 nm | SWIR Laser Diode | Moderate | Up to 3 W | Full Production43 |
| **1550** | \< 150 kHz | InGaAsP DFB Laser | \~10 \- 15% WPE | \> 100 mW | Full Production43 |

#### **Works cited**

1. EUV lithography systems – Products \- ASML, [https://www.asml.com/en/products/euv-lithography-systems](https://www.asml.com/en/products/euv-lithography-systems)  
2. ASML Boosts EUV Power to 1,000W for Better Yields and Lower Chip Costs | TechPowerUp, [https://www.techpowerup.com/346671/asml-boosts-euv-power-to-1-000w-for-better-yields-and-lower-chip-costs](https://www.techpowerup.com/346671/asml-boosts-euv-power-to-1-000w-for-better-yields-and-lower-chip-costs)  
3. Microdroplet-tin plasma sources of EUV radiation driven by solid-state-lasers (Topical Review) \- ARCNL Institutional Repository, [https://ir.arcnl.nl/pub/257/00205publishedVersion.pdf](https://ir.arcnl.nl/pub/257/00205publishedVersion.pdf)  
4. Extreme ultraviolet lithography \- Wikipedia, [https://en.wikipedia.org/wiki/Extreme\_ultraviolet\_lithography](https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography)  
5. EUV Source Technology: Challenges and Status \- SPIE, [https://spie.org/samples/PM149.pdf](https://spie.org/samples/PM149.pdf)  
6. Production of 13.5 nm light with 5% conversion efficiency from 2 μm laser-driven tin microdroplet plasma \- ARCNL, [https://arcnl.nl/publications/production-of-13-5-nm-light-with-5-conversion-efficiency-from-2-%CE%BCm-laser-driven-tin-microdroplet-plasma](https://arcnl.nl/publications/production-of-13-5-nm-light-with-5-conversion-efficiency-from-2-%CE%BCm-laser-driven-tin-microdroplet-plasma)  
7. What Are the Efficiency Metrics for EUV Lithography in Chip Fabrication \- PatSnap Eureka, [https://eureka.patsnap.com/report-what-are-the-efficiency-metrics-for-euv-lithography-in-chip-fabrication](https://eureka.patsnap.com/report-what-are-the-efficiency-metrics-for-euv-lithography-in-chip-fabrication)  
8. Excimer laser \- Wikipedia, [https://en.wikipedia.org/wiki/Excimer\_laser](https://en.wikipedia.org/wiki/Excimer_laser)  
9. Excimer Lasers \- RP Photonics, [https://www.rp-photonics.com/excimer\_lasers.html](https://www.rp-photonics.com/excimer_lasers.html)  
10. Development of Tunable Excimer Lasers \- DTIC, [https://apps.dtic.mil/sti/tr/pdf/ADA213521.pdf](https://apps.dtic.mil/sti/tr/pdf/ADA213521.pdf)  
11. Commercial Laser Lines | Photonics Marketplace, [https://www.photonics.com/LinearChart.aspx?ChartID=1](https://www.photonics.com/LinearChart.aspx?ChartID=1)  
12. Excimer lasers and their applications in industrial technology and in medicine, [https://optor.wat.edu.pl/1992/1%281%2913.pdf](https://optor.wat.edu.pl/1992/1%281%2913.pdf)  
13. Advanced Detection Electronics \- Photon Systems, [https://photonsystems.com/technology/advanced-detection-electronics/](https://photonsystems.com/technology/advanced-detection-electronics/)  
14. Multi mode high energy Q-switched Nd:YAG Lasers NanoFLux MM | EKSPLA, [https://ekspla.com/products/mm-high-energy-q-switched-ndyag-lasers-nanoflux-mm/](https://ekspla.com/products/mm-high-energy-q-switched-ndyag-lasers-nanoflux-mm/)  
15. What's in DPSS laser modules \- BeamQ, [https://beamq.com/laser/whats-in-dpss-laser-modules/](https://beamq.com/laser/whats-in-dpss-laser-modules/)  
16. Passively Q-switched DPSS Lasers, [https://www.sintec.sg/static/upload/file/DPSSp.pdf](https://www.sintec.sg/static/upload/file/DPSSp.pdf)  
17. Q2 \- High Energy DPSS Nanosecond laser | QLI \- Quantum Light Instruments, [https://www.qlinstruments.com/products/q-switched-lasers/dpss-lasers-q2/](https://www.qlinstruments.com/products/q-switched-lasers/dpss-lasers-q2/)  
18. Initial Benchmarks of UV LEDs and Comparisons with White LEDs \- Department of Energy, [https://www.energy.gov/sites/default/files/2022-01/ssl-rti-uv-leds-nov2021.pdf](https://www.energy.gov/sites/default/files/2022-01/ssl-rti-uv-leds-nov2021.pdf)  
19. Unmounted LEDs \- Thorlabs, [https://www.thorlabs.com/unmounted-leds](https://www.thorlabs.com/unmounted-leds)  
20. Mounted LEDs \- Thorlabs, [https://www.thorlabs.com/mounted-leds](https://www.thorlabs.com/mounted-leds)  
21. High-power gas-discharge excimer ArF, KrCl, KrF and XeCl lasers utilising two-component gas mixtures without a buffer gas \- INIS-IAEA, [https://inis.iaea.org/records/a5kt8-b3v91](https://inis.iaea.org/records/a5kt8-b3v91)  
22. Lasers \- ALPHALAS, [https://www.alphalas.com/products/lasers/](https://www.alphalas.com/products/lasers/)  
23. Fiber-Coupled LEDs \- Thorlabs, [https://www.thorlabs.com/fiber-coupled-leds](https://www.thorlabs.com/fiber-coupled-leds)  
24. Understanding Ultraviolet LED Wavelength \- UV+EB Technology, [https://uvebtech.com/articles/2016/understanding-ultraviolet-led-wavelength/](https://uvebtech.com/articles/2016/understanding-ultraviolet-led-wavelength/)  
25. What is a HeCd Laser? \- 405nm.com, [https://405nm.com/what-is-a-hecd-laser/](https://405nm.com/what-is-a-hecd-laser/)  
26. Blue laser \- Grokipedia, [https://grokipedia.com/page/Blue\_laser](https://grokipedia.com/page/Blue_laser)  
27. 320 nm laser, single frequency CW DPSS UV laser, HeCd alternative \- Skylark Lasers, [https://skylarklasers.com/products/320-nx/](https://skylarklasers.com/products/320-nx/)  
28. Nitrogen laser \- Wikipedia, [https://en.wikipedia.org/wiki/Nitrogen\_laser](https://en.wikipedia.org/wiki/Nitrogen_laser)  
29. Nitrogen laser \- Grokipedia, [https://grokipedia.com/page/Nitrogen\_laser](https://grokipedia.com/page/Nitrogen_laser)  
30. 337 nm molecular nitrogen laser excited by pulsed inductive discharge \- art. no. 67311D, [https://www.researchgate.net/publication/253026465\_337\_nm\_molecular\_nitrogen\_laser\_excited\_by\_pulsed\_inductive\_discharge\_-\_art\_no\_67311D](https://www.researchgate.net/publication/253026465_337_nm_molecular_nitrogen_laser_excited_by_pulsed_inductive_discharge_-_art_no_67311D)  
31. Excimer Lasers \- Choice, Size & Wavelength \- LASEA, [https://lasea.com/wp-content/uploads/2025/11/RAE02-Excimer-Lasers-Choice-Size-Wavelength.pdf](https://lasea.com/wp-content/uploads/2025/11/RAE02-Excimer-Lasers-Choice-Size-Wavelength.pdf)  
32. LED technology for UV systems \- Ultralight AG, [https://www.ultralight-uv.com/download\_file/view/7cc57426-25d0-45ef-b696-6f113f0a1764](https://www.ultralight-uv.com/download_file/view/7cc57426-25d0-45ef-b696-6f113f0a1764)  
33. UV LED Curing Wavelength Guide: 365nm, 385nm, 395nm, 405nm \- UVET, [https://www.uvndt.com/uv-led-curing-wavelengths/](https://www.uvndt.com/uv-led-curing-wavelengths/)  
34. LED Wavelength Guide: From UV to Infrared Light-Emitting Diodes, [https://tech-led.com/led-wavelength-guide-from-uv-to-infrared-light-emitting-diodes/](https://tech-led.com/led-wavelength-guide-from-uv-to-infrared-light-emitting-diodes/)  
35. Roithner Lasertechnik \- LEDs Diverse, [http://www.qubits.at/led\_diverse.html](http://www.qubits.at/led_diverse.html)  
36. LEDs Diverse \- Roithner Lasertechnik, [http://www.roithner-laser.com/led\_standard.html](http://www.roithner-laser.com/led_standard.html)  
37. LASER DIODES, [http://supernovae.in2p3.fr/\~llg/LEDs/docs/Roithner-LaserTechnik/Roithner-pricelist-2018-07.pdf](http://supernovae.in2p3.fr/~llg/LEDs/docs/Roithner-LaserTechnik/Roithner-pricelist-2018-07.pdf)  
38. Standard Laser Diodes \- Roithner Lasertechnik GmbH, [https://www.roithner-laser.com/ld\_standard.html](https://www.roithner-laser.com/ld_standard.html)  
39. Roithner Laser Price List 2024 | PDF | Laser | Light Emitting Diode \- Scribd, [https://www.scribd.com/document/733316090/Pricelist](https://www.scribd.com/document/733316090/Pricelist)  
40. Industrial | LD | NICHIA CORPORATION, [https://led-ld.nichia.co.jp/en/product/ld\_industry.html](https://led-ld.nichia.co.jp/en/product/ld_industry.html)  
41. MNL 100 HP N₂ \- LTB Lasertechnik Berlin GmbH, [https://www.ltb-berlin.de/en/products/mln-100-hp/](https://www.ltb-berlin.de/en/products/mln-100-hp/)  
42. Roithner Lasertechnik \- High Power Single Chip LEDs, SMD LEDs, [http://www.qubits.at/led\_highsingle\_smd.html](http://www.qubits.at/led_highsingle_smd.html)  
43. Laser Diodes | Components to Systems | UV-LWIR | Shop | RPMC, [https://www.rpmclasers.com/product-category/laser-diodes/](https://www.rpmclasers.com/product-category/laser-diodes/)  
44. Efficient emission of InGaN-based light-emitting diodes: toward orange and red, [https://www.researching.cn/articles/OJe92447b256e22816](https://www.researching.cn/articles/OJe92447b256e22816)  
45. Visible Laser Diodes: Center Wavelengths from 404 nm to 690 nm \- Thorlabs, [https://www.thorlabs.com/visible-laser-diodes-center-wavelengths-from-404-nm-to-690-nm](https://www.thorlabs.com/visible-laser-diodes-center-wavelengths-from-404-nm-to-690-nm)  
46. High Power Visible Laser Diodes \[HPVLD\], [https://www.apslasers.com/diode-lasers/high-power-visible-laser-diodes](https://www.apslasers.com/diode-lasers/high-power-visible-laser-diodes)  
47. DPSS Lasers \- Diode Pumped Solid State Lasers \- Cobolt \- Wavelength Opto-Electronic, [https://wavelength-oe.com/dpss-lasers/](https://wavelength-oe.com/dpss-lasers/)  
48. Manipulation of blue TADF top-emission OLEDs by the first-order optical cavity design: toward a highly pure blue emission and balanced charge transport, [https://opg.optica.org/abstract.cfm?uri=prj-9-8-1502](https://opg.optica.org/abstract.cfm?uri=prj-9-8-1502)  
49. Exceptionally high brightness and long lifetime of efficient blue OLEDs for programmable active-matrix display \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11982528/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11982528/)  
50. OLED \- Wikipedia, [https://en.wikipedia.org/wiki/OLED](https://en.wikipedia.org/wiki/OLED)  
51. Horizontally Oriented MRCT-TADF Emitter Achieves \>40% EQE in Sky-Blue OLEDs \- Fluxim, [https://www.fluxim.com/publications-overview/horizontally-oriented-mrct-type-tadf-emitter-achieving-eqe-over-40-for-sky-blue-oled](https://www.fluxim.com/publications-overview/horizontally-oriented-mrct-type-tadf-emitter-achieving-eqe-over-40-for-sky-blue-oled)  
52. Full article: Technical status of top-emission organic light-emitting diodes \- Taylor & Francis, [https://www.tandfonline.com/doi/full/10.1080/15980316.2021.1876173](https://www.tandfonline.com/doi/full/10.1080/15980316.2021.1876173)  
53. Laser Wavelengths \- RayComposer, [https://www.raycomposer.de/en/ressources/laser-wavelengths/index.html](https://www.raycomposer.de/en/ressources/laser-wavelengths/index.html)  
54. Laser Diodes from Nichia Corporation \- GoPhotonics, [https://www.gophotonics.com/search/laser-diodes/filters?page=1\&country=global\&manuid=;235;](https://www.gophotonics.com/search/laser-diodes/filters?page=1&country=global&manuid=;235;)  
55. Emerging ultra-narrow-band cyan-emitting phosphor for white LEDs with enhanced color rendition, [https://www.light-am.com/article/pdf/preview/xjzz-2019-8-341.pdf](https://www.light-am.com/article/pdf/preview/xjzz-2019-8-341.pdf)  
56. (PDF) Realization of high-luminous-efficiency InGaN light-emitting diodes in the “green gap” range \- ResearchGate, [https://www.researchgate.net/publication/277782029\_Realization\_of\_high-luminous-efficiency\_InGaN\_light-emitting\_diodes\_in\_the\_green\_gap\_range](https://www.researchgate.net/publication/277782029_Realization_of_high-luminous-efficiency_InGaN_light-emitting_diodes_in_the_green_gap_range)  
57. Luminous efficiency of InGaN/GaN-based green micro-LED improved by n-side graded quantum wells \- Optica Publishing Group, [https://opg.optica.org/abstract.cfm?uri=ol-50-8-2614](https://opg.optica.org/abstract.cfm?uri=ol-50-8-2614)  
58. Low-efficiency-droop InGaN quantum dot light-emitting diodes operating in the “green gap”, [https://opg.optica.org/prj/abstract.cfm?uri=prj-8-5-750](https://opg.optica.org/prj/abstract.cfm?uri=prj-8-5-750)  
59. (a) Peak wavelength and FWHM and (b) EQE and output power of a typical µLED at different current densities based on on-wafer testing. \- ResearchGate, [https://www.researchgate.net/figure/a-Peak-wavelength-and-FWHM-and-b-EQE-and-output-power-of-a-typical-LED-at-different\_fig3\_351647754](https://www.researchgate.net/figure/a-Peak-wavelength-and-FWHM-and-b-EQE-and-output-power-of-a-typical-LED-at-different_fig3_351647754)  
60. (a) EQE, (b) centroid wavelength, and (c) FWHM as a function of current... \- ResearchGate, [https://www.researchgate.net/figure/a-EQE-b-centroid-wavelength-and-c-FWHM-as-a-function-of-current-density-for-the\_fig3\_377800026](https://www.researchgate.net/figure/a-EQE-b-centroid-wavelength-and-c-FWHM-as-a-function-of-current-density-for-the_fig3_377800026)  
61. Very high external quantum efficiency and wall-plug efficiency 527 nm InGaN green LEDs by MOCVD \- Optica Publishing Group, [https://opg.optica.org/oe/fulltext.cfm?uri=oe-26-25-33108](https://opg.optica.org/oe/fulltext.cfm?uri=oe-26-25-33108)  
62. High-performance, narrow-band green-emitting phosphors for white LEDs: recent advances and perspectives \- Journal of Materials Chemistry C (RSC Publishing) DOI:10.1039/D4TC04457F, [https://pubs.rsc.org/en/content/articlehtml/2025/tc/d4tc04457f](https://pubs.rsc.org/en/content/articlehtml/2025/tc/d4tc04457f)  
63. Quantum dot \- Wikipedia, [https://en.wikipedia.org/wiki/Quantum\_dot](https://en.wikipedia.org/wiki/Quantum_dot)  
64. Quantum Dot Single-Photon Source Characterization Using … \- Swabian Instruments, [https://www.swabianinstruments.com/applications/quantum-dots/](https://www.swabianinstruments.com/applications/quantum-dots/)  
65. Enhanced Performance of Inverted Perovskite Quantum Dot Light-Emitting Diode Using Electron Suppression Layer and Surface Morphology Control \- MDPI, [https://www.mdpi.com/1996-1944/16/22/7171](https://www.mdpi.com/1996-1944/16/22/7171)  
66. Perovskite Quantum Dot Light-Emitting Diodes \- SciSpace, [https://scispace.com/pdf/perovskite-quantum-dot-light-emitting-diodes-3atycqb3qh.pdf](https://scispace.com/pdf/perovskite-quantum-dot-light-emitting-diodes-3atycqb3qh.pdf)  
67. The Full Width Half Maximum of Quantum Dots \- Avantama AG, [https://avantama.com/full-width-half-maximum-quantum-dots/](https://avantama.com/full-width-half-maximum-quantum-dots/)  
68. Perovskite Quantum Dots for Emerging Displays: Recent Progress and Perspectives \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9268187/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9268187/)  
69. Stable Perovskite Quantum Dots Light‐Emitting Diodes with Efficiency Exceeding 24%, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10754115/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10754115/)  
70. Highly efficient and eco-friendly green quantum dot light-emitting diodes through interfacial potential grading \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11850856/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11850856/)  
71. Enhancing photoluminescence performance of perovskite quantum dots with plasmonic nanoparticles: insights into mechanisms and light-emitting applications \- Nanoscale Advances (RSC Publishing), [https://pubs.rsc.org/en/content/articlelanding/2024/na/d3na01078c](https://pubs.rsc.org/en/content/articlelanding/2024/na/d3na01078c)  
72. LED Array Light Sources \- Thorlabs, [https://www.thorlabs.com/led-array-light-sources](https://www.thorlabs.com/led-array-light-sources)  
73. Investigation of Electrical and Optical Properties of AlGaInP Red Vertical Micro-Light-Emitting Diodes With Cu/Invar/Cu Metal Substrates | Request PDF \- ResearchGate, [https://www.researchgate.net/publication/351167192\_Investigation\_of\_Electrical\_and\_Optical\_Properties\_of\_AlGaInP\_Red\_Vertical\_Micro-Light-Emitting\_Diodes\_With\_CuInvarCu\_Metal\_Substrates](https://www.researchgate.net/publication/351167192_Investigation_of_Electrical_and_Optical_Properties_of_AlGaInP_Red_Vertical_Micro-Light-Emitting_Diodes_With_CuInvarCu_Metal_Substrates)  
74. High-performance AlGaInP light-emitting diodes integrated on silicon through a superior quality germanium-on-insulator \- Optica Publishing Group, [https://opg.optica.org/prj/fulltext.cfm?uri=prj-6-4-290](https://opg.optica.org/prj/fulltext.cfm?uri=prj-6-4-290)  
75. Efficiency improvement of AlGaInP-based red micron-scale light-emitting diodes using sidewall steam oxidation \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11947362/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11947362/)  
76. High-efficiency InGaN red micro-LEDs for visible light communication \- Optica Publishing Group, [https://opg.optica.org/prj/viewmedia.cfm?uri=prj-10-8-1978\&seq=0](https://opg.optica.org/prj/viewmedia.cfm?uri=prj-10-8-1978&seq=0)  
77. JP7873463B2 – Phosphors | PatSnap Eureka, [https://eureka.patsnap.com/patent-JP7873463B2](https://eureka.patsnap.com/patent-JP7873463B2)  
78. Initial Benchmarks and Long-Term Performance of Narrow-Band Red Emitters Used in SSL Devices \- Department of Energy, [https://www.energy.gov/sites/prod/files/2020/10/f79/ssl-rti-red-emitters-aug2020.pdf](https://www.energy.gov/sites/prod/files/2020/10/f79/ssl-rti-red-emitters-aug2020.pdf)  
79. Highly efficient narrow-band green and red phosphors enabling wider color-gamut LED backlight for more brilliant displays \- Optica Publishing Group, [https://opg.optica.org/oe/fulltext.cfm?uri=oe-23-22-28707](https://opg.optica.org/oe/fulltext.cfm?uri=oe-23-22-28707)  
80. Introduction to KSF Phosphor LEDs & Luminus LUX COBs, [https://luminusdevices.zendesk.com/hc/en-us/articles/39667252787341-Introduction-to-KSF-Phosphor-LEDs-Luminus-LUX-COBs](https://luminusdevices.zendesk.com/hc/en-us/articles/39667252787341-Introduction-to-KSF-Phosphor-LEDs-Luminus-LUX-COBs)  
81. LED phosphors | YUJILEDS, [https://www.yujiintl.com/phosphor.html](https://www.yujiintl.com/phosphor.html)  
82. High-Efficiency Pure-Red Perovskite Quantum-Dot Light-Emitting Diodes | Nano Letters, [https://pubs.acs.org/doi/10.1021/acs.nanolett.2c03062](https://pubs.acs.org/doi/10.1021/acs.nanolett.2c03062)  
83. Perovskite Quantum Dots for the Next‐Generation Displays: Progress and Prospect \- The Advanced Portfolio, [https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202401284](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202401284)  
84. Current development status of red high-power laser diodes for display applications at Nichia, [https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13345/1334512/Current-development-status-of-red-high-power-laser-diodes-for/10.1117/12.3040588.short](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13345/1334512/Current-development-status-of-red-high-power-laser-diodes-for/10.1117/12.3040588.short)  
85. NIR LED | Wavelength lineup | epitex | LED | Products | Ushio Inc., [https://www.ushio.co.jp/en/led/epitex/wavelength/nir.html](https://www.ushio.co.jp/en/led/epitex/wavelength/nir.html)  
86. Key Differences Between NIR LED Near Infrared Light Wavelengths \- SuperLightingLED, [https://www.superlightingled.com/blog/differences-between-nir-led-near-infrared-light-wavelengths/](https://www.superlightingled.com/blog/differences-between-nir-led-near-infrared-light-wavelengths/)  
87. 1310/1550nm Fused Biconic WDM-LD-PD PTE. LTD., [https://www.ld-pd.com/?a=cpinfo\&id=1550](https://www.ld-pd.com/?a=cpinfo&id=1550)  
88. Wavelengths in IR sensing: SWIR, MWIR, LWIR and why 1550 nm matters \- Phlux Technology, [https://phluxtechnology.com/latest/wavelengths-in-ir-sensing-swir-mwir-lwir-and-why-1550-nm-matters](https://phluxtechnology.com/latest/wavelengths-in-ir-sensing-swir-mwir-lwir-and-why-1550-nm-matters)  
89. The World of Near Infrared Light & Its Applications \- Musou Black, [https://the-black-market.com/blogs/news/the-world-of-near-infrared-light-and-its-applications](https://the-black-market.com/blogs/news/the-world-of-near-infrared-light-and-its-applications)  
90. High Power CW Laser for Co-Packaged Optics \- Lumentum, [https://www.lumentum.com/sites/default/files/2025-12/high\_power\_cw\_laser\_for\_co-packaged\_optics\_2022.pdf](https://www.lumentum.com/sites/default/files/2025-12/high_power_cw_laser_for_co-packaged_optics_2022.pdf)  
91. Integration Challenges and Solutions for 1310nm DFB Lasers in Silicon Photonics, [https://www.fiber-mart.com/news/integration-challenges-and-solutions-for-1310nm-dfb-lasers-in-silicon-photonics-a-6607.html](https://www.fiber-mart.com/news/integration-challenges-and-solutions-for-1310nm-dfb-lasers-in-silicon-photonics-a-6607.html)  
92. Advanced InP DFB Laser Sources for Silicon Photonics Hybrid Integration, [https://epic-photonics.com/wp-content/uploads/2022/08/2.5-Iain-Eddie-Sivers-Photonics.pdf](https://epic-photonics.com/wp-content/uploads/2022/08/2.5-Iain-Eddie-Sivers-Photonics.pdf)  
93. High Power DFBs, 1310nm & 1550nm \- AP Technologies, [https://www.aptechnologies.co.uk/products/laser-diodes/singlemode-laser-diodes/high-power-dfb-1310nm-1550nm](https://www.aptechnologies.co.uk/products/laser-diodes/singlemode-laser-diodes/high-power-dfb-1310nm-1550nm)  
94. Coherent Unveils High-Efficiency Lasers for Silicon Photonics Transceivers, [https://www.coherent.com/news/press-releases/high-efficiency-lasers-for-silicon-photonics-transceivers](https://www.coherent.com/news/press-releases/high-efficiency-lasers-for-silicon-photonics-transceivers)  
95. SWIR and MWIR LEDs \- Marktech Optoelectronics, [https://marktechopto.com/led-emitters/swir-and-mwir-leds/](https://marktechopto.com/led-emitters/swir-and-mwir-leds/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAaCAYAAAAXHBSTAAACV0lEQVR4Xu2WMUhVYRTHj6RQpEQFSaSgYTUkOISDoASRoUMR4ZabS4NLQTXlEg5NaTmJ4ChGTSE4iLwpRKMpCJJQGgoUdHIIofr/37kf79zju/e+6apwf/AHv3Pu9zzn3nPO94kUFBTkyV9owhuPMwPQv0h1zpdEM3RFKvsuGrVAd6Dfke9ktCc3TkGL0J5oANfj7lTqRfcw+Gp0QrvemAcfoRnohmhiv6CO2BPJ9IomNe4dEY1QyRvzgG+yR/Stz4kG+TL2RDJPRJ8fNLZH0Ivo7yZo2fhyoU80oUAoJyoL9tQPaAk6bezbol/9UGiA3okmYvkjmlS7s3tYevvQBjQdqQStQWcrj+ULS41Jefj1mNg61Op8lveiyV82Nk7Dh2ZdjVvQG9HnPkDzkY1f/WeCbpd31sCWaAIeTkMODwY86nyWTTk4rjnKu8z6HjTk1t/Nmr3L4TQlmlw4Tnhm8pg5Ad2EuiN7Kqz5fm80MLGs3qKP/zyNT9AZs2a5PjBrxjEJPTY2vhRWQWgLljIHTip8G3wzDDwNBszAL3iHZJ9P5Lwc/NLcY6fhOdHj46qxsSyfmzV/J/NCwIQ4xkNzJ+mzaBCroj9sYY3TV+184ssaE/X7YDj6WfahCu7G3eWvwkFzydkz4cgNP1qrhss7tX8YSBgSr0T7iFcj2tk/IWgOmyRGoK/QgsR7MlwA/EQ+kjDIt87G24btHTIr2nfHApbTirOxl+zQICy9TWc7sjyFXkNfoGfQN9GzKkD7jlTKnf5Du5XUyjXRG0wbdF/0ilVQUFCQD/8BmJmKeZCFOWIAAAAASUVORK5CYII=>