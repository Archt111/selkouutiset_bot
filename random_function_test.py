title = "Päiväkotien lakko"
sentences = [
    "Ensin lakkouutinen.",
    "Helsingin seudun päiväkodeissa on lakko.",
    "Lakon takia monet päiväkodit ovat nyt kiinni.",
    "Lakko kestää 2 päivää. Työntekijät eivät tee työtä tänään keskiviikkona ja huomenna torstaina.",
    "Helsingin seudun päiväkodeissa on lakko.",
    "Loppuviikolla lakkoja on myös muilla työpaikoilla.",
    "Esimerkiksi junat ja monet bussit pysähtyvät perjantaina, kun kuljettajat ovat lakossa.",
    "Lakkojen avulla työntekijöiden ammattiliitot vastustavat hallituksen politiikkaa."
]

# Using an f-string to format the content
formatted_content = f"{title}\n\n"
formatted_content += "\n".join(sentences)

# Print or use the formatted content as needed
print(formatted_content)