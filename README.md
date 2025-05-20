Automatizēta izdevumu kategorēšanas sistēma

Projekta apraksts

Šī projekta mērķis ir automatizēt personīgo vai uzņēmuma finanšu izdevumu klasifikāciju pēc tā, kur tiek tiek veikti, lai atvieglotu to pārvaldību un analīzi. Lietotājs ielādē CSV vai XLSX failu ar izdevumiem, kur katrai rindai ir preču/pakalpojumu iegādes vieta un to izdevumi. Programma, balstoties uz iepriekš definētiem piemēriem un "Google" sniegtajiem rezultātiem no saites "Firmas.lv", mēģina automātiski noteikt katra izdevuma kategoriju, piemēram, ēdiens, transports, rēķini, apģērbs utt., pēc preču/pakalpojumu iegādes vietas. Pēc tam tiek izvadīta pārskatāma tabula ar visiem izdevumiem un to kategorijām, kā arī tiek parādīts apkopojums par kopējiem izdevumiem katrā kategorijā. Šī sistēma ir īpaši noderīga, ja ir liels daudzums finanšu datu un nepieciešams ātrs pārskats par izdevumu sadalījumu pa kategorijām. 


Izmantotās Python bibliotēkas un to pielietojums:

time - izmanto, lai ievietotu pauzes starp "Google" meklēšanas pieprasījumiem, lai izvairītos no piekļuves ierobežojumiem;

googlesearch - ja nav iespējams noteikt kategoriju ar iepriekš definētiem piemēriem, tad šī bibliotēka nodrošina iespēju automatizēti meklēt uzņēmuma nosaukumus "Google meklētājā";

requests - nepieciešams, lai ielādētu tīmekļa lapas no rezultātiem, kas iegūti ar "Google meklēšanu", un analizētu to saturu;

os - nodrošina failu ceļu un paplašinājumu pārbaudi;

pandas - izmanto, lai nolasītu CSV un XLSX failus un strukturētu datus sarakstā, kas tālāk tiek analizēts.


Projektā izmantotās datu struktūras:

kategoriju_piemeri – vārdnīca, kas satur iepriekš definētus uzņēmumu (preču/pakalpojumu iegādes vietu) atslēgvārdus un tiem atbilstošās kategorijas;

meklesanas_cache – vārdnīca, kas saglabā rezultātus no iepriekšējām "Google" meklēšanām, lai nevajadzētu to darīt atkārtoti un netērētu laiku;

izdevumi – saraksts ar vārdnīcām, kur katrā ierakstā ir informācija par iegādes vietu, izdevumiem un kategoriju;

kategoriju_kopsavilkums – vārdnīca, kas apkopo kopējos izdevumus katrā kategorijā.


Programmas izmantošana:

1. Sagatavot CSV vai XLSX failu ar vismaz divām kolonnām: “Iegādes vieta” un “Izdevumi”. Piemērs:

Iegādes vieta	Izdevumi

Rimi	23.50

Circle K	45.00

2. Novietot sagatavoto failu mapē ar nosaukumu "dati" un pašu failu nosaukt "izdevumi";

3. Palaist programmu ("izdevumi.py");

4. Programma izlasa datus, nosaka katra ieraksta kategoriju, izvada sakārtotu tabulu ar visiem ierakstiem un to kategorijām, vēl izvada kopējos izdevumus katrā kategorijā.


+ lietotājs var papildināt "kategoriju_piemeri" vārdnīcu ar saviem uzņēmumiem un to kategorijām;


Autore - Samanta Marjeta Eglīte, 241RDC015
