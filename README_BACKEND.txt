SERVIZIO CLIENTI IA - BACKEND GMAIL (MODALITA PROTETTA)

1. Metti questo file Python e requirements.txt nella stessa cartella del JSON OAuth.
2. Rinomina il JSON OAuth in client_secret.json (oppure imposta GOOGLE_CLIENT_SECRET col suo percorso).
3. Installa: pip install -r requirements.txt
4. Avvia: python servizio_clienti_backend.py
5. Apri: http://localhost:8080/auth/google

Permesso richiesto: gmail.readonly. Il backend non cancella, archivia, invia o modifica email.

IMPORTANTE PER LA PUBBLICAZIONE HTTPS:
In Google Cloud dovrai aggiungere ESATTAMENTE https://TUO-DOMINIO/oauth2/callback tra gli URI di reindirizzamento autorizzati. Non inserire mai client_secret nel file HTML pubblico.
