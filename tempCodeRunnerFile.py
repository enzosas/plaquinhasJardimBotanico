# Abas
tabview = ctk.CTkTabview(
    app, fg_color="white", 
    segmented_button_selected_color=VERDEPLACA, 
    segmented_button_selected_hover_color=VERDEPLACADARK, 
    segmented_button_unselected_color=CINZAFRENTE, 
    segmented_button_fg_color=CINZAFRENTE)
tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
tab_placa = tabview.add("Gerar Plaquinha")
tab_sobre = tabview.add("Sobre")