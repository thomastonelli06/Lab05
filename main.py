import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO fatto

    txt_aggiunta_strumento = ft.Text("Aggiungi Nuovo Strumento", size = 20)
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno acquisto")
    txt_prezzo = ft.Text("0")




    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO

    def incrementa_prezzo(e):
        txt_prezzo.value = str(int(txt_prezzo.value) + 1)
        page.update()

    def decrementa_prezzo(e):
        if int(txt_prezzo.value) > 0:
            txt_prezzo.value = str(int(txt_prezzo.value) - 1)
        page.update()

    def conferma_aggiunta_strumento(e):
        tipo = input_tipo.value
        marca = input_marca.value
        anno = input_anno.value
        prezzo = int(txt_prezzo.value)

        if anno is None or not anno.isdigit():
            alert.show_alert("L'anno deve avere solo cifre")
            return

        anno = int(anno)

        #aggiungo strumento alla classe:
        deposito.aggiungi_strumento(tipo,marca,anno,prezzo)

        #pulisco i textfield
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value =""
        txt_prezzo.value = "0"

        aggiorna_lista_strumenti()






    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO

    contatore_prezzo = ft.Row(controls=[
            ft.Button("-", on_click=decrementa_prezzo),
            txt_prezzo,
            ft.Button("+", on_click=incrementa_prezzo),
        ])

    pulsante_aggiungi_strumento = ft.Button("aggiungi strumento",
            on_click= conferma_aggiunta_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        txt_aggiunta_strumento,
        ft.Row(
            controls=[
                input_tipo,
                input_marca,
                input_anno,
                contatore_prezzo,
            ],
            alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
