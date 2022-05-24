Genomlysning av PKI
===================

Detta dokument beskriver hur du gör en genomlysning av ditt PKI-system med hjälp av verktyget *ADCS Collector* från PKI Solutions.

Om du kör verktyget på en domänansluten maskin så kommer den automatiskt att detektera och genomlysa alla AD CS-servrar registrerade i Active Directory.

Om din miljö innehåller en så kallad *standalone CA* (dvs en AD CS-server som inte är ansluten till någon domän) så kommer du behöva köra verktyget flera gånger, en gång på en domänansluten maskin och en gång för varje AD CS-server med en standalone CA installerad.

Instruktioner
-------------

1. Ladda ner filen ``ADCS Collector-v1.0.35.exe`` som du erhåller från Atea, och överför filen till AD CS-servern som du vill genomlysa.

2. Logga in på AD CS-servern som enterprise admin om du gör en genomlysning av en eller flera domänanslutna AD CS-servrar, eller som lokal administratör om du gör en genomlysning av en standalone CA.

3. Dubbeklicka på filen ``ADCS Collector-v1.0.35.exe`` och följ installationsguiden.

![](graphics/wizard.png)

4. Öppna PowerShell och kör följande kommando för att importera ADCSCollector-modulen:
```
    Import-Module ADCSCollector
```

När modulen importeras så görs en systemkontroll. Åtgärda eventuella problem innan du fortsätter till nästa steg.

![Ett exempel på hur en lyckad systemkontroll ser ut efter att ha importerat ADCSCollector-modulen i PowerShell.](graphics/install_module.png)

5. Kontrollera vilka AD CS-servrar som kommer att genomlysas.
```
Get-AdcsServerList
```

6. Genomför genomlysningen av alla AD CS-servrar som listades i föregående steg och spara resultatet i mappen ``C:\AdcsCollector``.
```
Start-AdcsCollector
```

När verktyget har kört klart, kommer den skriva ut meddelandet "Data collection completed".

7. Öppna mappen ``C:\AdcsCollector\Reports\cab`` och dela filen som ligger i denna mapp med Atea.
![Mappen ``C:\AdcsCollector\Reports\cab`` innehåller en JSONX-fil som ska delas med Atea.](graphics/find_report.png)

**Viktigt!** ADCSCollector kan samla in känsliga data om ert PKI-system. Om filen skickas med mail är det viktigt att den krypteras med ett starkt lösenord innan den skickas till Atea. Skicka lösenordet via en separat kommunikationskanal, till exempel med SMS.